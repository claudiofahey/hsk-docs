Prepare Hadoop Virtual Machines
===============================

First you will create one virtual machine to run |hadoop-manager|.
It can be provisioned using any tool you like. This document will show how
to use BDE to deploy a "cluster" consisting of a single server that will
run |hadoop-manager|.

Then you will create your actual Hadoop nodes (e.g. Resource Manager, Node Managers) using BDE.

Provision Virtual Machines Using Big Data Extensions
----------------------------------------------------

#.  Copy the file isilon-hadoop-tools/etc/template-bde.json to
    isilon-hadoop-tools/etc/mycluster1-bde.json.

#.  Edit the file mycluster1-bde.json as desired.

    .. table:: Description of mycluster1-bde.json

      +---------------------------+----------------------------------------------------------+
      | Field Name                | Description                                              |
      +===========================+==========================================================+
      | nodeGroups.instanceNum    | The number of hosts that will be created in this node    |
      |                           | group. This should be 1 for all node groups except the   |
      |                           | worker group.                                            |
      +---------------------------+----------------------------------------------------------+
      | nodeGroups.storage.sizeGB | Size of additional disks for each host. Note that the OS |
      |                           | disk is always 20 GB and the swapdisk will depend on the |
      |                           | memory.                                                  |
      +---------------------------+----------------------------------------------------------+
      | nodeGroups.storage.type   | If "shared", virtual disks will be located on an NFS     |
      |                           | export. If "local", virtual disks will be located on     |
      |                           | disks directly attached to the ESXihosts.                |
      +---------------------------+----------------------------------------------------------+
      | nodeGroups.cpuNum         | Number of CPU cores assigned to the VM. This can be      |
      |                           | changed after the cluster has been deployed.             |
      +---------------------------+----------------------------------------------------------+
      | nodeGroups.memCapacityMB  | Amount of RAM assigned to the VM. This can be changed    |
      |                           | after the cluster has been deployed.                     |
      +---------------------------+----------------------------------------------------------+
      | nodeGroups.rpNames        | Resource pool name. For available names, type            |
      |                           | "resourcepool list" in the Serengeti CLI.                |
      +---------------------------+----------------------------------------------------------+

    *For more details, refer to the BDE documentation.*

#. Login to the Serengeti CLI.

#. If you want to use a dedicated |hadoop-manager| server, create the |hadoop-manager| cluster.

   .. parsed-literal::

      serengeti>\ **cluster create --name hadoopmanager \\
      --specFile basic-server.json --password 1 --networkName defaultNetwork**
      Hint: Password are from 8 to 128 characters, and can include
      alphanumeric characters ([0-9, a-z, A-Z]) and the following special
      characters: _, @, #, $, %, ^, &, *
      Enter the password: **\*\*\***
      Confirm the password: **\*\*\***

      COMPLETED 100%
      node group: server,  instance number: 1
      roles:[basic]
        NAME                     IP              STATUS         TASK
        ------------------------------------------------------------
        hadoopmanager-server-0  10.111.128.240  Service Ready
      cluster hadoopmanager created

  .. note::

    If any errors occur during cluster creation, you can try to
    resume the cluster creation with the --resume parameter. If that does
    not work, you may need to delete and recreate the cluster. For example:

    .. parsed-literal::

      serengeti>\ **cluster create --name mycluster1 --resume**
      serengeti>\ **cluster delete --name mycluster1**

5.  Create the Hadoop cluster.

    .. parsed-literal::

      serengeti>\ **cluster create --name mycluster1 --specFile mycluster1-bde.json \\
      --password 1 --networkName defaultNetwork**
      Hint: Password are from 8 to 128 characters, and can include
      alphanumeric characters ([0-9, a-z, A-Z]) and the following special
      characters: _, @, #, $, %, ^, &, *
      Enter the password: **\*\*\***
      Confirm the password: **\*\*\***

      COMPLETED 100%
      node group: namenode,  instance number: 1
      roles:[basic]
        NAME                   IP              STATUS         TASK
        ----------------------------------------------------------
        mycluster1-namenode-0  10.111.128.241  Service Ready     
      node group: worker,  instance number: 3
      roles:[basic]
        NAME                 IP              STATUS         TASK
        --------------------------------------------------------
        mycluster1-worker-0  10.111.128.244  Service Ready     
        mycluster1-worker-1  10.111.128.242  Service Ready     
        mycluster1-worker-2  10.111.128.245  Service Ready     
      node group: master,  instance number: 1
      roles:[basic]
        NAME                 IP              STATUS         TASK
        --------------------------------------------------------
        mycluster1-master-0  10.111.128.243  Service Ready     
      cluster mycluster1 created

#.  After the cluster has been provisioned, you should check the following:

    #.  The VMs should be distributed across your hosts evenly.

    #.  The data disks (not including the boot and swap disk) should be
        an equal size and distributed across datastores evenly.

BDE Post Deployment Script
--------------------------

Once the VMs come up, there are a few customizations that you will want
to make. The Python script
isilon-hadoop-tools/bde/bde\_cluster\_post\_deploy.py automates this
process.

This script performs the following actions:

- Retrieves the list of VMs in the BDE cluster.

- Writes a file consisting of the FQDNs of each VM. This will
  be used to script other cluster-wide activities.

- Enables password-less SSH to each VM.

- Updates /etc/sysconfig/network to set DHCP\_HOSTNAME instead
  of HOSTNAME and restarts the network service. With properly configured
  DHCP and DNS, this will result in correct forward and reverse DNS
  records with FQDNs such as mycluster1-worker-0.lab.example.com.

- Installs several packages using Yum.

- Mounts NFS directories.

- Mounts each virtual data disk in /data/*n*.

- Overwrites /etc/rc.local and /etc/sysctl.conf with
  recommended parameters.

To run the script, follow these steps:

#.  Login to your workstation (shown as user\@workstation in the prompts below).

#.  Ensure that you are running a Python version 2.6.6 or higher but less than 3.0.

    .. parsed-literal::

      [user\@workstation ~]$ **python --version**
      Python 2.6.6

#. If you do not have sshpass installed, you may install it on Centos 6.x using the following commands:

   .. parsed-literal::

    [root\@workstation ~]$ **wget \\
    http://dl.fedoraproject.org/pub/epel/6/x86_64/sshpass-1.05-1.el6.x86_64.rpm**
    [root\@workstation ~]$ **rpm -i sshpass-1.05-1.el6.x86\_64.rpm**

#. If you have not previously created your SSH key, run the following.

   .. parsed-literal::

    [user\@workstation ~]$ **ssh-keygen -t rsa**

#. Copy the file isilon-hadoop-tools/etc/template-\ |hsk_dst|\ -post.json to isilon-hadoop-tools/etc/mycluster1-post.json.

#.  Edit the file mycluster1-post.json with parameters that apply to your environment.

    .. table:: Description of mycluster1-post.json

      +--------------------------+-----------------------------------------------------------+
      | Field Name               | Description                                               |
      +==========================+===========================================================+
      | ser\_host                | The URL to the BDE web service. For example:              |
      |                          | \https://bde.lab.example.com:8443                         |
      +--------------------------+-----------------------------------------------------------+
      | ser\_username            | The user name used to authenticate to the BDE web         |
      |                          | service. This is the same account used to login using the |
      |                          | Serengeti CLI.                                            |
      +--------------------------+-----------------------------------------------------------+
      | ser\_password            | The password for the above account.                       |
      +--------------------------+-----------------------------------------------------------+
      | skip\_configure\_network | If "false" (the default), the script will set the         |
      |                          | DHCP\_HOSTNAME parameter on the host. If "false", you     |
      |                          | must also set the dhcp\_domain setting in this file. Set  |
      |                          | to "true" if you are using static IP addresses or DHCP    |
      |                          | without DNS integration.                                  |
      +--------------------------+-----------------------------------------------------------+
      | dhcp\_domain             | This is the DNS suffix that is appended to the host name  |
      |                          | to create a FQDN. It should begin with a dot. Ignored if  |
      |                          | skip\_configure\_network is true. For example:            |
      |                          | .lab.example.com                                          |
      +--------------------------+-----------------------------------------------------------+
      | cluster\_name            | This is the name of the BDE cluster.                      |
      +--------------------------+-----------------------------------------------------------+
      | host\_file\_name         | This file will be created and it will contain the FQDN of |
      |                          | each host in the BDE cluster.                             |
      +--------------------------+-----------------------------------------------------------+
      | node\_password           | This is the root password of the hosts created by BDE.    |
      |                          | This was specified when the cluster was created.          |
      +--------------------------+-----------------------------------------------------------+
      | name\_filter\_regex      | If non-empty, specify the name of a single host in your   |
      |                          | BDE cluster to apply this script to just a single host.   |
      +--------------------------+-----------------------------------------------------------+
      | tools\_root              | This is the fully-qualified path to the Isilon Hadoop     |
      |                          | Tools. It must be in an NFS mount.                        |
      +--------------------------+-----------------------------------------------------------+
      | nfs\_mounts              | This is a list of one or more NFS mounts that will be     |
      |                          | imported on each host in the BDE cluster.                 |
      +--------------------------+-----------------------------------------------------------+
      | nfs\_mounts.mount\_point | NFS mount point. For example: /mnt/isiloncluster1         |
      +--------------------------+-----------------------------------------------------------+
      | nfs\_mounts.path         | NFS path. For example: host.domain.com:/directory         |
      +--------------------------+-----------------------------------------------------------+
      | ssh\_commands            | This is a list of commands that will be executed on each  |
      |                          | host. This can be used to run scripts that will create    |
      |                          | users, adjust mount points, etc..                         |
      +--------------------------+-----------------------------------------------------------+

#.  Edit the file isilon-hadoop-tools/bde/create\_\ |hsk_dst|\ \_users.sh with
    the appropriate gid\_base and uid\_base values. This should match the
    values entered in
    isilon-hadoop-tools/onefs/isilon\_create\_\ |hsk_dst|\ \_users.sh in a previous
    step.

#.  Run bde\_cluster\_post\_deploy.py:

    .. parsed-literal::

      [user\@workstation ~]$ **cd /mnt/scripts/isilon-hadoop-tools**
      [user\@workstation isilon-hadoop-tools]$ **bde/bde\_cluster\_post\_deploy.py \\
      etc/mycluster1-post.json**
      ...
      Success!

#.  Repeat the above steps for your |hadoop-manager| cluster named *hadoopmanager*.

Resize Root Disk
----------------

By default, the / (root) partition size for a VM created by BDE is 20
GB. This is sufficient for a Hadoop worker but should be increased for
the your |hadoop-manager| (*hadoopmanager-server-0*) and the master node
(*mycluster1-master-0*). Follow the steps below on each of these nodes.

#.  Remove old data disk.

    #.  Edit /etc/fstab.

        .. parsed-literal::

          [root\@mycluster1-master-0 ~]# **vi /etc/fstab**

    #.  Remove line containing "/dev/sdc1", save the file, and then unmount it.

        .. parsed-literal::

          [root\@mycluster1-master-0 ~]# **umount /dev/sdc1**
          [root\@mycluster1-master-0 ~]# **rmdir /data/1**

    #.  Shutdown the VM.

    #.  Use the vSphere Web Client to remove virtual disk 3.

#.  Use the vSphere Web Client to increase the size of virtual disk 1 to 250 GB.

#.  Power on the VM and SSH into it.

#.  Extend the partition.

    .. warning::

      Perform the steps below very carefully. Failure performing these steps may
      result in an unusable system or lost data.

    .. parsed-literal::

      [root\@mycluster1-master-0 ~]# **fdisk /dev/sda**
      WARNING: DOS-compatible mode is deprecated. It's strongly recommended to
               switch off the mode (command 'c') and change display units to
               sectors (command 'u').
      Command (m for help): **d**
      Partition number (1-4): **3**
      Command (m for help): **n**
      Command action
         e   extended
         p   primary partition (1-4)
      **p**
      Partition number (1-4): **3**
      First cylinder (33-32635, default 33):
      Using default value 33
      Last cylinder, +cylinders or +size{K,M,G} (33-32635, default 32635):
      Using default value 32635
      Command (m for help): **w**
      The partition table has been altered!
      Calling ioctl() to re-read partition table.
      WARNING: Re-reading the partition table failed with error 16: Device or
      resource busy.
      The kernel still uses the old table. The new table will be used at
      the next reboot or after you run partprobe(8) or kpartx(8)
      Syncing disks.
      [root\@mycluster1-master-0 ~]# **reboot**

#.  After the server reboots, resize the file system.

    .. parsed-literal::

     [root\@mycluster1-master-0 ~]# **resize2fs /dev/sda3**

Fill Disk
---------

VMware Big Data Extensions creates VMDKs for each of the Hadoop server.
In an Isilon environment, these VMDKs are not used for HDFS, of course,
but large jobs that spill temporary intermediate data to local disks
will utilize the VMDKs. BDE creates VMDKs that are lazy-zeroed. This
means that the VMDKs are created very quickly but the drawback is that
the first write to each sector of the virtual disk is significantly
slower than subsequent writes to the same sector. This means that
optimal VMDK performance may not be achieved until after several days of
normal usage. To accelerate this, you can run the script fill\_disk.py.
This script will create a temporary file on each drive on each Hadoop
server. The file will grow until the disk runs out of space, then the
file will be deleted.

To use the script, provide it with file containing a list of Hadoop
server FQDNs.

.. parsed-literal::

  [user\@workstation etc]$ **/mnt/scripts/isilon-hadoop-tools/bde/fill\_disk.py \\
  mycluster1-hosts.txt**

Resizing Your Cluster
---------------------

VMware Big Data Extensions can be used to resize an existing cluster. It
will allow you to create additional VMs, change the amount RAM for each
VM, and change the number of CPUs for each VM. This can be done through
the vSphere Web Client or from the Serengeti CLI using the "cluster
resize" command. For instance:

.. parsed-literal::

  serengeti>\ **cluster resize --name mycluster1 --nodeGroup worker \\
  --instanceNum 20**
  serengeti>\ **cluster resize --name mycluster1 --nodeGroup worker \\
  --cpuNumPerNode 16 --memCapacityMbPerNode 131072**

After creating new VMs, you will want to run the BDE Post Deployment
script and the Fill Disk script on the new nodes. Then use |hadoop-manager|
to deploy the appropriate Hadoop components.

When changing the CPUs and RAM, you will usually want to change the
amount allocated for YARN or your other services using your Hadoop cluster manager.
