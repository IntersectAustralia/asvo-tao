#!/bin/bash

export PATH=../web/bin:$PATH
rm -rf build/*
rm -rf doxyxml/*
doxygen Doxyfile.conf
sphinx-build -b html ./source ./build
test -d ../web/static/docs && rm -rf ../web/tao/static/docs
cp -r build ../web/tao/static/docs
