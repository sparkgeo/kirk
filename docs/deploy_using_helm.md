# Overview

Initially created the deployment for kirk using openshift templates.  This is working
but have since evolved the openshift template approach to a helm chart.  Using the 
helm chart is now the preferred way to deploy KIRK.

# Net new project space

With a brand new openshift project space the following steps will deploy all the 
various objects required

## Log into openshift
Grab the login command from the openshift console

## Choose correct project

Get a list of all the projects you have access to

`oc projects`

log into a specific project

`oc project <project name>`

## Deploy the helm chart

### Define secret parameters file for the deployment

The following secrets need to be defined, the easiest way to define them is 
create a parameter file by coping the code snippet below and populate with 
the parameters you want.

```
app_name: <app name>
env: <dev or prod env>

# Parameters used to create and connect to the postgres database that
# sits behind kirk
kirk_pgdb_params:
  # Annotations to add to the service account
  annotations: {}
  # The user that will be created in the database and for 
  # subsequent database connections.
  kirk_database_user: <application database user>
  kirk_database_password: <application database user password>
  kirk_database_name: <application database name>
  kirk_database_port: <application database port>

# Secret name that contains the database parameters described above
kirk_pgdb_secret_name: <name of the secret for the database secrets>

# License plate for openshift namespaces
license_plate: <license plate>
        
```

### install the chart

```
helm install kirk-install kirk-helm \
  -f <path to the secrets file defined in previous step> \
  --set kirk_run_migration=true
```

### post install steps

Here there are a couple of options depending on what needs to exist, and many 
of  these post install steps could be automated using jobs.

*Not sure if links to subsections will work.. look for section (Data Migrations)  everthing is under there*

[loading fixtures](./deploy_notes.md#loading-fixtures)
[create superuser](./deploy_notes.md#create-superuser)
[create api token](./deploy_notes.md#create-api-token)

Another option is to do a data migration from another project.  If you are doing 
a data migration from another namespace then you do not have to do the steps above
as all those objects are stored in the database.

[info on data migration](./deploy_notes.md#data-migrations-for-deployments)


### install a new KIRK image

```
helm install kirk-install kirk-helm \
  -f <path to the secrets file defined in previous step> \
  --set kirk_run_migration=true
```

Because of the database component reverting an install is not possible if the database has already been migrated.  In 
these situations you will need to create a new release with a database migration that performs the reversion of the
datamodel.  Then deploy that new version that includes the migration code to revert the previously applied changes.
