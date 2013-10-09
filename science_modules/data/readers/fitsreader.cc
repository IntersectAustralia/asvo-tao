#include <string.h>
#include <stdio.h>
#include "fitsio.h"
#include <iostream>

using namespace std;

int main(int argc, char *argv[])
{
	fitsfile *fptr;      /* FITS file pointer, defined in fitsio.h */
	char *val, value[1000], nullstr[]="*";
	char keyword[FLEN_KEYWORD], colname[FLEN_VALUE],coltype[FLEN_VALUE],colDtype[FLEN_VALUE];
	int status = 0;   /*  CFITSIO status value MUST be initialized to zero!  */
	int hdunum, hdutype, ncols, anynul;
	long nrows;

	if (argc < 2)
	{
		printf("please specify an input file.\n");
		return 0;
	}

	if (!fits_open_file(&fptr, argv[1], READONLY, &status))
	{
		if ( fits_get_hdu_num(fptr, &hdunum) == 1 )
			/* This is the primary array;  try to move to the */
			/* first extension and see if it is a table */
			fits_movabs_hdu(fptr, 2, &hdutype, &status);
		else
			fits_get_hdu_type(fptr, &hdutype, &status); /* Get the HDU type */

		if (hdutype == IMAGE_HDU)
			cout<<"Error: this program only displays tables, not images"<<endl;
		else
		{
			fits_get_num_rows(fptr, &nrows, &status);
			fits_get_num_cols(fptr, &ncols, &status);

			cout<<"Number of Columns="<<ncols<<endl;



			/* print column names as column headers */

			for (int ii = 1; ii <= ncols; ii++)
			{
				int dispwidth;
				fits_make_keyn("TTYPE", ii, keyword, &status);
				fits_read_key(fptr, TSTRING, keyword, colname, NULL, &status);
				fits_get_col_display_width(fptr, ii, &dispwidth, &status);
				colname[dispwidth] = '\0';  /* truncate long names */

				fits_make_keyn("TUNIT", ii, keyword, &status);
				fits_read_key(fptr, TSTRING, keyword, coltype, NULL, &status);

				fits_make_keyn("TFORM", ii, keyword, &status);
				fits_read_key(fptr, TSTRING, keyword, colDtype, NULL, &status);
				string DataTypestr="";

				switch(colDtype[0])
				{
				case 'J':
					DataTypestr="Integer";
					break;
				case 'D':
					DataTypestr="Double";
					break;
				case 'K':
					DataTypestr="64 Bit Integer";
					break;
				case 'A':
					DataTypestr="String";
					break;
				default:
					DataTypestr="Not Supported";
					break;
				}

				cout<< colname<<":"<<coltype<<":"<<DataTypestr<<endl;
			}


			cout<<"Number of Rows="<<nrows<<endl;


			/* print each column, row by row (there are faster ways to do this) */
			val = value;
			for (long jj = 1; jj <= nrows && !status; jj++)
			{
				cout<<"("<< jj<<"):";
				for (int ii = 1; ii <= ncols; ii++)
				{
					/* read value as a string, regardless of intrinsic datatype */
					if (fits_read_col_str (fptr,ii,jj, 1, 1, nullstr, &val, &anynul, &status) )
						break;  /* jump out of loop on error */

					cout<<value;
					if(ii < ncols)
						cout<<",";
				}
				cout<<endl;
			}

		}
		fits_close_file(fptr, &status);
	}

	if (status) fits_report_error(stderr, status); /* print any error message */
	return(status);
}
