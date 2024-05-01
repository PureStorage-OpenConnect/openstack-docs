Deploying Pure Storage FlashBlade Manila driver in a Red Hat OpenStack Platform 17.1
====================================================================================

.. _purestorage-flashblade-rhosp171:

Overview
--------

This guide shows how to configure and deploy the Pure Storage FlashBlade Manila driver in a
**Red Hat OpenStack Platform (RHOSP) 17.1** Overcloud, using RHOSP Director.
After reading this, you'll be able to define the proper environment files and
deploy single or multiple FlashBlade Manila back ends in RHOSP Overcloud Controller
nodes.

.. note::

  For more information about RHOSP, please refer to its `documentation pages
  <https://access.redhat.com/documentation/en-us/red_hat_openstack_platform>`_.

.. warning::

  RHOSP17.1 is based on OpenStack Wallaby release with Xena backports. Features
  included after Wallaby release may not be available in RHOSP17.1.

Requirements
------------

In order to deploy Pure Storage FlashBlade Manila back ends, you should have the
following requirements satisfied:

- Pure Storage FlashBlades deployed and ready to be used as Manila
  back ends. See :ref:`manila_flashblade_prerequisites` for more details.

- RHOSP Director user credentials to deploy Overcloud.

- RHOSP Overcloud Controller nodes where Manila services will be installed.


Deployment Steps
----------------

Prepare the environment files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

RHOSP makes use of **TripleO Heat Templates (THT)**, which allows you to define
the Overcloud resources by creating environment files.

To ensure that your RHOSP environment is correctly configured for using
Pure Storage FlashBlades obtain a copy of `manila-flashblade-config.yaml <https://raw.githubusercontent.com/PureStorage-OpenConnect/tripleo-deployment-configs/master/manila/RHOSP17.1/manila-flashblade-config.yaml>`__
from the Pure Storage TripleO Deployment Config repo and save this in
the ``/home/stack/templates`` directory. This will be required when
deploying the Overcloud.

Use Certified Pure Storage Manila Share Container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Red Hat requires that you utilize the Certified Pure Storage Manila Share
Container when deploying RHOSP17.1 with a Pure Storage FlashArray backend.

This container can be found in the `Red Hat Container Catalog <https://catalog.redhat.com/software/containers/search?q=pure&p=1>`__
and should be stored in a local registry.

Create a Custom Environment File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new environment file ``custom_container_pure.yaml`` in the directory
``/home/stack/templates`` with only the custom container parameter.

.. code-block:: bash

  parameter_defaults:
    ContainerManilaShareImage: <registry:port>/<directory>/openstack-manila-share-pure:<version>

Alternatively, you may edit the container images environment file (usually
``overcloud_images.yaml``, created when the ``openstack overcloud container
image prepare`` command was executed) and change the appropriate
parameter to use the custom container image.

Deploy Overcloud
^^^^^^^^^^^^^^^^

Now that you have the Manila back end environment files defined, you can run
the command to deploy the RHOSP Overcloud. Run the following command as
the ``stack`` user in the RHOSP Director command line, specifying the
YAML file(s) you defined:

.. code-block:: bash
  :name: overcloud-deploy

   (undercloud) [stack@rhosp-undercloud ~]$ openstack overcloud deploy \
   --templates \
   -e /home/stack/manila-share-config.yaml \
   -e /home/stack/containers-prepare-parameter.yaml \
   -e /home/stack/templates/custom_container_pure.yaml \
   --stack overcloud

If you modified the container images environment file the
``custom_container_pure.yaml`` option is not required in the above command.

.. note::
  Alternatively, you can use ``--environment-directory`` parameter and specify
  the whole directory to the deployment command. It will consider all the YAML
  files within this directory:

  .. code-block:: bash
    :name: overcloud-deploy-environment-directory

     (undercloud) [stack@rhosp-undercloud ~]$ openstack overcloud deploy \
     --templates \
     -e /home/stack/containers-prepare-parameter.yaml \
     --environment-directory /home/stack/templates \
     --stack overcloud


Test the Deployed Back Ends
^^^^^^^^^^^^^^^^^^^^^^^^^^^

After RHOSP Overcloud is deployed, run the following command to check if the
Cinder services are up:

.. code-block:: bash
  :name: manila-service-list

  [stack@rhosp-undercloud ~]$ source ~/overcloudrc
  (overcloud) [stack@rhosp-undercloud ~]$ openstack share service list


Run the following commands as ``stack`` user in the RHOSP Director command line
to create the volume types mapped to the deployed back ends:

.. code-block:: bash
  :name: create-share-types

  [stack@rhosp-undercloud ~]$ source ~/overcloudrc
  (overcloud) [stack@rhosp-undercloud ~]$ manila type-create default false
  (overcloud) [stack@rhosp-undercloud ~]$ manila type-key default set snapshot_supoort=True revert_to_snapshot_support=True

Make sure that you're able to create Manila shares with the configured volume
types:

.. code-block:: bash
  :name: create-shares

  [stack@rhosp-undercloud ~]$ source ~/overcloudrc
  (overcloud) [stack@rhosp-undercloud ~]$ manila create NFS 1 --share-type dhss_false --name testshare
