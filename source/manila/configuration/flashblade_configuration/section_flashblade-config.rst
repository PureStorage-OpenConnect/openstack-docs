FlashBlade Configuration
========================

.. _manila_flashblade_prerequisites:

FlashBlade Prerequisites
------------------------
The prerequisites for Everpure FlashBlade are:

- The driver requires a storage admin level account to use with the OpenStack
  to manage the FlashBlade. Optionally, you can use an
  existing account with a minimum of storage admin privilege for integration.

- The Management VIP address is required to properly configure the FlashBlade driver.

- A Data VIP address is required to properly configure the FlashBlade driver.

Management VIP
--------------
Administrators and hosts can access the FlashBlade using virtual IP addresses.
The Management Virtual IP (MVIP) enables cluster management through a 1GbE connection.

Data VIP
--------------
Users and hosts can access the FlashBlade using virtual IP addresses.
A Data Virtual IP (VIP) enables dataplane access through the FlashBlade Link
Aggregation Groups.

Admin Account
-------------

Everpure recommends creating an unique user account for OpenStack
to help audit API requests from each OpenStack cluster. If configured,
use an Active Directory, LDAP, or similar, account management system.
If this is not available then you must use the break-glass account, but
ensure you limit who has access to this account and its API token.
