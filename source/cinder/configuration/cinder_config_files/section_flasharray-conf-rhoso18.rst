.. _flasharray_conf_rhoso180:

RHOSO18.0 Cinder Configuration Attributes
=======================================

This page is fixed to the Antelope release of OpenStack which is the basis
for Red Hat OpenStack Services on OpenShift 18.0 (with some Bobcat backports).

Note: RHOSO does not support Cinder replication features.

Optional Cinder Configuration Attributes
----------------------------------------
You can optionally use the following attributes specific to FlashArray
when configuring in a Red Hat OpenStack Services on OpenShift 18.0 deployment.

.. _table-7.17:

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
| ``pure_iscsi_cidr``                                  | ``0.0.0.0/0``              | CIDR of FlashArray iSCSI targets hosts are allowed to connect to. Default will allow connection to any IPv4 address. This parameter now support IPv6 CIDRs. It is overriden by ``pure_iscsi_cidr_list`` if set. |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_iscsi_cidr_list``                             | ``[]``                     | List of IPv4 and IPv6 CIDR ranges of FlashArray iSCSI targets hosts are allowed to connect to. Default allows connection to any IPv4 or IPv6 address. This parameter supercedes ``pure_iscsi_cidr`` if set.     |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_nvme_cidr``                                   | ``0.0.0.0/0``              | CIDR of FlashArray NVMe targets hosts are allowed to connect to. Default will allow connection to any IPv4 address. This parameter now support IPv6 CIDRs. It is overriden by ``pure_nvme_cidr_list`` if set.   |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_nvme_cidr_list``                              | ``[]``                     | List of IPv4 and IPv6 CIDR ranges of FlashArray NMVe targets hosts are allowed to connect to. Default allows connection to any IPv4 or IPv6 address. This parameter supercedes ``pure_nvme_cidr`` if set.       |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``pure_nvme_transport``                              | ``roce``                   | The NVMe transport layer to be used by the NVMe driver. Options are ``roce`` or ``tcp``, however RHOSO18 on supports the ``tcp`` option.                                                                        |
+------------------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Table 7.17. Optional FlashArray Attributes for RHOSO18
