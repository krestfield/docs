---
layout: default
title: Deploying to GKE
parent: Certdog
nav_order: 1102
---

# Deploying Certdog to Google Kubernetes Engine

> From version: 1.17.0

This guide outlines the steps required to deploy Certdog to Google Kubernetes Engine (GKE).

## 1. Create a cluster

Both [standard](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/creating-a-zonal-cluster) and
[autopilot](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/creating-an-autopilot-cluster)
clusters can be used with Certdog.
If you just want to get started quickly, using an autopilot takes care of much of the setup for a GKE
cluster.

If you want to expose your Certdog instance, make sure to enable Gateway API support.

## 2. Deploy Certdog to the cluster

See [Deploying to Kubernetes](deploying_to_kubernetes.html) for details of how to deploy Certdog
to the cluster.

Provider specific options are under `[component].provider` or `all.provider`.
Currently, the only options available for GKE are for configuring the
health check policies needed per service when using a gateway.

Note that if you decide to deploy cert-manager, as described in the
[Running Certdog on Kubernetes Locally](running_kubernetes_locally.html) guide,
you will need to include the following line in your `helm install` command:

```bash
--set global.leaderElection.namespace=cert-manager
```

This prevents cert-manager from attempting to access the protected kube-system namespace.
This may only be necessary on autopilot clusters.

## 3. Expose Certdog outside the cluster (optional)

Before GKE is able to provision a gateway for regional gateway classes, you will need to ensure
you have an active, [proxy-only subnet](https://docs.cloud.google.com/load-balancing/docs/proxy-only-subnets)
available in the same region you are deploying your cluster.

Once this is created, you can provision a load balancer by
[creating a gateway](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/deploying-gateways)
with the desired [gateway class](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/gatewayclass-capabilities).
For example, to load balance regional traffic, you can use the `gke-l7-regional-external-managed`
gateway class by placing this class under the `spec.gatewayClassName` field of the gateway.

You are expected to create the gateway yourself - it is not managed by Helm.

You will also need to [provide health checks](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/configure-gateway-resources#configure_health_check)
configured for each backend connected to the gateway.
These are nearly identical to the container health checks in the Certdog deployment, but described
using `HealthCheckPolicy` resources.

If you have installed Certdog with the Certdog Helm GKE chart, you can enable health checks by setting
`healthchecks.enabled` to true.
Otherwise, you can create health checks for each enabled service using plain manifests.

Once the gateway and corresponding load balancer are running, you should be able to access Certdog
via the provided IP address.
If you are using a HTTPS listener on the gateway, you may need to ensure a certificate is available to
terminate TLS.
An example of using cert-manager to provide a certificate for this purpose can be found in
the [Running Certdog on Kubernetes Locally](running_kubernetes_locally.html) guide.

## Next Steps

* [Customising Certdog on Kubernetes with Helm](customising_with_helm.html)
* [Integrating Certdog on Kubernetes with cert-manager](integration_with_cert_manager.html)
