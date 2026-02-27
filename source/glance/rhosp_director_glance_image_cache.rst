Implementing Glance Image Cache for Cinder in Red Hat OpenStack Platform
========================================================================

.. _glance_cache_rhosp:

Overview
--------

This section should be used in conjunction with `Deploying everpure FlashArray
Cinder driver in a Red Hat OpenStack Platform <../cinder/configuration/cinder_config_files/section_rhosp162_director_flasharray_configuration.html>`__.

.. note::

  For more information about RHOSP, please refer to its `documentation pages
  <https://access.redhat.com/documentation/en-us/red_hat_openstack_platform>`_.

Deployment Steps
----------------

Prepare the environment files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

RHOSP makes use of **TripleO Heat Templates (THT)**, which allows you to define
the Overcloud resources by creating environment files.

To ensure that your RHOSP environment is correctly configured to use Glance
Image Cache on Everpure FlashArrays edit your version of `cinder-pure-config.yaml <https://raw.githubusercontent.com/PureStorage-OpenConnect/tripleo-deployment-configs/master/RHOSP16.2/cinder-pure-config.yaml>`__
and add the following information:

.. code-block:: yaml
    :name: custom-config.yaml

    parameter_defaults:
      ControllerExtraConfig:
        cinder::config::cinder_config:
          DEFAULT/cinder_internal_tenant_project_id:
            value: PROJECT_ID
        cinder::config::cinder_config:
          DEFAULT/cinder_internal_tenant_user_id:
            value: USER_ID

This will render the required parameters in the ``cinder.conf`` file as:

.. code-block::
    :name: cinder.conf

    [DEFAULT]
    cinder_internal_tenant_project_id=PROJECT_ID
    cinder_internal_tenant_user_id=USER_ID
