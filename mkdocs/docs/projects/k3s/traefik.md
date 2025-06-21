# Traefik

## Brief

Enabling traefik access to dashboard and metrics for traefik ingress controller in k3s kubernetes cluster

- by `rskntroot` on `2024-07-01`

## Assumptions

``` bash
$ k3s --version
k3s version v1.32.5+k3s1 (8e8f2a47)
go version go1.23.8
```

``` bash
$ kubectl version
Client Version: v1.32.5+k3s1
Kustomize Version: v5.5.0
Server Version: v1.32.5+k3s1
```

## Dashboards

K3S comes packaged with `Traefik Dashboard` enabled by default, but not exposed.

### Preparation

#### DNS

=== "DNS"

    Set DNS record `traefik.your.domain.com`

=== "Hosts File"

    Alternatively, you can just edit your `hosts` file.

    ``` title="/etc/hosts"
    10.0.0.1    traefik.your.domain.com
    ```

!!! warning "This example does not include authentication. Exposing these dashboards is a security risk. Recommend enabling mTLS."

#### Middlewares

On host with `kubectl` access.

``` yaml title="middlewares.yml"
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: redirect-https
  namespace: default
spec:
  redirectScheme:
    scheme: https
    permanent: true
    port: "443"
---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: redirect-dashboard
  namespace: default
spec:
  redirectRegex:
    regex: "^https?://([^/]+)/?$"
    replacement: "https://${1}/dashboard/"
    permanent: true
---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: ratelimit
  namespace: default
spec:
  rateLimit:
    average: 100
    burst: 50
---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: compress
  namespace: default
spec:
  compress: {}
```

``` bash
kubectl apply -f middlewares.yml
```

### Setup IngressRoute

create `ingress.yml` and update `"edge.rskio.com"` with your domain name

``` yaml title="ingress.yml"
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: traefik-dashboard
spec:
  entryPoints:
    - web
    - websecure
  routes:
    - match: Host(`edge.rskio.com`) # Update with your domain name
      kind: Rule
      services:
        - name: api@internal
          kind: TraefikService
      middlewares:
        - name: redirect-https
        - name: redirect-dashboard
        - name: ratelimit
        - name: compress
```

``` bash
kubectl apply -f ingress.yml
```

## Access Dashboards

You should now be able to access the Traefik Ingress Controller Dashboard and metrics remotely.

From web browser go to the domain you specified in the ingress.

=== "Traefik Dashboard"

    ```
    https://edge.your.domain.com
    ```

    will follow `redirect-https` and get you to

    ```
    https://edge.your.domain.com/dashboard/#/
    ```

### Disable Dashboards

=== "Bash"

    ``` bash
    kubectl delete -f ingress.yml
    ```

=== "Example"

    ``` bash
    $ kubectl delete -f traefik/ingress.yml
    ingressroute.traefik.io "traefik-ingress" deleted
    ```


## References

- [https://docs.k3s.io](https://docs.k3s.io)
- [https://doc.traefik.io/traefik/](https://doc.traefik.io/traefik/)
