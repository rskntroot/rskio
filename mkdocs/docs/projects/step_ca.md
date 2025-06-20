# Step CA

An internal CA and ACME Provider.

## Brief

Guide to setup a internal Certificate Authority and ACME Provider
 for issuing trusted TLS certs for internal sites.
 This is useful for both traefik certificateResolver or kubernetes ClusterIssuer.
 Step can do more, but lets configure the basics.

- by `rskntroot` on `2025-06-18`

## Assumptions

- An Internal DNS server is configured and accessible.
- Debian is your choice for the ACME/CA server install.

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

=== "Config"

    ``` bash
    step ca init \
    --deployment-type standalone \
    --name ${CA_NAME} \
    --dns=${CA_DNS_NAMES} \
    --address "0.0.0.0:5001" \
    --provisioner ${CA_EMAIL} \
    --password-file ./secret
    ```

=== "Example"

    ``` bash
    step ca init \
    --deployment-type standalone \
    --name rskio \
    --dns=rskio.com,rskntr.com \
    --address "0.0.0.0:5001" \
    --provisioner dev@rskio.com \
    --password-file ./secret
    ```

``` bash
step ca provisioner add dev --type ACME
mv secret /root/.step/config/.
```

## Service

``` bash
vi /root/.step/step.service
```

paste the following and save with `[ESC] [:] [x] [ENTER]`

``` toml
[Unit]
Description=Step CA & ACME Provider
After=network-online.target
Requires=network-online.target

[Service]
Type=simple
RemainAfterExit=yes
ExecStart=/usr/bin/step-ca /root/.step/config/ca.json --password-file /root/.step/config/secret
User=root

Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

``` bash
ln -s /root/.step/step.service /etc/systemd/system/.
systemctl daemon-reload
systemctl enable --now step.service
systemctl status step.service
```

``` bash
ss -pnlt | grep 5001
curl -k https://localhost:5001/acme/dev/directory
```

you should see your service logs showing it is listening on port `:5001` and see the contents of the webpage from `curl`

## Certificates

### Trust

``` bash
cat ~/.step/certs/root_ca.crt
cat ~/.step/certs/intermediate_ca.crt
```

save and install the files into the trusted certificates on your endpoint and enable trust for ssl signing.

you should now be able to browse to your sites without warning

### ClusterIssuer

``` bash
cat .step/certs/root_ca.crt | base64 -w0
```

use above output under `spec.acme.caBundle`

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

## FAQs

> Why didnt you containerize this?

Because I have multiple kubernetes clusters.
 Running this on a separate machine means that I don't have to install a `rootCA.pem` for each cluster instance.
 You might say "yeah, but you can specify the rootCA as an input to step CA"--but who wants to key files and
 setup CA for each kuberenetes install?
 So yeah, maybe I'll do it in the future.
