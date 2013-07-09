#include <iostream>
#include <glut.h>
#include <libhpc/libhpc.hh>
#include "tao/base/types.hh"
#include "tao/base/globals.hh"
#include "tao/base/lightcone.hh"

using namespace hpc;
using namespace tao;

bool rotating = false, zooming = false;
int old_x = 0, old_y = 0;
float rotate_x = 0, rotate_y = 0;
array<float,3> bnd_min, bnd_max;
unsigned num_segs = 0;
float zoom = 1.0;

lightcone<real_type> lc;
list<tile<real_type>> tiles;

void
draw_tile( const tile<real_type>& tile )
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
            unsigned idx )
{
   static const unsigned char colors[11][3] = {
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

   idx = idx%11;
   glColor3f( colors[idx][0]/255.0, colors[idx][1]/255.0, colors[idx][2]/255.0 );
   draw_cap( lc, start, true );
   draw_cap( lc, finish, false );
   draw_edges( lc, start, finish );
}

void
draw_lightcone( const lightcone<real_type>& lc )
{
   glEnable( GL_CULL_FACE );
   glEnable( GL_LIGHTING );
   glPolygonMode( GL_FRONT, GL_FILL );

   // Get the distance bins from the lightcone.
   auto bins = lc.snapshot_bins();

   // Each bin will be given a different color.
   for( unsigned ii = 0; ii < bins.size() - 1; ++ii )
      draw_shell( lc, bins[ii], bins[ii + 1], ii );
}

void
idle()
{
}

void
render()
{
   // Scale longest edge to 1.
   float scale = 0;
   for( unsigned ii = 0; ii < 3; ++ii )
      scale = std::max<float>( scale, bnd_max[ii] - bnd_min[ii] );
   scale = 1.0/scale;

   // Include the zoom.
   scale *= zoom;

   glRotatef( rotate_x, 1, 0, 0 );
   glRotatef( rotate_y, 0, 1, 0 );
   glScalef( scale, scale, scale );
   glTranslatef( -0.5*(bnd_min[0] + bnd_max[0]),
                 -0.5*(bnd_min[2] + bnd_max[2]),
                  0.5*(bnd_min[1] + bnd_max[1]) );

   glDisable( GL_CULL_FACE );
   glDisable( GL_LIGHTING );
   glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );
   glColor3f( 0.43, 0.43, 0.43 );
   for( const auto& tile : tiles )
      draw_tile( tile );

   draw_lightcone( lc );
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
reshape( GLint width,
         GLint height )
{
   static const GLfloat near = 1e-1, far = 10;
   glViewport( 0, 0, width, height );
   glMatrixMode( GL_PROJECTION );
   glLoadIdentity();
   gluPerspective( 65.0, (GLfloat)width/(GLfloat)height, near, far );
   glMatrixMode( GL_MODELVIEW );
}

void
display()
{
   glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT );
   glLoadIdentity();
   gluLookAt( 0, 0, 1.8, 0, 0, 0, 0, 1, 0 );
   render();
   glFlush();
   glutSwapBuffers();
}

void
mouse_button( int button,
              int state,
              int x,
              int y )
{
   // std::cout << button << ", " << state << "\n";

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
   switch( key )
   {
      case 'w':
      case 'W':
         rotate_x -= 5;
         break;

      case 's':
      case 'S':
         rotate_x += 5;
         break;

      case 'd':
      case 'D':
         rotate_y += 5;
         break;

      case 'a':
      case 'A':
         rotate_y -= 5;
         break;

      case 27:   // ESCAPE
         exit( 0 );
   };

   glutPostRedisplay();
}

void
calc_bounds()
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

void
init_tao()
{
   lc.set_simulation( &millennium );
   lc.set_geometry( 40, 50, 40, 50, 0.6 );

   // Setup the number of segments used to render the cone
   // based on the geometry.
   num_segs = to_degrees( std::max( lc.max_ra() - lc.min_ra(), lc.max_dec() - lc.min_dec() ) );
   num_segs = 2.0*(0.1*(float)num_segs + 1.0);

   for( auto tile_it = lc.tile_begin(); tile_it != lc.tile_end(); ++tile_it )
      tiles.push_back( *tile_it );

   calc_bounds();
}

void
start()
{
   // Prepare the window.
   glutInitWindowPosition( 200, 200 );
   glutInitWindowSize( 800, 600 );
   glutInitDisplayMode( GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH );
   glutCreateWindow( "Zen" );

   // Initialise OpenGL.
   init_opengl();

   // Register callbacks.
   glutDisplayFunc( display );
   glutReshapeFunc( reshape );
   glutKeyboardFunc( keyboard );
   glutMouseFunc( mouse_button );
   glutMotionFunc( mouse_motion );
   glutIdleFunc( idle );

   // Initialise system.
   init_tao();

   // Hand over to GLUT.
   glutMainLoop();
}

int
main( int argc, char** argv )
{
   mpi::initialise( argc, argv );
   LOG_CONSOLE();
   glutInit( &argc, argv );
   start();
   mpi::finalise();
   return EXIT_SUCCESS;
}
