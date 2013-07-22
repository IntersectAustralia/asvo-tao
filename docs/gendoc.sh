#!/bin/bash

if [ "$1" = "doxygen" ]; then
  run_doxygen='Y'
fi

rm -rf build/*
if [ -n "$run_doxygen" ]; then
  echo 'RUNNING DOXYGEN. YOU HAVE TO COMMIT CHANGES TO doxyxml !!!'
  rm -rf doxyxml/*
  doxygen Doxyfile.conf
fi
sphinx-build -b html ./source ./build
test -d ../web/static/docs && rm -rf ../web/tao/static/docs && mkdir ../web/tao/static/docs && echo "Empty docs"
cp -r build/* ../web/tao/static/docs
