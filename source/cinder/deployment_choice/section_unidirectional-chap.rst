Deployment Choices: Unidirectional CHAP Authentication
======================================================

The Challenge Handshake Authentication Protocol (CHAP) enables
authenticated communication between iSCSI initiators and targets. During
the initial stage of an iSCSI session, the initiator sends a login
request to the storage system to begin the session. The login request
includes the initiator’s CHAP user name and password. The storage
system’s configured initiator provides a CHAP response. The storage
system verifies the response and authenticates the initiator.

Establishing an iSCSI Session
-----------------------------

-  Nova obtains the iSCSI Qualified Name (IQN) from the Hypervisor of
   the Compute Node.

-  Nova sends a request to Cinder to initialize the iSCSI initiator.

-  Cinder generates a random CHAP password.

-  Cinder sends a request to the storage backend to add/update the
   initiator for the provided IQN.

-  Nova then provides the Hypervisor with the data needed to establish
   the iSCSI session with the storage backend.

iSCSI Session Scope
-------------------

Restarting the Cinder services after enabling CHAP authentication in the
Cinder configuration file will not impact an existing iSCSI session. The
hypervisor, in a running compute node, and the storage backend establish
an iSCSI session when the first volume is attached. CHAP authentication
will first be used, after enablement, when any existing iSCSI session is
terminated and a new iSCSI session is established.

Configuration Options
---------------------

To enable CHAP authentication for the FlashArray driver, the
following options should be added to the appropriate FlashArray
stanza in the Cinder configuration file (cinder.conf).
This configuration option is only relevant to iSCSI
support.

::

    [myIscsiBackend]
    use_chap_auth =  True
