PROGRAM read_hdf5
  USE hdf5
  IMPLICIT NONE

  ! NOTE: Modify this parameter to reflect the number of fields
  ! you would like to read out of the file.
  INTEGER, PARAMETER :: num_fields = 3

  INTEGER, PARAMETER :: max_chunk_size = 100
  ! NOTE: Change filename to your input file
  CHARACTER(LEN=12), PARAMETER :: filename = "tao.output.0"
  INTEGER, PARAMETER :: mem_rank = 1

  ! NOTE: Add storage for additional fields here.
  REAL, DIMENSION(max_chunk_size) :: pos_x, pos_y, pos_z

  INTEGER(HID_T) :: file_id, memspace_id, dataspace_id
  INTEGER(HID_T), DIMENSION(num_fields) :: dataset_ids
  INTEGER(HSIZE_T), DIMENSION(1) :: mem_dims = (/ max_chunk_size /)
  INTEGER :: chunk_size, chunk_start, ii, jj, size
  INTEGER :: error
  INTEGER(HSIZE_T), DIMENSION(1) :: data_dims, max_data_dims, offset, count

  CALL h5open_f(error)

  CALL h5fopen_f( filename, H5F_ACC_RDONLY_F, file_id, error )

  ! NOTE: Add extra copies of these lines to open the dataset
  ! from the HDF5 file. Notice that each call uses a dataset
  ! identifier that is numbered. Be sure to increment the index
  ! with each call.
  CALL h5dopen_f( file_id, "k_apparent", dataset_ids(1), error )
  CALL h5dopen_f( file_id, "v_apparent", dataset_ids(2), error )
  CALL h5dopen_f( file_id, "bub_apparent", dataset_ids(3), error )

  CALL h5dget_space_f( dataset_ids(1), dataspace_id, error )
  CALL h5sget_simple_extent_dims_f( dataspace_id, data_dims, max_data_dims, error )

  CALL h5screate_simple_f( mem_rank, data_dims, memspace_id, error )

  size = data_dims(1)
  offset = 0

  data_dims(1) = max_chunk_size

  chunk_start = 0
  DO WHILE (chunk_start < size)

     chunk_size = MIN( size - chunk_start, max_chunk_size )

     offset = chunk_start
     count = chunk_size
     CALL h5sselect_hyperslab_f( dataspace_id, H5S_SELECT_SET_F, offset, count, error )

     offset = 0
     CALL h5sselect_hyperslab_f( memspace_id, H5S_SELECT_SET_F, offset, count, error )

     ! NOTE: Add a copy of one of these lines to read the contents of
     ! the datasets. Notice that you must provide the dataset ID and
     ! the storage location.
     CALL H5dread_f( dataset_ids(1), H5T_NATIVE_REAL, pos_x, data_dims, error, memspace_id, dataspace_id )
     CALL H5dread_f( dataset_ids(2), H5T_NATIVE_REAL, pos_y, data_dims, error, memspace_id, dataspace_id )
     CALL H5dread_f( dataset_ids(3), H5T_NATIVE_REAL, pos_z, data_dims, error, memspace_id, dataspace_id )

     ! NOTE: Add any required writing/processing here.
     DO ii = 1, chunk_size
        WRITE( *, '(E10.3,A)', ADVANCE="NO" ) pos_x(ii), "  "
        WRITE( *, '(E10.3,A)', ADVANCE="NO" ) pos_y(ii), "  "
        WRITE( *, '(E10.3,A)', ADVANCE="NO" ) pos_z(ii), "  "
        PRINT*,''
     END DO

     chunk_start = chunk_start + chunk_size

  END DO

END PROGRAM
