#ifndef tao_modules_settingreader_hh
#define tao_modules_settingreader_hh

#ifdef HAVE_POSTGRESQL
#include <soci/postgresql/soci-postgresql.h>
#endif
#include <soci/soci.h>
#include <libhpc/libhpc.hh>
#include <vector>
#include <iostream>
#include <pugixml.hpp>
#include "libhpc/containers/string.hh"
#include <libhpc/options/dictionary.hh>


namespace tao
{
   using namespace hpc;
   using namespace pugi;

   struct BasicSettings
   {
	   string ServerIP;
	   int Port;
	   string UserName;
	   string Password;
	   string TablePrefix;
	   string CurrentUserName;
	   string CurrentDB;
	   string WorkingFolder;
	   string LogFolder;
   };

   struct OutputField
   {
	   string FieldDBName;
	   string FieldLabel;
   };

   struct LightConeParams
   {
	   string ModuleVersion;
	   string Geometry;
	   string Simultation;
	   string GalaxyModel;
	   string BoxRepetition;

	   int NumberofCones;

	   float redshiftmin;
	   float redshiftmax;

	   float ramin,ramax;
	   float decmin,decmax;

	   vector<OutputField> OutputFieldsList;


	   string rngseed;


   };


   class SettingReader
   {
   	   public:
	   	   SettingReader(string BasicSettingsFile,string ParamsFile);
		  ~SettingReader();
		  BasicSettings CurrentBasicSettings;
		  LightConeParams LoadLightCone();




   	   protected:
		  pugi::xml_document ParamsDoc;
		  xml_node _GetNodeWithAssert(pugi::xml_document& doc,string XPathQuery);
		  void ReadBasicXMLSettings(string FileName);
		  void ReadXMLParams(string FileName);

   };

}
#endif

