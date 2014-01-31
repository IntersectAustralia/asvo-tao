#ifndef tao_base_backend_hh
#define tao_base_backend_hh

#include <libhpc/profile/timer.hh>
#include "simulation.hh"
#include "types.hh"

namespace tao {

   ///
   /// Base class for TAO backends. A backend defines access to
   /// data sources for astronomical datasets. For example, the
   /// datasets could be stored in a database (relational or
   /// otherwise), in HDF5 files or even simple text files. The
   /// backends abstract the storage from the processing.
   ///
   class backend
   {
   public:

      ///
      /// Construct with a simulation.
      ///
      /// @param[in] sim The simulation this backend refers to.
      ///
      backend( tao::simulation const* sim = nullptr );

      ///
      /// Set the simulation. Each backend is constructed to
      /// represent a particular dataset, which itself must refer
      /// to a simulation.
      ///
      /// @param[in] sim The simulation this backend refers to.
      ///
      virtual
      void
      set_simulation( tao::simulation const* sim );

      ///
      /// Get the simulation.
      ///
      /// @returns The simulation this backend refers to.
      ///
      tao::simulation const*
      simulation() const;

      ///
      /// Load the simulation details from the dataset. In most
      /// circumstances the simulation metadata will be stored
      /// along with the simulation data.
      ///
      /// @returns The loaded simulation.
      ///
      virtual
      tao::simulation const*
      load_simulation() = 0;

      hpc::profile::timer&
      timer();

   protected:

      tao::simulation const* _sim;
      hpc::profile::timer _timer;
   };

}

#endif
