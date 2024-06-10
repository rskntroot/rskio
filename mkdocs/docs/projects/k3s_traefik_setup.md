# K3S Traefik Setup

## Brief

Enabling traefik access to dashboard and metrics for traefik ingress controller in k3s kubernetes cluster

- by `rskntroot` on `2024-07-01`

## Assumptions

``` bash
$ k3s --version
k3s version v1.29.5+k3s1 (4e53a323)
go version go1.21.9
```

``` bash
$ kubectl version
Client Version: v1.29.5+k3s1
Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
Server Version: v1.29.5+k3s1
```

## Traefik Dashboards

K3S comes packaged with `Traefik Dashboard` and `Prometheus Metrics` which are disabled by default. 

### Preparation

=== "DNS"

    Set DNS record `traefik.your.domain.com` in a non-public DNS

=== "Hosts File"

    Alternatively, you can just edit your workstations `hosts` file.

    ``` title="/etc/hosts"

    10.0.0.1    traefik.your.domain.com

    ```

!!! warning "This example does not include authentication. Exposing these dashboards is a security risk." 

### Update Manifest

On host with `kubectl` access.

Add the following to `spec.valuesContent` in:

``` bash
vim /var/lib/rancher/k3s/server/manifests/traefik.yaml 
```

=== "Yaml"

    ``` yaml
        dashboard:
          enabled: true
        metrics:
          prometheus: true
    ```

=== "Example"

    ``` yaml
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

=== "Bash"

    ``` bash
    kubectl -n kube-system scale deployment traefik --replicas=0
    # wait a few seconds
    kubectl -n kube-system get deployment traefik
    kubectl -n kube-system scale deployment traefik --replicas=1
    ```

=== "Example"

    ``` bash
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

=== "Traefik Dashboard"

    ``` yaml title="traefik-dashboard.yml"
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

    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: traefik-ingress
      namespace: kube-system
      annotations:
        spec.ingressClassName: traefik
    spec:
      rules:
        - host: traefik.${DOMAIN}
          http:
            paths:
              - path: /
                pathType: Prefix
                backend:
                  service:
                    name: traefik-dashboard
                    port:
                      number: 9000
    ```

=== "Promethus Only"

    ``` yaml title="traefik-dashboard.yml"
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
        - host: traefik.${DOMAIN}
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

=== "Both"

    ``` yaml title="traefik-dashboard.yml"
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
        - host: traefik.${DOMAIN}
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

### Create Service & Ingress Resources

First, set the environment variable for to your domain.

``` bash
export DOMAIN=your.domain.com
```

=== "Bash"

    ``` bash
    envsubst < traefik-dashboard.yml | kubectl apply -f -
    ```

=== "Example"

    ``` bash
    $ envsubst < traefik-dashboards.yml | kubectl apply -f -
    service/traefik-dashboard created
    service/traefik-metrics created
    ingress.networking.k8s.io/traefik-ingress created
    $ kubectls get svc | grep traefik-
    traefik-dashboard   ClusterIP      10.43.157.54    <none>    9000/TCP    25s
    traefik-metrics     ClusterIP      10.43.189.128   <none>    9100/TCP    25s
    ```

!!! note annotate "Why are passing the yaml file into `envsubst`? (1)"

1. `envsubst` - [gnu](https://www.gnu.org/software/gettext/manual/html_node/envsubst-Invocation.html) - enables code-reuse by providing environment variable substituion as demonstrated above.

### Access Dashboards

That's it. You should now be able to access the Traefik Ingress Controller Dashboard and metrics remotely.  

Don't forget to include the appropriate uri paths:

=== "Traefik Dashboard"

    ```
    https://traefik.your.domain.com/dashboard/
    ```

    !!! tip "When navigating to the traefik dashboard the `/` at the end is necessary. `/dashboard` will not work. "

=== "Promethus Metrics"

      ```
      https://traefik.your.domain.com/metrics
      ```

### Disable Dashboards

=== "Bash"

    ``` bash
    envsubst < traefik-dashboard.yml | kubectl delete -f -
    ```

=== "Example"

    ``` bash
    $ envsubst < traefik-dashboards.yml | kubectl delete -f -
    service "traefik-dashboard" deleted
    service "traefik-metrics" deleted
    ingress.networking.k8s.io "traefik-ingress" deleted
    ```

## Shortcuts

### alias kubectls

!!! tip "When using an `alias` to substitute `kubectl` command completion will not work."

=== "Bash"

    ``` bash
    echo 'alias kubectls="kubectl -n kube-system"' >> ~/.bashrc
    source ~/.bashrc
    ```

=== "Example"

    ``` bash
    $ echo 'alias kubectls="kubectl -n kube-system"' >> ~/.bashrc
    $ source ~/.bashrc
    $ kubectls get deployments
    NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
    coredns                  1/1     1            1           3d2h
    local-path-provisioner   1/1     1            1           3d2h
    metrics-server           1/1     1            1           3d2h
    traefik                  1/1     1            1           3d2h
    ```

#### Alternatives 

- `skubectl` means you can hit `[up-arrow]` `[ctrl]+[a]` `[s]` `[enter]` when you inevitably forget to include `-n kube-system`
- `kubectls` just adds `[alt]+[right-arrow]` into the above before `[s]`
- `kubesctl` makes sense because all of these are really kube-system-ctl, but that adds 4x `[right-arrow]`, ewww.


## References

- [https://docs.k3s.io](https://docs.k3s.io)
- [https://k3s.rocks/traefik-dashboard/](https://k3s.rocks/traefik-dashboard/)
- [https://doc.traefik.io/traefik/v2.10/](https://doc.traefik.io/traefik/v2.10/)
