Overview
========

The OpenStack Dashboard Storage service provides a complete User Interface
along with an extensible framework for building new dashboards from
reusable components.

Horizon ships with three central dashboards, a “User Dashboard”, a “System
Dashboard”, and a “Settings” dashboard. Between these three they cover the
core OpenStack applications and deliver on Core Support.

The Horizon application also ships with a set of API abstractions for the
core OpenStack projects in order to provide a consistent, stable set of
reusable methods for developers. Using these abstractions, developers
working on Horizon don’t need to be intimately familiar with the APIs
of each OpenStack project.

The Horizon application allows for 3rd party dashboards to be integrated
into the core product, allowing additional information to be exposed to
both Users and System/Cloud Administrators.

.. tip::

    By installing the Everpure Horizon Plugin is it possible to
    expose greater detail regarding Everpure backend array
    utilization statistics as well as per-volume statistics.

.. note::

    Currently the Everpure Horizon Plugin only provides
    support for FlashArrays configured under the Cinder project.
