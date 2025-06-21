# Longhorn

Provides distributed storage for the cluster.
 We will only be editing the nodes as many of the defaults are sufficient.

## Requirements

All cluster nodes need these packages installed:

``` bash
sudo apt install open-iscsi nfs-common -y
```

see (longhorn os-specific requirements)[https://longhorn.io/docs/1.9.0/deploy/install/#osdistro-specific-configuration] for more information.

## Setup

=== "v1.9.0"

    ``` bash
    kubectl apply -f https://raw.githubusercontent.com/longhorn/longhorn/v1.9.0/deploy/longhorn.yaml
    ```

see (longhorn installation)[https://longhorn.io/docs/1.9.0/deploy/install/install-with-kubectl/#installing-longhorn] for more information.

## Dashboard

### Service

create and apply `longhorn/service.yml`

``` bash
apiVersion: v1
kind: Service
metadata:
  labels:
    app: longhorn-ui
  name: longhorn-dashboard
  namespace: longhorn-system
spec:
  ports:
    - port: 8000
      protocol: TCP
      targetPort: 8000
      name: web
  selector:
    app: longhorn-ui
```

### Ingress

create and apply `longhorn/ingress.yml`

``` bash
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: longhorn-dashboard
  namespace: longhorn-system
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`storage.${DOMAIN_NAME}`)
      kind: Rule
      services:
        - name: longhorn-dashboard
          port: 8000
```

After creating a `ClusterIssuer` be sure to create a `Certificate` and apply it with `spec.tls.secretName`.
 With Traefik you can also use certResolver, though clusterissuer certs allow for more fine-grain control.

## StorageClass

create and apply `longhorn/storageclass.yml`

``` bash
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: longhorn-data
provisioner: driver.longhorn.io
allowVolumeExpansion: true
reclaimPolicy: Delete
volumeBindingMode: Immediate
parameters:
  numberOfReplicas: "3"
  staleReplicaTimeout: "300"
  fromBackup: ""
  fsType: "ext4"
```

## PVC

create and apply `some-app/pvc.yml`

``` yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: some-app-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 500M
  storageClassName: longhorn-data
```
