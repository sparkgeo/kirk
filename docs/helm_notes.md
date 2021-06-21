# install the chart
helm install kirk-install kirk-helm -f ./helm-config-dev.yaml

# delete all objects defined in the chart
helm uninstall kirk-install

# debug / test a chart
helm install --dry-run --debug kirk-install kirk-helm -f ./helm-config-dev.yaml

# list what has been deployed
helm ls

# install new version of kirk

This is the command that would be run for a new KIRK deployment.

*Note: Consider the following github packages as archived as builds are now moved to openshift*

* [list of kirk images](https://github.com/bcgov/kirk/packages/466269/versions)
* [action that triggers build]()

```
HELM_KIRK_VALUES=<path to the secret / override values>
NAMESPACE=<OC namespace to deploy to>
oc project $NAMESPACE
helm upgrade --install kirk-install kirk-helm -f $HELM_KIRK_VALUES \
  --set kirk_run_migration=true
```

# install database backup container

The following HELM_BACKUP_VALUES need to be defined, the easiest way to define them is 
create a parameter file by coping the code snippet below and populate with 
the parameters you want.

```
image:
  repository: image-registry.openshift-image-registry.svc:5000/<license plate>-tools/backup-postgres
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
  secretName: <name of the secret for the database secrets>
  usernameKey: database-user
  passwordKey: database-password

env:
  DATABASE_SERVICE_NAME:
    value: <application database service name>
  ENVIRONMENT_FRIENDLY_NAME:
    value: "Kirk DB Backups"
  ENVIRONMENT_NAME:
    value: "dev"
  WEBHOOK_URL:
      value: "<webhook_id_token>"

backupConfig: |
  postgres=<application database service name>:5432/<application database name>
  0 1 * * * default ./backup.sh -s
  # 0 4 * * * default ./backup.sh -s -v all
      
```

This is likely something that can be installed and forgotten about. 

```
HELM_BACKUP_VALUES=<path to the helm overrides>
helm repo add bcgov http://bcgov.github.io/helm-charts

helm repo update

helm upgrade --install kirk-backup bcgov/backup-storage -f \
 $HELM_BACKUP_VALUES
```

*Note: Consider the following github packages as archived as builds are now moved to openshift*

* [action that builds the backup container]()
* [list of backup container images](https://github.com/bcgov/kirk/packages/489004/versions)
