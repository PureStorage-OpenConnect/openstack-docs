Manila Command Line Interface (CLI)
===================================

Manila Service Verification
---------------------------

Here we ensure that the Manila services are all correctly running.

::

    $ openstack share service lisr
    +----+------------------+-----------------------+------+---------+-------+----------------------------+
    | Id | Binary           | Host                  | Zone | Status  | State | Updated_at                 |
    +----+------------------+-----------------------+------+---------+-------+----------------------------+
    | 1  | manila-share     | devstack@flashblade-1 | nova | enabled | up    | 2021-02-25T17:18:32.000000 |
    | 2  | manila-scheduler | devstack              | nova | enabled | up    | 2021-02-25T17:18:32.000000 |
    | 3  | manila-data      | devstack              | nova | enabled | up    | 2021-02-25T17:18:32.000000 |
    +----+------------------+-----------------------+------+---------+-------+----------------------------+

Creating and Defining Manila Share Types
----------------------------------------

In this section, we create Manila Share Types that leverage
both the default capabilities of each driver, as well as the FlashBlade
specific extra specs described in
:ref:`Table 9.11, “FlashBlade supported Extra Specs for use with Manila Share Types”<table-9.11>`.

-  The ``general`` type provisions Manila shares onto the FlashBlade backend
   using all the default settings, excluding snapshot support.

-  The ``snapshot`` type provisions Manila shares onto the FlashBlade backend
   using all the default settings, including snapshot support.

-  The ``default`` type provisions Manila shares onto any pool of any
   driver without share server management and snapshot support.

::

    $ openstack share type create general False
    +----------------------+--------------------------------------+
    | Property             | Value                                |
    +----------------------+--------------------------------------+
    | ID                   | fa26c384-bacd-4bcc-b1a1-537628886827 |
    | Name                 | general                              |
    | Visibility           | public                               |
    | is_default           | -                                    |
    | required_extra_specs | driver_handles_share_servers : False |
    | optional_extra_specs |                                      |
    | Description          | None                                 |
    +----------------------+--------------------------------------+

::

    $ openstack share type create --extra-specs snapshot_support=True snapshot False
    +----------------------+--------------------------------------+
    | Property             | Value                                |
    +----------------------+--------------------------------------+
    | ID                   | e4bcd81b-474d-4b2b-af92-c08a653b373e |
    | Name                 | shapshot                             |
    | Visibility           | public                               |
    | is_default           | -                                    |
    | required_extra_specs | driver_handles_share_servers : False |
    | optional_extra_specs | snapshot_support : True              |
    | Description          | None                                 |
    +----------------------+--------------------------------------+


.. important::

   From OpenStack Ocata, the ``snapshot_support`` extra spec must be set to
   ``True`` in order to allow snapshots for a share type. If the
   ``snapshot_support`` extra_spec is omitted or if it is set to False,
   users would not be able to create snapshots on shares of this share
   type.

::

    $ openstack share type set --extra-specs share_backend_name=flashblade-1 general

::

    $ openstack share type set --extra-specs snapshot_support=False default

::

    $ openstack share type list --extra-specs
    +--------------------------------------+------------+--------------------------------------+
    | ID                                   | Name       | all_extra_specs                      |
    +--------------------------------------+------------+--------------------------------------+
    | 10007149-43cd-412e-ba17-086d3b01a670 | dhss_true  | driver_handles_share_servers : True  |
    | 3f72ffae-5723-4593-9849-5c46dc0343d2 | default    | driver_handles_share_servers : False |
    |                                      |            | snapshot_support : False             |
    | cb58ed1d-c61a-4cfb-b62e-6d9c2ddd826c | dhss_false | driver_handles_share_servers : False |
    | e4bcd81b-474d-4b2b-af92-c08a653b373e | shapshot   | snapshot_support : True              |
    |                                      |            | driver_handles_share_servers : False |
    | fa26c384-bacd-4bcc-b1a1-537628886827 | general    | driver_handles_share_servers : False |
    |                                      |            | share_backend_name : flashblade-1    |
    +--------------------------------------+------------+--------------------------------------+

Creating Manila Shares with Share Types
---------------------------------------

In this section, we create a share with the general type.

::

    $ openstack share create --name myGeneral --share-type general NFS 1
    +---------------------------------------+--------------------------------------+
    | Property                              | Value                                |
    +---------------------------------------+--------------------------------------+
    | id                                    | 79779ae4-f06b-4e24-918f-2cd3262d5da8 |
    | size                                  | 1                                    |
    | availability_zone                     | None                                 |
    | created_at                            | 2021-02-25T18:33:10.000000           |
    | status                                | creating                             |
    | name                                  | myGeneral                            |
    | description                           | None                                 |
    | project_id                            | 12e2ca2e858f45eba16e90cb13a0bfd0     |
    | snapshot_id                           | None                                 |
    | share_network_id                      | None                                 |
    | share_proto                           | NFS                                  |
    | metadata                              | {}                                   |
    | share_type                            | fa26c384-bacd-4bcc-b1a1-537628886827 |
    | is_public                             | False                                |
    | snapshot_support                      | True                                 |
    | task_state                            | None                                 |
    | share_type_name                       | general                              |
    | access_rules_status                   | active                               |
    | replication_type                      | None                                 |
    | has_replicas                          | False                                |
    | user_id                               | 991c3f4bca814130897d9988b93301da     |
    | create_share_from_snapshot_support    | False                                |
    | revert_to_snapshot_support            | True                                 |
    | share_group_id                        | None                                 |
    | source_share_group_snapshot_member_id | None                                 |
    | mount_snapshot_support                | False                                |
    | progress                              | None                                 |
    | share_server_id                       | None                                 |
    | host                                  |                                      |
    +---------------------------------------+--------------------------------------+

::

    $ openstack share list
    +--------------------------------------+-----------+------+-------------+-----------+-----------+-----------------+------------------------------------+-------------------+
    | ID                                   | Name      | Size | Share Proto | Status    | Is Public | Share Type Name | Host                               | Availability Zone |
    +--------------------------------------+-----------+------+-------------+-----------+-----------+-----------------+------------------------------------+-------------------+
    | 79779ae4-f06b-4e24-918f-2cd3262d5da8 | myGeneral | 1    | NFS         | available | False     | general         | devstack@flashblade-1#flashblade-1 | nova              |
    +--------------------------------------+-----------+------+-------------+-----------+-----------+-----------------+------------------------------------+-------------------+


Granting Access To Shares
-------------------------

We'll now add access rules for any IP-connected client in
two specific subnets to mount this
NFS share with full read/write privileges.

::

    $ openstack share access create myGeneral ip 10.21.200.0/24
    +--------------+--------------------------------------+
    | Property     | Value                                |
    +--------------+--------------------------------------+
    | id           | 06c2e7ac-b166-47f8-abd0-86ce7acaadff |
    | share_id     | 79779ae4-f06b-4e24-918f-2cd3262d5da8 |
    | access_level | rw                                   |
    | access_to    | 10.21.200.0/24                       |
    | access_type  | ip                                   |
    | state        | queued_to_apply                      |
    | access_key   | None                                 |
    | created_at   | 2021-02-25T18:36:16.000000           |
    | updated_at   | None                                 |
    | metadata     | {}                                   |
    +--------------+--------------------------------------+

::

    $ openstack share access create myGeneral ip 10.21.220.0/24
    +--------------+--------------------------------------+
    | Property     | Value                                |
    +--------------+--------------------------------------+
    | id           | e0eed540-e2e7-4014-aebd-83ff7a2f5d61 |
    | share_id     | 79779ae4-f06b-4e24-918f-2cd3262d5da8 |
    | access_level | rw                                   |
    | access_to    | 10.21.220.0/24                       |
    | access_type  | ip                                   |
    | state        | queued_to_apply                      |
    | access_key   | None                                 |
    | created_at   | 2021-02-25T19:39:11.000000           |
    | updated_at   | None                                 |
    | metadata     | {}                                   |
    +--------------+--------------------------------------+

Viewing Access Rules for Shares
-------------------------------

Now let's examine the access rules we have created for this NFS share.

::

    $ openstack share access list myGeneral
    +--------------------------------------+-------------+----------------+--------------+--------+------------+----------------------------+------------+
    | id                                   | access_type | access_to      | access_level | state  | access_key | created_at                 | updated_at |
    +--------------------------------------+-------------+----------------+--------------+--------+------------+----------------------------+------------+
    | a497038e-377d-440e-95e3-e99dc7a62121 | ip          | 10.21.200.0/24 | rw           | active | None       | 2021-02-25T19:37:03.000000 | None       |
    | e0eed540-e2e7-4014-aebd-83ff7a2f5d61 | ip          | 10.21.220.0/24 | rw           | active | None       | 2021-02-25T19:39:11.000000 | None       |
    +--------------------------------------+-------------+----------------+--------------+--------+------------+----------------------------+------------+


Removing Access From Shares
---------------------------

We'll now remove access rules to deny any IP-connected clients
in a specific subnet from mounting this NFS share with full
read/write privileges.

::

    $ openstack share access delete myGeneral e0eed540-e2e7-4014-aebd-83ff7a2f5d61

::

    $ openstack share access list myGeneral
    +--------------------------------------+-------------+----------------+--------------+--------+------------+----------------------------+------------+
    | id                                   | access_type | access_to      | access_level | state  | access_key | created_at                 | updated_at |
    +--------------------------------------+-------------+----------------+--------------+--------+------------+----------------------------+------------+
    | a497038e-377d-440e-95e3-e99dc7a62121 | ip          | 10.21.200.0/24 | rw           | active | None       | 2021-02-25T19:37:03.000000 | None       |
    +--------------------------------------+-------------+----------------+--------------+--------+------------+----------------------------+------------+


Viewing Export Locations
------------------------

We'll now list the export location(s) for the new share to see
its network path. There may be multiple export locations for a given
share.

::

    $ openstack share export location list 79779ae4-f06b-4e24-918f-2cd3262d5da8 \
               --column Path --column Preferred
    +----------------------------------------------------------------+-----------+
    | Path                                                           | Preferred |
    +----------------------------------------------------------------+-----------+
    | 10.21.200.4:/share-f875eed0-eed1-45d2-80a9-fe7492e331ce-manila | False     |
    +----------------------------------------------------------------+-----------+

Creating Manila Share Groups
----------------------------

In this section, we'll create and work with share groups and
share group (SG) snapshots. First we list the share types
that are available and create a share group type. This will
be subsequently used to create a SG.

::

    $ openstack share list
    +--------------------------------------+------------+------------+------------+--------------------------------------+-----------------------------------+-------------+
    | ID                                   | Name       | visibility | is_default | required_extra_specs                 | optional_extra_specs              | Description |
    +--------------------------------------+------------+------------+------------+--------------------------------------+-----------------------------------+-------------+
    | 10007149-43cd-412e-ba17-086d3b01a670 | dhss_true  | public     | -          | driver_handles_share_servers : True  |                                   | None        |
    | 3f72ffae-5723-4593-9849-5c46dc0343d2 | default    | public     | YES        | driver_handles_share_servers : False | snapshot_support : True           | None        |
    | cb58ed1d-c61a-4cfb-b62e-6d9c2ddd826c | dhss_false | public     | -          | driver_handles_share_servers : False |                                   | None        |
    | e4bcd81b-474d-4b2b-af92-c08a653b373e | shapshot   | public     | -          | driver_handles_share_servers : False | snapshot_support : True           | None        |
    | fa26c384-bacd-4bcc-b1a1-537628886827 | general    | public     | -          | driver_handles_share_servers : False | share_backend_name : flashblade-1 | None        |
    |                                      |            |            |            |                                      | snapshot_support : True           |             |
    +--------------------------------------+------------+------------+------------+--------------------------------------+-----------------------------------+-------------+

::

    $ openstack share group type create type1 general
    +------------+--------------------------------------+
    | Property   | Value                                |
    +------------+--------------------------------------+
    | ID         | bd76541e-a82f-4f73-95f5-df1100d87e1f |
    | Name       | type1                                |
    | Visibility | public                               |
    | is_default | -                                    |
    +------------+--------------------------------------+

::

    $ openstack share group type list
    +--------------------------------------+-------+------------+------------+
    | ID                                   | Name  | visibility | is_default |
    +--------------------------------------+-------+------------+------------+
    | bd76541e-a82f-4f73-95f5-df1100d87e1f | type1 | public     | -          |
    +--------------------------------------+-------+------------+------------+

Now we create a share group.

::

    $ openstack share group create \
    --name sg_1 \
    --description "sg_1 share group" \
    --share-group-type type1 \
    --share-type general
    +--------------------------------+--------------------------------------+
    | Property                       | Value                                |
    +--------------------------------+--------------------------------------+
    | id                             | 96bcb0e1-e595-4724-9fc8-4715eeff47f1 |
    | name                           | sg_1                                 |
    | created_at                     | 2021-02-25T18:51:24.847976           |
    | status                         | creating                             |
    | description                    | sg_1 share group                     |
    | project_id                     | 12e2ca2e858f45eba16e90cb13a0bfd0     |
    | host                           | None                                 |
    | share_group_type_id            | bd76541e-a82f-4f73-95f5-df1100d87e1f |
    | source_share_group_snapshot_id | None                                 |
    | share_network_id               | None                                 |
    | share_types                    | fa26c384-bacd-4bcc-b1a1-537628886827 |
    | availability_zone              | None                                 |
    | consistent_snapshot_support    | None                                 |
    | share_server_id                | None                                 |
    +--------------------------------+--------------------------------------+

::

    $ openstack share group list
    +--------------------------------------+------+-----------+------------------+
    | ID                                   | Name | Status    | Description      |
    +--------------------------------------+------+-----------+------------------+
    | 96bcb0e1-e595-4724-9fc8-4715eeff47f1 | sg_1 | available | sg_1 share group |
    +--------------------------------------+------+-----------+------------------+

::

    $ openstack share group show 96bcb0e1-e595-4724-9fc8-4715eeff47f1
    +--------------------------------+--------------------------------------+
    | Property                       | Value                                |
    +--------------------------------+--------------------------------------+
    | id                             | 96bcb0e1-e595-4724-9fc8-4715eeff47f1 |
    | name                           | sg_1                                 |
    | created_at                     | 2021-02-25T18:51:25.000000           |
    | status                         | available                            |
    | description                    | sg_1 share group                     |
    | project_id                     | 12e2ca2e858f45eba16e90cb13a0bfd0     |
    | host                           | devstack@flashblade-1#flashblade-1   |
    | share_group_type_id            | bd76541e-a82f-4f73-95f5-df1100d87e1f |
    | source_share_group_snapshot_id | None                                 |
    | share_network_id               | None                                 |
    | share_types                    | fa26c384-bacd-4bcc-b1a1-537628886827 |
    | availability_zone              | nova                                 |
    | consistent_snapshot_support    | None                                 |
    | share_server_id                | None                                 |
    +--------------------------------+--------------------------------------+

Next we'll create two shares in the new share group.

::

    $ openstack share create --name share_1 --share-group sg_1 --share-type general NFS 1
    +---------------------------------------+--------------------------------------+
    | Property                              | Value                                |
    +---------------------------------------+--------------------------------------+
    | id                                    | 56837375-7b0c-49cc-9bf8-ddfd83487a85 |
    | size                                  | 1                                    |
    | availability_zone                     | nova                                 |
    | created_at                            | 2021-02-25T18:54:35.000000           |
    | status                                | creating                             |
    | name                                  | share_1                              |
    | description                           | None                                 |
    | project_id                            | 12e2ca2e858f45eba16e90cb13a0bfd0     |
    | snapshot_id                           | None                                 |
    | share_network_id                      | None                                 |
    | share_proto                           | NFS                                  |
    | metadata                              | {}                                   |
    | share_type                            | fa26c384-bacd-4bcc-b1a1-537628886827 |
    | is_public                             | False                                |
    | snapshot_support                      | True                                 |
    | task_state                            | None                                 |
    | share_type_name                       | general                              |
    | access_rules_status                   | active                               |
    | replication_type                      | None                                 |
    | has_replicas                          | False                                |
    | user_id                               | 991c3f4bca814130897d9988b93301da     |
    | create_share_from_snapshot_support    | False                                |
    | revert_to_snapshot_support            | True                                 |
    | share_group_id                        | 96bcb0e1-e595-4724-9fc8-4715eeff47f1 |
    | source_share_group_snapshot_member_id | None                                 |
    | mount_snapshot_support                | False                                |
    | progress                              | None                                 |
    | share_server_id                       | None                                 |
    | host                                  | devstack@flashblade-1#flashblade-1   |
    +---------------------------------------+--------------------------------------+

::

    $ openstack share create --name share_2 --share-group sg_1 --share-type general NFS 1
    +---------------------------------------+--------------------------------------+
    | Property                              | Value                                |
    +---------------------------------------+--------------------------------------+
    | id                                    | 615b0c2c-22b1-4f70-bf68-7e4757f2ba2b |
    | size                                  | 1                                    |
    | availability_zone                     | nova                                 |
    | created_at                            | 2021-02-25T18:54:49.000000           |
    | status                                | creating                             |
    | name                                  | share_2                              |
    | description                           | None                                 |
    | project_id                            | 12e2ca2e858f45eba16e90cb13a0bfd0     |
    | snapshot_id                           | None                                 |
    | share_network_id                      | None                                 |
    | share_proto                           | NFS                                  |
    | metadata                              | {}                                   |
    | share_type                            | fa26c384-bacd-4bcc-b1a1-537628886827 |
    | is_public                             | False                                |
    | snapshot_support                      | True                                 |
    | task_state                            | None                                 |
    | share_type_name                       | general                              |
    | access_rules_status                   | active                               |
    | replication_type                      | None                                 |
    | has_replicas                          | False                                |
    | user_id                               | 991c3f4bca814130897d9988b93301da     |
    | create_share_from_snapshot_support    | False                                |
    | revert_to_snapshot_support            | False                                |
    | share_group_id                        | 96bcb0e1-e595-4724-9fc8-4715eeff47f1 |
    | source_share_group_snapshot_member_id | None                                 |
    | mount_snapshot_support                | False                                |
    | progress                              | None                                 |
    | share_server_id                       | None                                 |
    | host                                  | devstack@flashblade-1#flashblade-1   |
    +---------------------------------------+--------------------------------------+

Next we'll create two SG snapshots of the new share group.

::

    $ openstack share group snapshot create \
    --name snapshot_1 \
    --description 'first snapshot of sg-1' \
    sg_1
    +----------------+--------------------------------------+
    | Property       | Value                                |
    +----------------+--------------------------------------+
    | id             | d5e4d8a7-936f-40cc-b99f-05dd87ab3dd4 |
    | name           | snapshot_1                           |
    | created_at     | 2021-02-25T18:58:54.379776           |
    | status         | creating                             |
    | description    | first snapshot of sg-1               |
    | project_id     | 12e2ca2e858f45eba16e90cb13a0bfd0     |
    | share_group_id | 96bcb0e1-e595-4724-9fc8-4715eeff47f1 |
    +----------------+--------------------------------------+

::

    $ openstack share group snapshot list
    +--------------------------------------+------------+-----------+------------------------+
    | id                                   | name       | status    | description            |
    +--------------------------------------+------------+-----------+------------------------+
    | d5e4d8a7-936f-40cc-b99f-05dd87ab3dd4 | snapshot_1 | available | first snapshot of sg_1 |
    +--------------------------------------+------------+-----------+------------------------+

::

    $ openstack share group snapshot show d5e4d8a7-936f-40cc-b99f-05dd87ab3dd4
    +----------------+--------------------------------------+
    | Property       | Value                                |
    +----------------+--------------------------------------+
    | id             | d5e4d8a7-936f-40cc-b99f-05dd87ab3dd4 |
    | name           | snapshot_1                           |
    | created_at     | 2021-02-25T18:58:54.000000           |
    | status         | available                            |
    | description    | first snapshot of sg-1               |
    | project_id     | 12e2ca2e858f45eba16e90cb13a0bfd0     |
    | share_group_id | 96bcb0e1-e595-4724-9fc8-4715eeff47f1 |
    +----------------+--------------------------------------+

::

    $ openstack share group snapshot create \
    --name snapshot_2 \
    --description 'second snapshot of sg-1' \
    sg_1
    +----------------+--------------------------------------+
    | Property       | Value                                |
    +----------------+--------------------------------------+
    | id             | b2de1edc-0f88-45a2-a147-76b0e9546b86 |
    | name           | snapshot_2                           |
    | created_at     | 2021-02-25T19:26:55.910712           |
    | status         | creating                             |
    | description    | second snapshot of sg-1              |
    | project_id     | 12e2ca2e858f45eba16e90cb13a0bfd0     |
    | share_group_id | 96bcb0e1-e595-4724-9fc8-4715eeff47f1 |
    +----------------+--------------------------------------+

::

    $ manila share-group-snapshot-list
    +--------------------------------------+------------+-----------+-------------------------+
    | id                                   | name       | status    | description             |
    +--------------------------------------+------------+-----------+-------------------------+
    | b2de1edc-0f88-45a2-a147-76b0e9546b86 | snapshot_2 | available | second snapshot of sg-1 |
    | d5e4d8a7-936f-40cc-b99f-05dd87ab3dd4 | snapshot_1 | available | first snapshot of sg-1  |
    +--------------------------------------+------------+-----------+-------------------------+
