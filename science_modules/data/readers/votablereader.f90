! Fox Library is needed to use this code
! http://www1.gly.bris.ac.uk/~walker/FoX/source/
! gfortran votablereader.f90 -o votablereader_f `FoX-config`


      program main

	use FoX_dom
  	implicit none

	integer :: i
	integer :: j
	type(Node), pointer :: document, element,Field, datapoint, datacolumn 
	type(NodeList), pointer :: fieldsList, dataList,childlist
	document => parseFile("/home/amr/workspace/tao.0.xml")

	fieldsList => getElementsByTagname(document, "FIELD")
	dataList => getElementsByTagname(document, "TR")

	print*, "There are ", getLength(fieldsList), " Fields in this VOTable file."
	print*, "There are ", getLength(dataList), " Data Point in this VOTable file."

	do i = 0, getLength(fieldsList) - 1
   	 Field => item(fieldsList, i)
	 print*, i,":",getAttribute(Field, "name"),":",getAttribute(Field, "datatype"),":",getAttribute(Field, "unit")
	enddo

	do i = 0, getLength(dataList) - 1
   	 datapoint => item(dataList, i)
	 childlist => getElementsByTagname(datapoint, "TD")
	 print *,'Data Point (',i,')'
	 do j = 0, getLength(childlist) - 1
	   datacolumn => item(childlist, j)
	   print *,'    ',getTextContent(datacolumn)
	 enddo
	enddo

	
	call destroy(document)



      end

