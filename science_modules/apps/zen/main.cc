#include <iostream>
#include <glut.h>
#include <libhpc/libhpc.hh>
#include "tao/base/types.hh"
#include "tao/base/globals.hh"
#include "tao/base/lightcone.hh"

using namespace hpc;
using namespace tao;

float rotate_x = 0, rotate_y = 0;
float scale = 1.0/500.0;

lightcone<real_type> lc;
list<box<real_type>> boxes;

void
draw_box( const box<real_type>& box )
{
   auto min = box.min(), max = box.max();
   for( unsigned ii = 0; ii < 3; ++ii )
   {
      min[ii] *= scale;
      max[ii] *= scale;
   }

   glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );
   glColor3f( 1, 1, 1 );

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
idle()
{
}

void
render()
{
   glRotatef( rotate_x, 1, 0, 0 );
   glRotatef( rotate_y, 0, 1, 0 );
   glTranslatef( -4, -4, 4 );

   for( const auto& box : boxes )
      draw_box( box );
}

void
init_opengl()
{
   glEnable( GL_DEPTH_TEST );
   glDepthFunc( GL_LESS );
   glShadeModel( GL_SMOOTH );
   glClearColor( 0.7, 0.7, 0.7, 1 );
}

void
reshape( GLint width,
         GLint height )
{
   static const GLfloat near = 1, far = 1000;
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
   gluLookAt( 0, 0, 14, 0, 0, 0, 0, 1, 0 );
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
}

void
mouse_motion( int x,
              int y )
{
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
init_tao()
{
   lc.set_simulation( &millennium );
   lc.set_geometry( 10, 80, 10, 80, 1, 0.9 );

   for( auto box_it = lc.box_begin(); box_it != lc.box_end(); ++box_it )
      boxes.push_back( *box_it );
}

void
start()
{
   // Prepare the window.
   glutInitWindowSize( 640, 480 );
   glutInitDisplayMode( GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH );
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
   glutInit( &argc, argv );
   start();
   mpi::finalise();
   return EXIT_SUCCESS;
}
