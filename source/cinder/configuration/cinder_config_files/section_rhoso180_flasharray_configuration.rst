Deploying Pure Storage FlashArray Cinder driver in a Red Hat OpenStack Services on OpenShift 18.0
=================================================================================================

.. _purestorage-flsharray-rhoso180:

Overview
--------

This guide shows how to configure and deploy the Pure Storage FlashArray Cinder driver in a
**Red Hat OpenStack Services on OpenShift (RHOSO) 18.0** deployment.
After reading this, you'll be able to define the proper configuration and
deploy single or multiple FlashArray Cinder back ends in a RHOSO cluster.

.. note::

  For more information about RHOSO, please refer to its `documentation pages
  <https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0-beta/html/deploying_red_hat_openstack_services_on_openshift/index>`_.

.. warning::

  RHOSO18.0 is based on OpenStack 2023.1 (Antelope) release with 2023.2 (Bobcat) backports. Features
  included after Antelope release may not be available in RHOSO18.0.

In Red Hat OpenStack Services on OpenShift 18.0, the FlashArray cinder volume drivers support
the following dataplanes:

- iSCSI
- FibreChannel
- NVMe-TCP (support backported from OpenStack 2023.2 [Bobcat])

Requirements
------------

In order to deploy Pure Storage FlashArray Cinder back ends, you should have the
following requirements satisfied:

- Pure Storage FlashArrays deployed and ready to be used as Cinder
  back ends. See :ref:`cinder_flasharray_prerequisites` for more details.

- RHOSO openstack control plane deployed where Cinder services will be configured.


Deployment Steps
----------------

Prepare the OpenStack Control Plane
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following steps need to be applied after the OpenStackControlPlane has been
successfully deployed in your environment.

Use Certified Pure Storage Cinder Volume Image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Red Hat requires that you utilize the Certified Pure Storage Cinder Volume
Image when deploying RHOSO18.0 with a Pure Storage FlashArray backend.

This container can be found in the `Red Hat Container Catalog <https://catalog.redhat.com/search?searchType=containers&partnerName=Pure%20Storage%2C%20Inc.&p=1>`__
and should be stored in a local registry.

Create a Secret file
^^^^^^^^^^^^^^^^^^^^

It is necessary to create a secret file that will contain the access
credential(s) for your backend Pure FlashArray(s) in your RHOSO deployment.

In this following example file (``pure-secrets.yaml``) secrets are provided for
two backend FlashArrays. You need to define a unique secret for each of your backends.

.. code-block:: yaml
  :name: cinder-pure-secret

  apiVersion: v1
  kind: Secret
  metadata:
    labels:
      service: cinder
      component: cinder-volume
    name: cinder-volume-pure-secrets1
  type: Opaque
  stringData:
    pure-secrets.conf: |
      [pure-iscsi]
      san_ip=<INSERT YOUR FA1 IP HERE>
      pure_api_token=<INSERT YOUR FA1 API TOKEN HERE>
  ---
  apiVersion: v1
  kind: Secret
  metadata:
    labels:
      service: cinder
      component: cinder-volume
    name: cinder-volume-pure-secrets2
  type: Opaque
  stringData:
    pure-secrets.conf: |
      [pure-iscsi-2]
      san_ip=<INSERT YOUR FA2 IP HERE>
      pure_api_token=<INSERT YOUR FA2 API TOKEN HERE>

Create an OpenStackVersion config file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As previously mentioned, it is required, when using FlashArrays as Cinder
backends, that a certified Cinder Volume image is used within the RHOSO
deployment. This is defined in the following YAML file (``pure-c-vol-image.yaml``):

.. code-block:: yaml
  :name: cinder-pure-openstackversion

  apiVersion: core.openstack.org/v1beta1
  kind: OpenStackVersion
  metadata:
    name: openstack
  spec:
    customContainerImages:
      cinderVolumeImages:
        pure-iscsi: registry.connect.redhat.com/purestorage/openstack-cinder-volume-pure-18-0
        pure-iscsi-2: registry.connect.redhat.com/purestorage/openstack-cinder-volume-pure-18-0

In this example the image is being pulled directly from the Red Hat image registry, but you
may use a copy in your local image registry created by the OpenShift deployment.

Update the OpenStack Control Plane
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create the following file (``pure-c-vol-config.yaml``) to update the OpenStack
control plane with the FlashArray cinder backend(s):

.. code-block:: yaml
  :name: cinder-pure-openstackcontrolplane

  apiVersion: core.openstack.org/v1beta1
  kind: OpenStackControlPlane
  metadata:
    name: openstack
  spec:
    cinder:
      template:
        cinderVolumes:
          pure-iscsi:
            customServiceConfig: |
              [pure-iscsi]
              volume_backend_name=pure-iscsi
              volume_driver=cinder.volume.drivers.pure.PureISCSIDriver
            customServiceConfigSecrets:
              - cinder-volume-pure-secrets1
            networkAttachments:
            - storage
            replicas: 1
            resources: {}
          pure-iscsi-2:
            customServiceConfig: |
              [pure-iscsi-2]
              volume_backend_name=pure-iscsi-2
              volume_driver=cinder.volume.drivers.pure.PureISCSIDriver
            customServiceConfigSecrets:
              - cinder-volume-pure-secrets2
            networkAttachments:
            - storage
            replicas: 1
            resources: {}


The above example is again for two backends. Also notice that the Cinder configuration
part of the deployment (notice that *pure-iscsi* / *pure-iscsi-2* here must match the ones
used in the *OpenStackVersion* above):

Note that if you are using the NVMe volume driver an addtional parameter of
``pure_nvme_transport=tcp`` will needed to be added into the backend stanza(s).

Apply the custom configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After ensuring that you full admininstrative access to the OpenShift cluster, apply
the above configuration files:

.. code-block:: bash
  :name: pure-cinder-apply

  $ oc apply -f ./pure-c-vol.yaml
  $ oc apply -f ./pure-secrets.yaml
  $ oc apply -f ./pure-c-vol-image.yaml
  $ oc apply -f ./pure-c-vol-config.yaml

Test the Deployed Back Ends
^^^^^^^^^^^^^^^^^^^^^^^^^^^

After RHOSO system is deployed, access the provided pod openstackclient from where you can 
run the OpenStack commands to check if the Cinder services are up:

.. code-block:: bash
  :name: cinder-service-list

  $ oc rsh openstackclient
  sh-5.1$ export OS_PASSWORD=<your password>
  sh-5.1$ openstack volume service list


Run the following commands to create the volume types mapped to the deployed back ends:

.. code-block:: bash
  :name: create-volume-types

  sh-5.1$ openstack volume type create pure-iscsi
  sh-5.1$ openstack volume type set --property volume_backend_name=pure-iscsi pure-iscsi
  sh-5.1$ openstack volume type create pure-iscsi-2
  sh-5.1$ openstack volume type set --property volume_backend_name=pure-iscsi-2 pure-iscsi-2

Make sure that you're able to create Cinder volumes with the configured volume
types:

.. code-block:: bash
  :name: create-volumes

  sh-5.1$ openstack volume create --type pure-iscsi --size 1 v1
  sh-5.1$ openstack volume create --type pure-iscsi-2 --size 1 v2
