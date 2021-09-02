### Install Argo

Borrowing heavily from https://github.com/BCDevOps/developer-experience/blob/cailey/artifactory/argo/apps/artifactory/pipeline/README.md

This assumes that the CRDs have already been created (they have been in KLAB and Silver). Argo Workflows should be installed on the namespace scale.

To install using ansible, cd to install folder and run the following:
```
export CLUSTER=<CLUSTER> LICENSE_PLATE=<LICENSE_PLATE> && ansible-playbook playbook.yaml
```


### Unnstall Argo

To uninstall run the following:
```
for ns_en in tools dev test; do oc delete all,sa,configmap,service,route,secret,role,rolebinding -l "app=kirk-$LICENSE_PLATE-argo-workflow" -n "$LICENSE_PLATE-$ns_env"; done
```


### Argo Workflows

For pipeline development, argo workflows can be manually deployed by port-forwarding to the remote argo server:
```
oc -n $(oc project --short) port-forward svc/argo-server 2746:2746
```

Then run this sample workflow (this requires installing argo locally, or you could use kubectl):
```
argo submit -n $(oc project --short) pipeline/workflow_sample.yaml
```
