Deploying Pure Storage FlashArray Cinder driver in a Red Hat OpenStack Platform 17.1
====================================================================================

.. _purestorage-flsharray-rhosp171:

Overview
--------

This guide shows how to configure and deploy the Pure Storage FlashArray Cinder driver in a
**Red Hat OpenStack Platform (RHOSP) 17.1** Overcloud, using RHOSP Director.
After reading this, you'll be able to define the proper environment files and
deploy single or multiple FlashArray Cinder back ends in RHOSP Overcloud Controller
nodes.

.. note::

  For more information about RHOSP, please refer to its `documentation pages
  <https://access.redhat.com/documentation/en-us/red_hat_openstack_platform>`_.

.. warning::

  RHOSP17.1 is based on OpenStack Wallaby release with upstream backports. Features
  included after Wallaby release may not be available in RHOSP17.1.

Requirements
------------

In order to deploy Pure Storage FlashArray Cinder back ends, you should have the
following requirements satisfied:

- Pure Storage FlashArrays deployed and ready to be used as Cinder
  back ends. See :ref:`cinder_flasharray_prerequisites` for more details.

- RHOSP Director user credentials to deploy Overcloud.

- RHOSP Overcloud Controller nodes where Cinder services will be installed.


Deployment Steps
----------------

Prepare the environment files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

RHOSP makes use of **TripleO Heat Templates (THT)**, which allows you to define
the Overcloud resources by creating environment files.

To ensure that your RHOSP environment is correctly configured for using
Pure Storage FlashArrays obtain a copy of `pure-temp.yaml <https://raw.githubusercontent.com/PureStorage-OpenConnect/tripleo-deployment-configs/master/RHOSP17.0/pure-temp.yaml>`__
and `cinder-pure-config.yaml <https://raw.githubusercontent.com/PureStorage-OpenConnect/tripleo-deployment-configs/master/RHOSP17.1/cinder-pure-config.yaml>`__ 
from the Pure Storage TripleO Deployment Config repo and save these in
the ``/home/stack/templates`` directory. These will be required when
deploying the Overcloud.

Multiple back end configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Define Pure Storage Cinder back ends using Custom THT Configuration syntax.
It's possible to define all the back ends in a single environment file by
modifying the ``cinder-pure-config.yaml`` file as follows:

  .. code-block:: yaml
    :name: cinder-flasharray-backend1.yaml

    parameter_defaults:
      CinderPureBackendName:
        - tripleo_pure_1
        - tripleo_pure_2
      CinderPureSanIp: '' # Placeholder
      CinderPureAPIToken: '' # Placeholder
      CinderPureStorageProtocol: 'iSCSI' # Default value for all Pure backends
      CinderPureUseChap: false # Default value for the Pure backends
      CinderPureMultiConfig:
        tripleo_pure_1:
          CinderPureSanIp: '10.0.0.1'
          CinderPureAPIToken: 'secret'
        tripleo_pure_2:
          CinderPureSanIp: '10.0.0.2'
          CinderPureAPIToken: 'anothersecret'
          CinderPureUseChap: true # Specific value for this backend

  Modify the parameter values according to your Pure Storage back end
  configuration.

.. note::

  You can define arbitrary Custom THT Configurations using the following syntax:

  .. code-block:: yaml
      :name: custom-config.yaml

      parameter_defaults:
        ControllerExtraConfig:
          cinder::config::cinder_config:
            <backend_name>/<configuration_name>:
              value: <value>

  Each configuration will be rendered in ``cinder.conf`` file as:

  .. code-block::
      :name: cinder.conf

      [backend_name]
      configuration_name=value

  See `Optional Cinder Configuration Attributes (RHOSP17)
  <./section_flasharray-conf-wallaby.html#optional-cinder-configuration-attributes>`_
  for a complete list of the available Cinder Configuration Options.


Using the NVMe-TCP protocol (RHOSP 17.1.4 only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

From RHOSP 17.1.4 you can now use the Pure NVMe-TCP driver for FlashArray, but you must use
very specific TripleO configuration files, as this driver is not supported by the standard
Pure Storage TripleO system.

Create a new environment file ``pure-nvmet-config.yaml`` in your templates directory as follows

.. code-block:: yaml
  :name: pure-nvmet-config.yaml

  resource_registry:
    OS::TripleO::Services::CinderBackendNVMeOF: /usr/share/openstack-tripleo-heat-templates/deployment/cinder/cinder-backend-nvmeof-puppet.yaml

  parameter_defaults:
    CinderEnableIscsiBackend: false
    CinderEnableNVMeOFBackend: true
    StandaloneExtraConfig:
      cinder_user_enabled_backends: ['pure1']
      cinder::config::cinder_config:
        pure1/volume_backend_name:
          value: pure1
        pure1/volume_driver:
          value: cinder.volume.drivers.pure.PureNVMEDriver
        pure1/san_ip:
          value: <SAN IP>
        pure1/pure_api_token:
          value: <Pure API token>
        pure1/pure_nvme_transport:
          value: tcp
        pure1/pure_eradicate_on_delete:
          value: true
      tripleo::profile::base::cinder::volume::cinder_enable_nvmeof_backend: false
    ControllerParameters:
      ExtraKernelPackages:
        nvme-cli: {}
      ExtraKernelModules:
        nvme-fabrics: {}
    ComputeParameters:
      ExtraKernelPackages:
        nvme-cli: {}
      ExtraKernelModules:
        nvme-fabrics: {}

Add this file to your ``openstack overcloud deploy`` command (``-e pure-nvmet-config.yaml``) 

Use Certified Pure Storage Cinder Volume Container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Red Hat requires that you utilize the Certified Pure Storage Cinder Volume
Container when deploying RHOSP17.1 with a Pure Storage FlashArray backend.

This container can be found in the `Red Hat Container Catalog <https://catalog.redhat.com/software/containers/search?q=pure&p=1>`__
and should be stored in a local registry.

Create a Custom Environment File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new environment file ``custom_container_pure.yaml`` in the directory
``/home/stack/templates`` with only the custom container parameter.

.. code-block:: bash

  parameter_defaults:
    ContainerCinderVolumeImage: <registry:port>/<directory>/openstack-cinder-volume-pure:<version>

Alternatively, you may edit the container images environment file (usually
``overcloud_images.yaml``, created when the ``openstack overcloud container
image prepare`` command was executed) and change the appropriate
parameter to use the custom container image.

Deploy Overcloud
^^^^^^^^^^^^^^^^

Now that you have the Cinder back end environment files defined, you can run
the command to deploy the RHOSP Overcloud. Run the following command as
the ``stack`` user in the RHOSP Director command line, specifying the
YAML file(s) you defined:

.. code-block:: bash
  :name: overcloud-deploy

   (undercloud) [stack@rhosp-undercloud ~]$ openstack overcloud deploy \
   --templates \
   -e /usr/share/openstack-tripleo-heat-templates/environments/multipathd.yaml \
   -e /home/stack/cinder-pure-config.yaml \
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
     -e /usr/share/openstack-tripleo-heat-templates/environments/multipathd.yaml \
     -e /home/stack/containers-prepare-parameter.yaml \
     --environment-directory /home/stack/templates \
     --stack overcloud


Test the Deployed Back Ends
^^^^^^^^^^^^^^^^^^^^^^^^^^^

After RHOSP Overcloud is deployed, run the following command to check if the
Cinder services are up:

.. code-block:: bash
  :name: cinder-service-list

  [stack@rhosp-undercloud ~]$ source ~/overcloudrc
  (overcloud) [stack@rhosp-undercloud ~]$ cinder service-list


Run the following commands as ``stack`` user in the RHOSP Director command line
to create the volume types mapped to the deployed back ends:

.. code-block:: bash
  :name: create-volume-types

  [stack@rhosp-undercloud ~]$ source ~/overcloudrc
  (overcloud) [stack@rhosp-undercloud ~]$ cinder type-create pure1
  (overcloud) [stack@rhosp-undercloud ~]$ cinder type-key pure1 set volume_backend_name=tripleo_pure_1
  (overcloud) [stack@rhosp-undercloud ~]$ cinder type-create pure2
  (overcloud) [stack@rhosp-undercloud ~]$ cinder type-key pure2 set volume_backend_name=tripleo_pure_2

Make sure that you're able to create Cinder volumes with the configured volume
types:

.. code-block:: bash
  :name: create-volumes

  [stack@rhosp-undercloud ~]$ source ~/overcloudrc
  (overcloud) [stack@rhosp-undercloud ~]$ cinder create --volume-type pure1 --name v1 1
  (overcloud) [stack@rhosp-undercloud ~]$ cinder create --volume-type pure2 --name v2 1
