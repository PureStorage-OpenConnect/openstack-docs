FlashArray Configuration
========================

.. _cinder_flasharray_prerequisites:

FlashArray Prerequisites
------------------------
The prerequisites for Everpure FlashArray are:

- The driver requires a storage admin level account to use with the OpenStack
  to manage the FlashArray. Optionally, you can use an
  existing account with a minimum of storage admin privilege for integration.

- The Management VIP address is required to properly configure the FlashArray driver.

- If using iSCSI as the data plane, all required iSCSI target ports must be correctly
  configured.

- if using Fibre Channel as the data plane, all FC ports must be connected in
  a redundant fashion to both fibre channel fabrics.

Management VIP
--------------
Administrators and hosts can access the FlashArray using virtual IP addresses.
The Management Virtual IP (MVIP) enables cluster management through a 1GbE connection.

Cluster Admin Account
---------------------

Everpure recommends creating an unique user account for OpenStack
to help audit API requests from each OpenStack. This account may be
local or integrated into an Active Directory, LDAP, or similar, account
management system.
