ADDENDUM: Using Red Hat OpenStack Platform director Operator (RHOSPdO) 17.1
===========================================================================

.. _purestorage-flasharray-rhospdo171:

Overview
--------

This addendum shows the (additonal) steps required when deploying RHOSP using the
director Operator process on OpenShift.

Requirements
------------

In order to deploy Pure Storage FlashArray Cinder back ends, you should have the
following requirements satisfied:

- Pure Storage FlashArrays deployed and ready to be used as Cinder
  back ends. See :ref:`cinder_flasharray_prerequisites` for more details.

- RHOSP Director deployed on OpenShift using the director Operator.

- RHOSP Overcloud Controller nodes where Cinder services will be installed have
  multipath and iscsi software installed, configured and started.


Deployment Steps
----------------

Prepare the environment files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

RHOSPdO still makes use of **TripleO Heat Templates (THT)**, which allows you to define
the Overcloud resources by creating environment files as defined in 
:ref:`purestorage-flsharray-rhosp171`.

It is not required to to use the `pure-temp.yaml` file for a RHOSPdO deployment.

The only configuration file required is `cinder-pure-config.yaml <https://raw.githubusercontent.com/PureStorage-OpenConnect/tripleo-deployment-configs/master/RHOSP17.1/cinder-pure-config.yaml>`__, however there needs to be one modification made to this file.

Comment out, or remove the line

  .. code-block:: yaml

    OS::TripleO::NodeExtraConfigPost: /home/stack/templates/pure/pure-temp.yaml

This configuration file needs to be saved in the `heat-env-config` directory that
will be used to create the `heat-env-config ConfigMap`. See the Red Hat director
Operator documentation for more details on this.

Once the new ConfigMap has been created the OpenStack environemtn can be (re)deployed.
