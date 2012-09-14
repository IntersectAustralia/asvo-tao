#ifndef tao_base_flat_hh
#define tao_base_flat_hh

namespace tao {

   template< class T >
   struct flat_info
   {
      T disk_mass;
      T bulge_mass;
      T disk_rate;
      T bulge_rate;
      T disk_metal;
      T bulge_metal;
      T redshift;
   };

   template< class T >
   void
   make_hdf5_types( hpc::h5::datatype& mem_type,
                    hpc::h5::datatype& file_type )
   {
      // Map the templated type.
      hpc::h5::datatype real_type( boost::mpl::at<hpc::h5::datatype::type_map,T>::type::value );

      // Create memory type.
      mem_type.compound( sizeof(flat_info<T>) );
      mem_type.insert( real_type, "disk stellar mass", HOFFSET( flat_info<T>, disk_mass ) );
      mem_type.insert( real_type, "bulge stellar mass", HOFFSET( flat_info<T>, bulge_mass ) );
      mem_type.insert( real_type, "disk star formation rate", HOFFSET( flat_info<T>, disk_rate ) );
      mem_type.insert( real_type, "bulge star formation rate", HOFFSET( flat_info<T>, bulge_rate ) );
      mem_type.insert( real_type, "disk metallicity", HOFFSET( flat_info<T>, disk_metal ) );
      mem_type.insert( real_type, "bulge metallicity", HOFFSET( flat_info<T>, bulge_metal ) );
      mem_type.insert( real_type, "redshift", HOFFSET( flat_info<T>, redshift ) );

      // Create file type.
      file_type.compound( 7*8 );
      file_type.insert( hpc::h5::datatype::ieee_f64be, "disk stellar mass", 0*8 );
      file_type.insert( hpc::h5::datatype::ieee_f64be, "bulge stellar mass", 1*8 );
      file_type.insert( hpc::h5::datatype::ieee_f64be, "disk star formation rate", 2*8 );
      file_type.insert( hpc::h5::datatype::ieee_f64be, "bulge star formation rate", 3*8 );
      file_type.insert( hpc::h5::datatype::ieee_f64be, "disk metallicity", 4*8 );
      file_type.insert( hpc::h5::datatype::ieee_f64be, "bulge metallicity", 5*8 );
      file_type.insert( hpc::h5::datatype::ieee_f64be, "bulge metallicity", 6*8 );
   }
}

#endif
