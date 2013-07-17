      program main

!  This FITS Table Loader has been modified from CFITSIO cookbook
!  It is customized to read TAO FITS files

      integer status,unit,rmode,blocksize,hdutype,ntable,colcount
      integer felem,nelems,nullj,nfound,irow,colnum,icol,fvalueint
      real nulle
      real*8 fvaluedbl	      
      character filename*100,nullstr*1,fvaluestr*8,comment*80,format*5
      character*10, pointer :: ttype(:)
      character*10, pointer :: tunit(:)
      character*5, pointer :: tformat(:)
      logical anynull
      integer*4 rowscount
      integer*8 fvaluelng

!  The STATUS parameter must always be initialized.
      status=0

!  Get an unused Logical Unit Number to use to open the FITS file.
      call ftgiou(unit,status)

!  Open the FITS file
      if (iargc() .lt. 1) then
        write(*,*)"please specify an input file."
        call EXIT(0)
      endif
      CALL getarg(1, filename)

      rmode=0
      call ftopen(unit,filename,rmode,blocksize,status)

      ntable=2
      hdutype=0	
!  Move to the first extension
      call ftmahd(unit,ntable,hdutype,status)


      if (hdutype .eq. 2)then
        print *,'Reading binary table' 
      else
        print *,'Extension is not supported' 
	CALL EXIT(-1) 
      end if

!  Read Columns Count	  
	  call ftgkyj(unit,'TFIELDS',colcount,comment,status)
	  print *,'Number of Columns:',colcount



!  Read the TTYPEn keywords, which give the names of the columns
          
	  allocate (ttype(colcount))
	  call ftgkns(unit,'TTYPE',1,colcount,ttype,nfound,status)

          allocate (tunit(colcount))
	  call ftgkns(unit,'TUNIT',1,colcount,tunit,nfound,status)          

          allocate (tformat(colcount))
	  call ftgkns(unit,'TFORM',1,colcount,tformat,nfound,status)          


	  do icol=1,colcount
		  print *,'Column: ',ttype(icol),':',tunit(icol),':',tformat(icol)
	  end do 

!  Read Rows Count	  
	  call ftgkyk(unit,'NAXIS2',rowscount,comment,status)
	  print *,'Number of Rows:',rowscount


!  Read the data, one row at a time, and print them out
          felem=1
          nelems=1
          nullstr=' '
          nullj=0
          nulle=0.
          do irow=1,rowscount

              do colnum=1,colcount
		      format=tformat(colnum)(1:1)
		      if (format=='K') then
		              call ftgcvk(unit,colnum,irow,felem,nelems,nullj,fvaluelng,anynull,status)
	      		      WRITE( *, '(I15)', ADVANCE="NO" )fvaluelng

		      else if (format=='D') then
		              call ftgcvd(unit,colnum,irow,felem,nelems,nulle,fvaluedbl,anynull,status)
	      		      WRITE( *, '(D10.3)', ADVANCE="NO" )fvaluedbl

		      else if (format=='J') then
		              call ftgcvj(unit,colnum,irow,felem,nelems,nullj,fvalueint,anynull,status)
	      		      WRITE( *, '(I10)', ADVANCE="NO" )fvalueint

		      else if (format=='A') then
		              call ftgcvs(unit,colnum,irow,felem,nelems,nullstr,fvaluestr,anynull,status)
	      		      WRITE( *, '(A)', ADVANCE="NO" )fvaluestr

		      end if	

		     if (colnum==colcount) then
			PRINT *,''
		     end if

	      end do		


          end do


!  The FITS file must always be closed before exiting the program. 
!  Any unit numbers allocated with FTGIOU must be freed with FTFIOU.
      call ftclos(unit, status)
      call ftfiou(unit, status)


      end

