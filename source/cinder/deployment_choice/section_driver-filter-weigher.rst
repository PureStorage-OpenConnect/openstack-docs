Theory of Operation: Driver Filter and Weigher for Scheduler
============================================================

Overview
--------

Cinder provides the DriverFilter and GoodnessWeigher to exercise
more fine grained control when choosing a volume backend based
on backend specific properties. It is possible to customize
the backend definition to schedule the creation of Cinder volumes
on specific backends, based on the volume properties and the
backend specific properties. Refer to the
":ref:`Configuration<driver-filter-config>`"
section to take a look at how this would work.

Setup
-----

To enable the driver filter, set the ``scheduler_default_filters``
option in the ``[DEFAULT]`` section of the ``cinder.conf`` file
to include DriverFilter.

To enable the goodness filter as a weigher, set the
``scheduler_default_weighers`` option in the ``[DEFAULT]`` section
of the ``cinder.conf`` file to ``GoodnessWeigher`` or add it to
the list if other weighers are already present.

Example ``cinder.conf`` configuration file:

.. code-block:: ini

   [DEFAULT]
   scheduler_default_filters = DriverFilter,AvailabilityFilter,CapabilityFilter,CapacityFilter
   scheduler_default_weighers = GoodnessWeigher

You can choose to use the DriverFilter without the GoodnessWeigher
or vice-versa. The filter and weigher working together, however,
create the most benefits when helping the scheduler choose an
ideal back end.

.. important::

   The GoodnessWeigher can be used along with CapacityWeigher
   and others, but must be used with caution as it might
   obfuscate the CapacityWeigher.

Refer to
`Upstream Driver Filter
Weighing <https://docs.openstack.org/cinder/latest/admin/blockstorage-driver-filter-weighing.html>`__
which contains a more detailed explanation on how to use the driver
filter and goodness weigher to customize the scheduling mechanism.

There exist three property sets that can be referenced in the
``filter_funtion`` and ``goodness_function`` definitions:

- **Host stats for a backend**: These refer to the parameters
  that are specific for the host containing a defined
  backend. This would be analogous to a FlashArray
  system. They can be invoked as ``stats.<property>``.
  For example: ``stats.allocated_capacity_gb``.
  ":ref:`Table 7.10<table-7.10>`" lists the
  host stats that can be used for FlashArray systems.

.. _table-7.10:

+----------------------------+-----------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Property                   | Type      | Description                                                                                                                                                |
+============================+===========+============================================================================================================================================================+
| ``host``                   | String    | The name of the host.                                                                                                                                      |
+----------------------------+-----------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``volume_backend_name``    | String    | Volume backend name as defined in ``cinder.conf``                                                                                                          |
+----------------------------+-----------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``vendor_name``            | String    | The name of the vendor. For FlashArray this is ``Pure Storage``                                                                                            |
+----------------------------+-----------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``driver_version``         | String    | The Cinder driver version.                                                                                                                                 |
+----------------------------+-----------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``storage_protocol``       | String    | The storage protocol supported. For FlashArray this is either ``iSCSI`` or ``FC``.                                                                         |
+----------------------------+-----------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``multiattach_support``    | Boolean   | Boolean signifying whether volume multiattach is supported. This is reported as ``True`` for FlashArray.                                                   |
+----------------------------+-----------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``QoS_support``            | Boolean   | Boolean signifying whether QoS is supported. This is reported as ``True`` for FlashArray.                                                                  |
+----------------------------+-----------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``total_capacity_gb``      | Float     | The total capacity of each pool in GB.                                                                                                                     |
+----------------------------+-----------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``allocated_capacity_gb``  | Float     | The capacity that has been allocated for Cinder volumes on the cluster. This value is reported in GB.                                                      |
+----------------------------+-----------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``free_capacity_gb``       | Float     | The amount of free capacity of each pool in GB.                                                                                                            |
+----------------------------+-----------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``reserved_percentage``    | Float     | The reserved percentage for each pool. This specifies how much space is to be reduced from total_capacity when performing over subscription calculations.  |
+----------------------------+-----------+------------------------------------------------------------------------------------------------------------------------------------------------------------+

Table 7.10 Host statistics

- **Requested volume properties**: These statistics are used
  to control scheduling based on the specifications
  of the volume requested during creation. These parameters
  can be referenced as ``volume.<property>``. For example,
  the size of the requested volume is returned by ``volume.size``.
  ":ref:`Table 7.11<table-7.11>`" contains a list of statistics
  that can be queried from a volume request.

.. _table-7.11:

+-----------------------------------------+------------------------------------------------------------------------------------------+
| Property                                | Description                                                                              |
+=========================================+==========================================================================================+
| ``size``                                | The size of the volume requested.                                                        |
+-----------------------------------------+------------------------------------------------------------------------------------------+
| ``volume_type_id``                      | The UUID of the volume type.                                                             |
+-----------------------------------------+------------------------------------------------------------------------------------------+
| ``display_name``                        | Name of the volume.                                                                      |
+-----------------------------------------+------------------------------------------------------------------------------------------+
| ``volume_metadata``                     | Metadata associated with the volume.                                                     |
+-----------------------------------------+------------------------------------------------------------------------------------------+
| ``user_id``                             | User ID of the user that creates the volume.                                             |
+-----------------------------------------+------------------------------------------------------------------------------------------+
| ``display_description``                 | Display description for the volume.                                                      |
+-----------------------------------------+------------------------------------------------------------------------------------------+
| ``source_volid``                        | ID of the source volume, if the volume is cloned.                                        |
+-----------------------------------------+------------------------------------------------------------------------------------------+
| ``reservations``                        | Any reservation the volume has.                                                          |
+-----------------------------------------+------------------------------------------------------------------------------------------+
| ``attach_status``                       | The attach status for the volume.                                                        |
+-----------------------------------------+------------------------------------------------------------------------------------------+
| ``id``                                  | The volume's ID.                                                                         |
+-----------------------------------------+------------------------------------------------------------------------------------------+
| ``replication_status``                  | The volume's replication status.                                                         |
+-----------------------------------------+------------------------------------------------------------------------------------------+
| ``snapshot_id``                         | The volume's snapshot ID.                                                                |
+-----------------------------------------+------------------------------------------------------------------------------------------+
| ``encryption_key_id``                   | The volume's encryption key ID.                                                          |
+-----------------------------------------+------------------------------------------------------------------------------------------+
| ``volume_admin_metadata``               | Any admin metadata for this volume.                                                      |
+-----------------------------------------+------------------------------------------------------------------------------------------+
| ``source_replicaid``                    | The source replication ID.                                                               |
+-----------------------------------------+------------------------------------------------------------------------------------------+
| ``consistencygroup_id``                 | The consistency group ID.                                                                |
+-----------------------------------------+------------------------------------------------------------------------------------------+
| ``metadata``                            | General metadata.                                                                        |
+-----------------------------------------+------------------------------------------------------------------------------------------+

Table 7.11 Volume properties available for Filter and Goodness functions

.. important::

   The most commonly used ``volume.<property>`` is ``volume.size``. This enables
   admins to schedule volume placement based on the size of the volume that is
   requested.

- **Backend specific capabilities**: The following table
  contains a list of capabilities reported by the FlashArray Cinder driver.

.. _table-7.12:

+-----------------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------+
| Property                          | Type      | Description                                                                                                              |
+===================================+===========+==========================================================================================================================+
| ``total_capacity_gb``             | String    | Total amount of space (in GiB) available on the array.                                                                   |
+-----------------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------+
| ``free_capacity_gb``              | String    | Free capacity (in GiB) on the array.                                                                                     |
+-----------------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------+
| ``provisioned_capacity``          | String    | Total amount of provisioned space (in GiB) on the array.                                                                 |
+-----------------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------+
| ``total_volumes``                 | String    | Total count of volumes provisioned on the array, including volumes pending eradication.                                  |
+-----------------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------+
| ``total_dnapshots``               | String    | Total count of snapshots provisioned on the array, including snapshots pending eradication.                              |
+-----------------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------+
| ``total-hosts``                   | String    | Total count of hosts on the array.                                                                                       |
+-----------------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------+
| ``total_pgroups``                 | String    | Total count of protection groups on the array.                                                                           |
+-----------------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------+
| ``writes_per_sec``                | String    | Total number of write operations per second currently being processed on the array.                                      |
+-----------------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------+
| ``reads_per_sec``                 | String    | Total number of read operations per second currently being processed on the array.                                       |
+-----------------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------+
| ``inputs_per_sec``                | String    | Total input (in bytes) per second for the array.                                                                         |
+-----------------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------+
| ``output_per_sec``                | String    | Total output (in bytes) per second for the array.                                                                        |
+-----------------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------+
| ``usec_per_read_op``              | String    | Current latency per read operation for the array.                                                                        |
+-----------------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------+
| ``usec_per_write_op``             | String    | Current latency per write operation for the array.                                                                       |
+-----------------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------+
| ``queue_depth``                   | String    | Current queue depth for the array - DEPRECATED (to be removed in 2026.1)                                                 |
+-----------------------------------+-----------+--------------------------------------------------------------------------------------------------------------------------+

Table 7.12 Backend capabilities reported by FlashArray Cinder drivers

Configuration
-------------

To utilize the driver filter and goodness weigher, update the
``scheduler_default_filters`` and ``scheduler_default_weighers``
options in ``cinder.conf``. The required ``filter_function``
and ``goodness_function`` are defined on a per-backend basis
as shown below.

.. _driver-filter-config:

**Example1: Using Goodness Weighter**

.. code-block:: ini

   [default]
   .
   .
   scheduler_default_filters = DriverFilter,AvailabilityFilter,CapabilityFilter,CapacityFilter
   scheduler_default_weighers = GoodnessWeigher
   enabled_backends = pure,pure-2
   .
   .
   [pure]
   volume_driver = cinder.volume.drivers.pure.PureISCSIDriver
   san_ip = 192.168.1.32
   pure_api_token = f29643cf-bf70-a1c5-222a-a3015f86d7ea
   goodness_function = "100 * (1 / max(capabilities.usec_per_write_op, 1))"

   [pure-2]
   volume_driver = cinder.volume.drivers.pure.PureISCSIDriver
   san_ip = 192.168.1.32
   pure_api_token = f29643cf-bf70-a1c5-222a-a3015f86d7ea
   goodness_function = "100 * (1 / max(capabilities.usec_per_write_op, 1))"

In this example, the ``goodness_function`` is set for the available
backends. For every volume request, the goodness function is
calculated and uses the array with the lowest write latency.

**Example3: Using Driver Filter**

.. code-block:: ini

   [default]
   .
   .
   scheduler_default_filters = DriverFilter,AvailabilityFilter,CapabilityFilter,CapacityFilter
   scheduler_default_weighers = GoodnessWeigher
   enabled_backends = pure,pure-2
   .
   .
   [pure]
   volume_driver = cinder.volume.drivers.pure.PureISCSIDriver
   san_ip = 192.168.1.32
   pure_api_token = f29643cf-bf70-a1c5-222a-a3015f86d7ea
   filter_function = "capabilities.total_volumes < 500"

   [pure-2]
   volume_driver = cinder.volume.drivers.pure.PureISCSIDriver
   san_ip = 192.168.1.32
   pure_api_token = f29643cf-bf70-a1c5-222a-a3015f86d7eA
   filter_function = "capabilities.total_volumes < 500"

This example shows how the ``filter_function`` is set for the
available backends. This example prevents creating a new volume on an array
that already has 500 volumes.
