=============================
Notes for Mac OS/X Developers
=============================

This is a dump of the notes from the Developer Setup wiki page, it needs lots of love...

Mac users+:&nbsp;On Mac OS X, the dmg enables the GUI wizard from the Applications folder and the doxygen CLI is not&nbsp;

enabled by default. However, doxygen CLI is still there in the Resources folder of the application.

If installed for all users, a command like:

$ ln \-s /Applications/Doxygen.app/Contents/Resources/doxygen /usr/bin/

in the terminal will enable it. Otherwise, link it to a folder in your PATH.

On Mac OS X, the dmg enables the GUI wizard from the Applications folder and the doxygen CLI is not&nbsp;
enabled by default. However, doxygen CLI is still there in the Resources folder of the application.
If installed for all users, a command like:

$ ln \-s /Applications/Doxygen.app/Contents/Resources/doxygen /usr/bin/

in the terminal will enable it. Otherwise, link it to a folder in your PATH.

To install mysql:

\* download using homebrew:

brew install mysql

