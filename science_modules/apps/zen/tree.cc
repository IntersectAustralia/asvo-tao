#include <sstream>
#include <libhpc/interactive/text.hh>
#include <libhpc/interactive/colour_map.hh>
#include <tao/base/simulation.hh>
#include <tao/base/stellar_population.hh>
#include "tree.hh"

extern unsigned win_width, win_height;
extern tao::simulation* cur_sim;
extern tao::sfh cur_sfh;
extern unsigned cur_gal_id;
extern hpc::gl::colour_map<float> col_map;
extern float translate_x, translate_y;
extern std::vector<tao::real_type> stellar_mass;
extern tao::age_line<tao::real_type> sfh_ages;
extern tao::stellar_population ssp;
extern std::vector<tao::real_type> total_masses;
float sfh_width, sfh_height;

GLfloat norm;

namespace tao {

   void
   draw_colour_scale()
   {
      GLfloat x_pos = 770;
      GLfloat width = 20;

      glPolygonMode( GL_FRONT, GL_FILL );
      for( unsigned ii = 0; ii < col_map.num_points() - 1; ++ii )
      {
         GLfloat low_pos = (float)ii/((float)(col_map.num_points() - 1))*(win_height - 100) + 50.0;
         GLfloat upp_pos = (float)(ii + 1)/((float)(col_map.num_points() - 1))*(win_height - 100) + 50.0;
         glBegin( GL_POLYGON );
         glColor3fv( col_map.colour( ii ).data() );
         glVertex2f( x_pos, low_pos );
         glVertex2f( x_pos + width, low_pos );
         glColor3fv( col_map.colour( ii + 1 ).data() );
         glVertex2f( x_pos + width, upp_pos );
         glVertex2f( x_pos, upp_pos );
         glEnd();
      }

      glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );
      glColor3f( 0.7, 0.7, 0.7 );
      glBegin( GL_QUADS );
      glVertex2f( x_pos, 50 );
      glVertex2f( x_pos + width, 50 );
      glVertex2f( x_pos + width, win_height - 50 );
      glVertex2f( x_pos, win_height - 50 );
      glEnd();
      for( unsigned ii = 0; ii < col_map.num_points(); ++ii )
      {
         GLfloat pos = (float)ii/((float)(col_map.num_points() - 1))*(win_height - 100) + 50.0;
         glBegin( GL_LINES );
         glVertex2f( x_pos + width, pos );
         glVertex2f( x_pos + width + 5, pos );
         glEnd();

         std::stringstream ss;
         ss << std::fixed << std::setprecision( 1 ) << std::scientific << col_map.abscissa( ii );
         hpc::gl::draw_text( ss.str(), x_pos + width + 10, pos - 5 );
      }
   }

   void
   calc_colour_abscissa_recurse( tao::sfh const& sfh,
                                 unsigned gal_id,
                                 real_type& min,
                                 real_type& max )
   {
      if( stellar_mass[gal_id] < min )
        min = stellar_mass[gal_id];
      if( stellar_mass[gal_id] > max )
        max = stellar_mass[gal_id];
      auto pars = sfh.parents( gal_id );
      for( size_t ii = 0; ii < pars.size(); ++ii )
      {
         unsigned par_id = pars[ii];
         calc_colour_abscissa_recurse( sfh, par_id, min, max );
      }
   }

   std::array<unsigned,2>
   calc_snapshot_rng( tao::sfh const& sfh,
                      unsigned gal_id,
                      unsigned min_snap,
                      unsigned max_snap )
   {
      auto pars = sfh.parents( gal_id );
      for( size_t ii = 0; ii < pars.size(); ++ii )
      {
         std::array<unsigned,2> snap_rng = calc_snapshot_rng( sfh, pars[ii], min_snap, max_snap );
         min_snap = snap_rng[0];
         max_snap = snap_rng[1];
      }
      return std::array<unsigned,2>{
         std::max( min_snap, sfh.snapshot( gal_id ) ),
         std::min( max_snap, sfh.snapshot( gal_id ) )
         };
   }

   unsigned
   calc_num_lines( const age_line<real_type>& ages,
                   const age_line<real_type>& bin_ages,
                   const std::array<real_type,2>& snap_rng,
                   std::vector<unsigned>& line_map )
   {
      float oldest_age = ages[snap_rng[0]];
      unsigned age_idx = 0;
      unsigned line_pos = 0;
      line_map.clear();
      for( unsigned ii = snap_rng[0]; ii >= snap_rng[1] - 1; --ii )
      {
         GLfloat sfh_age = fabs( oldest_age - ages[ii] );

         // Draw any ages from the rebinning set.
         while( age_idx < bin_ages.size() && bin_ages[age_idx] < sfh_age )
         {
            ++line_pos;
            ++age_idx;
         }

         // Now draw the sfh age.
         line_map.push_back( line_pos );
         ++line_pos;
      }

      return line_pos;
   }

   void
   draw_snapshot_range( const simulation& sim,
                        const age_line<real_type>& ages,
                        const age_line<real_type>& bin_ages,
                        const std::array<real_type,2>& snap_rng )
   {
      glDisable( GL_DEPTH_TEST );
      glDisable( GL_LIGHTING );
      glDisable( GL_BLEND );
      glLineStipple( 1, 0b1100001111000011 );
      glEnable( GL_LINE_STIPPLE );
      glColor3f( 0.43, 0.43, 0.43 );
      float oldest_age = ages[snap_rng[0]];
      unsigned age_idx = 0;
      unsigned line_pos = 0;
      for( unsigned ii = snap_rng[0]; ii >= snap_rng[1] - 1; --ii )
      {
         GLfloat sfh_age = fabs( oldest_age - ages[ii] );

         // Draw any ages from the rebinning set.
         while( age_idx < bin_ages.size() && bin_ages[age_idx] < sfh_age )
         {
            GLfloat pos = 50 + 20*line_pos++;
            glColor3f( 0.43, 0.43, 0.43 );
            glEnable( GL_LINE_STIPPLE );
            glBegin( GL_LINES );
            glVertex2f( 50, pos );
            glVertex2f( 500, pos );
            glEnd();
            glDisable( GL_LINE_STIPPLE );

            std::stringstream ss;
            ss << std::fixed << std::setprecision( 1 ) << std::scientific << bin_ages[age_idx];
            hpc::gl::draw_text( ss.str(), 505, pos - 5 );

            ++age_idx;
         }

         // Now draw the sfh age.
         GLfloat pos = 50 + 20*line_pos++;
         glColor3f( 0.7, 0.7, 0.7 );
         glEnable( GL_LINE_STIPPLE );
         glBegin( GL_LINES );
         glVertex2f( 50, pos );
         glVertex2f( 500, pos );
         glEnd();
         glDisable( GL_LINE_STIPPLE );

         std::stringstream ss;
         ss << std::fixed << std::setprecision( 1 ) << std::scientific << sfh_age;
         hpc::gl::draw_text( ss.str(), 505, pos - 5 );
      }
   }

   void
   draw_bin_masses( const simulation& sim,
                    const age_line<real_type>& ages,
                    const age_line<real_type>& bin_ages,
                    const std::vector<real_type>& masses,
                    const std::array<real_type,2>& snap_rng )
   {
      glDisable( GL_DEPTH_TEST );
      glDisable( GL_LIGHTING );
      glDisable( GL_BLEND );
      float oldest_age = ages[snap_rng[0]];
      unsigned age_idx = 0;
      unsigned line_pos = 0;
      real_type sum = std::accumulate( masses.begin(), masses.end(), 0.0 );
      for( unsigned ii = snap_rng[0]; ii >= snap_rng[1] - 1; --ii )
      {
         GLfloat sfh_age = fabs( oldest_age - ages[ii] );

         // Draw any ages from the rebinning set.
         while( age_idx < bin_ages.size() && bin_ages[age_idx] < sfh_age )
         {
            GLfloat fac = masses[age_idx]/sum;
            GLfloat pos = 50 + 20*line_pos++;
            glColor3fv( col_map[masses[age_idx]*1e-10].data() );
            glBegin( GL_QUADS );
            glVertex2f( 580, pos - 9 );
            glVertex2f( 580 + 80*fac, pos - 9 );
            glVertex2f( 580 + 80*fac, pos + 9 );
            glVertex2f( 580, pos + 9 );
            glEnd();

            glColor3f( 0.7, 0.7, 0.7 );
            std::stringstream ss;
            ss << std::fixed << std::setprecision( 1 ) << std::scientific << masses[age_idx]*1e-10;
            ss << " (" << age_idx << ")";
            hpc::gl::draw_text( ss.str(), 665, pos - 5 );

            ++age_idx;
         }

         // Now draw the sfh age.
         ++line_pos;
      }

      // Now draw the final summation.
      glColor3fv( col_map[sum*1e-10].data() );
      glBegin( GL_QUADS );
      glVertex2f( 580, 50 - 9 );
      glVertex2f( 580 + 80, 50 - 9 );
      glVertex2f( 580 + 80, 50 + 9 );
      glVertex2f( 580, 50 + 9 );
      glEnd();

      glColor3f( 0.7, 0.7, 0.7 );
      std::stringstream ss;
      ss << std::fixed << std::setprecision( 1 ) << std::scientific << sum*1e-10;
      hpc::gl::draw_text( ss.str(), 665, 50 - 5 );
   }

   void
   _draw_tree_recurse( tao::sfh const& sfh,
                       unsigned gal_id,
                       hpc::view<std::vector<unsigned>> const& widths,
                       GLfloat x_offs,
                       GLfloat y_offs,
                       std::vector<unsigned>& line_map,
                       unsigned line_pos = 0,
                       GLfloat gal_size = 10 )
   {
      unsigned my_snap = sfh.snapshot( gal_id );
      GLfloat new_x_offs = x_offs + -0.5*(GLfloat)(widths[gal_id]*gal_size + (widths[gal_id] - 1)*5);

      auto pars = sfh.parents( gal_id );
      for( size_t ii = 0; ii < pars.size(); ++ii )
      {
         unsigned par_id = pars[ii];
         unsigned par_snap = sfh.snapshot( par_id );

         new_x_offs += 0.5*(widths[par_id]*gal_size + (widths[par_id] - 1)*5);
         int new_line_pos = line_pos + my_snap - par_snap;
         if( new_line_pos < 0 )
            new_line_pos = 0;
         GLfloat new_y_offs = y_offs + 20*(line_map[new_line_pos] - line_map[line_pos]);

         if( my_snap - par_snap > 1 )
            glColor3ub( 0xe7, 0x64, 0x5a );
         else
            glColor3f( 0.43, 0.43, 0.43 );

         glBegin( GL_LINES );
         glVertex2f( x_offs, y_offs );
         glVertex2f( new_x_offs, y_offs + 20 );
         glVertex2f( new_x_offs, y_offs + 20 );
         glVertex2f( new_x_offs, new_y_offs );
         glEnd();

         _draw_tree_recurse( sfh, par_id, widths, new_x_offs, new_y_offs, line_map, new_line_pos, gal_size );

         new_x_offs += 0.5*(widths[par_id]*gal_size + (widths[par_id] - 1)*5) + 5;
      }

      glColor3fv( col_map[stellar_mass[gal_id]].data() );
      glBegin( GL_QUADS );
      glVertex3f( x_offs + -0.5*gal_size, y_offs + -0.5*gal_size, 0 );
      glVertex3f( x_offs + 0.5*gal_size, y_offs + -0.5*gal_size, 0 );
      glVertex3f( x_offs + 0.5*gal_size, y_offs + 0.5*gal_size, 0 );
      glVertex3f( x_offs + -0.5*gal_size, y_offs + 0.5*gal_size, 0 );
      glEnd();
   }

   void
   draw_sfh_tree( const simulation& sim,
                  tao::sfh const& sfh,
                  unsigned gal_id )
   {
      // Put four additional clipping planes in place.
      glLoadIdentity();
      std::array<GLdouble,4> plane{ { 1, 0, 0, -50 } };
      glClipPlane( GL_CLIP_PLANE0, plane.data() );
      plane[0] = -1; plane[3] = 710;
      glClipPlane( GL_CLIP_PLANE1, plane.data() );
      plane[0] = 0; plane[1] = 1; plane[3] = -44;
      glClipPlane( GL_CLIP_PLANE2, plane.data() );
      plane[0] = 0; plane[1] = -1; plane[3] = win_height - 44;
      glClipPlane( GL_CLIP_PLANE3, plane.data() );
      for( unsigned ii = 0; ii < 4; ++ii )
         glEnable( GL_CLIP_PLANE0 + ii );

      // Calculate sub-heights of each tree node.
      std::vector<unsigned> widths( sfh.size() );
      algorithms::tree_widths( sfh, gal_id, widths );

      // Get snapshot range.
      std::array<unsigned,2> snap_rng_idxs = calc_snapshot_rng( sfh, gal_id );
      std::array<real_type,2> snap_rng{ { (real_type)snap_rng_idxs[0], (real_type)snap_rng_idxs[1] } };

      // Calculate pane size.
      std::vector<unsigned> line_map;
      unsigned num_lines = calc_num_lines( sfh_ages, ssp.bin_ages(), snap_rng, line_map );
      sfh_width = std::max<float>( widths[gal_id]*10 + (widths[gal_id] - 1)*5, 500 );
      sfh_height = num_lines*20 + 10;

      // Offset by translation.
      if( 275 - 0.5*sfh_width + translate_x > 0 )
         translate_x = 0 - 275 + 0.5*sfh_width;
      else if( 275 + 0.5*sfh_width + translate_x < 500 )
         translate_x = 500 - 275 - 0.5*sfh_width;
      if( translate_y > 0 )
         translate_y = 0;
      else if( sfh_height + translate_y < win_height - 100 )
         translate_y = std::min<float>( win_height - 100 - sfh_height, 0 );
      glTranslatef( translate_x, translate_y, 0 );

      // Draw snapshot range.
      draw_snapshot_range( sim, sfh_ages, ssp.bin_ages(), snap_rng );

      // Draw the tree.
      glPolygonMode( GL_FRONT, GL_FILL );
      _draw_tree_recurse( sfh, gal_id, widths, 275, 50, line_map );

      // Plot bins.
      draw_bin_masses( sim, sfh_ages, ssp.bin_ages(), total_masses, snap_rng );

      for( unsigned ii = 0; ii < 4; ++ii )
         glDisable( GL_CLIP_PLANE0 + ii );

      // Plot colour scale.
      real_type min = std::numeric_limits<real_type>::max();
      real_type max = std::numeric_limits<real_type>::min();
      calc_colour_abscissa_recurse( sfh, gal_id, min, max );
      col_map.set_abscissa_linear( min, max );
      glLoadIdentity();
      draw_colour_scale();
   }

   void
   render_sfh_tree()
   {
      draw_sfh_tree( *cur_sim, cur_sfh, cur_gal_id );
   }

}
