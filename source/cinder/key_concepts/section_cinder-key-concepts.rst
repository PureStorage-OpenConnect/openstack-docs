.. _cinder-key-concepts:

Key Concepts
============

Volume
------

A Cinder volume is the fundamental resource unit allocated by the Block
Storage service. It represents an allocation of persistent, readable,
and writable block storage that could be utilized as the root disk for a
compute instance, or as secondary storage that could be attached and/or
detached from a compute instance. The underlying connection between the
consumer of the volume and the Cinder service providing the volume can
be achieved with the iSCSI, NFS, NVMe or Fibre Channel storage protocols
(dependent on the support of the Cinder driver deployed).

Cinder volumes can be identified uniquely through a UUID assigned by the
Cinder service at the time of volume creation. A Cinder volume may also
be optionally referred to by a human-readable name, though this string
is not guaranteed to be unique within a single tenant or deployment of
Cinder.

The actual blocks provisioned in support of a Cinder volume reside on a
single Cinder backend. Starting in the Havana release, a Cinder volume
can be migrated from one storage backend to another within a deployment
of the Cinder service; refer to the section called ":ref:`cinder-cli`"
for an example of volume migration.

The ``cinder manage`` command allows importing existing storage objects
that are not managed by Cinder into new Cinder volumes. The operation
will attempt to locate an object within a specified Cinder backend and
create the necessary metadata within the Cinder database to allow it to
be managed like any other Cinder volume. The operation will also rename
the volume to a name appropriate to the particular Cinder driver in use.
The imported storage object could be a file, LUN, or a volume depending
on the protocol (iSCSI/FC/NVMe/NFS). This feature is
useful in migration scenarios where virtual machines or other data need
to be managed by Cinder; refer to the section called
":ref:`cinder-manage`" for an example of the ``cinder manage`` command.

The ``cinder unmanage`` command allows Cinder to cease management of a
particular Cinder volume. All data stored in the Cinder database related
to the volume is removed, but the volume's backing file, LUN, or
appropriate storage object is not deleted. This allows the volume to be
transferred to another environment for other use cases; refer to the
section called ":ref:`cinder-unmanage`" for an example of the
``cinder unmanage`` command.

Snapshot
--------

A Cinder snapshot is a point-in-time, read-only copy of a Cinder volume.
Snapshots can be created from an existing Cinder volume that is
operational and either attached to an instance or in a detached state. A
Cinder snapshot can serve as the content source for a new Cinder volume
when the Cinder volume is created with the *create from snapshot* option
specified or can be used to revert a volume to the most recent snapshot
using the *revert to snapshot* feature (as of the Pike release).

Backend
-------

A Cinder backend is the configuration object that represents a single
provider of block storage upon which provisioning requests may be
fulfilled. A Cinder backend communicates with the storage system through
a Cinder driver. Cinder supports multiple backends to be simultaneously
configured and managed (even with the same Cinder driver) as of the
Grizzly release.

Driver
------

A Cinder driver is a particular implementation of a Cinder backend that
maps the abstract APIs and primitives of Cinder to appropriate
constructs within the particular storage solution underpinning the
Cinder backend.

.. caution::

   The use of the term "driver" often creates confusion given common
   understanding of the behavior of “device drivers” in operating
   systems. The term can connote software that provides a data I/O
   path. In the case of Cinder driver implementations, the software
   provides provisioning and other manipulation of storage devices but
   does not lay in the path of data I/O. For this reason, the term
   "driver" is often used interchangeably with the alternative (and
   perhaps more appropriate) term “provider”.

Volume Type
-----------

A Cinder volume type is an abstract collection of criteria used to
characterize Cinder volumes. They are most commonly used to create a
hierarchy of functional capabilities that represent a tiered level of
storage services; for example, a cloud administrator might define a
``premium`` volume type that indicates a greater level of performance
than a ``basic`` volume type, which would represent a best-effort level
of performance.

The collection of criteria is specified as a list of key/value pairs,
which are inspected by the Cinder scheduler when determining which
Cinder backend(s) are able to fulfill a provisioning request. Individual
Cinder drivers (and subsequently Cinder backends) may advertise
arbitrary key/value pairs (also referred to as capabilities) to the
Cinder scheduler, which are then compared against volume type
definitions when determining which backend will fulfill a provisioning
request.

Extra Spec
----------

An extra spec is a key/value pair, expressed in the style of
``key=value``. Extra specs are associated with Cinder volume types, so
that when users request volumes of a particular volume type, the volumes
are created on storage backends that meet the specified criteria.

.. note::

   Pure Storage drivers support multi-attachment of volumes for iSCSI, FC
   and NVMe protocols from the Stein release. This enables attaching a
   volume to multiple servers simultaneously and can be configured
   by creating an extra-spec ``multiattach="<is> True`` for the associated
   Cinder volume type.


Quality of Service
------------------

The Cinder Quality of Service (QoS) support for volumes can be enforced
either at the hypervisor or at the storage subsystem (``backend``), or
both.

Within the FlashArray each volume may be configured with
maximum IOPS and bandwidth values that are strictly
enforced within the system.

QoS support for the FlashArray drivers includes the ability to set the
following capabilities in the OpenStack Block Storage API
``cinder.api.contrib.qos_specs_manage`` qos specs extension module:

.. _table-7.1:

+-----------------+-------------------------------------------------------------------------------------+
| Option          | Description                                                                         |
+=================+=====================================================================================+
| maxBWS          | The maximum bandwidth for this volume in MB/s. Limits: 1 - 524288 (512Gbs).        |
+-----------------+-------------------------------------------------------------------------------------+
| maxIOPS         | The maximum number of IOPS allowed for this volume. Limits: 100 - 100 million       |
+-----------------+-------------------------------------------------------------------------------------+

Table 7.1. FlashArray QoS Options

.. note::
   The FlashArray driver utilizes volume-types for QoS settings and
   allows dynamic changes to QoS.

Generic Volume Groups
---------------------

With the Newton release of OpenStack, Pure Storage supports Generic Volume
Groups in the FlashArray iSCSI/Fibre Channel drivers.
Existing consistency group operations will be migrated
to use generic volume group operations in future releases. The existing
Consistency Group construct cannot be extended easily to serve
purposes such as consistent group snapshots across multiple
volumes. A generic volume group makes it possible to group volumes used
in the same application and these volumes do not have to support
consistent group snapshot. It provides a means of managing volumes and
grouping them based on a common factor. Additional information about
volume groups and the proposed migration can be found at
`generic-volume-groups <https://docs.openstack.org/cinder/latest/admin/blockstorage-groups.html>`__

.. note::
   Only Block Storage V3 API supports groups. The minimum version for
   group operations supported by the FlashArray drivers is 3.14. The API
   version can be specified with the following CLI flag
   ``--os-volume-api-version 3.14``

Consistency Groups
------------------

With the Mitaka release of OpenStack, Pure Storage supports Cinder Consistency
Groups with the FlashArray iSCSI/Fibre Channel drivers.
Consistency group support allows snapshots of multiple volumes
in the same consistency group to be taken at the same point-in-time to
ensure data consistency. To illustrate the usefulness of consistency
groups, consider a bank account database where a transaction log is
written to Cinder volume V1 and the account table itself is written to
Cinder volume V2. Suppose that $100 is to be transferred from account A
to account B via the following sequence of writes:

1. Log start of transaction.

2. Log remove $100 from account A.

3. Log add $100 to account B.

4. Log commit transaction.

5. Update table A to reflect -$100.

6. Update table B to reflect +$100.

Writes 1-4 go to Cinder volume V1 whereas writes 5-6 go to Cinder volume
V2. To see that we need to keep write order fidelity in both snapshots
of V1 and V2, suppose a snapshot is in progress during writes 1-6, and
suppose that the snapshot completes at a point where writes 1-3 and 5
have completed, but not 4 and 6. Because write 4 (log of commit
transaction) did not complete, the transaction will be discarded. But
write 5 has completed anyways, so a restore from snapshot of the
secondary will result in a corrupt account database, one where account A
has been debited $100 without account B getting the corresponding
credit.

Before using consistency groups, you must change policies for the
consistency group APIs in the ``/etc/cinder/policy.json`` file. By
default, the consistency group APIs are disabled. Enable them before
running consistency group operations. Here are existing policy entries
for consistency groups::

    "consistencygroup:create": "group:nobody",
    "consistencygroup:delete": "group:nobody",
    "consistencygroup:update": "group:nobody",
    "consistencygroup:get": "group:nobody",
    "consistencygroup:get_all": "group:nobody",
    "consistencygroup:create_cgsnapshot" : "group:nobody",
    "consistencygroup:delete_cgsnapshot": "group:nobody",
    "consistencygroup:get_cgsnapshot": "group:nobody",
    "consistencygroup:get_all_cgsnapshots": "group:nobody",

Remove ``group:nobody`` to enable these APIs::

    "consistencygroup:create": "",
    "consistencygroup:delete": "",
    "consistencygroup:update": "",
    "consistencygroup:get": "",
    "consistencygroup:get_all": "",
    "consistencygroup:create_cgsnapshot" : "",
    "consistencygroup:delete_cgsnapshot": "",
    "consistencygroup:get_cgsnapshot": "",
    "consistencygroup:get_all_cgsnapshots": "",

Remember to restart the Block Storage API service after changing
policies.

.. note::
   Consistency group operations support has been deprecated in
   Block Storage V3 API. Only Block Storage V2 API supports consistency
   groups. Future releases will involve a migration of existing
   consistency group operations to use generic volume group operations.

Disaster Recovery
-----------------

In the Mitaka release of OpenStack, Pure Storage's Cinder driver for
FlashArray was updated to match Cinder's v2.1 spec
for replication. This makes it possible to replicate an entire backend,
and allow all replicated volumes across different pools to fail over
together. Intended to be a disaster recovery mechanism, it provides a
way to configure one or more disaster recovery partner storage systems
for your Cinder backend. For more details on the configuration and
failover process, refer to `Implementing Cinder Replication with
Pure Storage <https://support.purestorage.com/Solutions/OpenStack/z_Legacy_OpenStack_Reference/OpenStack%C2%AE_Mitaka%3A_Implementing_Cinder_Replication_with_Pure_Storage>`__

Revert to Snapshot
------------------

As of Victoria release the FlashArray driver supports the revert to snapshot feature.
This feature can be used to overwrite the current state and data of a volume to the most
recent snapshot taken. The volume can not be reverted if it was extended after
taking the snapshot.

NVMe Support
------------

As of the Zed release the FlashArray driver supports NVMe as a transport protocol,
with the initial release of this driver only supporting the RoCE/RDMA layer.
