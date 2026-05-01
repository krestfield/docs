---
layout: default
title: Customising with Helm
parent: Certdog
nav_order: 1110
---

# Customising Certdog on Kubernetes with Helm

> From version: 1.17.0

This guide covers various options available in the Certdog Helm chart for customising a
deployment of Certdog within Kubernetes.

For more detail or for less common options not mentioned in this guide,
view the `values.yaml` file within the Helm chart itself, or the `values.schema.json`
file alongside it.

## Inherited Configuration

Most component-specific configuration can also be set under `all`.
These options will be used as defaults if no override is present for that component.
E.g.

```yaml
# create a Horizontal Pod Autoscaler for all components by default
all:
  replicas:
    minReplicas: 1
    maxReplicas: 5
    targetCPU: 80

# override the default and only maintain one replica of the ACME server
acme:
  replicas: 1
```

Note that this uses Helm's `merge` function, and so uses the same semantics, meaning
arrays will be overridden, rather than appended to or strategically merged.
Maps will be merged, meaning for example sidecars will be combined, and only overwritten
if they share the same key (name).

## Configuring Components

Most aspects of each component's deployment and service can be customised with values under
the relevant component or `all`.
This includes:

* Replicas (fixed or dynamic via HPA)
* Deployment strategy
* Node selectors, affinities, and tolerations
* Additional labels and annotations
* Additional volumes
* Sidecar containers
* Container resources
* Service type (ClusterIP, NodePort, or LoadBalancer)

Additionally, all Java components (ACME, API, OCSP, SCEP) have common settings which
can be customised with values under `[component].config` or `all.config`.
This includes:

* Logging level
* Log4j configuration
* Spring configuration via `application.properties`
* Toggling the prometheus endpoint

These components also use an init container where necessary to wait for the database to
start before launching themselves.
This container can be customised by editing the options under `mongoReadiness`, which expose
the same container configuration options as those for the main component containers.

Each component may also have specific settings, under the relevant component or `all`.
These settings can be found in the component-specific section of the chart's `values.yaml`.

You may also configure components to automatically rollout new pods when configuration files
are changed (via component-specific settings or otherwise) by setting `[component].config.rolloutOnChange`
or equivalently `all.config.rolloutOnChange`.

## Provider Specific Configuration

Provider specific configuration is set under `[component].provider` or `all.provider`.
The current provider can be set by `[component].provider.provider` or `all.provider.provider`.
Options for each provider are then set under `[component].provider.[provider]` or `all.provider.[provider]`.

Currently only GKE provides extra configuration options.

### GKE

Currently, the only options available for GKE are for configuring the
health check policies needed per service when using a gateway.
These can be configured under `[component].provider.gke.healthCheck` or `all.provider.gke.healthCheck`.
Health check policies are automatically created when the chart is configured with gateways.

## Enabling OAuth Support

OAuth support can be enabled for both the UI and the API by setting `all.oauth.enabled` to `true`.
You will also need to set `all.oauth.issuerUri`, `all.oauth.audience`, `all.oauth.scope`,
and `all.oauth.redirectUri`, as described in the [relevant documentation](oauth_integration.html).

## Enabling Gateway Support

The Certdog Helm chart has support for generating the required HTTP routes for the
[Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/).
This can be done by adding gateways to `[component].gateway.gateways` or `all.gateway.gateways`.
Each route will reference each gateway specified for that component, setting up the required
HTTPS or HTTP routes.

Each gateway should take the following form:

```yaml
# each gateway is an entry in [component].gateway.gateways
gateway-name:
  # the name of the namespace holding the gateway
  namespace: my-namespace
  # the name of the section on the gateway to link HTTP routes to
  httpSection: http
  # the name of the section on the gateway to link HTTPS routes to
  httpsSection: https
```

Most components (such as the API) require HTTPS, and should not be accessed over HTTP.
As a result, the chart generates HTTP to HTTPS routes for these components, to prevent HTTP traffic.
For testing purposes, you can also enable `[component].gateway.allowHttp` or `all.gateway.allowHttp`,
which will create normal HTTP routes instead of redirects.

## Enabling and Disabling Components

Each component can be enabled with `[component].enabled`, and you can change the default
using `all.enabled`.
When disabled, all resources needed for that component (the deployment, service, any HTTP routes, etc.)
will not be generated by the chart.

## Configuring the Managed Database

All configuration of the managed database is present under `db.managed`.
Basic settings such as the number of replicas, the version of the database, and database user
details can be set through the corresponding options in the Helm chart.

Additional configuration may be provided via `db.managed.additionalConfig`, which is placed
within `spec` in the `MongoDBCommunity` resource itself.
This allows providing any other settings covered by the [MongoDB Controllers for Kubernetes
documentation](https://www.mongodb.com/docs/kubernetes/current/), such as setting the resources
allocated to each container, or changing the requested persistent volume claim, as seen below:

```yaml
db:
  managed:
    additionalConfig:
      podSpec:
        persistence:
          multiple:
            data:
              storage: 2G
              storageClass: standard
      statefulSet:
        spec:
          template:
            spec:
              containers:
              - name: mongod
                resources:
                  requests:
                    cpu: 200m
                    memory: 400M
```

The container used to initialise the database can also be customised, by providing settings
under `db`, just the same as providing pod and container configuration to other components.

## Setting the Service Account

By default, a service account is autogenerated and used by every pod.
To disable this, set `serviceAccount.create` to false.

To set the name of the autogenerated service account, or to give the name of a preexisting
service account to use, set `serviceAccount.name` to the desired name.

## Configuring Images and the Image Registry

The images used by the components can be customised under `all.image` and `[component].image`.
For each component the repository/registry can be set, along with the component name, the
version, the image pull policy, and the secrets used by pods to access the registry.

Unlike most other settings, `all.image` only applies to some components, and does not
override the `image.repository`, `image.name`, and `image.version` keys found under `db`,
`mongoReadiness`, and `crl`, as these typically have different values than the rest of the
Certdog components.

## Further Customisation

If you need to customise your deployment beyond the offerings of the Helm chart,
you have a few options:

* Manually edit the manifests produced by `helm manifest`
* Switch to using plain manifests
* Use `kustomize` as a Helm post renderer (see [this example](https://github.com/thomastaylor312/advanced-helm-demos/tree/master/post-render))

If you feel a feature is important enough to be included in the Helm chart's options,
contact support, and we may be able to add this option in a later release.
