#include <iostream>
#include <glut.h>
#include <AntTweakBar.h>
#include <libhpc/libhpc.hh>
#include "tao/base/types.hh"
#include "tao/base/globals.hh"
#include "tao/base/lightcone.hh"

using namespace hpc;
using namespace tao;

enum view_type
{
   MAIN,
   BOX
};

view_type cur_view = MAIN;
bool rotating = false, zooming = false;
int old_x = 0, old_y = 0;
float rotate_x = 0, rotate_y = 0;
array<float,3> bnd_min, bnd_max;
unsigned num_segs = 0;
float zoom = 1;
float gal_size = 10;
GLuint gal_tex_id;

lightcone<real_type> lc;
list<tile<real_type>> tiles;
tile<real_type>* cur_box;

TwBar* main_tb;

const unsigned char colors[11][3] = {
   {94, 79, 162},
   {50, 136, 189},
   {102, 194, 165},
   {171, 221, 164},
   {230, 245, 152},
   {255, 255, 191},
   {254, 224, 139},
   {253, 174, 97},
   {244, 109, 67},
   {213, 62, 79},
   {158, 1, 66}
};

// void
// setup_galaxy_texture()
// {
//    unsigned tex_size = 32;
//    vector<byte> data( tex_size*tex_size*4 );
//    for( int ii = 0; ii < tex_size; ++ii )
//    {
//       float iif = ii - (int)tex_size/2;
//       for( int jj = 0; jj < tex_size; ++jj )
//       {
//          float jjf = jj - (int)tex_size/2;
//          unsigned idx = 4*(ii*tex_size + jj);
//          if( (iif*iif + jjf*jjf) < (tex_size/2)*(tex_size/2) )
//          {
//             data[idx] = data[idx + 1] = data[idx + 2] = 255;
//             data[idx + 3] = 1;
//          }
//          else
//          {
//             data[idx + 0] = data[idx + 1] = data[idx + 2] = data[idx + 3] = 0;
//          }
//       }
//    }

//    glGenTextures( 1, &gal_tex_id );
//    glBindTexture( GL_TEXTURE_2D, gal_tex_id );
//    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, tex_size, tex_size, 0, GL_RGBA, GL_UNSIGNED_BYTE, data.data() );
//    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE );
//    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE );
//    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR );
//    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR );
// }

template< class Tile >
void
draw_tile( const Tile& tile )
{
   auto min = tile.min(), max = tile.max();

   glBegin( GL_POLYGON );
   glVertex3f( min[0], min[2], -min[1] );
   glVertex3f( max[0], min[2], -min[1] );
   glVertex3f( max[0], max[2], -min[1] );
   glVertex3f( min[0], max[2], -min[1] );
   glEnd();

   glBegin( GL_POLYGON );
   glVertex3f( min[0], min[2], -max[1] );
   glVertex3f( max[0], min[2], -max[1] );
   glVertex3f( max[0], max[2], -max[1] );
   glVertex3f( min[0], max[2], -max[1] );
   glEnd();

   glBegin( GL_POLYGON );
   glVertex3f( min[0], min[2], -max[1] );
   glVertex3f( min[0], min[2], -min[1] );
   glVertex3f( min[0], max[2], -min[1] );
   glVertex3f( min[0], max[2], -max[1] );
   glEnd();

   glBegin( GL_POLYGON );
   glVertex3f( max[0], min[2], -min[1] );
   glVertex3f( max[0], min[2], -max[1] );
   glVertex3f( max[0], max[2], -max[1] );
   glVertex3f( max[0], max[2], -min[1] );
   glEnd();
}

void
draw_cap( const lightcone<real_type>& lc,
          float dist,
          bool out )
{
   for( unsigned ii = 0; ii < num_segs; ++ii )
   {
      array<float,2> ra;
      ra[0] = lc.min_ra() + ((float)ii/(float)num_segs)*(lc.max_ra() - lc.min_ra());
      ra[1] = lc.min_ra() + ((float)(ii + 1)/(float)num_segs)*(lc.max_ra() - lc.min_ra());
      for( unsigned jj = 0; jj < num_segs; ++jj )
      {
         array<float,2> dec;
         dec[0] = lc.min_dec() + ((float)jj/(float)num_segs)*(lc.max_dec() - lc.min_dec());
         dec[1] = lc.min_dec() + ((float)(jj + 1)/(float)num_segs)*(lc.max_dec() - lc.min_dec());
         float x, y, z, mag;
         glBegin( GL_POLYGON );
         if( out )
         {
            numerics::ecs_to_cartesian<float>( ra[0], dec[0], x, y, z, dist );
            glNormal3f( x, z, -y );
            glVertex3f( x, z, -y );
            numerics::ecs_to_cartesian<float>( ra[1], dec[0], x, y, z, dist );
            glNormal3f( x, z, -y );
            glVertex3f( x, z, -y );
            numerics::ecs_to_cartesian<float>( ra[1], dec[1], x, y, z, dist );
            glNormal3f( x, z, -y );
            glVertex3f( x, z, -y );
            numerics::ecs_to_cartesian<float>( ra[0], dec[1], x, y, z, dist );
            glNormal3f( x, z, -y );
            glVertex3f( x, z, -y );
         }
         else
         {
            numerics::ecs_to_cartesian<float>( ra[1], dec[0], x, y, z, dist );
            glNormal3f( -x, -z, y );
            glVertex3f( x, z, -y );
            numerics::ecs_to_cartesian<float>( ra[0], dec[0], x, y, z, dist );
            glNormal3f( -x, -z, y );
            glVertex3f( x, z, -y );
            numerics::ecs_to_cartesian<float>( ra[0], dec[1], x, y, z, dist );
            glNormal3f( -x, -z, y );
            glVertex3f( x, z, -y );
            numerics::ecs_to_cartesian<float>( ra[1], dec[1], x, y, z, dist );
            glNormal3f( -x, -z, y );
            glVertex3f( x, z, -y );
         }
         glEnd();
      }
   }
}

void
draw_edges( const lightcone<real_type>& lc,
            float start,
            float finish )
{
   // Calculate the first two surface normals.
   float x, y, z;
   float a, b, c;
   array<GLfloat,3> low_norm, upp_norm;
   numerics::ecs_to_cartesian<float>( lc.min_ra(), lc.min_dec(), x, y, z, start );
   numerics::ecs_to_cartesian<float>( lc.max_ra(), lc.min_dec(), a, b, c, start );
   low_norm[0] = -(y*c - z*b);
   low_norm[1] = -(z*a - x*c);
   low_norm[2] = -(x*b - y*a);
   numerics::ecs_to_cartesian<float>( lc.min_ra(), lc.max_dec(), x, y, z, start );
   numerics::ecs_to_cartesian<float>( lc.max_ra(), lc.max_dec(), a, b, c, start );
   upp_norm[0] = y*c - z*b;
   upp_norm[1] = z*a - x*c;
   upp_norm[2] = x*b - y*a;

   for( unsigned ii = 0; ii < num_segs; ++ii )
   {
      array<float,2> ra;
      ra[0] = lc.min_ra() + ((float)ii/(float)num_segs)*(lc.max_ra() - lc.min_ra());
      ra[1] = lc.min_ra() + ((float)(ii + 1)/(float)num_segs)*(lc.max_ra() - lc.min_ra());
      glBegin( GL_POLYGON );
      glNormal3f( low_norm[0], low_norm[2], -low_norm[1] );
      numerics::ecs_to_cartesian<float>( ra[0], lc.min_dec(), x, y, z, finish );
      glVertex3f( x, z, -y );
      numerics::ecs_to_cartesian<float>( ra[1], lc.min_dec(), x, y, z, finish );
      glVertex3f( x, z, -y );
      numerics::ecs_to_cartesian<float>( ra[1], lc.min_dec(), x, y, z, start );
      glVertex3f( x, z, -y );
      numerics::ecs_to_cartesian<float>( ra[0], lc.min_dec(), x, y, z, start );
      glVertex3f( x, z, -y );
      glEnd();
      glBegin( GL_POLYGON );
      glNormal3f( upp_norm[0], upp_norm[2], -upp_norm[1] );
      numerics::ecs_to_cartesian<float>( ra[1], lc.max_dec(), x, y, z, finish );
      glVertex3f( x, z, -y );
      numerics::ecs_to_cartesian<float>( ra[0], lc.max_dec(), x, y, z, finish );
      glVertex3f( x, z, -y );
      numerics::ecs_to_cartesian<float>( ra[0], lc.max_dec(), x, y, z, start );
      glVertex3f( x, z, -y );
      numerics::ecs_to_cartesian<float>( ra[1], lc.max_dec(), x, y, z, start );
      glVertex3f( x, z, -y );
      glEnd();
   }

   // Second two normals.
   numerics::ecs_to_cartesian<float>( lc.min_ra(), lc.min_dec(), x, y, z, start );
   numerics::ecs_to_cartesian<float>( lc.min_ra(), lc.max_dec(), a, b, c, start );
   low_norm[0] = y*c - z*b;
   low_norm[1] = z*a - x*c;
   low_norm[2] = x*b - y*a;
   numerics::ecs_to_cartesian<float>( lc.max_ra(), lc.min_dec(), x, y, z, start );
   numerics::ecs_to_cartesian<float>( lc.max_ra(), lc.max_dec(), a, b, c, start );
   upp_norm[0] = -(y*c - z*b);
   upp_norm[1] = -(z*a - x*c);
   upp_norm[2] = -(x*b - y*a);

   for( unsigned ii = 0; ii < num_segs; ++ii )
   {
      array<float,2> dec;
      dec[0] = lc.min_dec() + ((float)ii/(float)num_segs)*(lc.max_dec() - lc.min_dec());
      dec[1] = lc.min_dec() + ((float)(ii + 1)/(float)num_segs)*(lc.max_dec() - lc.min_dec());
      glBegin( GL_POLYGON );
      glNormal3f( low_norm[0], low_norm[2], -low_norm[1] );
      numerics::ecs_to_cartesian<float>( lc.min_ra(), dec[1], x, y, z, finish );
      glVertex3f( x, z, -y );
      numerics::ecs_to_cartesian<float>( lc.min_ra(), dec[0], x, y, z, finish );
      glVertex3f( x, z, -y );
      numerics::ecs_to_cartesian<float>( lc.min_ra(), dec[0], x, y, z, start );
      glVertex3f( x, z, -y );
      numerics::ecs_to_cartesian<float>( lc.min_ra(), dec[1], x, y, z, start );
      glVertex3f( x, z, -y );
      glEnd();
      glBegin( GL_POLYGON );
      glNormal3f( upp_norm[0], upp_norm[2], -upp_norm[1] );
      numerics::ecs_to_cartesian<float>( lc.max_ra(), dec[0], x, y, z, finish );
      glVertex3f( x, z, -y );
      numerics::ecs_to_cartesian<float>( lc.max_ra(), dec[1], x, y, z, finish );
      glVertex3f( x, z, -y );
      numerics::ecs_to_cartesian<float>( lc.max_ra(), dec[1], x, y, z, start );
      glVertex3f( x, z, -y );
      numerics::ecs_to_cartesian<float>( lc.max_ra(), dec[0], x, y, z, start );
      glVertex3f( x, z, -y );
      glEnd();
   }
}

void
draw_shell( const lightcone<real_type>& lc,
            float start,
            float finish,
            unsigned idx,
            float alpha = 1 )
{
   idx = idx%11;
   glColor4f( colors[idx][0]/255.0, colors[idx][1]/255.0, colors[idx][2]/255.0, alpha );
   draw_cap( lc, start, true );
   draw_cap( lc, finish, false );
   draw_edges( lc, start, finish );
}

void
draw_lightcone( const lightcone<real_type>& lc,
                float alpha = 1 )
{
   glEnable( GL_CULL_FACE );
   glEnable( GL_LIGHTING );
   glPolygonMode( GL_FRONT, GL_FILL );

   // Get the distance bins from the lightcone.
   auto bins = lc.snapshot_bins();

   // Each bin will be given a different color.
   for( unsigned ii = 0; ii < bins.size() - 1; ++ii )
   {
      unsigned idx = bins.size() - ii - 2;
      draw_shell( lc, bins[idx], bins[idx + 1], ii, alpha );
   }
}

void
draw_redshift_scale( const lightcone<real_type>& lc )
{
   float len = 0.8;
   int num_cols = 11;

   glPolygonMode( GL_FRONT, GL_FILL );
   for( unsigned ii = 0; ii < num_cols; ++ii )
   {
      float h = len/(float)num_cols;
      float pos = -0.4 + ((float)ii)*h;
      glColor3f( colors[ii][0]/255.0, colors[ii][1]/255.0, colors[ii][2]/255.0 );
      glBegin( GL_POLYGON );
      glVertex3f( 0.63,  pos, -1 );
      glVertex3f( 0.7,  pos, -1 );
      glVertex3f( 0.7, pos + h, -1 );
      glVertex3f( 0.63, pos + h, -1 );
      glEnd();
   }

   glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );
   glColor3f( 0.7, 0.7, 0.7 );
   glBegin( GL_POLYGON );
   glVertex3f( 0.63, -0.4, -1 );
   glVertex3f( 0.7, -0.4, -1 );
   glVertex3f( 0.7, 0.4, -1 );
   glVertex3f( 0.63, 0.4, -1 );
   glEnd();
   for( unsigned ii = 0; ii < num_cols + 1; ++ii )
   {
      float h = len/(float)num_cols;
      float pos = -0.4 + ((float)ii)*h;
      glBegin( GL_LINES );
      glVertex3f( 0.63, pos, -1 );
      glVertex3f( 0.71, pos, -1 );
      glEnd();
   }
}

void
idle()
{
}

// template< class T >
// void
// billboard_matrix( const array<T,3>& pos,
//                   T* mat )
// {
//    mat[8] = cam[0] - bill[0];
//    mat[9] = cam[1] - bill[1];
//    mat[10] = cam[2] - bill[2];
//    float mag = 1.0/sqrt( mat[8]*mat[8] + mat[9]*mat[9] + mat[10]*mat[10] );
//    mat[8] *= mag;
//    mat[9] *= mag;
//    mat[10] *= mag;

//    mat[0] = cam_up[1]*mat[10] - cam_up[2]*mat[9];
//    mat[1] = cam_up[2]*mat[8] - cam_up[0]*mat[10];
//    mat[2] = cam_up[0]*mat[9] - cam_up[1]*mat[8];

//    mat[4] = mat[9]*mat[2] - mat[10]*mat[1];
//    mat[5] = mat[10]*mat[0] - mat[8]*mat[2];
//    mat[6] = mat[8]*mat[1] - mat[9]*mat[0];

//    for( unsigned ii = 0; ii < 16; ++ii )
//       mat[ii] = 0.0;
//    mat[0] = mat[5] = mat[10] = mat[15] = 1;

//    mat[12] = pos[0];
//    mat[13] = pos[2];
//    mat[14] = -pos[1];

//    mat[3] = mat[7] = mat[11] = 0;
//    mat[15] = 1;
// }

void
draw_galaxies()
{
   array<float,3> pos;
   srand( 1 );
   // glEnable( GL_TEXTURE_2D );
   // glBindTexture( GL_TEXTURE_2D, gal_tex_id );
   // glTexEnvi( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE );
   // glDisable( GL_DEPTH_TEST );
   glPolygonMode( GL_FRONT, GL_FILL );
   glDisable( GL_LIGHTING );
   // glEnable( GL_BLEND );
   // glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA );

   for( unsigned ii = 0; ii < 1000; ++ii )
   {
      pos[0] = 500.0*((float)rand())/((float)RAND_MAX);
      pos[1] = 500.0*((float)rand())/((float)RAND_MAX);
      pos[2] = 500.0*((float)rand())/((float)RAND_MAX);
      mass = 1e10*((float)rand()/(float)RAND_MAX);

      glPushMatrix();
      glTranslatef( pos[0], pos[2], -pos[1] );
      glRotatef( -rotate_y, 0, 1, 0 );
      glRotatef( -rotate_x, 1, 0, 0 );
      glColor3fv( col_map[mass].data() );
      glBegin( GL_POLYGON );
      // glTexCoord2f( 0, 0 );
      glVertex3f( -0.5*gal_size, -0.5*gal_size, 0 );
      // glTexCoord2f( 1, 0 );
      glVertex3f( 0.5*gal_size, -0.5*gal_size, 0 );
      // glTexCoord2f( 1, 1 );
      glVertex3f( 0.5*gal_size, 0.5*gal_size, 0 );
      // glTexCoord2f( 0, 1 );
      glVertex3f( -0.5*gal_size, 0.5*gal_size, 0 );
      glEnd();
      glPopMatrix();
   }
   // glDisable( GL_TEXTURE_2D );
}

float
setup_scale()
{
   // Scale longest edge to 1.
   float scale = 0;
   for( unsigned ii = 0; ii < 3; ++ii )
      scale = std::max<float>( scale, bnd_max[ii] - bnd_min[ii] );
   scale = 1.0/scale;

   // Include the zoom.
   scale *= zoom;

   return scale;
}

void
setup_interaction( float scale )
{
   glRotatef( rotate_x, 1, 0, 0 );
   glRotatef( rotate_y, 0, 1, 0 );
   glScalef( scale, scale, scale );
   glTranslatef( -0.5*(bnd_min[0] + bnd_max[0]),
                 -0.5*(bnd_min[2] + bnd_max[2]),
                 0.5*(bnd_min[1] + bnd_max[1]) );
}

void
render_main()
{
   float scale = setup_scale();
   setup_interaction( scale );

   glEnable( GL_DEPTH_TEST );
   glDisable( GL_CULL_FACE );
   glDisable( GL_LIGHTING );
   glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );
   glColor3f( 0.43, 0.43, 0.43 );
   for( const auto& tile : tiles )
      draw_tile( tile );

   draw_lightcone( lc );

   glLoadIdentity();
   glDisable( GL_LIGHTING );
   glDisable( GL_DEPTH_TEST );
   glDisable( GL_CULL_FACE );
   draw_redshift_scale( lc );
}

void
render_box_view()
{
   float scale = setup_scale();
   setup_interaction( scale );

   glEnable( GL_DEPTH_TEST );
   glDisable( GL_CULL_FACE );
   glDisable( GL_LIGHTING );
   glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );
   glColor3f( 0.43, 0.43, 0.43 );
   draw_tile( *cur_box );

   draw_galaxies();

   glEnable( GL_BLEND );
   glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA );
   draw_lightcone( lc, 0.2 );
   glDisable( GL_BLEND );
}

void
init_opengl()
{
   glEnable( GL_DEPTH_TEST );
   glDepthFunc( GL_LESS );
   glShadeModel( GL_SMOOTH );
   glCullFace( GL_BACK );
   glClearColor( 0.23, 0.23, 0.23, 1 );

   // GLfloat mat_ambient[] = { 1, 1, 1, 1 };
   // GLfloat mat_specular[] = { 1, 1, 1, 1 };
   // GLfloat mat_shininess[] = { 100 };
   GLfloat light_position[] = { 4, 3, 4 };
   // glMaterialfv( GL_FRONT, GL_SPECULAR, mat_specular );
   // glMaterialfv( GL_FRONT, GL_SHININESS, mat_shininess );
   // glColorMaterial( GL_FRONT, GL_AMBIENT_AND_DIFFUSE );
   glEnable( GL_COLOR_MATERIAL );
   glLightfv( GL_LIGHT0, GL_POSITION, light_position );
   glEnable( GL_LIGHT0 );
   glEnable( GL_NORMALIZE );
}

void
calc_bounds()
{
   if( cur_view == MAIN )
   {
      std::fill( bnd_min.begin(), bnd_min.end(), std::numeric_limits<float>::max() );
      std::fill( bnd_max.begin(), bnd_max.end(), -std::numeric_limits<float>::max() );
      for( const auto& tile : tiles )
      {
         for( unsigned ii = 0; ii < 3; ++ii )
         {
            bnd_min[ii] = std::min<float>( tile.min()[ii], bnd_min[ii] );
            bnd_max[ii] = std::max<float>( tile.max()[ii], bnd_max[ii] );
         }
      }
   }
   else
   {
      std::copy( cur_box->min().begin(), cur_box->min().end(), bnd_min.begin() );
      std::copy( cur_box->max().begin(), cur_box->max().end(), bnd_max.begin() );
   }
}

void
reshape( GLint width,
         GLint height )
{
   static const GLfloat near = 1e-1, far = 10;
   glViewport( 0, 0, width, height );
   glMatrixMode( GL_PROJECTION );
   glLoadIdentity();
   gluPerspective( 65.0, (GLfloat)width/(GLfloat)height, near, far );
   glMatrixMode( GL_MODELVIEW );
   TwWindowSize( width, height );
}

void
display()
{
   glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT );
   glLoadIdentity();
   gluLookAt( 0, 0, 1.8, 0, 0, 0, 0, 1, 0 );
   switch( cur_view )
   {
      case MAIN:
         render_main();
         break;
      case BOX:
         render_box_view();
         break;
   };
   glFlush();
   TwDraw();
   glutSwapBuffers();
   glutPostRedisplay();
}

void
mouse_button( int button,
              int state,
              int x,
              int y )
{
   if( TwEventMouseButtonGLUT( button, state, x, y ) )
      return;

   switch( button )
   {
      case 0:
         rotating = (state == 0);
         old_x = x;
         old_y = y;
         break;

      case 2:
         zooming = (state == 0);
         old_y = y;
         break;
   };
}

void
mouse_motion( int x,
              int y )
{
   if( TwEventMouseMotionGLUT( x, y ) )
      return;

   if( rotating )
   {
      int dx = x - old_x;
      int dy = y - old_y;
      old_x = x;
      old_y = y;
      rotate_y += dx;
      rotate_x += dy;
      glutPostRedisplay();
   }
   else if( zooming )
   {
      int dy = old_y - y;
      old_y = y;
      zoom += 0.1*(float)dy;
      zoom = std::max<float>( zoom, 1.0 );
      glutPostRedisplay();
   }
}

void
keyboard( unsigned char key,
          int x,
          int y )
{
   if( TwEventKeyboardGLUT( key, x, y ) )
      return;

   switch( key )
   {
      case 'b':
         cur_view = BOX;
         cur_box = &tiles.front();
         calc_bounds();
         break;
      case 'm':
         cur_view = MAIN;
         cur_box = NULL;
         calc_bounds();
         break;
      case 27:   // ESCAPE
         exit( 0 );
   };

   glutPostRedisplay();
}

void
update_tao()
{
   // Setup the number of segments used to render the cone
   // based on the geometry.
   num_segs = to_degrees( std::max( lc.max_ra() - lc.min_ra(), lc.max_dec() - lc.min_dec() ) );
   num_segs = 2.0*(0.1*(float)num_segs + 1.0);

   tiles.clear();
   for( auto tile_it = lc.tile_begin(); tile_it != lc.tile_end(); ++tile_it )
      tiles.push_back( *tile_it );

   calc_bounds();

   glutPostRedisplay();
}

void
init_tao()
{
   lc.set_simulation( &millennium );
   lc.set_geometry( 40, 50, 40, 50, 0.6, 0.15 );
   update_tao();
}

void TW_CALL
set_min_ra( const void* val,
            void* data )
{
   double _val = *(const double*)val;
   lc.set_min_ra( _val );
   string def = string( " Main/MaxRA min=" ) + to_string( _val + 1 ) + " ";
   TwDefine( def.c_str() );
   update_tao();
}

void TW_CALL
get_min_ra( void* val,
            void* data )
{
   *(double*)val = to_degrees( lc.min_ra() );
}

void TW_CALL
set_max_ra( const void* val,
            void* data )
{
   double _val = *(const double*)val;
   lc.set_max_ra( _val );
   string def = string( " Main/MinRA max=" ) + to_string( _val - 1 ) + " ";
   TwDefine( def.c_str() );
   update_tao();
}

void TW_CALL
get_max_ra( void* val,
            void* data )
{
   *(double*)val = to_degrees( lc.max_ra() );
}

void TW_CALL
set_min_dec( const void* val,
             void* data )
{
   double _val = *(const double*)val;
   lc.set_min_dec( _val );
   string def = string( " Main/MaxDEC min=" ) + to_string( _val + 1 ) + " ";
   TwDefine( def.c_str() );
   update_tao();
}

void TW_CALL
get_min_dec( void* val,
             void* data )
{
   *(double*)val = to_degrees( lc.min_dec() );
}

void TW_CALL
set_max_dec( const void* val,
             void* data )
{
   double _val = *(const double*)val;
   lc.set_max_dec( _val );
   string def = string( " Main/MinDEC max=" ) + to_string( _val - 1 ) + " ";
   TwDefine( def.c_str() );
   update_tao();
}

void TW_CALL
get_max_dec( void* val,
             void* data )
{
   *(double*)val = to_degrees( lc.max_dec() );
}

void TW_CALL
set_min_z( const void* val,
           void* data )
{
   double _val = *(const double*)val;
   lc.set_min_redshift( _val );
   string def = string( " Main/MaxZ min=" ) + to_string( _val + 0.01 ) + " ";
   TwDefine( def.c_str() );
   update_tao();
}

void TW_CALL
get_min_z( void* val,
           void* data )
{
   *(double*)val = lc.min_redshift();
}

void TW_CALL
set_max_z( const void* val,
           void* data )
{
   double _val = *(const double*)val;
   lc.set_max_redshift( _val );
   string def = string( " Main/MinZ max=" ) + to_string( _val - 0.01 ) + " ";
   TwDefine( def.c_str() );
   update_tao();
}

void TW_CALL
get_max_z( void* val,
           void* data )
{
   *(double*)val = lc.max_redshift();
}

void
start()
{
   // Prepare the window.
   glutInitWindowPosition( 200, 200 );
   glutInitWindowSize( 800, 600 );
   glutInitDisplayMode( GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH );
   glutCreateWindow( "Zen" );

   // Register callbacks.
   glutDisplayFunc( display );
   glutReshapeFunc( reshape );

   TwInit( TW_OPENGL, NULL );
   glutKeyboardFunc( keyboard );
   glutMouseFunc( mouse_button );
   glutMotionFunc( mouse_motion );
   glutPassiveMotionFunc( (GLUTmousemotionfun)TwEventMouseMotionGLUT );
   glutSpecialFunc( (GLUTspecialfun)TwEventSpecialGLUT );
   glutIdleFunc( idle );
   TwGLUTModifiersFunc( glutGetModifiers );

   main_tb = TwNewBar( "Main" );
   TwDefine(" GLOBAL help='This example shows how to integrate AntTweakBar with GLUT and OpenGL.' "); // Message added to the help bar.
   TwDefine(" Main size='200 400' color='96 216 224' "); // change default tweak bar size and color
   TwAddVarCB( main_tb, "MinRA", TW_TYPE_DOUBLE, set_min_ra, get_min_ra, NULL,
               " label='Minimum RA' min=0 max=49 step=1 help='Minimum right-ascension.' " );
   TwAddVarCB( main_tb, "MaxRA", TW_TYPE_DOUBLE, set_max_ra, get_max_ra, NULL,
               " label='Maximum RA' min=41 max=90 step=1 help='Maximum right-ascension.' " );
   TwAddVarCB( main_tb, "MinDEC", TW_TYPE_DOUBLE, set_min_dec, get_min_dec, NULL,
               " label='Minimum DEC' min=0 max=49 step=1 help='Minimum declination.' " );
   TwAddVarCB( main_tb, "MaxDEC", TW_TYPE_DOUBLE, set_max_dec, get_max_dec, NULL,
               " label='Maximum DEC' min=41 max=90 step=1 help='Maximum declination.' " );
   TwAddVarCB( main_tb, "MinZ", TW_TYPE_DOUBLE, set_min_z, get_min_z, NULL,
               " label='Minimum redshift' min=0 max=0.49 step=0.01 help='Minimum redshift.' " );
   TwAddVarCB( main_tb, "MaxZ", TW_TYPE_DOUBLE, set_max_z, get_max_z, NULL,
               " label='Maximum redshift' min=0.14 max=127 step=0.01 help='Maximum redshift.' " );

   // Initialise OpenGL.
   init_opengl();

   // // Setup textures.
   // setup_galaxy_texture();

   // Initialise system.
   init_tao();

   // Hand over to GLUT.
   glutMainLoop();
}

int
main( int argc, char** argv )
{
   mpi::initialise( argc, argv );
   // LOG_CONSOLE();
   glutInit( &argc, argv );
   start();
   mpi::finalise();
   return EXIT_SUCCESS;
}
