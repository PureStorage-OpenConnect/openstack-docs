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
  <https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_red_hat_openstack_services_on_openshift/index>`_.

.. warning::

  RHOSO18.0 is based on OpenStack 2023.1 (Antelope) release with a backport of the 
  2023.2 (Bobcat) NVMe-TCP Cinder driver for Pure Storage. Other Pure Storage driver features
  included after the Antelope release may not be available in RHOSO18.0.

In Red Hat OpenStack Services on OpenShift 18.0, the FlashArray cinder volume drivers support
the following dataplanes:

- iSCSI
- NVMe-TCP (support backported from OpenStack 2023.2 [Bobcat])
- FibreChannel [certification pending]

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

This container can be found in the `Red Hat Container Catalog <https://catalog.redhat.com/search?searchType=containers&partnerName=Pure%20Storage%2C%20Inc.&p=1>`__.

Ensure the certified image is added to the ``openstackversion`` CR.  This is defined in the following YAML file (``openstack_version.yaml``):

.. code-block:: yaml
  :name: cinder-openstackversion

  apiVersion: core.openstack.org/v1beta1
  kind: OpenStackVersion
  metadata:
    name: openstack
  spec:
    customContainerImages:
      cinderVolumeImages:
        pure1: registry.connect.redhat.com/purestorage/openstack-cinder-volume-pure-18-0:latest
        pure2: registry.connect.redhat.com/purestorage/openstack-cinder-volume-pure-18-0:latest

This example is for two Pure Storage backends - defined later in the OpenStackControlPlane CR.

Save this file and update:

.. code-block:: bash
   :name: openstackversion-apply

   $ oc apply -f openstack-version.yaml

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
      [pure1]
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
      [pure2]
      san_ip=<INSERT YOUR FA2 IP HERE>
      pure_api_token=<INSERT YOUR FA2 API TOKEN HERE>

Save this file and apply:

.. code-block:: bash
   :name: secret-apply

   $ oc apply -f ./pure-secrets.yaml

Update the OpenStack Control Plane
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open your OpenStackControlPlane CR file, ``openstack_control_plane.yaml``. Edit the CR file and add in the
Pure Storage Cinder volume backend.

**iSCSI driver example:**

.. code-block:: yaml
  :name: cinder-pureiscsi-openstackcontrolplane

  apiVersion: core.openstack.org/v1beta1
  kind: OpenStackControlPlane
  metadata:
    name: openstack
  spec:
    cinder:
      template:
        cinderVolumes:
          pure1:
            customServiceConfig: |
              [pure1]
              volume_backend_name=pure
              volume_driver=cinder.volume.drivers.pure.PureISCSIDriver
            customServiceConfigSecrets:
              - cinder-volume-pure-secrets1
            networkAttachments:
            - storage
            - storageMgmt
            replicas: 1
            resources: {}
          pure2:
            customServiceConfig: |
              [pure2]
              volume_backend_name=pure2
              volume_driver=cinder.volume.drivers.pure.PureISCSIDriver
            customServiceConfigSecrets:
              - cinder-volume-pure-secrets2
            networkAttachments:
            - storage
            - storageMgmt
            replicas: 1
            resources: {}

**NVMe-TCP driver example:**

.. code-block:: yaml
  :name: cinder-purenvme-openstackcontrolplane

  apiVersion: core.openstack.org/v1beta1
  kind: OpenStackControlPlane
  metadata:
    name: openstack
  spec:
    cinder:
      template:
        cinderVolumes:
          pure1:
            customServiceConfig: |
              [pure1]
              volume_backend_name=pure
              volume_driver=cinder.volume.drivers.pure.PureNVMEDriver
              pure_nvme_transport=tcp
            customServiceConfigSecrets:
              - cinder-volume-pure-secrets1
            networkAttachments:
            - storage
            - storageMgmt
            replicas: 1
            resources: {}
          pure2:
            customServiceConfig: |
              [pure2]
              volume_backend_name=pure2
              volume_driver=cinder.volume.drivers.pure.PureNVMEDriver
              pure_nvme_transport=tcp
            customServiceConfigSecrets:
              - cinder-volume-pure-secrets2
            networkAttachments:
            - storage
            - storageMgmt
            replicas: 1
            resources: {}

 
The above examples are for two backends. Notice that the Cinder configuration
part of the deployment (*pure1* / *pure2*) here must match the names
used in the *OpenStackVersion* above):

Save this file and update:

.. code-block:: bash
   :name: openstackversion-apply

   $ oc apply -f openstack_control_plane.yaml

Test the Deployed Back Ends
^^^^^^^^^^^^^^^^^^^^^^^^^^^

After RHOSO system is deployed, access the provided pod openstackclient from where you can 
run the OpenStack commands to check if the Cinder services are up:

.. code-block:: bash
  :name: cinder-service-list

  $ oc rsh openstackclient
  sh-5.1$ openstack volume service list


Run the following commands to create the volume types mapped to the deployed back ends:

.. code-block:: bash
  :name: create-volume-types

  sh-5.1$ openstack volume type create pure1
  sh-5.1$ openstack volume type set --property volume_backend_name=pure1 pure1
  sh-5.1$ openstack volume type create pure2
  sh-5.1$ openstack volume type set --property volume_backend_name=pure2 pure2

Make sure that you're able to create Cinder volumes with the configured volume
types:

.. code-block:: bash
  :name: create-volumes

  sh-5.1$ openstack volume create --type pure1 --size 1 v1
  sh-5.1$ openstack volume create --type pure2 --size 1 v2
