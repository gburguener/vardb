# vardb
Toolbox to create and analyze sequence variants from multiple sources.


	>>> from VARDB import initialize
	>>> from VARDB.DbIO import DbIO
	>>> connect_to_db(password="123") #by default it uses a mysql and 'vardb' database name
	>>> db = DbIO()
	>>> db.create_db() 

               
        