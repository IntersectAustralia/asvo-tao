#include "settingReader.hh"
#include <iostream>
using namespace std;

namespace tao
{

	SettingReader::SettingReader(string BasicSettingsFile,string ParamsFile)
	{
		ReadBasicXMLSettings(BasicSettingsFile);
		ReadXMLParams(ParamsFile);
	}

	SettingReader::~SettingReader()
	{

	}

	void SettingReader::ReadBasicXMLSettings(string FileName)
	{
		pugi::xml_document doc;
		// Load the File and validate that the loading was done correctly
		pugi::xml_parse_result result=doc.load_file(FileName.c_str());
		if(result)
		{

			// Fill the Current Setting Struct with its values
			CurrentBasicSettings.ServerIP=_GetNodeWithAssert(doc,"/settings/Database/serverip").child_value();
			CurrentBasicSettings.Port=_GetNodeWithAssert(doc,"/settings/Database/port").text().as_int();
			CurrentBasicSettings.UserName=_GetNodeWithAssert(doc,"/settings/Database/user").child_value();
			CurrentBasicSettings.Password=_GetNodeWithAssert(doc,"/settings/Database/password").child_value();
			CurrentBasicSettings.TablePrefix=_GetNodeWithAssert(doc,"/settings/Database/TreeTablePrefix").child_value();

		}
		else
		{
			//File Loading was not performed Correctly
			cout<<"Error loading the basic settings file. The error is : "<<result.description()<<endl;
			assert(result);
		}


	}
	void SettingReader::ReadXMLParams(string FileName)
	{

		pugi::xml_parse_result result=ParamsDoc.load_file(FileName.c_str());
		if(result)
		{

			//Get The Current UserName
			CurrentBasicSettings.CurrentUserName=_GetNodeWithAssert(ParamsDoc,"/tao/username").child_value();
			CurrentBasicSettings.CurrentDB=_GetNodeWithAssert(ParamsDoc,"/tao/database").child_value();


		}
		else
		{
			//File Loading was not performed Correctly
			cout<<"Error loading the basic settings file. The error is : "<<result.description()<<endl;
			assert(result);
		}


	}
	xml_node SettingReader::_GetNodeWithAssert(pugi::xml_document& doc,string XPathQuery)
	{

		xml_node SENode=doc.select_single_node(XPathQuery.c_str()).node();
		if(SENode.empty())
		{
			cout<<"Error Node Empty. Node Path= "<<XPathQuery<<endl;
			assert(!SENode.empty());
		}
		return SENode;
	}

	LightConeParams SettingReader::LoadLightCone()
	{
		LightConeParams Params;
		Params.ModuleVersion=_GetNodeWithAssert(ParamsDoc,"/tao/workflow/lightcone/moduleversion").child_value();
		Params.Geometry=_GetNodeWithAssert(ParamsDoc,"/tao/workflow/lightcone/geometry").child_value();
		Params.Simultation=_GetNodeWithAssert(ParamsDoc,"/tao/workflow/lightcone/simulation").child_value();
		Params.GalaxyModel=_GetNodeWithAssert(ParamsDoc,"/tao/workflow/lightcone/galaxymodel").child_value();
		Params.BoxRepetition=_GetNodeWithAssert(ParamsDoc,"/tao/workflow/lightcone/boxrepetition").child_value();

		Params.NumberofCones=_GetNodeWithAssert(ParamsDoc,"/tao/workflow/lightcone/numcones").text().as_int();

		Params.redshiftmin=_GetNodeWithAssert(ParamsDoc,"/tao/workflow/lightcone/redshiftmin").text().as_float();
		Params.redshiftmax=_GetNodeWithAssert(ParamsDoc,"/tao/workflow/lightcone/redshiftmax").text().as_float();

		Params.ramin=_GetNodeWithAssert(ParamsDoc,"/tao/workflow/lightcone/ramin").text().as_float();
		Params.ramax=_GetNodeWithAssert(ParamsDoc,"/tao/workflow/lightcone/ramax").text().as_float();
		Params.decmin=_GetNodeWithAssert(ParamsDoc,"/tao/workflow/lightcone/decmin").text().as_float();
		Params.decmax=_GetNodeWithAssert(ParamsDoc,"/tao/workflow/lightcone/decmax").text().as_float();

		xml_node OutputNodes=_GetNodeWithAssert(ParamsDoc,"/tao/workflow/lightcone/outputfields");

		for (pugi::xml_node OutputNode = OutputNodes.child("item"); OutputNode; OutputNode = OutputNode.next_sibling("item"))
		{
			OutputField F;
			F.FieldLabel=OutputNode.attribute("label").value();
			F.FieldDBName=OutputNode.child_value();
			Params.OutputFieldsList.push_back(F);
		}



	    string rngseed=_GetNodeWithAssert(ParamsDoc,"/tao/workflow/lightcone/rngseed").child_value();

	    return Params;

	}








}
