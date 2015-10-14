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
  
.. note::

  Starting with OneFS 8.0.0.0 some commands have changed.  Any
  differences in syntax or approach are called out in separate code 
  blocks.  Please follow the syntax for your version.

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

For OneFS 7.2.x.x
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

For OneFS 8.x.x.x
.. parsed-literal::

	isiloncluster1-1# isi zone zones list
	Name   Path
	------------
	System /ifs
	------------
	Total: 1
	
	isiloncluster1-1# **isi network pools list -v**
                          ID: groupnet0.subnet0.pool0
                    Groupnet: groupnet0
                      Subnet: subnet0
                        Name: pool0
                       Rules: rule0
                 Access Zone: System
           Allocation Method: static
            Aggregation Mode: lacp
          SC Suspended Nodes: -
                 Description: Initial 10gige-1 pool
                      Ifaces: 1:10gige-1
                   IP Ranges: 10.111.129.115-10.111.129.126
            Rebalance Policy: auto
     SC Auto Unsuspend Delay: 0
           SC Connect Policy: round_robin
                     SC Zone:
         SC DNS Zone Aliases: -
          SC Failover Policy: round_robin
                   SC Subnet: -
                      SC Ttl: 0
               Static Routes: -

Alternatively, using the OneFS UI in OneFS 8.x.x.x
|image33|

To create a new access zone and an associated IP address pool:

For OneFS 7.2.x.x
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

For OneFS 8.x.x.x
.. parsed-literal::

	isiloncluster1-1# **mkdir -p /ifs/isiloncluster1/zone1**
	isiloncluster1-1# **isi zone zones create --name zone1 \\
	--path /ifs/isiloncluster1/zone1**
	isiloncluster1-1# **isi network pools create groupnet0.subnet0.pool1 --ranges \\
	10.111.129.127-10.111.129.138 --ifaces 1-4:10gige-1 --access-zone zone1 \\
	--sc-dns-zone subnet0-pool1.isiloncluster1.lab.example.com\\
	--sc-subnet subnet0 --alloc-method dynamic**
	isiloncluster1-1# **isi network pool list**
	ID                      SC Zone                                      Allocation Method
	---------------------------------------------------------------------------------------
	groupnet0.subnet0.pool0                                              static
	groupnet0.subnet0.pool1 subnet0-pool1.isiloncluster1.lab.example.com dynamic
	---------------------------------------------------------------------------------------
	Total: 2

Alternatively using the OneFS Web UI in OneFS 8.x.x.x

Create the Access Zone, Declare the root, make sure to check "Create zone base directory."
|image34|

Create your IP Pool and bind it to your new Access Zone.  Then scroll down in the wizard
window before you commit "Add Pool."
|image35|

Now add your zone name, choose the dynamic allocation method, and then hit "Add Pool."
|image36|

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

Alternatively if using OneFS 8.x.x.x you can accomplish this in the Web Interface
|image37|

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
    \https://\ *isilon\_node\_ip\_address*:8080, where
    *isilon\_node\_ip\_address* is any IP address on any Isilon node that is in
    the System access zone. This usually corresponds to the ext-1
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

For OneFS 7.x.x.x
   .. parsed-literal::

    isiloncluster1-1# **isi license**
    Module                    License Status    Configuration     Expiration Date
    ------                    --------------    -------------     ---------------
    HDFS                      Evaluation        Not Configured    September 4, 2014
	
For OneFS 8.x.x.x you may use either the command below OR accomplish this in the OneFS WebUI
   .. parsed-literal::
   
   isiloncluster1-1# isi license view --name HDFS
         Name: HDFS
       Status: Activated
   Expiration: - 

#.  Create the HDFS root directory. This is usually called *hadoop* and
    must be within the access zone directory.

    .. parsed-literal::

      isiloncluster1-1# **mkdir -p /ifs/isiloncluster1/zone1/hadoop**
	  
	Alternatively all of the CLI steps below can be accomplished in the OneFS WEbUI if using
	OneFS 8.x.x.x
	|image38|

#.  Set the HDFS root directory for the access zone.  The HDFS root can either be the root of the
    Access Zone or it can be a subfolder in the Access Zone's folder tree.
   
   For OneFS 7.x.x.x
    .. parsed-literal::

      isiloncluster1-1# **isi zone zones modify zone1 \\
      --hdfs-root-directory /ifs/isiloncluster1/zone1/hadoop**
	  
   For OneFS 8.x.x.x
	.. parsed-literal::
	
	  isiloncluster1-1# **isi hdfs settings modify --zone=zone1 \\
	  --root-directory=/ifs/isiloncluster1/zone1/hadoop**

#.  Increase the HDFS daemon thread count.  **This is no longer required with OneFS 8.x.x.x**

	For OneFS 7.x.x.x Only
    .. parsed-literal::

      isiloncluster1-1# **isi hdfs settings modify --server-threads 256**

#.  Set the HDFS block size used for reading from Isilon.

	For OneFS 7.x.x.x
    .. parsed-literal::

      isiloncluster1-1# **isi hdfs settings modify --default-block-size 128M**
	  
	For OneFS 8.x.x.x
	.. Parsed-literal::
	  isiloncluster1-1# **isi hdfs settings modify --zone=zone1 --default-block-size=128M**

#.  Create an indicator file so that we can easily determine when we are looking your Isilon cluster via HDFS.
    No matter the OneFS version the steps below will use the OneFS command line.
    
    .. parsed-literal::

      isiloncluster1-1# **touch \\
      /ifs/isiloncluster1/zone1/hadoop/THIS\_IS\_ISILON\_isiloncluster1\_zone1**

#.  Extract the Isilon Hadoop Tools to your Isilon cluster. 
    This can be placed in any directory under /ifs.
    It is recommended to use /ifs/*isiloncluster1*/scripts where *isiloncluster1* is the name
    of your Isilon cluster.

    .. parsed-literal::

      [user\@workstation ~]$ **scp isilon-hadoop-tools-x.x.tar.gz \\
      root\@isilon\_node\_ip\_address:/ifs/isiloncluster1/scripts**

      isiloncluster1-1# **tar -xzvf \\
      /ifs/isiloncluster1/isilon-hadoop-tools-x.x.tar.gz \\
      -C /ifs/isiloncluster1/scripts**

      isiloncluster1-1# **mv /ifs/isiloncluster1/scripts/isilon-hadoop-tools-x.x \\
      /ifs/isiloncluster1/scripts/isilon-hadoop-tools**


#.  Execute the script isilon\_create\_users.sh.
    This script will create all required users and groups for the Hadoop services
    and applications.

    .. warning::

      The script isilon\_create\_users.sh will create local
      user and group accounts on your Isilon cluster for Hadoop services. If you are using a
      directory service such as Active Directory, and you want these users and
      groups to be defined in your directory service, then DO NOT run this
      script. Instead, refer to the OneFS documentation and `EMC
      Isilon Best Practices for Hadoop Data
      Storage <http://www.emc.com/collateral/white-paper/h12877-wp-emc-isilon-hadoop-best-practices.pdf>`__.  
      
    Script Usage: isilon\_create\_users.sh --dist <DIST> [--startgid <GID>] [--startuid <UID>] [--zone <ZONE>]

    dist
      This will correspond to your Hadoop distribution - |hsk_dst|

    startgid
      Group IDs will begin with this value. For example: 501

    startuid
      User IDs will begin with this value. This is generally the same as gid_base. For example: 501

    zone
      Access Zone name. For example: System

    .. parsed-literal::

      isiloncluster1-1# **bash \\
      /ifs/isiloncluster1/scripts/isilon-hadoop-tools/onefs/isilon\_create\_users.sh \\
      --dist** |hsk_dst_strong| **--startgid 501 --startuid 501 --zone zone1**

#.  Execute the script isilon\_create\_directories.sh.
    This script will create all required directories with the appropriate ownership and permissions.

    Script Usage: isilon\_create\_directories.sh --dist <DIST> [--fixperm] [--zone <ZONE>]

    dist
      This will correspond to your Hadoop distribution - |hsk_dst|

    fixperm
      If specified, ownership and permissions will be set on existing directories.

    zone
      Access Zone name. For example: System

    .. parsed-literal::

      isiloncluster1-1# **bash \\
      /ifs/isiloncluster1/scripts/isilon-hadoop-tools/onefs/isilon\_create\_directories.sh \\
      --dist** |hsk_dst_strong| **--fixperm --zone zone1**


#.  Map the *hdfs* user to the Isilon superuser. This will allow the
    *hdfs* user to chown (change ownership of) all files.

    .. warning::

      The command below will restart the HDFS service on Isilon to ensure
      that any cached user mapping rules are flushed. This will temporarily
      interrupt any HDFS connections coming from other Hadoop clusters.

    .. parsed-literal::

      isiloncluster1-1# **isi zone zones modify --user-mapping-rules="hdfs=>root" \\
      --zone zone1**
      isiloncluster1-1# **isi services isi\_hdfs\_d disable ; \\
      isi services isi\_hdfs\_d enable**
      The service 'isi\_hdfs\_d' has been disabled.
      The service 'isi\_hdfs\_d' has been enabled.
