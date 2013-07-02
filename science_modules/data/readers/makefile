# Set this variable to point to where you have
# HDF5 installed, if it is in a non-standard
# location. Otherwise leave it blank.
HDF5_DIR=


HDF5_LIBS=-lhdf5_fortran -lhdf5 -lz
ifdef HDF5_DIR
HDF5_FLAGS=-I$(HDF5_DIR)/include -L$(HDF5_DIR)/lib 
else
HDF5_FLAGS=
endif

all: hdf5reader

hdf5reader : hdf5reader.f90
	gfortran -o hdf5reader $(HDF5_FLAGS) hdf5reader.f90 $(HDF5_LIBS)
