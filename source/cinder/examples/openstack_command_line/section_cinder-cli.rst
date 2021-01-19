.. _cinder-cli:

Cinder Command Line Interface (CLI)
===================================

Cinder Service Verification
---------------------------

In this section, we use the Cinder CLI to verify that the configuration
presented in the section called ":ref:`cinder-conf`"
has been properly initialized by Cinder.

::

    user@opstack:~/$ cinder service-list
    +------------------+----------------+------+---------+-------+----------------------------+-----------------+
    | Binary           | Host           | Zone | Status  | State | Updated_at                 | Disabled Reason |
    +------------------+----------------+------+---------+-------+----------------------------+-----------------+
    | cinder-scheduler | opstack        | nova | enabled | up    | 2021-01-15T21:43:51.000000 | -               |
    | cinder-volume    | opstack@pure   | nova | enabled | up    | 2021-01-15T21:43:54.000000 | -               |
    | cinder-volume    | opstack@pure-2 | nova | enabled | up    | 2021-01-15T21:43:54.000000 | -               |
    +------------------+----------------+------+---------+-------+----------------------------+-----------------+


-  ``opstack@pure`` is the backend defined by the configuration
   stanza ``[pure]``.

-  ``opstack@pure-2`` is the backend defined by the configuration
   stanza ``[pure-2]``.

.. _create-volume:

Creating and Defining Cinder Volume Types
-----------------------------------------

In this section, we create a variety of Cinder volume Types that
leverage different capabilities of the driver.

-  The ``gold`` type provisions Cinder volumes onto a specified FlashArray
   (in this example, that would be ``[pure]``.

-  The ``replicated`` type provisions Cinder volumes onto any backend that
   has replicated enabled .

::

    $ cinder type-create gold
    +--------------------------------------+------+-------------+-----------+
    | ID                                   | Name | Description | Is_Public |
    +--------------------------------------+------+-------------+-----------+
    | 79c91521-b667-40f9-a841-12ab53310a24 | gold | -           | True      |
    +--------------------------------------+------+-------------+-----------+

::

    $ cinder type-create replicated
    +--------------------------------------+------------+-------------+-----------+
    | ID                                   | Name       | Description | Is_Public |
    +--------------------------------------+------------+-------------+-----------+
    | c0b0f7e8-ef65-4d41-933f-128e37ecddc9 | replicated | -           | True      |
    +--------------------------------------+------------+-------------+-----------+

::

    $ cinder type-key gold set volume_backend_name=pure

::

    $ cinder type-key replicated set replication_enabled="<is> True"

::

    $ cinder extra-specs-list
    +--------------------------------------+-------------+-----------------------------------------+
    | ID                                   | Name        | extra_specs                             |
    +--------------------------------------+-------------+-----------------------------------------+
    | 112d1f1b-5b0c-4735-972a-c538123c16d0 | replicated  | {'replication_enabled': '<is> True'}    |
    | 40314332-50e4-4e0b-b928-708c8cc375d6 | __DEFAULT__ | {}                                      |
    | 79c91521-b667-40f9-a841-12ab53310a24 | gold        | {'volume_backend_name': 'pure-2'}       |
    +--------------------------------------+-------------+-----------------------------------------+

Creating Cinder Volumes with Volume Types
-----------------------------------------

In this section, we create volumes with no type, as well as each of the
previously defined volume types.

::

    $ cinder create --display-name myGold --volume-type gold 1
    +--------------------------------+--------------------------------------+
    |            Property            |                Value                 |
    +--------------------------------+--------------------------------------+
    |          attachments           |                  []                  |
    |       availability_zone        |                 nova                 |
    |            bootable            |                false                 |
    |           created_at           |      2014-05-20T17:23:57.000000      |
    |          description           |                 None                 |
    |           encrypted            |                False                 |
    |               id               | 3678281e-3924-4512-952a-5b89713fac4d |
    |            metadata            |                  {}                  |
    |              name              |                myGold                |
    |     os-vol-host-attr:host      |                 None                 |
    | os-vol-mig-status-attr:migstat |                 None                 |
    | os-vol-mig-status-attr:name_id |                 None                 |
    |  os-vol-tenant-attr:tenant_id  |   f42d5597fb084480a9626c2ca844db3c   |
    |              size              |                  1                   |
    |          snapshot_id           |                 None                 |
    |          source_volid          |                 None                 |
    |             status             |               creating               |
    |            user_id             |   a9ef3a9f935f4761861afb003986bdab   |
    |          volume_type           |                 gold                 |
    +--------------------------------+--------------------------------------+

::

    $ cinder create --display-name myReplicated --volume-type replicated 1
    +--------------------------------+--------------------------------------+
    |            Property            |                Value                 |
    +--------------------------------+--------------------------------------+
    |          attachments           |                  []                  |
    |       availability_zone        |                 nova                 |
    |            bootable            |                false                 |
    |           created_at           |      2014-05-20T18:01:02.000000      |
    |          description           |                 None                 |
    |           encrypted            |                False                 |
    |               id               | 12938589-3ca9-49a7-bcd7-003bbcd62895 |
    |            metadata            |                  {}                  |
    |              name              |             myReplicated             |
    |     os-vol-host-attr:host      |                 None                 |
    | os-vol-mig-status-attr:migstat |                 None                 |
    | os-vol-mig-status-attr:name_id |                 None                 |
    |  os-vol-tenant-attr:tenant_id  |   f42d5597fb084480a9626c2ca844db3c   |
    |              size              |                  1                   |
    |          snapshot_id           |                 None                 |
    |          source_volid          |                 None                 |
    |             status             |               creating               |
    |            user_id             |   a9ef3a9f935f4761861afb003986bdab   |
    |          volume_type           |              replicated              |
    +--------------------------------+--------------------------------------+

::

    $ cinder list
    +--------------------------------------+-----------+--------------+------+-------------+----------+-------------+
    |                  ID                  |   Status  | Name         | Size | Volume Type | Bootable | Attached to |
    +--------------------------------------+-----------+--------------+------+-------------+----------+-------------+
    | 3678281e-3924-4512-952a-5b89713fac4d | available | myGold       |  1   | gold        |  false   |             |
    | 93ef9627-ac75-46ae-820b-f722765d7828 | available | myReplicated |  1   | replicated  |  false   |             |
    +--------------------------------------+-----------+--------------+------+-------------+----------+-------------+

.. _cinder-manage:

Cinder Manage Usage
-------------------

In this section we import an FlashArray LUN by specifying it by
name or UUID.

::

    $ cinder get-pools
    +----------+-----------------------------------+
    | Property |              Value                |
    +----------+-----------------------------------+
    |   name   | opstack@puredriver-1#puredriver-1 |
    +----------+-----------------------------------+

::

    $ cinder --os-volume-api-version 3.8 manageable-list opstack@puredriver-1#puredriver-1
    +----------------------------------------------------------------+------+----------------+---------------------------------------------------------------------------+--------------------------------------+------------+
    | reference                                                      | size | safe_to_manage | reason_not_safe                                                           | cinder_id                            | extra_info |
    +----------------------------------------------------------------+------+----------------+---------------------------------------------------------------------------+--------------------------------------+------------+
    | {'name': 'volume-e898e997-1254-4c56-9136-239b1568fe0b-cinder'} | 1    | False          | Volume connected to host devstack-bbabda406f7846c6b0d9e1ec53761419-cinder | -                                    | -          |
    | {'name': 'volume-648bcd17-e36e-41b3-8087-391544e3b9ac-cinder'} | 1    | False          | Volume already managed                                                    | 648bcd17-e36e-41b3-8087-391544e3b9ac | -          |
    | {'name': 'volume-17eb768e-8758-44ff-afc1-45720c1b19f1-cinder'} | 1    | False          | Volume already managed                                                    | 17eb768e-8758-44ff-afc1-45720c1b19f1 | -          |
    | {'name': 'manage-me'}                                          | 2    | True           |                                                                           | -                                    | -          |
+----------------------------------------------------------------+------+----------------+---------------------------------------------------------------------------+--------------------------------------+------------+

::

    $ cinder manage --id-type source-name opstack@puredriver-1#puredriver-1 manage-me
    +--------------------------------+--------------------------------------+
    | Property                       | Value                                |
    +--------------------------------+--------------------------------------+
    | attachments                    | []                                   |
    | availability_zone              | nova                                 |
    | bootable                       | false                                |
    | consistencygroup_id            | None                                 |
    | created_at                     | 2021-01-19T22:09:52.000000           |
    | description                    | None                                 |
    | encrypted                      | False                                |
    | id                             | be126563-201a-4025-bf82-5338e4ececb2 |
    | metadata                       | {}                                   |
    | migration_status               | None                                 |
    | multiattach                    | False                                |
    | name                           | None                                 |
    | os-vol-host-attr:host          | opstack@puredriver-1#puredriver-1    |
    | os-vol-mig-status-attr:migstat | None                                 |
    | os-vol-mig-status-attr:name_id | None                                 |
    | os-vol-tenant-attr:tenant_id   | 45a06744d6fa44418eb2c261dae0ccf9     |
    | replication_status             | None                                 |
    | size                           | 0                                    |
    | snapshot_id                    | None                                 |
    | source_volid                   | None                                 |
    | status                         | creating                             |
    | updated_at                     | 2021-01-19T22:09:52.000000           |
    | user_id                        | c008a02d553a4f9595d8437da67996b4     |
    | volume_type                    | gold                                 |
    +--------------------------------+--------------------------------------+

::

    $ cinder list
    +--------------------------------------+----------------+------+------+-------------+----------+-------------+
    |                  ID                  |     Status     | Name | Size | Volume Type | Bootable | Attached to |
    +--------------------------------------+----------------+------+------+-------------+----------+-------------+
    | be126563-201a-4025-bf82-5338e4ececb2 |   available    | None |  2   | gold        |  false   |             |
    +--------------------------------------+----------------+------+------+-------------+----------+-------------+

.. _cinder-unmanage:

Cinder Unmanage Usage
---------------------

In this section we unmanage a Cinder volume by specifying its ID.

::

    $ cinder list
    +--------------------------------------+----------------+------+------+-------------+----------+-------------+
    |                  ID                  |     Status     | Name | Size | Volume Type | Bootable | Attached to |
    +--------------------------------------+----------------+------+------+-------------+----------+-------------+
    | 206a6731-f23b-419d-8131-8bccbbd83647 |   available    | None |  1   |     None    |  false   |             |
    | ad0262e0-bbe6-4b4d-8c36-ea6a361d777a |   available    | None |  1   |     None    |  false   |             |
    +--------------------------------------+----------------+------+------+-------------+----------+-------------+

::

    $ cinder unmanage 206a6731-f23b-419d-8131-8bccbbd83647

::

    $ cinder list
    +--------------------------------------+----------------+------+------+-------------+----------+-------------+
    |                  ID                  |     Status     | Name | Size | Volume Type | Bootable | Attached to |
    +--------------------------------------+----------------+------+------+-------------+----------+-------------+
    | ad0262e0-bbe6-4b4d-8c36-ea6a361d777a |   available    | None |  1   |     None    |  false   |             |
    +--------------------------------------+----------------+------+------+-------------+----------+-------------+

Applying Cinder QoS via the Command Line
----------------------------------------

In this section, we will configure a Cinder volume type, a Cinder QoS
spec, and lastly associate the QoS spec with the volume type.

::

    $ cinder type-create vol_type_qos_demo
    +--------------------------------------+-------------------+
    |                  ID                  |        Name       |
    +--------------------------------------+-------------------+
    | 7b060008-632c-412d-8fdc-a12351f7dfe4 | vol_type_qos_demo |
    +--------------------------------------+-------------------+

::

    $ cinder qos-create qos_demo maxIOPS=100
    +----------+--------------------------------------+
    | Property |                Value                 |
    +----------+--------------------------------------+
    | consumer |               back-end               |
    |    id    | db081cde-1a9a-41bd-a8a3-a0259db7409b |
    |   name   |               qos_demo               |
    |  specs   |         {u'maxIOPS': u'100'}         |
    +----------+--------------------------------------+

::

    $ cinder qos-associate db081cde-1a9a-41bd-a8a3-a0259db7409b 7b060008-632c-412d-8fdc-a12351f7dfe4

::

    $ cinder qos-list
    +--------------------------------------+----------+----------+----------------------+
    |                  ID                  |   Name   | Consumer |        specs         |
    +--------------------------------------+----------+----------+----------------------+
    | db081cde-1a9a-41bd-a8a3-a0259db7409b | qos_demo | back-end | {u'maxIOPS': u'100'} |
    +--------------------------------------+----------+----------+----------------------+

::

    $ cinder create 1 --volume-type vol_type_qos_demo
    +---------------------------------------+--------------------------------------+
    |                Property               |                Value                 |
    +---------------------------------------+--------------------------------------+
    |              attachments              |                  []                  |
    |           availability_zone           |                 nova                 |
    |                bootable               |                false                 |
    |          consistencygroup_id          |                 None                 |
    |               created_at              |      2015-04-22T13:39:50.000000      |
    |              description              |                 None                 |
    |               encrypted               |                False                 |
    |                   id                  | 66027b97-11d1-4399-b8c6-031ad8e38da0 |
    |                metadata               |                  {}                  |
    |              multiattach              |                False                 |
    |                  name                 |                 None                 |
    |         os-vol-host-attr:host         |                 None                 |
    |     os-vol-mig-status-attr:migstat    |                 None                 |
    |     os-vol-mig-status-attr:name_id    |                 None                 |
    |      os-vol-tenant-attr:tenant_id     |   3149a10c07bd42569bd5094b83aefdfa   |
    |   os-volume-replication:driver_data   |                 None                 |
    | os-volume-replication:extended_status |                 None                 |
    |           replication_status          |               disabled               |
    |                  size                 |                  1                   |
    |              snapshot_id              |                 None                 |
    |              source_volid             |                 None                 |
    |                 status                |               creating               |
    |                user_id                |   322aff449dac4503b7cab8f38440597e   |
    |              volume_type              |          vol_type_qos_demo           |
    +---------------------------------------+--------------------------------------+

After we associate the QoS spec with the volume type, we can use the
volume type just as we did in the section called
:ref:`“Creating and Defining Cinder volume Types”<create-volume>`.

Manipulating Cinder Consistency Groups via the Command Line
-----------------------------------------------------------

.. note::

   Support for Consistency groups has been deprecated in Block Storage V3
   API. Only Block Storage V2 API supports consistency groups. Future
   releases will involve a migration of existing consistency group operations
   to use generic volume group operations.

In this section, we will configure a Cinder volume type, associate the
volume type with a backend capable of supporting consistency groups,
create a Cinder consistency group, create a Cinder volume within the
consistency group, take a snapshot of the consistency group, and then
finally create a second consistency group from the snapshot of the first
consistency group.

::

    $ cinder type-create consistency-group-support
    +--------------------------------------+---------------------------+-------------+-----------+
    | ID                                   | Name                      | Description | Is_Public |
    +--------------------------------------+---------------------------+-------------+-----------+
    | e9a652da-8cc9-4130-866b-4c7bd25b2cb2 | consistency-group-support | -           | True      |
    +--------------------------------------+---------------------------+-------------+-----------+

::

    $ cinder type-key consistency-group-support set volume_backend_name=BACKEND_WITH_CG_SUPPORT

::

    $ cinder consisgroup-create consistency-group-support --name cg1
    +-------------------+------------------------------------------+
    | Property          | Value                                    |
    +-------------------+------------------------------------------+
    | availability_zone | nova                                     |
    | created_at        | 2021-01-19T22:20:27.000000               |
    | description       | None                                     |
    | id                | 1e875dfe-e213-43c6-a365-12610b92341b     |
    | name              | cg1                                      |
    | status            | creating                                 |
    | volume_types      | ['e9a652da-8cc9-4130-866b-4c7bd25b2cb2'] |
    +-------------------+------------------------------------------+

::

    $ cinder create --name vol-in-cg1 --consisgroup-id 1e875dfe-e213-43c6-a365-12610b92341b --volume-type consistency-group-support 1
    +---------------------------------------+-------------------------------------------+
    |                Property               |                   Value                   |
    +---------------------------------------+-------------------------------------------+
    |              attachments              |                     []                    |
    |           availability_zone           |                    nova                   |
    |                bootable               |                   false                   |
    |          consistencygroup_id          |   1e875dfe-e213-43c6-a365-12610b92341b    |
    |               created_at              |         2016-02-29T15:59:36.000000        |
    |              description              |                    None                   |
    |               encrypted               |                   False                   |
    |                   id                  |    959e5f9f-67b9-4011-bd60-5dad2ee43200   |
    |                metadata               |                     {}                    |
    |            migration_status           |                    None                   |
    |              multiattach              |                   False                   |
    |                  name                 |                 vol-in-cg1                |
    |         os-vol-host-attr:host         |                    None                   |
    |     os-vol-mig-status-attr:migstat    |                    None                   |
    |     os-vol-mig-status-attr:name_id    |                    None                   |
    |      os-vol-tenant-attr:tenant_id     |      b2b6110ec5c3411089e60e928aafbba6     |
    |   os-volume-replication:driver_data   |                    None                   |
    | os-volume-replication:extended_status |                    None                   |
    |           replication_status          |                  disabled                 |
    |                  size                 |                     1                     |
    |              snapshot_id              |                    None                   |
    |              source_volid             |                    None                   |
    |                 status                |                  creating                 |
    |               updated_at              |         2016-02-29T15:59:37.000000        |
    |                user_id                |      12364c2f57ee4d459ae535af100fdf63     |
    |              volume_type              |         consistency-group-support         |
    +---------------------------------------+-------------------------------------------+

::

    $ cinder cgsnapshot-create 2cc3d172-af05-421b-babd-01d4cd91078d --name snap-of-cg1
    +---------------------+--------------------------------------+
    |       Property      |                Value                 |
    +---------------------+--------------------------------------+
    | consistencygroup_id | 1e875dfe-e213-43c6-a365-12610b92341b |
    |      created_at     |      2016-02-29T16:01:30.000000      |
    |     description     |                 None                 |
    |          id         | cd3770e1-fa59-48a6-ba48-2f3581f2b03b |
    |         name        |             snap-of-cg1              |
    |        status       |               creating               |
    +---------------------+--------------------------------------+

::

    $ cinder consisgroup-create-from-src --name cg2 --cgsnapshot cd3770e1-fa59-48a6-ba48-2f3581f2b03b
    +----------+--------------------------------------+
    | Property |                Value                 |
    +----------+--------------------------------------+
    |    id    | f84529af-e639-477e-a6e7-53dd401ab909 |
    |   name   |                 cg2                  |
    +----------+--------------------------------------+

To delete a consistency group, first make sure that any snapshots of the
consistency group have first been deleted, and that any volumes in the
consistency group have been removed via an update command on the
consistency group.

::

    $ cinder consisgroup-update cg2 --remove-volumes ddb31a53-6550-410c-ba48-a0a912c8ae95

::

    $ cinder delete ddb31a53-6550-410c-ba48-a0a912c8ae95
    Request to delete volume ddb31a53-6550-410c-ba48-a0a912c8ae95 has been accepted.

::

    $ cinder consisgroup-delete cg2

::

    $ cinder cgsnapshot-delete snap-of-cg1

::

    $ cinder consisgroup-update cg1 --remove-volumes 959e5f9f-67b9-4011-bd60-5dad2ee43200

::

    $ cinder delete 959e5f9f-67b9-4011-bd60-5dad2ee43200
    Request to delete volume 959e5f9f-67b9-4011-bd60-5dad2ee43200 has been accepted.

::

    $ cinder consisgroup-delete cg1


Manipulating Cinder Groups via the Command Line
-----------------------------------------------------------
In this section, we will configure a Cinder volume type, associate the
volume type with a backend capable of supporting groups, create a Cinder
group type, create a Cinder group, create a Cinder volume within the group,
take a snapshot of the group, and then finally create a group from the
snapshot of the first group.

.. note::
   Currently only the Block Storage V3 API supports group operations. The
   minimum version for group operations supported by the FlashArray drivers is
   3.14. The API version can be specified with the following CLI flag
   ``--os-volume-api-version 3.14``. Optionally an environment variable can
   be set: ``export OS_VOLUME_API_VERSION=3.14``

.. note::
   The Cinder community plans to migrate existing consistency group operations
   to group operations in an upcoming release. Please review Cinder
   release notes for upgrade instructions prior to using group operations.

.. note::
   The FlashArray volume drivers support the consistent_group_snapshot_enabled
   group type. By default Cinder group snapshots take individual snapshots
   of each Cinder volume in the group. To enable consistency group snapshots set
   ``consistent_group_snapshot_enabled="<is> True"`` in the group type used.

::

    $ cinder type-create volume-support
    +--------------------------------------+----------------+-------------+-----------+
    | ID                                   | Name           | Description | Is_Public |
    +--------------------------------------+----------------+-------------+-----------+
    | 52c62136-4c87-4ec1-9e29-1132e975eab9 | volume-support | -           | True      |
    +--------------------------------------+----------------+-------------+-----------+

::

    $ cinder type-key volume-support set volume_backend_name=BACKEND_WITH_CG_SUPPORT

::

    $ cinder --os-volume-api-version 3.14 group-type-create group-support
    +--------------------------------------+---------------+-------------+
    | ID                                   | Name          | Description |
    +--------------------------------------+---------------+-------------+
    | bc910903-35d8-49cd-842e-77c77c1d52f5 | group-support | -           |
    +--------------------------------------+---------------+-------------+

::

    $ cinder --os-volume-api-version 3.14 group-type-key group-support set consistent_group_snapshot_enabled="<is> True"

::

    $ cinder --os-volume-api-version 3.14 group-create --name group1 group-support volume-support
    +-------------------+-------------------------------------------+
    | Property          | Value                                     |
    +-------------------+-------------------------------------------+
    | availability_zone | nova                                      |
    | created_at        | 2017-09-08T22:24:57.000000                |
    | description       | None                                      |
    | group_snapshot_id | None                                      |
    | group_type        | 5bf45d12-0ea3-4061-b6b9-287965edce41      |
    | id                | 68ea5b1d-0b09-44ae-ad9f-5e6d9672cc93      |
    | name              | group1                                    |
    | source_group_id   | None                                      |
    | status            | creating                                  |
    | volume_types      | [u'0ca68595-7218-4d44-a992-9f6db4b75143'] |
    +-------------------+-------------------------------------------+

::

    $ cinder --os-volume-api-version 3.14 create --name vol-in-group1 --group-id 68ea5b1d-0b09-44ae-ad9f-5e6d9672cc93 --volume-type volume-support 1
    +--------------------------------+--------------------------------------+
    | Property                       | Value                                |
    +--------------------------------+--------------------------------------+
    | attachments                    | []                                   |
    | availability_zone              | nova                                 |
    | bootable                       | false                                |
    | consistencygroup_id            | None                                 |
    | created_at                     | 2017-09-08T22:30:11.000000           |
    | description                    | None                                 |
    | encrypted                      | False                                |
    | group_id                       | 68ea5b1d-0b09-44ae-ad9f-5e6d9672cc93 |
    | id                             | e982211e-1c34-4996-bee4-af30c5661d8a |
    | metadata                       | {}                                   |
    | migration_status               | None                                 |
    | multiattach                    | False                                |
    | name                           | vol-in-group1                        |
    | os-vol-host-attr:host          | None                                 |
    | os-vol-mig-status-attr:migstat | None                                 |
    | os-vol-mig-status-attr:name_id | None                                 |
    | os-vol-tenant-attr:tenant_id   | a9a7c9d88ad34fa889fd3b63c3d03292     |
    | replication_status             | None                                 |
    | size                           | 1                                    |
    | snapshot_id                    | None                                 |
    | source_volid                   | None                                 |
    | status                         | creating                             |
    | updated_at                     | None                                 |
    | user_id                        | f7d1f04baac34064a238a45dc5a6aa1b     |
    | volume_type                    | volume-support                       |
    +--------------------------------+--------------------------------------+

::

    $ cinder --os-volume-api-version 3.14 group-snapshot-create group1 --name group1-snapshot1
    +---------------+--------------------------------------+
    | Property      | Value                                |
    +---------------+--------------------------------------+
    | created_at    | 2017-09-08T22:32:06.000000           |
    | description   | None                                 |
    | group_id      | 68ea5b1d-0b09-44ae-ad9f-5e6d9672cc93 |
    | group_type_id | 5bf45d12-0ea3-4061-b6b9-287965edce41 |
    | id            | 3ac3a4cc-658a-4b1a-96c5-6272756ea60e |
    | name          | group1-snapshot1                     |
    | status        | creating                             |
    +---------------+--------------------------------------+

::

    $ cinder --os-volume-api-version 3.14 group-create-from-src --group-snapshot group1-snapshot1 --name group2
    +----------+--------------------------------------+
    | Property | Value                                |
    +----------+--------------------------------------+
    | id       | 66c4d2a0-13b7-49a2-a144-89fcc4cf3362 |
    | name     | group2                               |
    +----------+--------------------------------------+


Revert to Snapshot
------------------
In this section, we will create a new volume, take a snapshot from it and
revert to that last snapshot.

.. note::
   This command is only available in microversion 3.40 and above.

.. note::
   You can only revert the volume to the last snapshot taken. If you need to
   revert to an earlier snapshot, you have to delete snapshots until that one
   is the most recent.

.. note::
   The snapshot being reverted to must have the same size of the volume.

::

    $ cinder create --name cinder-vol-1 --volume-type gold 1
    +--------------------------------+--------------------------------------+
    | Property                       | Value                                |
    +--------------------------------+--------------------------------------+
    | attachments                    | []                                   |
    | availability_zone              | nova                                 |
    | bootable                       | false                                |
    | consistencygroup_id            | None                                 |
    | created_at                     | 2018-10-15T11:49:59.000000           |
    | description                    | None                                 |
    | encrypted                      | False                                |
    | id                             | c4913fc6-1dc9-4380-8372-9d290c23f32e |
    | metadata                       | {}                                   |
    | migration_status               | None                                 |
    | multiattach                    | False                                |
    | name                           | cinder-vol-1                         |
    | os-vol-host-attr:host          | None                                 |
    | os-vol-mig-status-attr:migstat | None                                 |
    | os-vol-mig-status-attr:name_id | None                                 |
    | os-vol-tenant-attr:tenant_id   | 3810b2bf356f430d9a06019cd9e56cc2     |
    | replication_status             | None                                 |
    | size                           | 1                                    |
    | snapshot_id                    | None                                 |
    | source_volid                   | None                                 |
    | status                         | creating                             |
    | updated_at                     | None                                 |
    | user_id                        | 90d2c8d154594c2eb51929a89474c753     |
    | volume_type                    | gold                                 |
    +--------------------------------+--------------------------------------+

::

    $ cinder snapshot-create --name cinder-snapshot-1 cinder-vol-1
    +-------------+--------------------------------------+
    | Property    | Value                                |
    +-------------+--------------------------------------+
    | created_at  | 2018-10-20T11:51:11.943346           |
    | description | None                                 |
    | id          | a2dee3cd-d14a-4920-8a73-17a3a8ca8fdc |
    | metadata    | {}                                   |
    | name        | cinder-snapshot-1                    |
    | size        | 1                                    |
    | status      | creating                             |
    | updated_at  | None                                 |
    | volume_id   | c4913fc6-1dc9-4380-8372-9d290c23f32e |
    +-------------+--------------------------------------+

::

    $ cinder --os-volume-api-version=3.40 revert-to-snapshot a2dee3cd-d14a-4920-8a73-17a3a8ca8fdc
