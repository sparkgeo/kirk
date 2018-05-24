# APP_KIRK (Keeping Information Replicated Kontinuously)
**APP_KIRK** moves away from conventional [FME](https://www.safe.com/) replication 
configuration model where replication metadata is stored in individual scripts.
Replication metadata includes:
   - Source dataset / table
   - Destination dataset / table
   - Data Transformations 

APP_KIRK re-uses FMW scripts populating them at run time with parameters that 
get retrieved from a database.  The approach makes replication information more 
transparent as replication metadata is stored in plain database tables as oppose
embedded in individual FME scripts.  

Re-using FMW's also makes it much easier for us to switch to different reader / 
writers.

App is currently under development with primary priority being the construction 
of the REST api to broker communication to the database layer.