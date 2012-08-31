#include <cmath>
#include <boost/algorithm/string/trim.hpp>
#include <boost/tokenizer.hpp>
#include "filter.hh"

using namespace hpc;

namespace tao {

   filter::filter()
   {
   }

   filter::~filter()
   {
   }

   ///
   ///
   ///
   void
   filter::setup_options( options::dictionary& dict,
                          optional<const string&> prefix )
   {
      dict.add_option( new options::string( "filter_filenames" ), prefix );
   }

   ///
   ///
   ///
   void
   filter::setup_options( hpc::options::dictionary& dict,
                          const char* prefix )
   {
      setup_options( dict, string( prefix ) );
   }

   ///
   /// Initialise the module.
   ///
   void
   filter::initialise( const options::dictionary& dict,
                       optional<const string&> prefix )
   {
      LOG_ENTER();

      _read_options( dict, prefix );

      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   filter::initialise( hpc::options::dictionary& dict,
                       const char* prefix )
   {
      initialise( dict, string( prefix ) );
   }

   void
   filter::run()
   {
   }

   filter::real_type
   filter::process_galaxy( const soci::row& galaxy,
                           vector<real_type>::view spectra )
   {
   }

   void
   filter::_read_options( const options::dictionary& dict,
                          optional<const string&> prefix )
   {
      // Get the sub dictionary, if it exists.
      const options::dictionary& sub = prefix ? dict.sub( *prefix ) : dict;

      // Split out the filter filenames.
      list<string> filenames;
      {
         string filters_str = sub.get<string>( "filter_filenames" );
         boost::tokenizer<boost::char_separator<char> > tokens( filters_str, boost::char_separator<char>( "," ) );
         for( const auto& fn : tokens )
            filenames.push_back( boost::trim_copy( fn ) );
      }

      // Allocate room for the filters.
      _filters.reallocate( filenames.size() );
      _filters.resize( 0 );

      // Load each filter into memory.
      for( const auto& fn : filenames )
         _load_filter( fn );

      // Get rid of the filenames now.
      filenames.clear();
   }

   void
   filter::_load_filter( const string& filename )
   {
      std::ifstream file( filename, std::ios::in );

      // First entry is number of spectral bands.
      unsigned num_spectra;
      file >> num_spectra;

      // Allocate for this filter.
      unsigned cur_filter = _filters.size();
      _filters.resize( cur_filter + 1 );
      vector<real_type>& filter = _filters[cur_filter];
      filter.reallocate( num_spectra );

      // Read in all the values.
      for( unsigned ii = 0; ii < num_spectra; ++ii )
         file >> filter[ii];
   }
}
