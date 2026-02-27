.. _over-subscription:

Theory of Operation: Over-Subscription and Thin-Provisioning
============================================================

Overview
--------

With a thick-provisioned Cinder volume, an amount of space is
reserved from the backend storage system equal to the size of the
requested volume. Because users typically do not actually consume all
the space in the Cinder volume, overall storage efficiency is reduced.

With a thin-provisioned Cinder volume, space is only carved from the
backend storage system as required for actual usage.

Thin-provisioning allows for capacity over-subscription. In other words,
more storage space may be allocated than is available on the storage
controller.

As example, in a 1TB storage pool, if four 250GB thick-provisioned volumes
are created, it would be necessary to add more storage capacity to the
pool in order to create another Cinder volume even if the Cinder volumes
were to remain empty.

::

    Storage Pool: Thick provisioned
    Storage Pool capacity = 1TB
    Cinder volume One:   250GB allocated
    Cinder volume Two:   250GB allocated
    Cinder volume Three: 250GB allocated
    Cinder volume Four:  250GB allocated
    Storage Pool space consumed = 1TB

Thin-provisioning with over-subscription allows flexibility in capacity
planning and reduces the likelihood of wasted storage capacity.

::

    Storage Pool: Thin provisioned
    Storage Pool capacity = 1TB
    Cinder volume One:  250GB allocated
    Cinder volume Two:  250GB allocated
    Cinder volume Three 250GB allocated
    Cinder volume Four: 250GB allocated
    Cinder volume Five: 250GB allocated
    Storage Pool space consumed = ~0GB

.. note::

   Thin provisioning helps maximize storage utilization. However, if
   aggregates are over committed through thin provisioning, usage must
   be monitored, and capacity must be increased as usage nears
   predefined thresholds.

The Everpure FlashArray driver conforms to the standard
Cinder scheduler-based over-subscription framework
in which the ``max_over_subscription_ratio`` and ``reserved_percentage``
configuration options are used to control the degree of
over-subscription allowed in the relevant storage pool. Note that the
Cinder scheduler only allows over-subscription of a storage pool if the
pool reports the ``thin_provisioning_support`` capability, which the
FlashArray does.

Details
-------

Refer to the following snippet in exploring further:

::

    $  cinder get-pools --detail
    +-----------------------------+-------------------------+
    | Property                    | Value                   |                                                                                       |
    +-----------------------------+-------------------------+
    ....
    | free_capacity_gb            | 6363.92                 |
    | max_over_subscription_ratio | 33.0695                 |
    | reserved_percentage         | 0                       |
    | total_capacity_gb           | 6521.73                 |
    ....
    +-----------------------------+-------------------------+

The attribute ``max_over_subscription_ratio`` is a multiplier
that controls how much beyond the reported storage pool
capacity may be allocated for additional Cinder volumes. This number
is obtained directly from the FlashArrays data reduction rate when
``pure_automatic_max_oversubscription_ratio`` is set to ``True``, which
is the default.

In the example above, the FlashArray has a capacity of 6521.73GB.
A ``reserved_percentage`` of 0% will be applied against this 6521.73GB
``total_capacity_gb`` value.

::

      reserved_percentage   = 0
      max_over_subscription_ratio   =  33.0695
      total_capacity_gb   = 6521.73GB

The following derives the maximum amount of space that may be
allocated to Cinder volumes.

::

    ( max_over_subscription_ratio * ( total_capacity_gb - ( total_capacity_gb * ( reserved_percentage / 100  ) ) ) )
    ( 33.0695 * ( 6521.73 - ( 6521.73 * (0 / 100 ) ) ) ) = 215,670.35 GB

Every sixty seconds, the total and free capacity is reported
to the Cinder Scheduler. Between the sixty second updates,
the Cinder Scheduler assumes a pessimistic view of free space.
The allocated capacity of each newly created Cinder volume
is subtracted from the free space value returned previously
by the Cinder volume Controller.

At the time of Cinder volume creation, the requested Cinder volume
size must be less than or equal to the amount of free space known by the
Cinder scheduler.

The above snippet reports the following free space at the reporting interval:

::

    free_capacity_gb =  6363.92GB

Consider what happens in the following Cinder volume creation scenario
where four thin volume creation requests come in back to back within the
reporting interval:

::

   request 1: 3000GB (success: free space goes from 6363.92GB to 3363.92GB)
   request 2: 3000GB  (success: free space drops from 3363.92GB to 363.92GB)
   request 3: 500GB  (failure: insufficient free space)
   Space Update Occurs
   request 4: 300GB  (success: free space goes from 363.92GB to 6258.92GB)



FlashArray Thin-Provisioning and Over-Provisioning
--------------------------------------------------

Thin Provisioning is enabled by default on FlashArray backends and cannot be disabled.

The only ``cinder.conf`` configuration setting for the FlashArray driver is:

``pure_automatic_max_oversubscription_ratio``: This setting controls whether the driver
automatically calculates the oversubscription ration as total provisioned / actual used.

When set to **True**, he driver ignores the  ``max_over_subscription_ratio`` value.

When set to **False**, the driver uses the value set by the configuration option
max_over_subscription_ratio, which sets a hard limit on oversubscription.

This option defaults to **True**.

.. note::

  The pure_automatic_max_oversubscription_ratio is recommended for most
  use. There are a couple limited scenarios in which to consider setting this parameter to False.
  One scenario is in a large cloud environment. The scheduler could report thinly-provisioned
  arrays as having thousands of terabytes of free space. Later, provisioning a large amount of
  storage in a short time on such an array could be problematic. The other scenario is if the
  parameter is incompatible with an unusual data set and unusual workload.

::

    FlashArray Backend
    +===========================================================+====================+
    | Config Option: pure_automatic_max_oversubscription_ratio  |   Default: True    |
    +-----------------------------------------------------------+--------------------+
    | FlashArray Volume Setting: thin_provisioning_support      |     '<is> True'    |
    +-----------------------------------------------------------+--------------------+
    | Config Option: max_over_subscription_ratio                |        > 1.0       |
    +-----------------------------------------------------------+--------------------+
