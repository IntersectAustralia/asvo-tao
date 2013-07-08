#include "glut.h"

void
render()
{
}

void
init_opengl()
{
   glEnable( GL_DEPTH_TEST );
   glDepthFunc( GL_LESS );
   glShadeModel( GL_SMOOTH );
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
   gluLookAt( 0, 0, 10, 0, 0, -1, 0, 1, 0 );
   render();
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
      case 27:   // ESCAPE
         exit( 0 );
   };
}

int
main( int argc, char** argv )
{
   // Prepare the window.
   glutInit( &argc, &argv );
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

   // Hand over to GLUT.
   glutMainLoop();

   return EXIT_SUCCESS;
}
