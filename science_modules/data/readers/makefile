# Set locations to point to HDF5, FITS and PUGIXML (required for VO) 
# installed, if it is in a non-standard location. Otherwise leave it 
# blank.

HDF5_DIR=
FITS_DIR=
PUGIXML=


HDF5_LIBS=-lhdf5_fortran -lhdf5
ifdef HDF5_DIR
HDF5_FLAGS=-I$(HDF5_DIR)/include -L$(HDF5_DIR)/lib 
else
HDF5_FLAGS=
endif


FITS_LIBS=-lcfitsio
ifdef FITS_DIR
FITS_FLAGS=-I$(FITS_DIR)/include -L$(FITS_DIR)/lib 
else
FITS_FLAGS=
endif


ifdef PUGIXML
VO_FLAGS=-I$(PUGIXML)/src/
else
VO_FLAGS=
endif

VO_FORT_FLAGS=`FoX-config`


all: hdf5readerF90 hdf5readerC fitsreaderF90 fitsreaderCC votablereaderF90 votablereaderCC

hdf5readerF90 : hdf5reader.f90
	gfortran -o hdf5readerF90 $(HDF5_FLAGS) hdf5reader.f90 $(HDF5_LIBS) || true

hdf5readerC: hdf5reader.c
	gcc -o hdf5readerC $(HDF5_FLAGS) hdf5reader.c $(HDF5_LIBS) || true

fitsreaderF90 : fitsreader.f90
	gfortran -o fitsreaderF90 $(FITS_FLAGS) fitsreader.f90 $(FITS_LIBS) || true

fitsreaderCC: fitsreader.cc
	g++ -o fitsreaderCC $(FITS_FLAGS) fitsreader.cc $(FITS_LIBS) || true

votablereaderF90 : votablereader.f90
	gfortran -o votablereaderF90 votablereader.f90 $(VO_FORT_FLAGS) || true

votablereaderCC: votablereader.cc
	g++ -o votablereaderCC votablereader.cc $(VO_FLAGS) || true

default: all

clean:
	rm hdf5readerF90 hdf5readerC fitsreaderF90 fitsreaderCC votablereaderF90 votablereaderCC
