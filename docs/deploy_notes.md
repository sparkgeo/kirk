# Overview

<img src="https://www.thewrap.com/wp-content/uploads/2014/10/Shatner.jpeg" width="600px">

PP_KIRK is a replication system that defines replication configurations in a database.

* [Local Developement Testing](#Local-Developement-Testing)
* [Data Migrations](#Data-Migrations)
* [FME Related Information](#KIRK-API-/-Replication-overview)
* [Openshift Deployment]()
* [Debugging Openshift Deployment Notes](#Debugging-Openshift-Deployments)

# Local Developement Testing

## Dev Machine

run the server and make sure it does what its suppose to:

```
python ./src/backend/app_kirk_rest/manage.py runserver
```

Then hit 127.0.0.1:8000 to verify the app is working

## Test Dockerfile

Build the image:

`docker build -t kirk:latest  .`

## Run the image
`docker run -p 8000:8000 kirk`

then hit the same address... 127.0.0.1:8000 to verify everything is workin in the container.

assuming it is, test on openshift...

## Build Image

a github action has been setup to build images on pull request to dev. (not implemented ATM)

# Data Migrations

### data model migrations:

* ~~python manage.py makemigrations api~~
* ~~python manage.py migrate api~~

*not required, now part of helm deployment*

### loading fixtures

these are a one time load!  Only need to be loaded when the new openshift project
is created.

Log into a kirk pod and run the following command there.  This is a one time thing
for net new installs.  Could create a job to do this and configure with a flag that
triggers its run.

* `python manage.py loaddata Destination_Keywords.json`
* `python manage.py loaddata fme_data_types.json`
* `python manage.py loaddata job_data.json`

### create superuser

Also a one time thing for new deployment to openshift, before doing this change the email and the username
listed below.

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
       
# Openshift Deployment

Kirk app has automated builds, the automation currently stops there, the deployments
are templated but require manually running the template.

## Template Deployment

*Note: This may be changing as we work to convert the templates to helm charts*

There are currently two templates:
1. KIRK application and all the dependencies used by that app.
1. Database backup which is based on the bcgov backup container

### Deploying Kirk

The docker images used for KIRK are built using github actions.

Deploying kirk to a namespace, the example below shows using a parameter file...
```
NAMESPACE=<namespace in oc to deploy to>
oc -n $NAMESPACE process -f ./openshift/kirk_oc_template.yaml --param-file <path to parameter file> | oc -n $NAMESPACE create -f - 
```

Secrets that should be populated either with -P overrides or with a parameter file:

* GITHUB_PACKAGE_ACCESS_JSON_BASE64 - base 64 encoded github package access json
* CONTAINER_SRC - path used by docker to refer to the image, example: docker.pkg.github.com/bcgov/kirk/kirk
* CONTAINER_SRC_SECRET_NAME - name of the secret that will be created and used to gain access to the github packages
* ENV - environment string
* DEPLOY_NAMESPACE - openshift namespace
* IMAGE_LABEL - docker image tag
* DB_SECRETS_NAME - name of the secret used to store db data.
* PGDB_NAME - name of the postgres database that will be created
* PGDB_PASSWORD - database password
* PGDB_USER - database user
* PGDB_PORT - database port

### Deploying Backup Container

Currently using a slighly modified version of the backup container from here:
https://github.com/franTarkenton/backup-container

Changes from the parent version:
* configured github action to build image
* Copied the rest of the configs and am storing with local repo.

#### Parameters that should be overriden
* **TAG_NAME** - The package tag from the backup-container repo that is to be deployed
* **DATABASE_SECRET_NAME** - name of the database secrets (re-used not created, this is created by kirk deploy)
* **DATABASE_USER_KEY_NAME** - key in the secret above that contains the db user
* **DATABASE_PASSWORD_KEY_NAME** - key that contains the database password
* **BACKUP_VOLUME_NAME** - backup volume name
* **BACKUP_VOLUME_SIZE** - backup size
* **VERIFICATION_VOLUME_SIZE** - verification volume size
* **VERIFICATION_VOLUME_CLASS** - verification volume class
* **ENVIRONMENT_FRIENDLY_NAME** - descriptive name of the backup container 
* **GITHUB_PACKAGE_ACCESS_SECRET_NAM** - name of the secret that will be created to access the github packages
* **GITHUB_PACKAGE_ACCESS_JSON_BASE64** - 64 bit encoded json snippet with the github personal access token that can be used to read the packages
* **BACKUP_CONFIG** - backup configuration string that goes in  the backup config map

to deploy process and run the template: *backup-deploy.json*

## Data Migrations for deployments

[good article on how to properly handle data migrations for django apps](https://itnext.io/django-migrations-with-init-containers-on-openshift-597db8138dad)
[migrations using jobs](https://medium.com/@markgituma/kubernetes-local-to-production-with-django-3-postgres-with-migrations-on-minikube-31f2baa8926e)

# Debugging Openshift Deployments

### Get the pods

`oc get pods`

kirk pod will have a prefix of *kirk-dc*

### Log into a kirk pod

`oc rsh <kirk pod name>`

### Verify that you can communicate from the kirk pod to the database pod:

`curl -v telnet://postgresql-svc:5432`

**on helm deploy renamed the service so use:
`curl -v telnet://kirk-postgres-svc:5432`


### Verify that kirk pod can talk to the db

``` python
import psycopg2
import os
dbname = os.environ['POSTGRES_DB_NAME']
dbuser = os.environ['POSTGRES_USER_NAME']
dbhost = os.environ['POSTGRES_HOST']
dbpasswd = os.environ['POSTGRES_PASSWORD']
connStr = f"dbname='{dbname}' user='{dbuser}' host='{dbhost}' password='{dbpasswd}'"
db = psycopg2.connect(connStr)
```

### Configure Port Forwarding on db pod

This is to capture that communication exists between the pods, by
capturing traffic to the db pod.

*Parameterized example*

`oc port-forward <podname> <srcport>:<destport>`

*with a hypothetical pod name*

`oc port-forward postgresql-dc-1-4x9h6 5432:5432`

### deploy quickstart nsp examples:
In theory these network security profiles (NSP's) will render the network 
security policies similar to default policies configured in OCP3.

```
NAMESPACE=<project namespace>
oc process -f https://raw.githubusercontent.com/BCDevOps/platform-services/master/security/aporeto/docs/sample/quickstart-nsp.yaml NAMESPACE=$NAMESPACE | oc create -f -
```

[link to github file](https://github.com/BCDevOps/platform-services/blob/master/security/aporeto/docs/sample/quickstart-nsp.yaml)

[example NSP policy in oc template](https://github.com/bcgov/cass-api/blob/master/openshift/templates/api/api-postgres-deploy.yaml)

### Get network security policies
`oc get networksecuritypolicies`

or 

`oc get nsp`

## Postgres Database Debugging:

The following cheat sheets shows how to connect to a database, list tables
etc...

[postgresql cheat sheet](https://www.postgresqltutorial.com/postgresql-cheat-sheet/)

Rest of the sections here are a bunch of misc tasks that I have performed to debug / data migrate etc from database to database.

### dump database to backup file

`pg_dump -Fp -h $POSTGRESQL_SVC_SERVICE_HOST -p $POSTGRESQL_SVC_SERVICE_PORT -U POSTGRESQL_USER $POSTGRESQL_DATABASE > dumpfile.gz`

### Connect / Login to database

`psql -U $POSTGRESQL_USER`

### drop database
`psql -ac "DROP DATABASE $POSTGRESQL_DATABASE"`

### copy data to a pod
`oc rsync junk postgresql-dc-1-qs9sl:/var/lib/pgsql/data/userdata/tmp`

### log into pod and run this to restore
`gunzip < db_dump.gz | psql -v ON_ERROR_STOP=1 -x  -d $POSTGRESQL_DATABASE`