#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include "tao/sed.hh"

using namespace hpc;
using namespace tao;

#include "mpi_fixture.hh"

///
/// SED class test suite.
///
class sed_suite : public CxxTest::TestSuite
{
public:

   ///
   /// Test default constructor.
   ///
   void test_ctor()
   {
     sed mod;
   }

   ///
   /// Test no galaxies.
   ///
   void test_no_galaxies()
   {
   }

   ///
   /// Test no time-points.
   ///
   void test_no_timepoints()
   {
   }

   ///
   /// Test no time-points.
   ///
   void test_no_timepoints()
   {
   }

   ///
   /// Test invalid input array sizes.
   ///
   /// The stellar mass production rates and metallicities must all
   /// be the correct sized arrays in order to function. I expect
   /// errors to be raised if this is not the case.
   ///
   void test_array_sizes()
   {
   }

   ///
   /// Test invalid spectral bands.
   ///
   /// While it's possible to run the code with zero spectral
   /// bands, it doesn't make much sense. I expect an error to
   /// be raised if this happens.
   ///
   void test_num_spectral_bands()
   {
   }

   ///
   /// Test single-stellar population array size.
   ///
   /// When reading from the SSP table, it should return a row
   /// of the same size as the number of spectral bands. I
   /// expect an error to be thrown if this is not the case.
   ///
   void test_ssp_size()
   {
   }

   ///
   /// Test metallicity interpolation.
   ///
   /// Check the regions of metallicity interpolation. It should
   /// look like the following:
   ///
   ///    Metallicity range | Index
   ///   ---------------------------
   ///    0.0000 - 0.0005   | 0
   ///    0.0005 - 0.0025   | 1
   ///    0.0025 - 0.0070   | 2
   ///    0.0070 - 0.0150   | 3
   ///    0.0150 - 0.0300   | 4
   ///    0.0300 - 0.0550   | 5
   ///    0.0550 - inf      | 6
   ///
   void test_metal_interp()
   {
   }

   ///
   /// Test spectral summation.
   ///
   void test_sepctral_sum()
   {
   }

   void setUp()
   {
      CLEAR_STACK_TRACE();

      this->num_ranks = mpi::comm::world.size();
      this->my_rank = mpi::comm::world.rank();
   }

private:

   int num_ranks, my_rank;
};
