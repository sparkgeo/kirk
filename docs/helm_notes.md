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

* [list of kirk images](https://github.com/bcgov/kirk/packages/466269/versions)
* [action that triggers build]()

```
HELM_KIRK_VALUES=<path to the secret / override values>
KIRK_IMAGE_TAG=<container image tag>
NAMESPACE=<OC namespace to deploy to>
oc project $NAMESPACE
helm upgrade --install kirk-install kirk-helm -f $HELM_KIRK_VALUES \
  --set github_imagepull_parameters.imagetag=$KIRK_IMAGE_TAG \
  --set kirk_run_migration=true
```

# install database backup container

This is likely something that can be installed and forgotten about. 

```
HELM_BACKUP_VALUES=<path to the helm overrides>
helm repo add bcgov http://bcgov.github.io/helm-charts

helm repo update

helm upgrade --install kirk-backup bcgov/backup-storage -f \
 $HELM_BACKUP_VALUES
```

* [action that builds the backup container]()
* [list of backup container images](https://github.com/bcgov/kirk/packages/489004/versions)

to deploy a specific version of the backup container:

```
helm upgrade --install kirk-backup bcgov/backup-storage -f \
 $HELM_BACKUP_VALUES \
 --set image.tag=20201104-1728
```


