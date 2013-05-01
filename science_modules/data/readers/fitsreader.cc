/////// This File has been modified from tablist CFITSIO sample
// g++ fitsreader.cc -L/usr/local/x86_64/gnu/cfitsio-3.290/lib -lcfitsio -I/usr/local/x86_64/gnu/cfitsio-3.290/include -o fitreader
// g++ fitsreader.cc -L/home/amr/Downloads/cfitsio/lib -lcfitsio -I/home/amr/Downloads/cfitsio/include -o fitreader

#include <string.h>
#include <stdio.h>
#include "fitsio.h"


int main(int argc, char *argv[])
{
	fitsfile *fptr;      /* FITS file pointer, defined in fitsio.h */
	char *val, value[1000], nullstr[]="*";
	char keyword[FLEN_KEYWORD], colname[FLEN_VALUE];
	int status = 0;   /*  CFITSIO status value MUST be initialized to zero!  */
	int hdunum, hdutype, ncols, anynul, dispwidth[1000];
	long nrows;

	if (!fits_open_file(&fptr, argv[1], READONLY, &status))
	{
		if ( fits_get_hdu_num(fptr, &hdunum) == 1 )
			/* This is the primary array;  try to move to the */
			/* first extension and see if it is a table */
			fits_movabs_hdu(fptr, 2, &hdutype, &status);
		else
			fits_get_hdu_type(fptr, &hdutype, &status); /* Get the HDU type */

		if (hdutype == IMAGE_HDU)
			printf("Error: this program only displays tables, not images\n");
		else
		{
			fits_get_num_rows(fptr, &nrows, &status);
			printf("Number of Rows=%ld \n",nrows);
			fits_get_num_cols(fptr, &ncols, &status);


			for (int lcol = 1; lcol <= ncols; lcol++)
			{
				fits_get_col_display_width(fptr, lcol, &dispwidth[lcol], &status);
			}


			/* print column names as column headers */
			printf("\n    ");
			for (int ii = 1; ii <= ncols; ii++)
			{
				fits_make_keyn("TTYPE", ii, keyword, &status);
				fits_read_key(fptr, TSTRING, keyword, colname, NULL, &status);
				colname[dispwidth[ii]] = '\0';  /* truncate long names */
				printf("%*s ",dispwidth[ii], colname);
			}
			printf("\n");  /* terminate header line */

			/* print each column, row by row (there are faster ways to do this) */
			val = value;
			for (long jj = 1; jj <= nrows && !status; jj++)
			{
				printf("(%4ld) ", jj);
				for (int ii = 1; ii <= ncols; ii++)
				{
					/* read value as a string, regardless of intrinsic datatype */
					if (fits_read_col_str (fptr,ii,jj, 1, 1, nullstr,
							&val, &anynul, &status) )
						break;  /* jump out of loop on error */

					printf("%-*s ",dispwidth[ii], value);
				}
				printf("\n");
			}

		}
		fits_close_file(fptr, &status);
	}

	if (status) fits_report_error(stderr, status); /* print any error message */
	return(status);
}
