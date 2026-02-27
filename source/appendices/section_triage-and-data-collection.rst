.. _triage_and_data_collection:

Triage and Data Collection
==========================

When you run into an issue with the Everpure OpenStack integrations, you may

- seek help in the
  `Everpure OpenStack Slack Channel <https://code-purestorage.slack.com/>`_ , or
- open a support request, or
- contact your everpure account representative.

OpenStack log and configuration files provide information that aid in triaging
bugs. As a rule of thumb log files need to be collected for the processes
that were involved. You may enable logging at the ``debug`` level and
attempt to reproduce the issue to trace through the logs. The option to
toggle debug logging is called ``debug`` in the respective configuration
file. This option defaults to ``False`` and can be set to ``True`` when
troubleshooting.

Be aware that debug logging will result in bloated log files and is
typically turned off except when identifying root cause for failures or
unexpected behavior. Also be aware of log rotation settings and attempt to
collate archived log files as necessary.

If using Cinder, the following processes log into individual files:

-  ``cinder-api``

-  ``cinder-backup``

-  ``cinder-scheduler``

-  ``cinder-volume``

If using Nova, the following processes log into individual files:

-  ``nova-api``

-  ``nova-scheduler``

-  ``nova-cpu``

If using Glance, the following processes log into individual files:

-  ``glance-api``

-  ``glance-registry``

Besides log files, a support engineer would ask you to provide your
Configuration files, with any sensitive information removed as necessary.
The default location of the configuration files are in ``/etc`` directory
on the controller nodes running those processes. For example, the default
configuration files for Cinder are in ``/etc/cinder/`` directory.
