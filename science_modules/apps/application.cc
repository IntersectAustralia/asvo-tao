#include <pugixml.hpp>
#include "application.hh"
#include "tao/base/base.hh"
#include "tao/modules/modules.hh"
#include <libhpc/logging/file.hh>

using namespace hpc;
using namespace pugi;

namespace tao {

   application::application()
   {
      tao_start_time = posix::timer();
   }

   application::application( int argc,
                             char* argv[] )
   {
      tao_start_time = posix::timer();
      arguments( argc, argv );
   }

   void
   application::arguments( int argc,
                           char* argv[] )
   {
      // Check for insufficient arguments.
      if( argc != 3 || !argv[1] || !argv[2] )
      {
         std::cout << "Insufficient arguments.\n";
         std::cout << "Please supply a path to an input XML and a database\n";
         std::cout << "configuration XML.\n";
         exit( 1 );
      }

      // Check that the files exists.
      {
         std::ifstream file( argv[1] );
         if( !file )
         {
            std::cout << "Could not open XML file.\n";
            exit( 1 );
         }
      }
      {
         std::ifstream file( argv[2] );
         if( !file )
         {
            std::cout << "Could not open DB config file.\n";
            exit( 1 );
         }
      }

      // Cache the filename.
      _xml_file = argv[1];
      _dbcfg_file = argv[2];
   }

   void
   application::run()
   {
      LOG_ENTER();

      // Preprocess the incoming XML file, only if we're
      // the root process, as we don't want any conflicts
      // in writing the processed file.
      if( mpi::comm::world.rank() == 0 )
	 _preprocess_xml();
      mpi::comm::world.bcast( _currentxml_version );
      LOGDLN("Current XMl Schema Version: ",_currentxml_version);

      // Load all the modules first up.
      _load_modules();
      _connect_parents();

      // Read the options dictionary.
      options::xml_dict xml;
      _read_xml( xml );

      // Prepare the logging.
      string subjobindex=xml.get<string>( "subjobindex" );
      LOGDLN("LOG DIRECTORY:"+xml.get<string>( "logdir" ) );
      LOGDLN("SubJobIndex:"+xml.get<string>( "subjobindex" ) );
      _setup_log( xml.get<string>( "logdir" ) + "tao.log."+ subjobindex);

      // Initialise all the modules.
      for( auto module : tao::factory )
         module->initialise( xml );

      // Mark the beginning of the run.
      LOG_PUSH_TAG( "progress" );
      LOGILN( runtime(), ",start" );
      LOG_POP_TAG( "progress" );

      // Run.
      _execute();

      // Finalise all the modules.
      for( auto module : tao::factory )
         module->finalise();

      // Mark the conclusion of the run.
      mpi::comm::world.barrier();
      LOG_PUSH_TAG( "progress" );
      LOGILN( runtime(), ",end,successful" );
      LOG_POP_TAG( "progress" );

      // Dump timing information to the end of the info file.
      LOGILN( "Module metrics:", setindent( 2 ) );
      for( auto module : tao::factory )
         module->log_metrics();

      LOG_EXIT();
   }

   ///
   /// Load modules.
   ///
   void
   application::_load_modules()
   {
      LOG_ENTER();

      // Register all the available science modules.
      tao::register_modules();
      LOGILN( "Load Modules From File",_xml_file );

      // Open the primary XML file using pugixml.
      if( _currentxml_version != "1.0" )
	 INSIST( _doc.load_file( string( _xml_file).c_str() ), == true );
      else
	 INSIST( _doc.load_file( string( _xml_file+".processed").c_str() ), == true );

      // Iterate over the module nodes.
      xpath_node_set nodes = _doc.select_nodes( "/tao/workflow/*[@id]" );
      for( const xpath_node* it = nodes.begin(); it != nodes.end(); ++it )
      {
         xml_node cur = it->node();
         string name = cur.attribute( "id" ).value();
         string type = cur.name();
#ifdef PREPROCESSING
         LOGILN( "Loading Module : ",type);
         if (type=="light-cone")
        	 tao::factory.create_module( type, name, cur );
         else
        	 LOGILN( " Pre-Processing mode : Ignore Loading Module : ",type);
#else
         tao::factory.create_module( type, name, cur );
#endif

      }

      LOG_EXIT();
   }

   ///
   /// Connect parents.
   ///
   void
   application::_connect_parents()
   {
      LOG_ENTER();

      // Connect 'em all up!
      for( auto module : tao::factory )
      {
	 auto nodes = module->local_xml_node().select_nodes( "parents/item" );
	 for( const xpath_node* it = nodes.begin(); it != nodes.end(); ++it )
	 {
	    string name = it->node().first_child().value();
	    module->add_parent( *tao::factory[name] );
	 }
      }

      LOG_EXIT();
   }


   ///
   /// Massage incoming XML.
   ///
   void
   application::_preprocess_xml()
   {
      // Open the primary XML file using pugixml.
      xml_document inp_doc, out_doc;
      INSIST( inp_doc.load_file( string( _xml_file ).c_str() ), == true );
      _currentxml_version=inp_doc.select_single_node( "/tao/workflow/schema-version" ).node().first_child().value();
      if (_currentxml_version!="1.0")
	 return;

      // Create tao and workflow nodes.
      xml_node tao_node = out_doc.append_child( "tao" );
      xml_node workflow_node = tao_node.append_child( "workflow" );

      string subjobindex=inp_doc.select_single_node( "/tao/subjobindex" ).node().first_child().value();
      // Transfer the lightcone module intact.
      xml_node lc_node = inp_doc.select_single_node( "/tao/workflow/light-cone" ).node();
      lc_node = workflow_node.append_copy( lc_node );
      lc_node.append_attribute( "id" ).set_value( "light-cone" );

      // Copy the SED module, but remove the bandpass filters.
      xml_node sed_node = inp_doc.select_single_node( "/tao/workflow/sed" ).node();
      if( sed_node )
      {
	 sed_node = workflow_node.append_copy( sed_node );
	 sed_node.remove_child( "bandpass-filters" );
	 sed_node.append_attribute( "id" ).set_value( "sed" );
	 sed_node.append_child( "parents" ).append_child( "item" ).append_child( node_pcdata ).set_value( "light-cone" );

	 // Create the filter module, copying in the bandpass filters from
	 // the sed module.
	 xml_node filter_node = workflow_node.append_child( "filter" );
	 filter_node.append_attribute( "id" ).set_value( "filter" );
	 filter_node.append_copy( inp_doc.select_single_node( "/tao/workflow/sed/bandpass-filters" ).node() );
	 filter_node.append_child( "parents" ).append_child( "item" ).append_child( node_pcdata ).set_value( "sed" );
      }


      // Create the csv module, copying in output fields from the
      // lightcone module.
      LOGILN(inp_doc.select_single_node( "/tao/workflow/output-file/format" ).node().first_child().value());


      string outputformat = inp_doc.select_single_node( "/tao/workflow/output-file/format" ).node().first_child().value();
      LOGILN( "Output Format:",outputformat );
      xml_node output_fields_node;
      if(outputformat=="votable")
      {
	 LOGILN( "Writing Output to VOTable");
	 xml_node votable_node = workflow_node.append_child( "votable" );
	 votable_node.append_attribute( "id" ).set_value( "votable" );
	 output_fields_node = votable_node.append_copy( inp_doc.select_single_node( "/tao/workflow/light-cone/output-fields" ).node() );
	 output_fields_node.set_name( "fields" );
	 votable_node.append_child( "filename" ).append_child( node_pcdata ).set_value( string( string( inp_doc.select_single_node( "/tao/outputdir" ).node().first_child().value() ) + "tao."+subjobindex+".xml" ).c_str() );
	 votable_node.append_child( "parents" ).append_child( "item" ).append_child( node_pcdata ).set_value( sed_node ? "sed" : "light-cone" );
      }
      else if(outputformat=="fits")
      {
	 LOGILN( "Writing Output to FITS");
	 xml_node fits_node = workflow_node.append_child( "fits" );
	 fits_node.append_attribute( "id" ).set_value( "fits" );
	 output_fields_node = fits_node.append_copy( inp_doc.select_single_node( "/tao/workflow/light-cone/output-fields" ).node() );
	 output_fields_node.set_name( "fields" );
	 fits_node.append_child( "filename" ).append_child( node_pcdata ).set_value( string( string( inp_doc.select_single_node( "/tao/outputdir" ).node().first_child().value() ) + "tao."+subjobindex+".fits" ).c_str() );
	 fits_node.append_child( "parents" ).append_child( "item" ).append_child( node_pcdata ).set_value( sed_node ? "sed" : "light-cone" );
      }
      else if(outputformat=="hdf5")
      {
	 LOGILN( "Writing Output to hdf5");
	 xml_node hdf_node = workflow_node.append_child( "hdf5" );
	 hdf_node.append_attribute( "id" ).set_value( "hdf5" );
	 output_fields_node = hdf_node.append_copy( inp_doc.select_single_node( "/tao/workflow/light-cone/output-fields" ).node() );
	 output_fields_node.set_name( "fields" );
	 hdf_node.append_child( "filename" ).append_child( node_pcdata ).set_value( string( string( inp_doc.select_single_node( "/tao/outputdir" ).node().first_child().value() ) + "tao."+subjobindex+".hdf" ).c_str() );
	 hdf_node.append_child( "parents" ).append_child( "item" ).append_child( node_pcdata ).set_value( sed_node ? "sed" : "light-cone" );
      }
      else // if(outputformat=="csv")
      {
	 LOGILN( "Writing Output to csv");
	 xml_node csv_node = workflow_node.append_child( "csv" );
	 csv_node.append_attribute( "id" ).set_value( "csv" );
	 output_fields_node = csv_node.append_copy( inp_doc.select_single_node( "/tao/workflow/light-cone/output-fields" ).node() );
	 output_fields_node.set_name( "fields" );
	 csv_node.append_child( "filename" ).append_child( node_pcdata ).set_value( string( string( inp_doc.select_single_node( "/tao/outputdir" ).node().first_child().value() ) + "tao."+subjobindex+".csv" ).c_str() );
	 csv_node.append_child( "parents" ).append_child( "item" ).append_child( node_pcdata ).set_value( sed_node ? "sed" : "light-cone" );
      }



      // Copy the record filter node.
      xml_node rf_node = inp_doc.select_single_node( "/tao/workflow/record-filter" ).node();
      if( rf_node )
      {
	 rf_node = workflow_node.append_copy( rf_node );
      }

      // Automatically add apparent magnitudes onto the output list.
      if( sed_node )
      {
	 auto bpfs = inp_doc.select_nodes( "/tao/workflow/sed/bandpass-filters/item" );
	 for( auto bpf : bpfs )
	 {
	    string tmp = bpf.node().first_child().value();
	    auto it = std::find( tmp.rbegin(), tmp.rend(), '.' );
	    it++;
	    string field_name( tmp.begin(), it.base() );
	    field_name += "_apparent";
	    output_fields_node.append_child( "item" ).append_child( node_pcdata ).set_value( field_name.c_str() );
	 }
      }

      // Check for and copy the skymaker module.
      xml_node sky_node = inp_doc.select_single_node( "/tao/workflow/skymaker" ).node();
      if( sky_node )
      {
	 sky_node = workflow_node.append_copy( sky_node );
	 sky_node.append_attribute( "id" ).set_value( "skymaker" );
	 sky_node.append_child( "parents" ).append_child( "item" ).append_child( node_pcdata ).set_value( "filter" );
      }

      // Copy database and log directory.
      tao_node.append_child( "database" ).append_child( node_pcdata ).set_value( inp_doc.select_single_node( "/tao/database" ).node().first_child().value() );
      tao_node.append_child( "logdir" ).append_child( node_pcdata ).set_value( inp_doc.select_single_node( "/tao/logdir" ).node().first_child().value() );
      tao_node.append_child( "subjobindex" ).append_child( node_pcdata ).set_value( subjobindex.c_str());
      // Write out the new file.
      out_doc.save_file( string( _xml_file + ".processed" ).c_str() );
   }


   ///
   /// Read the XML file into a dictionary.
   ///
   void
   application::_read_xml( options::xml_dict& xml ) const
   {
      LOG_ENTER();
      LOGDLN( "XML File:", _xml_file );
      LOGDLN( "Basic Config XML File:", _dbcfg_file );
      if (_currentxml_version!="1.0")
	 xml.read( _xml_file, "/tao" );
      else
	 xml.read( _xml_file+".processed", "/tao" );
      xml.read( _dbcfg_file );
      LOG_EXIT();
   }

   ///
   /// Prepare log file.
   ///
   void
   application::_setup_log( const string& filename )
   {
      LOG_ENTER();

      if( mpi::comm::world.rank() == 0 )
      {
         LOGDLN( "Setting logging file to: ", filename );
         logging::file* Logf=new logging::file( filename, logging::info );
         Logf->add_tag("progress");
         LOG_PUSH(Logf);
      }

      LOG_EXIT();
   }

   ///
   /// Execute the application.
   ///
   void
   application::_execute()
   {
      LOG_ENTER();

      // Keep looping over modules until all report being complete.
      bool complete;
      unsigned long long it = 1;

      do
      {
         LOGDLN( "Beginning iteration: ", it, hpc::setindent( 2 ) );

         // Reset the complete flag.
         complete = true;

         // Loop over the modules.
         for( auto module : tao::factory )
         {
            module->process( it );
            if( !module->complete() )
               complete = false;
         }

         // Advance the counter.
         ++it;

         LOGD( hpc::setindent( -2 ) );
      }
      while( !complete );

      LOG_EXIT();
   }
}
