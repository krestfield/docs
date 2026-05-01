---
layout: default
title: Running on Kubernetes Locally
parent: Certdog
nav_order: 1101
---

# Running Certdog on Kubernetes Locally

> From version: 1.17.0

The following guide provides steps to set up a local Minikube cluster for testing,
including a managed MongoDB instance, a kgateway instance, cert-manager, and a
deployment of Certdog.

## Prerequisites

The following tools will be required for this guide:

* `minikube`
* `helm`
* `kubectl` (or use `minikube kubectl`)

## 1. Create a Minikube cluster

You will first need to [create a cluster in Minikube](https://minikube.sigs.k8s.io/docs/start/)
with enough resources to run all the components.
The cluster can be run with minimal resources by using the Helm options and `values.yaml`
provided below.

Make sure to select the correct driver for your system, or exclude it to let Minikube
auto-select the driver for you.

```bash
minikube start [--driver=<driver>] --cpus='2' --memory='4096m' [-p cluster-name]
```

## 2. Install and deploy the MongoDB Controllers for Kubernetes Operator

To deploy the database, you will need to install the
[MongoDB Controllers for Kubernetes Operator](https://www.mongodb.com/docs/kubernetes/current/).

```bash
helm repo add mongodb https://mongodb.github.io/helm-charts
helm repo update
helm install mongodb-kubernetes-operator mongodb/mongodb-kubernetes \
    --set operator.resources.requests.cpu=100m \
    --set operator.resources.limits.cpu=200m \
    --set operator.resources.requests.memory=200M
```

## 3. Install and deploy the kgateway operator (optional)

To deploy the Gateway resources, you will need to install the
[kgateway operator](https://kgateway.dev/docs/envoy/latest/install/helm/).
You may skip this if you do not want to use a gateway.

```bash
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.4.1/standard-install.yaml
helm install kgateway-crds oci://cr.kgateway.dev/kgateway-dev/charts/kgateway-crds \
    --namespace kgateway-system --create-namespace \
    --version v2.1.2
helm install kgateway oci://cr.kgateway.dev/kgateway-dev/charts/kgateway \
     --namespace kgateway-system \
     --version v2.1.2 \
     --set resources.requests.cpu=100m \
     --set resources.limits.cpu=200m \
     --set resources.requests.memory=200M
```

## 4. Install and deploy cert-manager (optional)

To test Certdog's ACME server, you can optionally install cert-manager.
You can enable Gateway API support too to issue certificates for Gateway resources.

```bash
install cert-manager oci://quay.io/jetstack/charts/cert-manager \
    --namespace cert-manager --create-namespace \
    --set config.apiVersion="controller.config.cert-manager.io/v1alpha1" \
    --set config.kind="ControllerConfiguration" \
    --set config.enableGatewayAPI=true \
    --set crds.enabled=true \
    --set resources.requests.cpu=50m \
    --set resources.requests.memory=100M \
    --set cainjector.resources.requests.cpu=50m \
    --set cainjector.resources.requests.memory=100M \
    --set webhook.resources.requests.cpu=50m \
    --set webhook.resources.requests.memory=100M \
    --set startupapicheck.resources.requests.cpu=50m \
    --set startupapicheck.resources.requests.memory=100M
```

## 5. Deploy a bootstrap issuer for the gateway (optional)

The gateway requires a certificate for its HTTPS listener.
We can create a CA issuer bootstrapped by a self-signed issuer for this purpose.
Alternatively you could just use the self-signed issuer directly.

```bash
kubectl apply -f bootstrap.yaml
```

```yaml
# bootstrap.yaml
---
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: certdog-bootstrap-selfsigned
spec:
  selfSigned: {}
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: certdog-bootstrap-ca
spec:
  isCA: true
  commonName: certdog-bootstrap-ca
  secretName: certdog-bootstrap-secret
  privateKey:
    algorithm: RSA
    size: 2048
  issuerRef:
    name: certdog-bootstrap-selfsigned
    kind: Issuer
    group: cert-manager.io
---
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: certdog-bootstrap-issuer
spec:
  ca:
    secretName: certdog-bootstrap-secret   
```

## 6. Deploy a kgateway gateway instance (optional)

To expose the Certdog components under a single hostname, we will use
a gateway (in this case managed by kgateway), combined with HTTP routes generated
by the Helm chart.
The following manifest creates a gateway with HTTP and HTTPS listeners on the standard
ports, and links to the previously created issuer to request certificates for the HTTPS listener.

Note the hostname used to access the gateway must match the hostname defined in the spec.
This usually means adding an entry into the host's host file (or using a tool to manually
specify the hostname, such as `curl`).

This restriction also applies to traffic originating from the cluster, if it goes through
the gateway.
Usually services will communicate directly, so this is not an issue.
However, if you want to try issuing certificates with the in-cluster Certdog ACME server,
it will need a HTTPS connection, which can be provided by this gateway.
In this case, you either need to add an entry into the cluster's host file, or use
the Kubernetes-assigned DNS name of the service used to expose this gateway, which for
this installation is `certdog-bootstrap-gateway.default.svc.cluster.local`.

```bash
kubectl apply -f gateway.yaml
```

```yaml
# gateway.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: certdog-bootstrap-gateway
  labels:
    app: certdog-bootstrap-gateway
  annotations:
    cert-manager.io/issuer: certdog-bootstrap-issuer
spec:
  gatewayClassName: kgateway
  listeners:
  - name: http
    protocol: HTTP
    port: 80
    hostname: your-hostname.example
    allowedRoutes:
      namespaces:
        from: All
  - name: https
    protocol: HTTPS
    port: 443
    hostname: your-hostname.example
    tls:
      mode: Terminate
      certificateRefs:
      - name: certdog-bootstrap-tls
    allowedRoutes:
      namespaces:
        from: All
```

## 7. Deploy Certdog to the cluster

To deploy Certdog itself, simply install the Helm chart, passing any required values,
such as connecting it to the gateway, through the `values.yaml` file.

Contact support for more information on where to access the chart and required images.

```bash
helm install -f values.yaml <release-name> <path-or-url-to-chart>
```

```yaml
# values.yaml
all:
  gateway:
    gateways:
      certdog-bootstrap-gateway: {}

  strategy:
    type: Recreate

  probes:
    startup:
      successThreshold: 1
      failureThreshold: 30
      periodSeconds: 10

  resources:
    requests:
      cpu: 200m
      memory: 1G

database:
  resources:
    requests:
      cpu: 100m
      memory: 100M
  
  managed:
    replicas: 1
    additionalConfig:
      podSpec:
        persistence:
          multiple:
            data:
              storage: 2G
              storageClass: standard
            logs:
              storage: 2G
              storageClass: standard
      statefulSet:
        spec:
          template:
            spec:
              initContainers:
                - name: mongod-posthook
                  resources:
                    requests:
                      cpu: 100m
                      memory: 200M
                - name: mongodb-agent-readinessprobe
                  resources:
                    requests:
                      cpu: 100m
                      memory: 200M
              containers:
                - name: mongod
                  resources:
                    requests:
                      cpu: 100m
                      memory: 200M
                - name: mongodb-agent
                  resources:
                    requests:
                      cpu: 100m
                      memory: 200M
```

## 8. Access Certdog

Currently, the gateway is not accessible from outside the cluster.
To expose the cluster to the host, you can either port forward a specific port
(such as 443 for HTTPS), or create a tunnel to assign IPs to the gateway's service.

```bash
# port forward
kubectl port-forward svc/certdog-bootstrap-gateway 8443:443
# assign IPs
minikube tunnel
```

After port forwarding, you should be able to access Certdog via,
https://your-hostname.example:8443/ui/#/login, having previously set `your-hostname.example` to
resolve to the loopback address.

If instead you created a tunnel, you should be able to access Certdog via
https://your-hostname.example/ui/#/login (no need to change the port this time), having previously
set `your-hostname.example` to resolve to the external IP assigned to the service.
You can view this IP address using `kubectl get svc certdog-bootstrap-gateway` and looking for
the "External Address" column.

## Next Steps

* [Customising Certdog on Kubernetes with Helm](customising_with_helm.html)
* [Integrating Certdog on Kubernetes with cert-manager](integration_with_cert_manager.html)
