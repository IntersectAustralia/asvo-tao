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

  protected:
    void _read_options( const options::xml_dict& global_dict );

    string _sqlquery;
    string _language;

    bool _pass_through;

    string _database;
    string _server;

  };
}


#endif
