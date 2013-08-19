#!/bin/bash
set -e

BUILDDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ "$1" = "doxygen" ]; then
  run_doxygen='Y'
fi

rm -rf build/*
if [ -n "$run_doxygen" ]; then
  echo 'RUNNING DOXYGEN. YOU HAVE TO COMMIT CHANGES TO doxyxml !!!'
  rm -rf doxyxml/*
  doxygen Doxyfile.conf
fi

# Generate sample script archive
# This will be copied in to the downloads directory as part of the sphinx-build
test -d "$BUILDDIR/tmp" && rm -rf "$BUILDDIR/tmp"
mkdir $BUILDDIR/tmp
cd $BUILDDIR/../science_modules/data
zip -r $BUILDDIR/tmp/samplescripts.zip readers
cd $BUILDDIR

sphinx-build -b html ./source ./build
test -d ../web/static/docs && rm -rf ../web/tao/static/docs && mkdir ../web/tao/static/docs && echo "Empty docs"
cp -r build/* ../web/tao/static/docs

# Tidy up
rm -r "$BUILDDIR/tmp"

