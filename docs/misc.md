# Misc notes

### GHA
set up workflow dispatch: https://levelup.gitconnected.com/how-to-manually-trigger-a-github-actions-workflow-4712542f1960

### Data Migrations for Django apps

[good article on how to properly handle data migrations for django apps](https://itnext.io/django-migrations-with-init-containers-on-openshift-597db8138dad)
[migrations using jobs](https://medium.com/@markgituma/kubernetes-local-to-production-with-django-3-postgres-with-migrations-on-minikube-31f2baa8926e)

### KIRK API / Replication overview

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