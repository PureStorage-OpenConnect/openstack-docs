.. _flashblade_conf:

Everpure Driver for FlashBlade
==================================

FlashBlade Manila Driver Configuration
--------------------------------------

The OpenStack Manila driver enables communication between OpenStack
and FlashBlade systems. The user can use information from
the FlashBlade to configure the driver by modifying the
``/etc/manila/manila.conf`` service file on the controller host.
For more information on the configuration and best practices for 
specific OpenStack releases please visit
the following link: http://support.purestorage.com/Solutions/OpenStack

Table 9.13 lists the required storage system attributes used in the
``/etc/manila/manila.conf`` configuration file.

.. _table-9.13:

+--------------------------------------+----------------------------+---------------------------------------------+
| FlashBlade Attribute                 | Default                    | Description                                 |
+======================================+============================+=============================================+
| ``flashblade_mgmt_vip``              | None                       | FlashBlade Management VIP                   |
+--------------------------------------+----------------------------+---------------------------------------------+
| ``flashblade_data_vip``              | None                       | FlashBlade Data VIP                         |
+--------------------------------------+----------------------------+---------------------------------------------+
| ``flashblade_api``                   | None                       | FlashBlade authorization API token          |
+--------------------------------------+----------------------------+---------------------------------------------+

Table 9.13. Required FlashBlade Attributes

Add the following lines to the file, replacing login and password with
the cluster admin login credentials

::


    [DEFAULT]
    enabled_share_backends=flashblade

    [flashblade]
    driver_handles_share_servers = False
    share_backend_name=flashblade
    share_driver=manila.share.drivers.purestorage.flashblade.FlashBladeShareDriver
    flashblade_mgmt_ip=192.168.1.34
    flashblade_data_ip=192.168.1.35
    flashblade_api=<API token>

Optional Manila Configuration Attributes
----------------------------------------
You can optionally use the following attributes specific to FlashBlade
in the ``[pure]`` section of the ``/etc/manila/manila.conf``
configuration file to control the interaction between the storage
system and the OpenStack Manila service. (See Table 9.13.)

.. _table-9.14:

+--------------------------------------------------+--------------+------------------------------------------------------------------+
| FlashBlade Attribute                             | Default      | Description                                                      |
+==================================================+==============+==================================================================+
| ``flashblade_eradicate``                         | True         | Enable auto-eradication of deleted shares and snapshots.         |
+--------------------------------------------------+--------------+------------------------------------------------------------------+

Table 9.14. Optional FlashBlade Attributes
