Theory of Operation & Deployment Choices
========================================

.. _disk-choices:

Root Disk Choices When Booting Nova Instances
---------------------------------------------

There are several choices for how the root disk should be created which
are presented to cloud users when booting Nova instances.

**Boot from image**

This option allows a user to specify an image from the Glance
repository to copy into an ephemeral disk.

**Boot from snapshot**

This option allows a user to specify an instance snapshot to use as
the root disk; the snapshot is copied into an ephemeral disk.

**Boot from volume**

This option allows a user to specify a Cinder volume (by name or
UUID) that should be directly attached to the instance as the root
disk; no copy is made into an ephemeral disk and any content stored
in the volume is persistent.

**Boot from image (create new volume)**

This option allows a user to specify an image from the Glance
repository to be copied into a persistent Cinder volume, which is
subsequently attached as the root disk for the instance.

**Boot from volume snapshot (create new volume)**

This option allows a user to specify a Cinder volume snapshot (by
name or UUID) that should be used as the root disk; the snapshot is
copied into a new, persistent Cinder volume which is subsequently
attached as the root disk for the instance.

.. tip::

   Leveraging the "boot from volume", “boot from image (creates a new
   volume)”, or "boot from volume snapshot (create new volume)" options
   in Nova normally results in volumes that are persistent beyond the
   life of a particular instance. However, you can select the “delete
   on terminate” option in combination with any of the aforementioned
   options to create an ephemeral volume while still leveraging the
   Glance Image Cache instance creation capabilities described in the section called
   ":ref:`gic-fa-iscsi-or-fc`". This can provide a significantly
   faster provisioning and boot sequence than the normal way that
   ephemeral disks are provisioned, where a copy of the disk image is
   made from Glance to local storage on the hypervisor node where the
   instance resides.

Instance Snapshots vs. Cinder Snapshots
---------------------------------------

Instance snapshots allow you to take a point in time snapshot of the
content of an instance's disk. Instance snapshots can subsequently be
used to create an image that can be stored in Glance which can be
referenced upon subsequent boot requests.

While Cinder snapshots also allow you to take a point-in-time snapshot
of the content of a disk, they are more flexible than instance
snapshots. For example, you can use a Cinder snapshot as the content
source for a new root disk for a new instance, or as a new auxiliary
persistent volume that can be attached to an existing or new instance.
For more information on Cinder snapshots, refer to the section called
":ref:`cinder-key-concepts`".

Instance Storage Options at the Hypervisor
------------------------------------------

The Nova configuration option ``instances_path`` specifies where
instances are stored on the hypervisor's disk. While this may normally
point to locally attached storage (which could be desirable from a
performance perspective), it prohibits the ability to support live
migration of instances between hypervisors. By specifying a directory
that is a mounted external storage volume (from a FlashArray), it is
possible to increase the storage capacity available for instance 
storage and to leverage the inherent deduplication capabilities of
similar instances using the global data reduction rates of the FlashArray.
This removes the architectural limitation of the number and capacity of
local storage in the Nova compute hypervisors.
