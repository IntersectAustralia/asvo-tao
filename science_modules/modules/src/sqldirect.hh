#ifndef tao_sqldirect_sqldirect_hh
#define tao_sqldirect_sqldirect_hh

#include "tao/base/base.hh"
#include "tao/base/types.hh"



namespace tao {
using namespace hpc;

class sqldirect: public module
{
public:

	sqldirect( const string& name = string(),pugi::xml_node base = pugi::xml_node() );

	~sqldirect();

	static module* factory( const string& name,pugi::xml_node base );
	virtual	void initialise( const options::xml_dict& global_dict );
	///
	/// Run the module.
	///
	virtual void execute();
	virtual	tao::galaxy& galaxy();


	///
	/// Begin iterating over galaxies.
	///
	void begin();

	///
	/// Check for completed iteration.
	///
	bool done();

	///
	/// Advance to next galaxy.
	///
	void operator++();

	///
	/// Get current galaxy.
	///
	tao::galaxy& operator*();



protected:
	void _read_options( const options::xml_dict& global_dict );

	string _sqlquery;
	string _language;

	bool _pass_through;

	tao::galaxy _gal;
	profile::progress _prog;

	string _database;
	std::list<string>::iterator _Tables_it;



	vector<void*> _field_stor;
	vector<galaxy::field_value_type> _field_types;
	vector<string> _field_names;
	long _OutputLimit;
	long _RecordsCount;
	bool _IsRecordLimitReached;
	bool RecordLimitReached();
	void FetchData(string query);
	void PrepareGalaxyObject(string query);


};
}


#endif
