Prepare Isilon
==============

Assumptions
-----------

This document makes the assumptions listed below. These are not
necessarily requirements but they are usually valid and simplify the
process.

- It is assumed that you are not using a directory service such
  as Active Directory for Hadoop users and groups.

- It is assumed that you are not using Kerberos authentication
  for Hadoop.

SmartConnect For HDFS
---------------------

A best practices for HDFS on Isilon is to utilize two SmartConnect IP
address pools for each access zone. One IP address pool should be used
by Hadoop clients to connect to the HDFS name node service on Isilon and
it should use the dynamic IP allocation method to minimize connection
interruptions in the event that an Isilon node fails. Note that dyanamic
IP allocation requires a SmartConnect Advanced license. A Hadoop client
uses a specific SmartConnect IP address pool simply by using its zone
name (DNS name) in the HDFS URI (e.g.
hdfs://subnet0-pool1.isiloncluster1.lab.example.com:8020).

A second IP address pool should be used for HDFS data node connections
and it should use the static IP allocation method to ensure that data
node connections are balanced evenly among all Isilon nodes. To assign
specific SmartConnect IP address pools for data node connections, you
will use the "isi hdfs racks modify" command.

If IP addresses are limited and you have a SmartConnect Advanced
license, you may choose to use a single dynamic pool for name node and
data node connections. This may result in uneven utilization of Isilon
nodes.

If you do not have a SmartConnect Advanced license, you may choose to
use a single static pool for name node and data node connections. This
may result in some failed HDFS connections immediately after Isilon node
failures.

For more information, see `EMC Isilon Best Practices for Hadoop Data
Storage <http://www.emc.com/collateral/white-paper/h12877-wp-emc-isilon-hadoop-best-practices.pdf>`__.

OneFS Access Zones
------------------

Access zones on OneFS are a way to select a distinct configuration for
the OneFS cluster based on the IP address that the client connects to. 
For HDFS, this configuration includes authentication methods, HDFS root
path, and authentication providers (AD, LDAP, local, etc.).  By default,
OneFS includes a single access zone called System.

If you will only have a single Hadoop cluster connecting to your Isilon
cluster, then you can use the System access zone with no additional
configuration. However, to have more than one Hadoop cluster connect to
your Isilon cluster, it is best to have each Hadoop cluster connect to a
separate OneFS access zone. This will allow OneFS to present each Hadoop
cluster with its own HDFS namespace and an independent set of users.

For more information, see `Security and Compliance for Scale-out
Hadoop Data Lakes
<http://www.emc.com/collateral/white-paper/h13354-wp-security-compliance-scale-out-hadoop-data-lakes.pdf>`__.

To view your current list of access zones and the IP pools associated
with them:

.. parsed-literal::

    isiloncluster1-1# **isi zone zones list**
    Name   Path
    ------------
    System /ifs
    ------------
    Total: 1

    isiloncluster1-1# **isi networks list pools -v**
    subnet0:pool0
              In Subnet: subnet0
             Allocation: Static
                 Ranges: 1
                         10.111.129.115-10.111.129.126
        Pool Membership: 4
                         1:10gige-1 (up)
                         2:10gige-1 (up)
                         3:10gige-1 (up)
                         4:10gige-1 (up)
       Aggregation Mode: Link Aggregation Control Protocol (LACP)
            Access Zone: System (1)
           SmartConnect:                    
                         Suspended Nodes  : None
                         Auto Unsuspend ... 0
                         Zone             : subnet0-pool0.isiloncluster1.lab.example.com
                         Time to Live     : 0
                         Service Subnet   : subnet0
                         Connection Policy: Round Robin
                         Failover Policy  : Round Robin
                         Rebalance Policy : Automatic Failback

To create a new access zone and an associated IP address pool:

.. parsed-literal::

    isiloncluster1-1# **mkdir -p /ifs/isiloncluster1/zone1**
    isiloncluster1-1# **isi zone zones create --name zone1 \\
    --path /ifs/isiloncluster1/zone1**

    isiloncluster1-1# **isi networks create pool --name subnet0:pool1 \\
    --ranges 10.111.129.127-10.111.129.138 --ifaces 1-4:10gige-1 \\
    --access-zone zone1 --zone subnet0-pool1.isiloncluster1.lab.example.com \\
    --sc-subnet subnet0 --dynamic**

    Creating pool
    'subnet0:pool1':                                                   OK

    Saving:                                                                         
    OK

.. note::

  If you do not have a SmartConnect Advanced license, you will need to omit
  the --dynamic option.

To allow the new IP address pool to be used by data node connections:

.. parsed-literal::

    isiloncluster1-1# **isi hdfs racks create /rack0 --client-ip-ranges \\
    0.0.0.0-255.255.255.255**
    isiloncluster1-1# **isi hdfs racks modify /rack0 --add-ip-pools subnet0:pool1**
    isiloncluster1-1# **isi hdfs racks list**
    Name   Client IP Ranges        IP Pools    
    --------------------------------------------
    /rack0 0.0.0.0-255.255.255.255 subnet0:pool1
    --------------------------------------------
    Total: 1

Sharing Data Between Access Zones
---------------------------------

Access zones in OneFS provide a measure of multi-tenancy in
that data within one access zone cannot be accessed by another access
zone. In certain use cases, however, you may actually want to make the
same dataset available to more than one Hadoop cluster. This can be done
by using fully-qualified paths to refer to data in other access zones.

To use this approach, you will
configure your Hadoop jobs to simply access the datasets from a common
shared HDFS namespace. For instance, you would start with two independent
Hadoop clusters, each with its own access zone on Isilon. Then you can
add a 3\ :sup:`rd` access zone on Isilon, with its own IP addresses and
HDFS root, and containing a dataset that is shared with other Hadoop
clusters.

User and Group IDs
------------------

Isilon clusters and Hadoop servers each have their own mapping of user
IDs (uid) to user names and group IDs (gid) to group names. When Isilon
is used only for HDFS storage by the Hadoop servers, the IDs do not need
to match. This is due to the fact that the HDFS wire protocol only
refers to users and groups by their *names*, and never their numeric
IDs.

In contrast, the NFS wire protocol refers to users and groups by their
numeric IDs. Although NFS is rarely used in traditional Hadoop
environments, the high-performance, enterprise-class, and
POSIX-compatible NFS functionality of Isilon makes NFS a compelling
protocol for certain workflows. If you expect to use both NFS and HDFS
on your Isilon cluster (or simply want to be open to the possibility in
the future), it is highly recommended to maintain consistent names and
numeric IDs for all users and groups on Isilon and your Hadoop servers.
In a multi-tenant environment with multiple Hadoop clusters, numeric IDs
for users in different clusters should be distinct.

For instance, the user sqoop in Hadoop cluster A will have ID 610 and
this same ID will be used in the Isilon access zone for Hadoop cluster A
as well as every server in Hadoop cluster A. The user sqoop in Hadoop
cluster B will have ID 710 and this ID will be used in the Isilon access
zone for Hadoop cluster B as well as every server in Hadoop cluster B.

Configure Isilon For HDFS
-------------------------

.. note::

    In the steps below, replace *zone1* with ``System`` to use the default System access zone
    or you may specify the name of a new access zone that you previously created.
  
#.  Open a web browser to the your Isilon cluster's web administration
    page. If you don't know the URL, simply point your browser to
    https://\ *isilon\_node\_ip\_address*:8080, where
    *isilon\_node\_ip\_address* is any IP address on any Isilon node (except
    for InfiniBand addresses). This usually corresponds to the ext-1
    interface of any Isilon node.

    |image14|

#. Login with your root account. You specified the root password when
   you configured your first node using the console.

#. Check, and edit as necessary, your NTP settings. Click Cluster
   Management -> General Settings -> NTP.

  |image16|

#. SSH into any node in your Isilon cluster as root.

#. Confirm that your Isilon cluster is at OneFS version 7.1.1.0 or higher.
   
   .. parsed-literal::   

    isiloncluster1-1# **isi version**
    Isilon OneFS v7.1.1.0 ...

#. For OneFS version 7.1.1.0, you must have patch-130611 installed.
   You can view the list of patches you have installed with:

   .. parsed-literal::

    isiloncluster1-1# **isi pkg info**
    patch-130611:
      This patch allows clients to use
      version 2.4 of the Hadoop Distributed File System (HDFS)
      with an Isilon cluster.

#. Install the patch if needed:

   .. parsed-literal::

    [user\@workstation ~]$ **scp patch-130611.tgz root@mycluster1-hdfs:/tmp**
    isiloncluster1-1# **gunzip < /tmp/patch-130611.tgz \| tar -xvf -**
    isiloncluster1-1# **isi pkg install patch-130611.tar**
    Preparing to install the package...
    Checking the package for installation...
    Installing the package
    Committing the installation...
    Package successfully installed.

#. Verify your HDFS license.

   .. parsed-literal::

    isiloncluster1-1# **isi license**
    Module                    License Status    Configuration     Expiration Date
    ------                    --------------    -------------     ---------------
    HDFS                      Evaluation        Not Configured    September 4, 2014

#. Extract the Isilon Hadoop Tools to your Isilon cluster. This can
   be placed in any directory under /ifs. However, Isilon best-practices
   suggest /ifs/*isiloncluster1*/scripts where *isiloncluster1* is the name
   of your Isilon cluster.

   .. parsed-literal::

    [user\@workstation ~]$ **scp isilon-hadoop-tools-x.x.tar.gz \\
    root\@isilon\_node\_ip\_address:/ifs/isiloncluster1/scripts**

    isiloncluster1-1# **tar -xzvf \\
    /ifs/isiloncluster1/isilon-hadoop-tools-x.x.tar.gz \\
    -C /ifs/isiloncluster1/scripts**

    isiloncluster1-1# **mv /ifs/isiloncluster1/scripts/isilon-hadoop-tools-x.x \\
    /ifs/isiloncluster1/scripts/isilon-hadoop-tools**

#.  Create the HDFS root directory. This is usually called *hadoop* and
    must be within the access zone directory.

    .. parsed-literal::

      isiloncluster1-1# **mkdir -p /ifs/isiloncluster1/zone1/hadoop**

#.  Set the HDFS root directory for the access zone.
   
    .. parsed-literal::

      isiloncluster1-1# **isi zone zones modify zone1 \\
      --hdfs-root-directory /ifs/isiloncluster1/zone1/hadoop**

#.  Create an indicator file so that we can easily determine when we are looking your Isilon cluster via HDFS.
    
    .. parsed-literal::

      isiloncluster1-1# **touch \\
      /ifs/isiloncluster1/zone1/hadoop/THIS\_IS\_ISILON\_isiloncluster1\_zone1**
