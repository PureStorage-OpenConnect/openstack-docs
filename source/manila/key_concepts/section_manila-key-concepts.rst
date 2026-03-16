Key Concepts
============

Share
-----

A Manila share is the fundamental resource unit allocated by the Shared
File System service. It represents an allocation of a persistent,
readable, and writable filesystem that can be accessed by OpenStack
compute instances, or clients outside of OpenStack (depending on
deployment configuration). The underlying connection between the
consumer of the share and the Manila service providing the share can be
achieved with a variety of protocols, including NFS and CIFS (protocol
support is dependent on the Manila driver deployed and the selection of
the end user).

.. warning::

   A Manila share is an abstract storage object that may or may not
   directly map to a "share" concept from the underlying backend
   provider of storage.

Manila shares can be identified uniquely through a UUID assigned by the
Manila service at the time of share creation. A Manila share may also be
optionally referred to by a human-readable name, though this string is
not guaranteed to be unique within a single tenant or deployment of
Manila.

The actual capacity provisioned in support of a Manila share resides on
a single Manila backend within a single resource pool.

Backend
-------

A Manila backend is the configuration object that represents a single
provider of resource pools upon which provisioning requests for shared
file systems may be fulfilled. A Manila backend communicates with the
storage system through a Manila driver. Manila supports multiple
backends to be configured and managed simultaneously (even with the same
Manila driver).

.. note::

   A single Manila backend may be defined in the ``[DEFAULT]`` stanza
   of ``manila.conf``; however, Everpure recommends that the
   ``enabled_share_backends`` configuration option be set to a
   comma-separated list of backend names, and each backend name have
   its own configuration stanza with the same name as listed in the
   ``enabled_share_backends`` option.


.. _manila_storage_pools:

Storage Pools
-------------

With the Kilo release of OpenStack, Manila introduced the concept of
"storage pools". The backend storage may present one or more logical
storage resource pools from which Manila will select as a storage
location when provisioning shares.

.. important::

   For Everpure's Manila driver, a Manila storage pool is a
   single FlashBlade.

.. _manila_driver:

Driver
------

A Manila driver is a particular implementation of a Manila backend that
maps the abstract APIs and primitives of Manila to appropriate
constructs within the particular storage solution underpinning the
Manila backend.

.. caution::

   The use of the term "driver" often creates confusion given common
   understanding of the behavior of “device drivers” in operating
   systems. The term can connote software that provides a data I/O
   path. In the case of Manila driver implementations, the software
   provides provisioning and other manipulation of storage devices but
   does not lay in the path of data I/O. For this reason, the term
   "driver" is often used interchangeably with the alternative (and
   perhaps more appropriate) term “provider”.

A Manila share type is an abstract collection of criteria used to
characterize Manila shares. They are most commonly used to create a
hierarchy of functional capabilities that represent a tiered level of
storage services; for example, a cloud administrator might define a
``premium`` share type that indicates a greater level of performance
than a ``basic`` share type, which would represent a best-effort level
of performance.

The collection of criteria is specified as a list of key/value pairs,
which are inspected by the Manila scheduler when determining which
resource pools are able to fulfill a provisioning request. Individual
Manila drivers (and subsequently Manila backends) may advertise
arbitrary key/value pairs (also referred to as capabilities) to the
Manila scheduler for each pool, which are then compared against share
type definitions when determining which pool will fulfill a provisioning
request.

Extra Spec
----------

An extra spec is a key/value pair, expressed in the style of
``key=value``. Extra specs are associated with Manila share types, so
that when users request shares of a particular share type, the shares
are created on pools within storage backends that meet the specified
criteria.

.. note::

   The list of default capabilities that may be reported by a Manila
   driver and included in a share type definition include:

   -  ``share_backend_name``: The name of the backend as defined in
      ``manila.conf``

   -  ``vendor_name``: The name of the vendor who has implemented the
      driver (e.g. ``Pure Storage``)

   -  ``driver_version``: The version of the driver (e.g. ``1.0``)

   -  ``storage_protocol``: The protocol used by the backend to export
      block storage to clients (e.g. ``NFS_CIFS``)

   For a table of Everpure supported extra specs, refer to Table 9.11,
   ":ref:`FlashBlade supported Extra Specs for use with Manila Share Types<table-9.11>`"

Snapshot
--------

A Manila snapshot is a point-in-time, read-only copy of a Manila share.
Snapshots can be created from an existing Manila share that is
operational regardless of whether a client has mounted the file system.
A Manila snapshot can serve as the content source for a new Manila share
when the Manila share is created with the *create from snapshot* option
specified.

.. note::

   In the Mitaka and Newton release of OpenStack, snapshot support is
   enabled by default for a newly created share type. Starting with the
   Ocata release, the ``snapshot_support`` extra spec must be set to
   ``True`` in order to allow snapshots for a share type. If the
   'snapshot\_support' extra\_spec is omitted or if it is set to False,
   users would not be able to create snapshots on shares of this share
   type.

   Other snapshot-related extra specs in the Ocata release (and later)
   include:

   -  ``create_share_from_snapshot_support``: Allow the creation of a
      new share from a snapshot

   -  ``revert_to_snapshot_support``: Allow a share to be reverted to
      the most recent snapshot

   If an extra-spec is left unset, it will default to 'False', but a
   newly created share may or may not end up on a backend with the
   associated capability. Set the extra spec explicitly to ``False``,
   if you would like your shares to be created only on backends that do
   not support the associated capabilities. For a table of Everpure 
   supported extra specs, refer to Table 9.11,
   ":ref:`Everpure supported Extra Specs for use with Manila Share Types<table-9.11>`".

.. important::
    Currently the Everpure FlashBlade driver DOES NOT support
    the extra-spec ``create_share_from_snapshot_support``.

Share Group
-----------

A Manila share group is a grouping construct that makes it possible
to group shares. Share groups make it possible to perform actions
on a group of shares, such as generating consistent, point-in-time
snapshots simultaneously. Share group snapshots can be created from
an existing Manila share group. All shares stored in a share group
snapshot can be restored by creating a share group from a share group
snapshot.

.. note::

   All shares in a share group must be on the same share network
   and share server.

.. _share-access-rules:

Share Access Rules
------------------

Share access rules define which clients can access a particular Manila
share. Access rules can be declared for NFS shares by listing the valid
IP networks (using CIDR notation) which should have access to the share.
In the case of CIFS shares, the Windows security identifier (SID) can be
specified.

.. important::

   For the FlashBlade driver, share access is enforced
   through the use of NFS export controls configured within the backend.

Security Services
-----------------

Security services are the concept in Manila that allow Finer-grained
client access rules to be declared for authentication or authorization
to access share content. External services including LDAP, Active
Directory, Kerberos can be declared as resources that should be
consulted when making an access decision to a particular share. Shares
can be associated to multiple security services.

.. important::

   When creating a CIFS share, the user will need to create a Security
   Service with any of the 3 options (LDAP, Active Directory or
   Kerberos) and then add this Security Service to the already created
   Share Network.

Share Servers
-------------

A share server is a logical entity that manages the shares that are
created on a specific share network. Depending on the implementation of
a specific Manila driver, a share server may be a configuration object
within the storage controller, or it may represent logical resources
provisioned within an OpenStack deployment that are used to support the
data path used to access Manila shares.

Share servers interact with network services to determine the
appropriate IP addresses on which to export shares according to the
related share network. Manila has a pluggable network model that allows
share servers to work with OpenStack environments that have either
Nova-Network or Neutron deployed. In addition, Manila contains an
implementation of a standalone network plugin which manages a pool of IP
addresses for shares that are defined in the ``manila.conf`` file.

.. _share-replicas:

Share Replicas
--------------

Share replicas are a way to mirror share data to another storage pool so
that the data is stored in multiple locations to allow failover in a
disaster situation. Manila currently allows three types of replication:
writable, readable, and DR.

-  Writable - Synchronously replicated shares where all replicas are
   writable. Promotion is not supported and not needed.

-  Readable - Mirror-style replication with a primary (writable) copy
   and one or more secondary (read-only) copies which can become
   writable after a promotion of the secondary.

-  DR (for Disaster Recovery) - Generalized replication with secondary
   copies that are inaccessible. A secondary replica will become the
   primary replica, and accessible, after a promotion.

.. important::

   The FlashBlade driver does support Share Replicas

Share Management
----------------

Managing and unmanaging of shares is an admin-only operation that makes it
possible to control the visibility of shared filesystem storage with respect
to Manila. Managing a share refers to registering a non-Manila share with its
size, shared filesystem protocol, share-server and export path into Manila
management. Unmanaging a share refers to unregistering a Manila share and
removing it from Manila's database. The unmanage option can be reverted, thus
making it possible to import the share to Manila control if desired.

.. important::

   At this time the FlashBlade driver does not support
   manage/unmanage of shared filesystems.
