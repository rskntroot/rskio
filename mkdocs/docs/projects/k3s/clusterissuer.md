# ClusterIssuer

Allows certificate requests from an ACME provider. This is used to enable HTTPS TLS for services you stand up.

## Setup

see [cert-manager kubectl install](https://cert-manager.io/docs/installation/kubectl/) for more info

=== "v1.18"

    ``` bash
    kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.18.0/cert-manager.yaml
    ```

create at least one of the `clusterissuers` types below

### External

uses LetsEncrypt and public DNS records to sign https for your sites

``` yaml title="letsencrypt/clusterissuer.yml"
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
  namespace: default
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: ${EMAIL}
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
      - selector: {}
        http01:
          ingress:
            class: traefik
```

### Internal

pointed at an internal ACME provider to generate certs for an intranet

``` yaml title="internal/clusterissuer.yml"
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: internal-issuer
spec:
  acme:
    email: ${EMAIL}
    server: ${ACME_URL}
    privateKeySecretRef:
      name: interal-issuer-account-key
    caBundle: ${CA_BUNDLE_BASE64} # ca bundle that was used to generate the tls cert for the acme site
    solvers:
      - selector: {}
        http01:
          ingress:
            class: traefik
```

## Certificate

### Example

create a `certificate.yml` file for a traefik `IngressRoute`

=== "Certificate"

    ``` yaml
    apiVersion: cert-manager.io/v1
    kind: Certificate
    metadata:
      name: io-rsk-docs-tls
    spec:
      secretName: io-rsk-docs-tls
      issuerRef:
        name: dev-step-issuer
        kind: ClusterIssuer
      commonName: docs.dev.rsk.io
      dnsNames:
        - docs.dev.rsk.io
      privateKey:
        algorithm: RSA
        encoding: PKCS1
        size: 2048
      usages:
        - server auth
        - client auth
      duration: 2160h # 90 days
      renewBefore: 360h # 15 days
      secretTemplate:
        annotations:
          kubeseal-secret: "true"
        labels:
          domain: docs-dev-rsk-io
    ```

=== "IngressRoute"

    ``` yaml
    apiVersion: traefik.io/v1alpha1
    kind: IngressRoute
    metadata:
      name: rskio-docs
    spec:
      entryPoints:
        - web
        - websecure
      routes:
        - match: Host(`docs.dev.rsk.io`)
          kind: Rule
          services:
            - name: rskio-docs
              port: 80
      tls:
        secretName: io-rsk-docs-tls
    ```

After applying this `Certifcate` a `Secret` is created containing the `.crt` and `.key` files.
 These are loaded by the traefik.io `IngressRoute` under `spec.tls.secretName`.
 This enables usage of the tls cert for https client reachability.
