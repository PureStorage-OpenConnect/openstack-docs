Deploying Pure Storage FlashBlade Manila driver in a Red Hat OpenStack Services on OpenShift 18.0
=================================================================================================

.. _purestorage-flashblade-rhoso18:

Overview
--------

This guide shows how to configure and deploy the Pure Storage FlashBlade Manila driver in a
**Red Hat OpenStack Services on OpenShift (RHOSO) 18.0** deployment.
After reading this, you'll be able to define the proper configuration and
deploy single or multiple FlashBlade manila back ends in a RHOSO cluster.

.. note::

  For more information about RHOSO, please refer to its `documentation pages
  <https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0-beta/html/deploying_red_hat_openstack_services_on_openshift/index>`_.

.. warning::

  RHOSO18.0 is based on OpenStack 2023.1 (Antelope) release with 2023.2 (Bobcat) backports. Features
  included after Antelope release may not be available in RHOSO18.0.

Requirements
------------

In order to deploy Pure Storage FlashBlade Manila back ends, you should have the
following requirements satisfied:

- Pure Storage FlashBlades deployed and ready to be used as Manila
  back ends. See :ref:`manila_flashblade_prerequisites` for more details.

- RHOSO openstack control plane deployed where Manila services will be configured.


Deployment Steps
----------------

Use Certified Pure Storage Manila Share Image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Red Hat requires that you utilize the Certified Pure Storage Manila Share
Image when deploying RHOSO18.0 with a Pure Storage FlashArray backend.

This container can be found in the `Red Hat Container Catalog <https://catalog.redhat.com/search?searchType=containers&partnerName=Pure%20Storage%2C%20Inc.&p=1>`__
and should be stored in a local registry.

Create a Secret file
^^^^^^^^^^^^^^^^^^^^

It is necessary to create a secret file that will contain the access
credential(s) for your backend Pure FlashBlade(s) in your RHOSO deployment.

In this following example file (``pure-secrets.yaml``) secrets are provided for
a FlashBlade. If using multiple backends you need to define a unique secret for each.

.. code-block:: yaml
  :name: manila-pure-secret

    [flashblade]
    flashblade_mgmt_vip = <INSERT FB MGMT VIP HERE>
    flashblade_data_vip = <INSERT FB DATA VIP HERE>
    flashblade_api = <INSERT FB API TOKEN HERE>

Create the OpenShift secret based on the above configuration file:

.. code-block:: bash
  :name: manila-secret

    $ oc create secret generic pure-fb-secret --from-file=pure-secrets.yaml

For security, you may now delete the configuration file.

Create an OpenStackVersion config file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As previously mentioned, it is required, when using FlashBlades as Manila
backends, that a certified Manila Share image is used within the RHOSO
deployment. This is defined in the following YAML file (``pure-m-shr-image.yaml``):

.. code-block:: yaml
  :name: manila-pure-openstackversion

  apiVersion: core.openstack.org/v1beta1
  kind: OpenStackVersion
  metadata:
    name: openstack
  spec:
    customContainerImages:
      manilaShareImages:
        flashblade: registry.connect.redhat.com/purestorage/openstack-manila-share-pure-18-0

In this example the image is being pulled directly from the Red Hat image registry, but you
may use a copy in your local image registry created by the OpenShift deployment.

Update the OpenStack Control Plane
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create the following file (``pure-m-shr-config.yaml``) to update the OpenStack
control plane with the FlashBlade manila backend(s):

.. code-block:: yaml
  :name: manila-pure-openstackcontrolplane

  apiVersion: core.openstack.org/v1beta1
  kind: OpenStackControlPlane
  metadata:
    name: openstack
  spec:
    manila:
      enabled: true
      template:
        manilaAPI:
          replicas: 3
          customServiceConfig: |
            [DEFAULT]
            debug = true
            enabled_share_protocols=nfs
        manilaScheduler:
          replicas: 3
        manilaShares:
          flashblade:
            networkAttachments:
            - storage
            customServiceConfigSecrets:
            - pure-fb-_secret
            customServiceConfig: |
              [DEFAULT]
              debug = true
              enabled_share_backends=flashblade
              [flashblade]
              driver_handles_share_servers=False
              share_backend_name=flashblade
              share_driver=manila.share.drivers.purestorage.flashblade.FlashBladeShareDriver


Apply the custom configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After ensuring that you full admininstrative access to the OpenShift cluster, apply
the above configuration files:

.. code-block:: bash
  :name: pure-manila-apply

  $ oc apply -f ./pure-secrets.yaml
  $ oc apply -f ./pure-m-shr-image.yaml
  $ oc apply -f ./pure-m-shr-config.yaml

Test the Deployed Back Ends
^^^^^^^^^^^^^^^^^^^^^^^^^^^

After RHOSO system is deployed, run the following command to check if the
Manila services are up:

.. code-block:: bash
  :name: manila-service-list

  $ export OS_CLOUD=<your cloud name>
  $ export OS_PASSWORD=<your password>
  $ openstack share service list


Run the following commands to create the share types mapped to the deployed back ends:

.. code-block:: bash
  :name: create-share-types

  $ openstack share type create --snapshot_support true ---revert_to_snapshot_support true flashblade false

Make sure that you're able to create Manila shares with the configured volume
types:

.. code-block:: bash
  :name: create-shares

  $ openstack share create --share-type flashblade --name testshare NFS 1
