# Webhooks

Continuous integration on easy mode.
 Webhooks allow for a ton of functionality,
 but we are going to use it to kick off a kubernetes job.
 Effectivitely automating reloading content on a static website.

## Background

This docs website is a static site that is hosted inside an nginx container.
 The storage for these redundant pods is a longhorn rwx pvc that gets stood up.
 To initialize the storage a kubernetes job is run. This job does the following:

- git clones the `rskntroot/rskio` repo containing the artifacts required to render the site
- executes the `mkdocs` command to render the static site

So what if when we push to github, we setup a webhook that tells kubernetes to kick off that job?
 Well, we achieve some form of automation.
 So how do we do this?

## Setup

### RBAC

=== "ServiceAccount"

    ``` yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: webhook-job-trigger
    ```

=== "Dev Roles"

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      name: job-creator
      namespace: dev
    rules:
      - apiGroups: ["batch"]
        resources: ["jobs"]
        verbs: ["create"]
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: RoleBinding
    metadata:
      name: job-creator-binding
      namespace: dev
    subjects:
      - kind: ServiceAccount
        name: webhook-job-trigger
        namespace: default
    roleRef:
      kind: Role
      name: job-creator
      apiGroup: rbac.authorization.k8s.io
    ```

=== "Prod Roles"

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      name: job-creator
      namespace: prod
    rules:
      - apiGroups: ["batch"]
        resources: ["jobs"]
        verbs: ["create"]
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: RoleBinding
    metadata:
      name: job-creator-binding
      namespace: prod
    subjects:
      - kind: ServiceAccount
        name: webhook-job-trigger
        namespace: default
    roleRef:
      kind: Role
      name: job-creator
      apiGroup: rbac.authorization.k8s.io
    ```

### ConfigMap

We will create a config map from a directory including the following files.

#### ConvertJob

We are going to be using curl to call the kubernetes API directly,
 so we need to convert our job from yaml to json.

Convert the job to JSON and save to `etc/mkdocs-dev.json`

=== "Job"

    ``` yaml
    apiVersion: batch/v1
    kind: Job
    metadata:
      generateName: mkdocs-builder-
      namespace: dev
    spec:
      ttlSecondsAfterFinished: 600
      template:
        spec:
          containers:
            - name: mkdocs
              image: squidfunk/mkdocs-material
              command: ["/bin/sh", "-c"]
              args:
                - |
                  git clone --single-branch -b dev https://github.com/rskntroot/rskio.git --depth 1 /docs
                  cd /docs/mkdocs
                  mkdocs build --site-dir /output
              volumeMounts:
                - name: mkdocs-storage
                  mountPath: /output
          restartPolicy: Never
          volumes:
            - name: mkdocs-storage
              persistentVolumeClaim:
                claimName: mkdocs-pvc
    ```

=== "Convert"

    ``` bash
    mkdir etc
    cat job.yml | yq -e -j | jq > etc/mkdocs-dev.json
    ```

The following docs we will assume that you also created `etc/mkdocs-main.json`.

#### Hooks

create `etc/hooks.yaml`

=== "etc/hooks.yaml"

    ``` yaml
    - id: rskio-mkdocs
      execute-command: /etc/webhook/reload.sh
      command-working-directory: /etc/webhook
      response-message: payload received
      response-headers:
        - name: Access-Control-Allow-Origin
          value: "*"
      pass-arguments-to-command:
        - source: payload
          name: ref
        - source: payload
          name: repository.full_name
      trigger-rule:
        and:
          - match:
              type: value
              value: push
              parameter:
                source: header
                name: X-GitHub-Event
          - match:
              type: value
              value: rskntroot/rskio
              parameter:
                source: payload
                name: repository.full_name
    ```

=== "Secret"

    after testing come back to implement secrets

    ``` yaml
    trigger-rule:
      and:
      - match:
          type: payload-hmac-sha1
          secret: mysecret
          parameter:
            source: header
            name: X-Hub-Signature
    ```

    apply the `configmap` and rollout restart the webhook deployment

#### Command

``` bash title="etc/reload.sh"
#!/bin/sh

REF=$1
REPO=$2

dispatch() {
    NS=$1
    JOB_JSON=$2
    SA_PATH="/var/run/secrets/kubernetes.io/serviceaccount"
    curl https://kubernetes.default.svc/apis/batch/v1/namespaces/${NS}/jobs \
        -X POST \
        -H "Authorization: Bearer $(cat ${SA_PATH}/token)" \
        -H "Content-Type: application/json" \
        --cacert "${SA_PATH}/ca.crt" \
        -d "@${JOB_JSON}"
}

docs(){
    case ${REF} in
        refs/heads/dev)
            dispatch dev "/etc/webhook/mkdocs-dev.json"
            ;;
        refs/heads/main)
            dispatch prod "/etc/webhook/mkdocs-main.json"
            ;;
        *)
            echo "skipping push to unsupported ref ${REF}"
            exit 0
            ;;
    esac
}

case ${REPO} in
    rskntroot/rskio)
        docs
        ;;
    *)
        echo "skipping push to unsupported repo ${REPO}"
        ;;
esac
```

#### Create

once all resources in `etc` are created run the following command:

``` bash
kubectl create configmap webhook-etc --from-file=etc
```

if you need to update anything run the following:

``` bash
kubectl delete configmap webhook-etc
kubectl create configmap webhook-etc --from-file=etc
```

### Resources

The following resources will complete the work

=== "Deployment"

    ``` yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: webhook-docs
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: webhook-docs
      template:
        metadata:
          labels:
            app: webhook-docs
        spec:
          serviceAccountName: webhook-job-trigger
          containers:
            - name: webhook-docs
              image: ghcr.io/linuxserver-labs/webhook:latest
              command: ["/app/webhook"]
              args:
                - -hooks=/etc/webhook/hooks.yaml
                - -hotreload
                - -verbose
              volumeMounts:
                - name: webhook-etc
                  mountPath: /etc/webhook
          volumes:
            - name: webhook-etc
              configMap:
                name: webhook-etc
                defaultMode: 493 # 0755
    ```

=== "Service"

    ``` yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: webhook
    spec:
      selector:
        app: webhook-docs
      ports:
        - protocol: TCP
          port: 9000
          targetPort: 9000
      type: ClusterIP
    ```

=== "Certificate"

    ``` yaml
    apiVersion: cert-manager.io/v1
    kind: Certificate
    metadata:
      name: io-rsk-dev-hooks-tls
    spec:
      secretName: io-rsk-dev-hooks-tls
      issuerRef:
        name: dev-step-issuer
        kind: ClusterIssuer
      commonName: hooks.dev.rsk.io
      dnsNames:
        - hooks.dev.rsk.io
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
          domain: hooks-dev-rsk-io
    ```

=== "Ingress"

    ``` yaml
    apiVersion: traefik.io/v1alpha1
    kind: IngressRoute
    metadata:
      name: webhook
    spec:
      entryPoints:
        - websecure
      routes:
        - match: Host(`hooks.dev.rsk.io`)
          kind: Rule
          services:
            - name: webhook
              port: 9000
          middlewares:
            - name: ratelimit
      tls:
        secretName: io-rsk-hooks-tls
    ```

## Testing

``` bash
curl -X POST https://hooks.dev.rsk.io/hooks/rskio-mkdocs \
  -H 'X-Github-Event: push' \
  -H 'Content-type: application-json' \
  -d '{"ref": "refs/heads/dev","repository": {"full_name":"rskntroot/rskio"}}'
```

!!! note "Github needs access to a public domain for this to work."
