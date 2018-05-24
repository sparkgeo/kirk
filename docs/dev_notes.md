# Overview
PP_KIRK is a replication system that defines replication configurations in a database. 

# REST API
The APP_KIRK is initially going to be set up to use two rest-apis.
1.   The first will use and oracle trigger that will make a rest call based on a
     defined schedule. to FME Server.  It will send a single argument:
       - Jobid

2.   Having received a rest call FME Server will initiate a job.  It will query
     the APP_KIRK api for the following information:
        - sources (jobid) GET / POST / UPDATE / DELETE
        - destinations (jobid)
        - fieldmap (jobid)
        
        - would be nice to get all this information as a single query 
          something like getJobInfo GET
        

For Later on creating new entries in the API:
1.   View Jobs w/ sources /w destinations /w transformer switches
     basically this table would be the starting point for configurations

2.   Add new Job, allows you to:
     a) define the source data
     b) define the destination data
     c) (optional) define the source data field map
     d) (optional) define the transformer switches
          - These get defined on as needed basis, each transformer switch
            will have its own configuration parameters.
        
  
  
  
Job Triggered
  - Sends jobid with Rest call
  - FMW then starts excution
      - using job id:
         - rest call to get sources
         - rest call to get destinations
         - rest call to get transformers
         - rest call to get ???
       Would be nice to be able to just make one call that returns
       all this info.
       
  

# Theoretical Datamodel
The datamodel used to define replications will include the following features:
*Not worrying about this at the moment, datamodel will evolve as the app gets*
*developed*

a) Job Description:
    - job status
    - source data definition
    - destination data definition

b) source data type
    - could be database in which case need
       - host
       - servicename
       - port 
       - database type (sql server / oracle / postgres)
    - file based
       - container (directory of something like fgdb)
       - feature class (table)
    
c) destinations
    - initially set up using id's to destination defs.  Opens the door
      for writing to other data types down the road.
      
d) field map
    - unique id
    - source field
    - destination field
    - types?  (think this might be required)
    - target type?
    
      
d) reporting
    - thinking this would be a table that reports on the number of  records
      in the sources / destination, before and after.
    - need to think more about what this would do.




Currently
configured for an oracle database but could likely be modified to work with any 
database.