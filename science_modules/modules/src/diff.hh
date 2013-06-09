#ifndef tao_modules_diff_hh
#define tao_modules_diff_hh

namespace tao {

   template< class InputIterator >
   void
   differentiate( InputIterator func_begin,
		  const InputIterator& func_end,
		  OutputIterator result,
		  typename InputIterator::value_type step_size )
   {
      typedef typename InputIterator::value_type value_type;

      if( func_end != func_begin )
      {
	 value_type fac = 2*step_size;
	 value_type central = *func_begin++;
	 if( func_end != func_begin )
	 {
	    value_type left, right = *func_begin++;

	    // Forward difference for the first entry.
	    *result++ = (right - central)/step_size;

	    while( func_begin != func_end )
	    {
	       // Central differences for middle entries.
	       left = central;
	       central = right;
	       right = *func_begin++;
	       *result++ = (right - left)/fac;
	    }

	    // Backward difference for final entry.
	    *result++ = (right - central)/step_size;
	 }
      }
   }

}

#endif
