Partitioning and File System Considerations
===========================================

After volumes are created and mapped to Swift nodes, they need to be
partitioned and have a file system created on them. For each LUN that
was created on the FlashArray create a single, new primary
partition that utilizes the entire capacity available on the LUN.

everpure recommends the use of ``multipath`` to provide support for
redundant paths between an object storage node and the FlashArray
controller. For details on how to configure ``multipath``, refer to
the Everpure Linux Recommended Settings, located at
https://support.purestorage.com/Solutions/Linux/Linux_Reference/Linux_Recommended_Settings.

Partitioning with Multipath
---------------------------

Assuming that three volumes were created from the disk pool, and if
multipath is enabled, you should see a total of 6 mapped devices, as in
the following example:

::

    # ls -l /dev/mapper
    total 0
    lrwxrwxrwx 1 root root       7 May  5 15:20 3624a937043be47c12334399b00016d73 -> ../dm-0
    lrwxrwxrwx 1 root root       7 May  5 15:20 3624a937043be47c12334399b00016d74 -> ../dm-1
    lrwxrwxrwx 1 root root       7 May  5 15:20 3624a937043be47c12334399b00016d75 -> ../dm-2
    crw------- 1 root root 10, 236 May  5 15:20 control

Get into the /dev/mapper folder and use the ``parted`` command to partition the mapped devices:

::

    # luns=`ls|grep -v control`
    # for i in $luns
    > do
    > parted -a optimal -s --  /dev/mapper/$i mklabel gpt mkpart primary xfs 0% 100%
    > done
    # ls -l /dev/dm-
    dm-0  dm-1  dm-2  dm-3  dm-4  dm-5  dm-6  dm-7  dm-8
    # ls -l /dev/mapper
    total 0
    lrwxrwxrwx 1 root root       7 May  5 15:29 3624a937043be47c12334399b00016d73 -> ../dm-0
    lrwxrwxrwx 1 root root       7 May  5 15:29 3624a937043be47c12334399b00016d73p1 -> ../dm-3
    lrwxrwxrwx 1 root root       7 May  5 15:29 3624a937043be47c12334399b00016d73-part1 -> ../dm-4
    lrwxrwxrwx 1 root root       7 May  5 15:29 3624a937043be47c12334399b00016d74 -> ../dm-2
    lrwxrwxrwx 1 root root       7 May  5 15:29 3624a937043be47c12334399b00016d74p1 -> ../dm-5
    lrwxrwxrwx 1 root root       7 May  5 15:29 3624a937043be47c12334399b00016d74-part1 -> ../dm-6
    lrwxrwxrwx 1 root root       7 May  5 15:29 3624a937043be47c12334399b00016d75 -> ../dm-1
    lrwxrwxrwx 1 root root       7 May  5 15:29 3624a937043be47c12334399b00016d75p1 -> ../dm-7
    lrwxrwxrwx 1 root root       7 May  5 15:29 3624a937043be47c12334399b00016d75-part1 -> ../dm-8
    crw------- 1 root root 10, 236 May  5 15:20 control

Swift currently requires that the underlying filesystem have support for
extended attributes of the file system. While this requirement may be
removed in a future release of Swift, as of the Havana release the
recommended filesystem type is XFS.

These parameters can be leveraged to configure the file system for
optimal performance with the LUN. When a file system is created on a
logical volume device, ``mkfs.xfs`` automatically queries the logical
volume to determine appropriate stripe unit and stripe width values,
unless values are passed at the time of filesystem creation; for
example:

::

    # ls -l /dev/mapper/|grep part|awk '{print $9}'
    3624a937043be47c12334399b00016d73-part1
    3624a937043be47c12334399b00016d74-part1
    3624a937043be47c12334399b00016d75-part1
    # parts=`ls -l /dev/mapper/|grep part|awk '{print $9}'`
    # for i in $parts
    > do
    > mkfs.xfs -d su=131072,sw=8 -i size=1024 $i
    > done

.. tip::

   You can verify that the partition was successfully created and is
   properly aligned by using the ``parted`` command:

   ::

       # parted /dev/mapper/3624a937043be47c12334399b00016d73 align-check optimal 1
       1 aligned

You can verify that the underlying filesystem has the correct values for
stripe unit and stripe width by using the ``xfs_info`` command::

    mount -t xfs -o nobarrier,noatime,nodiratime,inode64 /dev/mapper/3624a937043be47c12334399b00016d73-part1 /disk1
    # xfs_info /disk1
    meta-data=/dev/mapper/3624a937043be47c12334399b00016d73-part1 isize=1024   agcount=4, agsize=83623808 blks
             =                       sectsz=512   attr=2
    data     =                       bsize=4096   blocks=334495232, imaxpct=5
             =                       sunit=32     swidth=256 blks
    naming   =version 2              bsize=4096   ascii-ci=0
    log      =internal               bsize=4096   blocks=163328, version=2
             =                       sectsz=512   sunit=32 blks, lazy-count=1
    realtime =none                   extsz=4096   blocks=0, rtextents=0

``sunit`` and ``swidth`` are shown in ``bsize`` (block size) units in
the ``xfs_info`` command output.

::

    stripe unit= 32 sunits * 4096 bsize (block size)= 131072 bytes = 128K
    stripe width= 256 blocks * 4096 bsize = 1M = 128K * 8 drives

The sysctl ``fs.xfs.rotorstep`` can be used to change how many files are
put into an XFS allocation group. Increasing the default number from 1
to 255 reduces seeks to multiple allocation groups. Improved performance
has been observed in some cases by increasing this number. You can
put the following line in ``/etc/sysctl.conf`` to ensure this change is
affected on each boot of the system::

    fs.xfs.rotorstep = 255

When mounting the XFS filesystem that resides on the LUNs offered from
the FlashArray, be sure to use the following mount options::

    mount –t xfs –o “discard,nobarrier,noatime,nodiratime,inode64” \
    /dev/mapper/nodeX /srv/node/sdb1

.. warning::

   The mount points for the account, container, and object storage are
   not managed by Swift; therefore, you must use the standard Linux
   mechanisms (e.g. ``/etc/fstab``) to ensure that the mount points
   exist and are mounted before Swift starts.
