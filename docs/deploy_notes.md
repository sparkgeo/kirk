# Overview
PP_KIRK is a replication system that defines replication configurations in a database.

# Migrations
### data model migrations:

* ~~python manage.py makemigrations api~~
* ~~python manage.py migrate api~~


*not required, now part of dockerfile*

### loading fixtures: 
these are a one time load!  Only need to be loaded when the new openshift project
is created.

* `python manage.py loaddata Destination_Keywords.json`
* `python manage.py loaddata fme_data_types.json`
* `python manage.py loaddata job_data.json`

### create superuser
Also a one time thing for new deployment to openshift, before doing this change the email and the username
listed below

`python manage.py createsuperuser --email <su email address> admin@example.com --username <su username>`

### create api token
Only the first time kirk is set up.
`$ python manage.py drf_create_token spock`

Then put api token into pmp along with the superuser you created in the previous
step.


# KIRK API / Replication overview

1.   FME Schedules will be configured to run the APPKIRK_FGDB.fmw.  Each 
     schedule will call the fmw with a different jobid.

2.   FME will retrieve from the rest api the rest of the transformation config
     data associated with the job:
        - sources 
        - destinations
        - fieldmaps
        - transformers
        
3.  the APPKIRK_FGDB.fmw proceeds and completes the replication.

4.  *future*: update the status of the job back to kirk
          
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
         
       

        
  
