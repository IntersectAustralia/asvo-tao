#include <pugixml.hpp>
#include <string.h>
#include <stdio.h>
#include <iostream>

using namespace pugi;
using namespace std;

int main(int argc, char *argv[])
{
	xml_document inp_doc;

	if (argc < 2)
	{
		printf("please specify an input file.\n");
		return 0;
	}
	if( inp_doc.load_file(argv[1]) == false )
	{
		printf("Error! I can't open the file as an XML doc\n");
		return -1;
	}
	xml_node Table_node = inp_doc.select_single_node( "/VOTABLE/TABLE" ).node();

	//Metadata
	xpath_node_set Fields=inp_doc.select_nodes( "/VOTABLE/RESOURCE/TABLE/FIELD" );
	int index=1;
	cout<<"Number of Columns: "<<Fields.size()<<endl;
	for (pugi::xpath_node_set::const_iterator it = Fields.begin(); it != Fields.end(); it++)
	{
	    pugi::xml_node node = (*it).node();
	    cout << "("<<index<<")\t" << node.attribute("name").value()<<":\t"<<node.attribute("datatype").value();
	    cout << ":\t" << node.attribute("unit").value()<<endl;
	    index++;
	}

	//File Data
	xpath_node_set TableData_nodes = inp_doc.select_nodes( "/VOTABLE/RESOURCE/TABLE/DATA/TABLEDATA/TR" );
	cout<<"Number of Rows: "<<TableData_nodes.size()<<endl;
	index=1;
	for (pugi::xpath_node_set::const_iterator it = TableData_nodes.begin(); it != TableData_nodes.end(); it++)
	{
		cout << "("<<index<<")\t";
		pugi::xml_node node = (*it).node();
		for (pugi::xml_node datanode = node.first_child(); datanode; datanode = datanode.next_sibling())
		{
			cout<<datanode.child_value();
			if(datanode.next_sibling())
				cout<<",";
		}
		cout<<endl;

		index++;
	}


	return 0;
}
