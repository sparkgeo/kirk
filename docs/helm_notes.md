# install the chart
helm install kirk-install kirk-helm -f ./helm-config-dev.yaml

# delete all objects defined in the chart
helm uninstall kirk-install

# debug / test a chart
helm install --dry-run --debug kirk-install kirk-helm -f ./helm-config-dev.yaml

# list what has been deployed
helm ls

# install new version of kirk
helm upgrade kirk-install kirk-helm -f ./helm-config-dev.yaml \
  --set github_imagepull_parameters.imagetag=20201029-2204 \
  --set kirk_run_migration=true
   
