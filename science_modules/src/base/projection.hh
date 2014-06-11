#ifndef tao_base_projection_hh
#define tao_base_projection_hh

#include <array>
#include <string>
#include "lightcone.hh"

namespace tao {

   //
   class projection_iterator;

   ///
   ///
   ///
   class projection
   {
   public:

      enum format_type
      {
         FITS,
         PNG
      };

      typedef projection_iterator iterator;

   public:

      projection();

      projection( lightcone const& lc,
                  unsigned width,
                  unsigned height );

      void
      project( real_type gal_x,
               real_type gal_y,
               real_type gal_z,
               real_type& img_x,
               real_type& img_y ) const;

      iterator
      begin( const batch<real_type>& batch );

      iterator
      end( const batch<real_type>& batch );

   protected:

      void
      _calc_scale();

   protected:

      int _sub_cone;
      format_type _fmt;
      std::string _mag_field;
      real_type _min_mag;
      std::array<real_type,2> _z;
      std::array<real_type,2> _org;
      std::array<real_type,2> _fov;
      std::array<unsigned,2> _dim;
      std::array<real_type,2> _scale;
   };

   ///
   ///
   ///
   class projection_iterator
      : public boost::iterator_facade< projection_iterator,
                                       const std::array<real_type,2>&,
				       std::forward_iterator_tag,
                                       const std::array<real_type,2>& >
   {
      friend class boost::iterator_core_access;

   public:

      typedef const std::array<real_type,2>& value_type;
      typedef value_type reference_type;

   public:

      projection_iterator( const batch<real_type>& bat );

      projection_iterator( const projection& proj,
                           const batch<real_type>& bat );

      bool
      done() const;

      reference_type
      operator*();

      real_type
      magnitude() const;

      unsigned
      index() const;

   protected:

      void
      increment();

      bool
      equal( const projection_iterator& op ) const;

      reference_type
      dereference() const;

   protected:

      const projection* _proj;
      hpc::view<std::vector<real_type>> _x, _y, _z, _mag;
      std::array<real_type,2> _pos;
      const batch<real_type>* _bat;
      unsigned _gal_idx;
   };

}

#endif