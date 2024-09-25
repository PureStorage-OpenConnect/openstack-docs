.. _flasharray_conf:

Pure Storage Driver for FlashArray
==================================

FlashArray Cinder Driver Configuration
--------------------------------------

The OpenStack Cinder driver enables communication between OpenStack
and FlashArray systems. The user can use information from
the FlashArray to configure the driver by modifying the
``/etc/cinder/cinder.conf`` service file on the controller host.
For more information on the configuration and best practices for 
specific OpenStack releases please visit
the following link: http://support.purestorage.com/Solutions/OpenStack

Table 7.13 lists the required storage system attributes used in the
``/etc/cinder/cinder.conf`` configuration file.

.. _table-7.13:

+--------------------------------------+----------------------------+---------------------------------------------+
| FlashArray Attribute                 | Default                    | Description                                 |
+======================================+============================+=============================================+
| ``san_ip``                           | None                       | FlashArray Management VIP                   |
+--------------------------------------+----------------------------+---------------------------------------------+
| ``pure_api_token``                   | None                       | FlashArray authorization API token          |
+--------------------------------------+----------------------------+---------------------------------------------+

Table 7.13. Required FlashArray Attributes

Add the following lines to the file, replacing login and password with
the cluster admin login credentials

::


    [DEFAULT]
    enabled_backends=pure

    [pure]
    volume_backend_name=pure
    volume_driver=PURE_VOLUME_DRIVER
    san_ip=192.168.1.34
    pure_api_token=

For ``PURE_VOLUME_DRIVER`` use either ``cinder.volume.drivers.pure.PureISCSIDriver`` for iSCSI or
``cinder.volume.drivers.pure.PureFCDriver`` for Fibre Channel or
``cinder.volume.drivers.pure.PureNVMEDriver`` for NVMe connectivity.

Optional Cinder Configuration Attributes
----------------------------------------
You can optionally use the following attributes specific to FlashArray
in the ``[pure]`` section of the ``/etc/cinder/cinder.conf``
configuration file to control the interaction between the storage
system and the OpenStack Cinder service. (See Table 7.14.)

.. _table-7.14:

+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| FlashArray Attribute                                 | Default                    | Description                                                                                                                                                                                                     |
+======================================================+============================+=================================================================================================================================================================================================================+
| ``pure_eradicate_on_delete``                         | False                      | Enable auto-eradication of deleted volumes, snapshots and consistency groups on deletion.                                                                                                                       |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_host_personality``                            | None                       | Set the host personality to tune the communication protocol between the FlashArray and the hypervisors. Recommended to leave this at the default setting.                                                       |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``driver_ssl_cert_verify``                           | False                      | Set verification of FlashArray SSL certificates.                                                                                                                                                                |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``driver_ssl_cert_path``                             | None                       | Non-default directory path to ``CA_Bundle`` file with certificates of trusted CAs.                                                                                                                              |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_automatic_max_oversubscription_ratio``        | True                       | Allow FlashArray to calculate the array oversubscription ratio.                                                                                                                                                 |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``replication_device``                               | None                       | FlashArray Target for Replication. This option uses the format ``backend_id:<backend-id>,san_ip:<target-vip>,api_token:<target-api-token>,type:<replication-type>``                                             |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_replica_interval_default``                    | 3600                       | Snapshot replication interval in seconds.                                                                                                                                                                       |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_replica_retention_short_term_default``        | 14400                      | Retain all snapshots on target for this time (in seconds).                                                                                                                                                      |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_replica_retention_long_term_per_day_default`` | 3                          | Retain how many snapshots for each day.                                                                                                                                                                         |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_replica_retention_long_term_default``         | 7                          | Retain snapshots per day on target for this time (in days).                                                                                                                                                     |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_replication_pg_name``                         | ``cinder-group``           | Pure Protection Group name to use for async replication (will be created if it does not exist).                                                                                                                 |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_trisync_pg_name``                             | ``cinder-trisync``         | Pure Protection Group name to use for trisync replication leg inside the sync replication pod (will be created if it does not exist).                                                                           |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_replication_pod_name``                        | ``cinder-pod``             | Pure Pod name to use for sync replication (will be created if it does not exist).                                                                                                                               |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_iscsi_cidr``                                  | ``0.0.0.0/0``              | CIDR of FlashArray iSCSI targets hosts are allowed to connect to. Default will allow connection to any IPv4 address. This parameter now support IPv6 CIDRs. It is overriden by ``pure_iscsi_cidr_list`` if set. |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_iscsi_cidr_list``                             | ``[]``                     | List of IPv4 and IPv6 CIDR ranges of FlashArray iSCSI targets hosts are allowed to connect to. Default allows connection to any IPv4 or IPv6 address. This parameter supercedes ``pure_iscsi_cidr`` if set.     |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_nvme_cidr``                                   | ``0.0.0.0/0``              | CIDR of FlashArray NVMe targets hosts are allowed to connect to. Default will allow connection to any IPv4 address. This parameter now support IPv6 CIDRs. It is overriden by ``pure_nvme_cidr_list`` if set.   |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_nvme_cidr_list``                              | ``[]``                     | List of IPv4 and IPv6 CIDR ranges of FlashArray NMVe targets hosts are allowed to connect to. Default allows connection to any IPv4 or IPv6 address. This parameter supercedes ``pure_nvme_cidr`` if set.       |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_nvme_transport``                              | ``roce``                   | The NVMe transport layer to be used by the NVMe driver. This only supports RoCE at this time.                                                                                                                   |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_trisync_enabled``                             | False                      | Enable tri-sync replication.                                                                                                                                                                                    |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Table 7.14. Optional FlashArray Attributes

FlashArray Replication Setup
----------------------------

In order to use FlashArray with Replication enabled you must have a secondary
target backend configured and being referenced by primary host under
``replication_device`` attribute. Example:

::

    [pure]
    volume_backend_name=pure
    volume_driver=cinder.volume.drivers.pure.PureISCSIDriver
    san_ip=192.168.1.55
    pure_api_token=PURE_API_TOKEN
    replication_device=backend_id:pure-2,san_ip:192.168.1.32,api_token::type:async

    [pure-2]
    volume_backend_name=pure2
    volume_driver=cinder.volume.drivers.pure.PureISCSIDriver
    san_ip=192.18.1.32
    pure_api_token=PURE_API_TOKEN

    [DEFAULT]
    enabled_backends=pure

.. note::

   The secondary FlashArray is not required to be in the ``enabled_backends``
   like in the example above.

   The secondary FlashArray is not required to be managed by OpenStack at all.

The value for the ``type`` key can be either ``sync`` or ``async``.

If the ``type`` is ``sync`` volumes will be created in a stretched ActiveCluster
Pod. This requires two arrays preconfigured with ActiveCluster enabled. You can
optionally specify ``uniform`` as ``true`` or ``false``, which will instruct
the driver that data paths are uniform between arrays in the cluster and data
connections should be made to both upon attaching.

Note that more than one ``replication_device`` line can be added to allow for
multi-target device replication.

To enable 3-site replication, ie. a volume that is synchronously replicated to
one array and also asynchronously replicated to another then you must supply
two, and only two, ``replication_device`` lines, where one has ``type`` of
``sync`` and one where ``type`` is ``async``. Additionally, the parameter
``pure_trisync_enabled`` must be set ``True``.

A volume is only replicated if the volume is of a volume-type that has
the extra spec ``replication_enabled`` set to ``<is> True``. You can optionally
specify the ``replication_type`` key to specify ``<in> sync`` or ``<in> async``
or ``<in> trisync`` to choose the type of replication for that volume. If not
specified it will default to ``async``.

To create a volume type that specifies replication to remote back ends with
async replication:

.. code-block:: console

   $ openstack volume type create ReplicationType
   $ openstack volume type set --property replication_enabled='<is> True' ReplicationType
   $ openstack volume type set --property replication_type='<in> async' ReplicationType

Refer to ":ref:`Table 7.14<table-7.14>`" for optional configuration parameters available
for async replication configuration.
