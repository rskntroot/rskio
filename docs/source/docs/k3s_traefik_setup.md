# K3S Traefik Setup

## Brief

Enabling internal access to dashboard and metrics for traefik ingress controller in k3s kubernetes cluster

- by `rskntroot` on `2024-07-01`

## Assumptions

```
$ k3s --version
k3s version v1.29.5+k3s1 (4e53a323)
go version go1.21.9
```

```
$ kubectl version
Client Version: v1.29.5+k3s1
Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
Server Version: v1.29.5+k3s1
```

## Traefik Dashboards

*Note: `Traefik Dashboards` refers to both traefik dashboard and prometheus*

### Preparation

Enable `internal`+`.your.domain.com` in non-public DNS
- (alt) edit the `hosts` file on your admin to point the desired k3s host IP

On host with `kubectl` access:
```
export DOMAIN=your.domain.com
```

*Note: This example does not currently include authentication and exposing these dashboards is a security risk.* 

### Update Manifest

Add the following to `spec.valuesContent` section of `/var/lib/rancher/k3s/server/manifests/traefik.yaml`
```
    dashboard:
      enabled: true
    metrics:
      prometheus: true
```

Example:
```
spec:
  chart: https://%{KUBERNETES_API}%/static/charts/traefik-25.0.3+up25.0.0.tgz
  set:
    global.systemDefaultRegistry: ""
  valuesContent: |-
    deployment:
      podAnnotations:
        prometheus.io/port: "8082"
        prometheus.io/scrape: "true"
    dashboard:
      enabled: true
    metrics:
      prometheus: true
```

### Restart Ingress Controller

```
kubectl -n kube-system scale deployment traefik --replicas=0
kubectl -n kube-system get deployment traefik
```
```
kubectl -n kube-system scale deployment traefik --replicas=1
```

Example: (`kubectls`?! see `#shortcuts`)
```
$ kubectls scale deployment traefik --replicas=0
deployment.apps/traefik scaled
$ kubectls get deployment traefik
NAME      READY   UP-TO-DATE   AVAILABLE   AGE
traefik   0/0     0            0           3d1h
$ kubectls scale deployment traefik --replicas=1
deployment.apps/traefik scaled
```

### Create Resource Definition YAML

Save the following to `traefik-dashboard.yml` in your workspace.
```
apiVersion: v1
kind: Service
metadata:
  name: traefik-dashboard
  namespace: kube-system
  labels:
    app.kubernetes.io/instance: traefik
    app.kubernetes.io/name: traefik-dashboard
spec:
  type: ClusterIP
  ports:
  - name: traefik
    port: 9000
    targetPort: 9000
    protocol: TCP
  selector:
    app.kubernetes.io/instance: traefik-kube-system
    app.kubernetes.io/name: traefik

---

apiVersion: v1
kind: Service
metadata:
  name: traefik-metrics
  namespace: kube-system
  labels:
    app.kubernetes.io/instance: traefik
    app.kubernetes.io/name: traefik-metrics
spec:
  type: ClusterIP
  ports:
  - name: traefik
    port: 9100
    targetPort: 9100
    protocol: TCP
  selector:
    app.kubernetes.io/instance: traefik-kube-system
    app.kubernetes.io/name: traefik

---

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: traefik-ingress
  namespace: kube-system
  annotations:
    spec.ingressClassName: traefik
spec:
  rules:
    - host: internal.${DOMAIN}
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: traefik-dashboard
                port:
                  number: 9000
          - path: /metrics
            pathType: Prefix
            backend:
              service:
                name: traefik-metrics
                port:
                  number: 9100
```

If you don't want `traefik-metrics` simply do not include the service definition and remove the `- path: metrics` section from the ingress definition.

### Create Service & Ingress Resources

[envsubst](https://www.gnu.org/software/gettext/manual/html_node/envsubst-Invocation.html) - `envsusbst` enables code-reuse by providing environment variable substituion as demonstrated below.

```
envsubst < traefik-dashboard.yml | kubectl apply -f -
```

Example:
```
$ envsubst < traefik-dashboards.yml | kubectl apply -f -
service/traefik-dashboard created
service/traefik-metrics created
ingress.networking.k8s.io/traefik-ingress created
$ kubectls get svc | grep traefik-
traefik-dashboard   ClusterIP      10.43.157.54    <none>    9000/TCP    25s
traefik-metrics     ClusterIP      10.43.189.128   <none>    9100/TCP    25s
```

### Access Dashboards

That's it. You should now be able to access the Traefik Ingress Controller Dashboard and metrics remotely.  

Don't forget to include the appropriate uri paths:
- `internal.your.domain.com/dashboard/` for `Traefik Dashboard` *(Note: just `/dashboard` will not work.)*
- `internal.your.domain.com/metrics` for `Traefik Metrics`

### Disable Dashboards

```
envsubst < traefik-dashboard.yml | kubectl delete -f -
```

Example:
```
envsubst < traefik-dashboards.yml | kubectl delete -f -
service "traefik-dashboard" deleted
service "traefik-metrics" deleted
ingress.networking.k8s.io "traefik-ingress" deleted
```

## Shortcuts

### alias kubectls

*Note: kubectl-completion will not work for `kubectls`*

```
echo 'alias kubectls="kubectl -n kube-system"' >> ~/.bashrc
source ~/.bashrc
```

Example:
```
$ echo 'alias kubectls="kubectl -n kube-system"' >> ~/.bashrc
$ source ~/.bashrc
$ kubectls get deployments
NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
coredns                  1/1     1            1           3d2h
local-path-provisioner   1/1     1            1           3d2h
metrics-server           1/1     1            1           3d2h
traefik                  1/1     1            1           3d2h
```

(alt) use `skubectl` or `kubesctl` as the alias instead. comparisons:
- `skubectl` means you can hit `[up-arrow]` `[ctrl]+[a]` `[s]` `[enter]` when you inevitably forget to include `-n kube-system`
- `kubectls` just adds `[alt]+[right-arrow]` to the above
- `kubesctl` makes sense because all of these are really kube-system-ctl, but that adds 4x `[right-arrow]`, ewww.


## References

- [https://docs.k3s.io](https://docs.k3s.io)
- [https://k3s.rocks/traefik-dashboard/](https://k3s.rocks/traefik-dashboard/)
- [https://doc.traefik.io/traefik/v2.10/](https://doc.traefik.io/traefik/v2.10/)
