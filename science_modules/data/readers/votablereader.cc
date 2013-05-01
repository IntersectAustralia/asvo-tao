// g++ votablereader.cc -L/home/amr/workspace/asvo-tao-science/science_modules/external_packages/pugixml/lib -lpugixml -I/home/amr/workspace/asvo-tao-science/science_modules/external_packages/pugixml/include -o votablereader
//g++ votablereader.cc -L/lustre/projects/p014_swin/amr_work/asvo-tao-science/science_modules/external_packages/pugixml/lib -lpugixml -I/lustre/projects/p014_swin/amr_work/asvo-tao-science/science_modules/external_packages/pugixml/include -o votablereader

/// The main Intension of this sample is to provide a simple and easy way to access the data stored and it is not a standard votable reader

#include <pugixml.hpp>
#include <string.h>
#include <stdio.h>

using namespace pugi;


int main(int argc, char *argv[])
{

	//FileName=argv[1]
	xml_document inp_doc;
	if( inp_doc.load_file(argv[1]) == false )
	{
		printf("Error! I can't open the file as an XML doc\n");
		return -1;
	}
	xml_node Table_node = inp_doc.select_single_node( "/VOTABLE/TABLE" ).node();

	xml_node TableData_node = inp_doc.select_single_node( "/VOTABLE/TABLE/DATA/TABLEDATA" ).node();
	inp_doc.select_nodes( "/VOTABLE/TABLE/FIELD" );



	return 0;
}
