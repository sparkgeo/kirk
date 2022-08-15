# Deploy notes

### Overview

- APP_KIRK: Python Django app + postgres DB.

- APP_KIRK + DB backup container are deployed via helm charts.

- Deployment environment: a namespace set on BC Gov openshift silver cluster.

  - APP_KIRK is deployed on prod, test and dev namespace.

  - DB backup is deployed on tools namespace.

- Container images are now built and stored on tool namespace.
  - ~~Container images *used* to be built via GH actions and retrieved from GH packages.~~
  - ~~[List of kirk images](https://github.com/bcgov/kirk/packages/466269/versions)~~


### Deploy on a net new project namespace set

0. Log into openshift - grab the login command from the openshift console.

1. Choose correct project - get a list of all the projects you have access to `oc projects`.

2. Log into a specific project `oc project <project_namespace>`.

3. Prepare deployment configuration files, [see this section](#deployment-configuration-files).

4. Prepare container images in tools namespace, [see this section](#build-container-images).

5. Run the following helm chart deployment - kirk-install in dev, test or prod.
```
helm install kirk-install kirk-helm \
     -f <path_to_kirk_install_helm_chart_config_yaml> \
     --set kirk_run_migration=true
```

6. Post install steps, [see this section](#data-migrations).

7. Run the followiing helm chart deployment - kirk-backup in dev, test or prod.in dev, test or prod.
```
helm repo add bcgov http://bcgov.github.io/helm-charts

helm repo update

helm install kirk-backup bcgov/backup-storage \
     -f <path_to_kirk_backup_helm_chart_config>
```


### Redeploy

- Use `helm upgrade --install` instead.

```
helm upgrade --install kirk-install kirk-helm \
     -f <path_to_kirk_install_helm_chart_config_yaml> \
     --set kirk_run_migration=true

helm upgrade --install kirk-backup bcgov/backup-storage \
     -f <path_to_kirk_backup_helm_chart_config>
```

- If DB has already been migrated, reverting an install is not possible because of the DB component. In situation like this, you will need to:
  - create a new release with a database migration that performs the reversion of the
datamodel; and
  - then deploy that new version that includes the migration code to revert the previously applied changes.


### Details

#### Deployment configuration files

Create *kirk_install_helm_chart_config.yaml* by coping the code snippet below and populate with the parameters you want.

```
app_name: <app_name>
env: <dev_or_prod_env>

# Parameters used to create and connect to the postgres database that
# sits behind kirk
kirk_pgdb_params:
  # Annotations to add to the service account
  annotations: {}
  # The user that will be created in the database and for
  # subsequent database connections.
  kirk_database_user: <application_database_user>
  kirk_database_password: <application_database_user_password>
  kirk_database_name: <application_database_name>
  kirk_database_port: <application_database_port>

# Secret name that contains the database parameters described above
kirk_pgdb_secret_name: <name_of_the_secret_for_the_database_secrets>

# License plate for openshift namespaces
license_plate: <license_plate>

# License plate for where kong api lives
license_plate_kong: <kong_license_plate>

```

Create *kirk_backup_helm_chart_config.yaml* by coping the code snippet below and populate with the parameters you want.

```
image:
  repository: image-registry.openshift-image-registry.svc:5000/<license_plate>-tools/backup-postgres
  pullPolicy: Always
  tag: latest

persistence:
  backup:
    size: 5Gi
    storageClassName: netapp-file-backup
  verification:
    size: 1Gi
    storageClassName: netapp-file-standard

db:
  secretName: <db_secret_name>
  usernameKey: database-user
  passwordKey: database-password

env:
  DATABASE_SERVICE_NAME:
    value: <db_service_name>
  ENVIRONMENT_FRIENDLY_NAME:
    value: "Kirk DB Backups"
  ENVIRONMENT_NAME:
    value: "dev"

backupConfig: |
  postgres=<db_service_name>:5432/<db_name>
  0 8-17 * * 1-5 default ./backup.sh -s
  10 8-17 * * 1-5 default ./backup.sh -s -v all
  0 8 * * 6,0 default ./backup.sh -s
  10 8 * * 6,0 default ./backup.sh -s -v all

```

#### Build container images

To start building images in tools namespace and to allow images being pulled, run the following.

```
BUILD_VALUES=<path_to_kirk_install_helm_chart_config>

oc process --ignore-unknown-parameters=true \
     --param-file=$BUILD_VALUES \
     -f openshift/templates/sa_rbac.yaml | \
     oc apply -f -

curl https://raw.githubusercontent.com/BCDevOps/backup-container/master/openshift/templates/backup/backup-build.yaml | \
     oc process -f - | \
     oc apply -f -

cat kirk-helm/Chart.yaml $BUILD_VALUES > temp.yaml && \
     oc process --ignore-unknown-parameters=true --param-file=temp.yaml \-f openshift/templates/kirk_bc.yaml | oc apply -f - && \
     rm temp.yaml
```

#### Data Migrations

- Data model migrations
  - *Not required, now part of helm deployment.*
  - ~~python manage.py makemigrations api~~
  - ~~python manage.py migrate api~~

- Loading fixtures
  - *A one time thing for new deployment to openshift.*
  - Log into a kirk_app pod and run the following command there.
    - ```python manage.py loaddata Destination_Keywords.json```
    - ```python manage.py loaddata fme_data_types.json```
    - ```python manage.py loaddata job_data.json```

- Create superuser
  - *Also a one time thing for new deployment to openshift.*
  - ```python manage.py createsuperuser --email <YOUR_SU_EMAIL_ADDRESS> --username <YOUR_SU_USERNAME>```

- Create api token
  - *Only the first time kirk is set up.*
  - ```python manage.py drf_create_token spock```
  - Then put api token into PMP along with the superuser you created in the previous step.


### Developer / debugging notes

Local developement testing

- Run the server ```docker-compose up```

- Then hit 127.0.0.1:8000 to verify the app is working.

Helm deployments

- Install the chart ```helm install kirk-install kirk-helm -f ./helm-config-dev.yaml```

- Delete all objects defined in the chart ```helm uninstall kirk-install```

- Debug / test a chart ```helm install --dry-run --debug kirk-install kirk-helm -f ./helm-config-dev.yaml```

- List what has been deployed ```helm ls```

- Upgrade ```helm upgrade --install kirk-install kirk-helm -f $HELM_KIRK_VALUES \
  --set kirk_run_migration=true```

Openshift Deployments

- To get the pods ```oc get pods```
  - Kirk pod will have a prefix of *kirk-dc*

- Log into a kirk pod ```oc rsh <kirk_pod_name>```

- Verify that you can communicate from the kirk pod to the database pod ```curl -v telnet://<db_service_name>:5432```

- Verify that kirk pod can talk to the db
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

- Configure Port Forwarding on db pod ```oc port-forward <podname> <srcport>:<destport>```
  - This is to capture that communication exists between the pods, by capturing traffic to the db pod.


Postgres Database Debugging

- [Postgresql cheat sheet](https://www.postgresqltutorial.com/postgresql-cheat-sheet/)

- Dump database to backup file ```pg_dump -Fp -h $POSTGRESQL_SVC_SERVICE_HOST -p $POSTGRESQL_SVC_SERVICE_PORT -U POSTGRESQL_USER $POSTGRESQL_DATABASE > dumpfile.gz```

- Connect / Login to database ```psql -U $POSTGRESQL_USER```

- Drop database ```psql -ac "DROP DATABASE $POSTGRESQL_DATABASE"```

- Copy data to a pod ```oc rsync junk postgresql-dc-1-qs9sl:/var/lib/pgsql/data/userdata/tmp```

- Log into pod and run this to restore ```gunzip < db_dump.gz | psql -v ON_ERROR_STOP=1 -x  -d $POSTGRESQL_DATABASE```
