# Step CA

An internal CA and ACME Provider.

## Brief

Step can do more, but lets configure the basics.

## Install

``` bash
sudo -i
```

``` bash
apt-get update && apt-get install -y --no-install-recommends curl vim gpg ca-certificates
curl -fsSL https://packages.smallstep.com/keys/apt/repo-signing-key.gpg -o /etc/apt/trusted.gpg.d/smallstep.asc && \
    echo 'deb [signed-by=/etc/apt/trusted.gpg.d/smallstep.asc] https://packages.smallstep.com/stable/debian debs main' \
    | tee /etc/apt/sources.list.d/smallstep.list
apt-get update && apt-get -y install step-cli step-ca
```

!!! note "For more install instructions see smallstep [installation guide](https://smallstep.com/docs/step-ca/installation/)."

## Config Setup

``` bash
echo 'some-password' > secret
```

=== Config

  ``` bash
  step ca init \
  --deployment-type standalone \
  --name ${CA_NAME} \
  --dns=${CA_DNS_NAMES} \
  --address 0.0.0.0:5001 \
  --provisioner ${CA_EMAIL} \
  --password-file ./secret
  ```

=== Example

  ``` bash
  step ca init \
  --deployment-type standalone \
  --name rskio \
  --dns=rskio.com,rskntr.com \
  --address 0.0.0.0:5001 \
  --provisioner dev@rskio.com \
  --password-file ./secret
  ```

``` bash
step ca provisioner add dev --type ACME
```

## Service

## Certificates

### Trust

``` bash
cat ~/.step/certs/root_ca.crt
cat ~/.step/certs/intermediate_ca.crt
```

save and install the files into the trusted certificates on your endpoint and enable trust for ssl signing

### ClusterIssuer

``` bash
cat .step/certs/root_ca.crt | base64 -w0
```

use output in the spec.

``` yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: dev-step-issuer
spec:
  acme:
    email: ${SOME_EMAIL}
    server: https://${CA_DOMAIN}/acme/dev/directory
    privateKeySecretRef:
      name: dev-step-issuer-account-key
    caBundle: ${CA_ROOT_PEM}
    solvers:
      - selector: {}
        http01:
          ingress:
            class: traefik
```
