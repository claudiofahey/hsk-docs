
.. The following substitutions are used by the common documents.

.. |hsk_dst| replace:: phd
.. |hsk_dst_strong| replace:: **phd**
.. |hadoop-manager| replace:: Pivotal Command Center
.. |hadoop-mapreduce-examples-jar| replace:: **/usr/lib/gphd/hadoop-mapreduce/hadoop-mapreduce-examples.jar**


****************************************************************************
EMC Isilon Hadoop Starter Kit for Pivotal HD 2.x with VMware Big Data Extensions
****************************************************************************

This document describes how to create a Hadoop environment utilizing
Pivotal HD and an EMC Isilon Scale-Out NAS for HDFS accessible
shared storage. VMware Big Data Extensions is used to provision and
manage the compute resources.

#RememberRuddy

.. note::
  The latest version of this document is available at http://hsk-phd.readthedocs.org/.

Introduction
============

IDC published an update to their Digital Universe study in December 2012
and found that the rate of digital data creation is not only continuing
to grow, but the rate is actually accelerating. By the end of this
decade we will create 40 Zettabytes of new digital information yearly or
the equivalent of 1.7MB of digital information for every man, woman, and
child every second of every day.

This information explosion is creating new opportunities for our
businesses to leverage digital information to serve their customers
better, faster, and most cost effectively through Big Data Analytics
applications.  Hadoop technologies can be cost effective solutions and
can manage structured, semi-structured and unstructured data unlike
traditional solutions such as RDBMS. The need to track and analyze
consumer behavior, maintain inventory and space, target marketing offers
on the basis of consumer preferences and attract and retain consumers,
are some of the factors pushing the demand for Big Data Analytics
solutions using Hadoop technologies. According to a new market report
published by Transparency Market Research
(http://www.transparencymarketresearch.com) "Hadoop Market - Global
Industry Analysis, Size, Share, Growth, Trends, and Forecast, 2012-
2018," the global Hadoop market was worth USD 1.5 billion in 2012 and is
expected to reach USD 20.9 billion in 2018, growing at a CAGR of 54.7%
from 2012 to 2018.

Hadoop like any new technology can be time consuming, and expensive for
our customers to get deployed and operational. When we surveyed a number
of our customers, two main challenges were identified to getting
started: confusion over which Hadoop distribution to use and how to
deploy using existing IT assets and knowledge. Hadoop software is
distributed by several vendors including Pivotal, Hortonworks, and
Cloudera with proprietary extensions. In addition to these
distributions, Apache distributes a free open source version. From an
infrastructure perspective many Hadoop deployments start outside the IT
data center and do not leverage the existing IT automation, storage
efficiency, and protection capabilities. Many customers cited the time
it took IT to deploy Hadoop as the primary reason to start with a
deployment outside of IT.

This guide is intended to simplify Hadoop deployments by creating a
shared storage model with EMC Isilon scale out NAS and Pivotal HD,
reduce the time to
deployment, and the cost of deployment leveraging
tools that can automate Hadoop cluster deployments.

Audience
--------

This document is intended for IT program managers, IT architects,
Developers, and IT management to easily deploy Hadoop with
automation tools and leverage EMC Isilon for HDFS shared storage. It can
be used by somebody who does not yet have an EMC Isilon cluster by
downloading the free EMC Isilon OneFS Simulator which can be installed
as a virtual machine for testing and training. However, this document
can also be used by somebody who will be installing in a production
environment as best-practices are followed whenever possible.


.. include:: ../common/apache-hadoop-projects.rst


Pivotal HD with HAWQ
--------------------

Open-source Hadoop frameworks have rapidly emerged as preferred technology to
grapple with the explosion of structured and unstructured big data. You can accelerate
your Hadoop investment with an enterprise-ready, fully supported Hadoop distribution
that ensures you can harness—and quickly gain insight from—the massive data being driven
by new apps, systems, machines, and the torrent of customer sources.

HAWQ™ adds SQL’s expressive power to Hadoop to accelerate data analytics
projects, simplify development while increasing productivity, expand Hadoop’s
capabilities and cut costs. HAWQ can help your organization render Hadoop
queries faster than any Hadoop-based query interface on the market by adding
rich, proven, parallel SQL processing facilities. HAWQ leverages your existing
business intelligence products, analytic products, and your workforce’s SQL skills
to bring more than 100X performance improvement (in some cases up to 600X) to a wide
range of query types and workloads. The world’s fastest SQL query engine on Hadoop,
HAWQ is 100 percent SQL compliant.

The first true SQL processing for enterprise-ready Hadoop, Pivotal HD with HAWQ
is available to you as software only or as an appliance-based solution.

More information on Pivotal HD and HAWQ can be found on http://www.pivotal.io/big-data/pivotal-hd.


.. include:: ../common/intro-isilon.rst


Environment
===========

Versions
--------

The test environment used for this document consists of the following
software versions:

* Pivotal HD 2.1.0
* Pivotal Command Center 2.3.0
* Pivotal HAWQ 1.2.1.0
* Isilon OneFS 7.2.0
* VMware vSphere Enterprise 5.5.0
* VMware Big Data Extensions 2.0
 

.. include:: ../common/environment-hosts.rst


Installation Overview
=====================

Below is the overview of the installation process that this document
will describe.

#. Confirm prerequisites.

#. Prepare your network infrastructure including DNS and DHCP.

#. Prepare your Isilon cluster.

#. Prepare VMware Big Data Extensions (BDE).

#. Use BDE to provision multiple virtual machines.

#. Install Pivotal Command Center.

#. Use Pivotal Command Center to deploy Pivotal HD to the virtual machines.

#. Initialize HAWQ.

#. Perform key functional tests.


.. include:: ../common/prereq.rst

.. include:: ../common/prepare-network-infrastructure.rst

.. include:: ../common/prepare-isilon-1.rst

.. include:: ../common/create-dns-records-for-isilon.rst

.. include:: ../common/prepare-nfs-clients.rst

.. include:: ../common/prepare-bde.rst

.. include:: ../common/prepare-hadoop-vm.rst


Install Pivotal Command Center
==============================

.. note::
  The steps below will walk you through one way of installing Pivotal Command Center and Pivotal HD.
  This is intended to guide you through your first POC.
  In particular, Kerberos security is **not** enabled.
  For complete details, refer to the Pivotal HD documentation
  (http://pivotalhd.docs.pivotal.io/doc/2100/index.html).

#.  Download the following files from https://network.pivotal.io/products/pivotal-hd.
    This document assumes they have been downloaded to your Isilon cluster in
    /mnt/scripts/downloads

    -  PHD 2.1.0
    -  PHD 2.1.0: Pivotal Command Center 2.3.0
    -  PHD 2.1.0: Pivotal HAWQ 1.2.1.0 (optional)

#.  Extract Pivotal Command Center and install it.

    .. parsed-literal::

      [root\@hadoopmanager-server-0 ~]# **mkdir phd**
      [root\@hadoopmanager-server-0 ~]# **cd phd**
      [root\@hadoopmanager-server-0 phd]# **tar --no-same-owner -zxvf \\
      /mnt/scripts/downloads/PCC-2.3.0-443.x86_64.tgz**
      [root\@hadoopmanager-server-0 phd]# **cd PCC-2.3.0-443**
      [root\@hadoopmanager-server-0 PCC-2.3.0-443]# **./install**
      You may find the logs in /usr/local/pivotal-cc/pcc_installation.log
      Performing pre-install checks ...                          [  OK  ]
      [INFO]: User gpadmin does not exist. It will be created as part of the
      installation process.
      [INFO]: By default, the directory '/home/gpadmin' is created as the default
      home directory for the gpadmin user. This directory must must be consistent
      across all nodes.
      Do you wish to use the default home directory? [Yy|Nn]: **y**
      [INFO]: Continuing with default /home/gpadmin as home directory for gpadmin
      ...
      You have successfully installed Pivotal Command Center 2.3.0.
      You now need to install a PHD cluster to monitor with Pivotal Command
      Center.
      You can view your cluster statuses here:
      \https://hadoopmanager-server-0.lab.example.com:5443/status
      [root\@hadoopmanager-server-0 PCC-2.3.0-443]# **service commander status**
      nodeagent is running
      Jetty is running
      httpd is running
      Pivotal Command Center HTTPS is running
      Pivotal Command Center Background Worker is running

#.  Import packages into Pivotal Command Center.

    .. parsed-literal::

      [root\@hadoopmanager-server-0 ~]# su - gpadmin
      [gpadmin\@hadoopmanager-server-0 ~] -bash-4.1$ **tar zxf \\
      /mnt/scripts/downloads/PHD-2.1.0.0-175.tgz**
      [gpadmin\@hadoopmanager-server-0 ~] -bash-4.1$ **tar zxf \\
      /mnt/scripts/downloads/PADS-1.2.1.0-10335.tgz**
      [gpadmin\@hadoopmanager-server-0 ~] -bash-4.1$ **icm_client import -s \\
      PHD-2.1.0.0-175/**
      stack: PHD-2.1.0.0
      [INFO] Importing stack
      [INFO] Finding and copying available stack rpms from PHD-2.1.0.0-175/... [OK]
      [INFO] Creating local stack repository...
      [OK]
      [INFO] Import complete
      [gpadmin\@hadoopmanager-server-0 ~] -bash-4.1$ **icm_client import -s \\
      PADS-1.2.1.0-10335/**
      stack: PADS-1.2.1.0
      [INFO] Importing stack
      [INFO] Finding and copying available stack rpms from PADS-1.2.1.0-10335/...
      [OK]
      [INFO] Creating local stack repository...
      [OK]
      [INFO] Import complete


Deploy a Pivotal HD Cluster
===========================

#.  Make a copy of the cluster configuration template directory.

    .. parsed-literal::

      [gpadmin\@hadoopmanager-server-0 ~] -bash-4.1$ **cd \\
      /mnt/scripts/isilon-hadoop-tools/etc**
      [gpadmin\@hadoopmanager-server-0 etc] -bash-4.1$ **cp -rv template-pcc \\
      mycluster1-pcc**

#.  Edit mycluster1-pcc/clusterConfig.xml.

    #.  Replace all occurances of *mycluster1* with your actual BDE cluster name. This will
        identify your host names.

    #.  Replace the value of the *url* element within *isi-hdfs* with your Isilon HDFS URL.
        For example. ``hdfs://mycluster1-hdfs.lab.example.com:8020``.

    #.  Update *yarn-nodemanager*, *hawq-segment*, and *pxf-service* elements with the complete list
        of worker host names. You may copy and paste from the file
        isilon-hadoop-tools/etc/mycluster1-hosts.txt.
        Do *not* include your master node in these lists.

    #.  Update *datanode.disk.mount.points* so that it refers to the local disks that you will use
        for temporary files. For example, if you deployed your VMs to ESXi hosts with 4 local disks,
        the value will be ``/data/1,/data/2,/data/3,/data/4``. You should confirm that these mounts
        points exists on your workers using the ``df`` command.

    #.  Update *yarn.nodemanager.resource.memory-mb* with the maximum number of MB that you will
        allow YARN applications to use on your worker nodes.
        You must ensure that the machine has enough RAM for the OS, Hadoop services, YARN applications, and HAWQ.
        Usually 12 GB less than the machine RAM is recommended. You may need to reduce this further
        if you are using multiple HAWQ segments.

    #.  If you want to run more than one HAWQ segment per worker node, update *hawq.segment.directory*. For example,
        to run two HAWQ segments, the value can be ``(/data/1/primary /data/2/primary)``.

    For complete details, refer to http://pivotalhd.docs.pivotal.io/doc/2100/EditingtheClusterConfigurationFiles.html.

#.  Deploy your cluster.

    .. parsed-literal::

      [gpadmin\@hadoopmanager-server-0 etc] -bash-4.1$ **icm_client deploy \\
      --confdir mycluster1-pcc --selinuxoff --iptablesoff**
      Please enter the root password for the cluster nodes: **\*\*\***
      PCC creates a gpadmin user on the newly added cluster nodes (if any).
      Please enter a non-empty password to be used for the gpadmin user: **\*\*\***
      Verifying input
      Starting install
      [==================================================================] 100%
      Results:
      mycluster1-hdfs.lab.example.com... [Success]
      mycluster1-worker-1.lab.example.com... [Success]
      mycluster1-master-0.lab.example.com... [Success]
      mycluster1-worker-2.lab.example.com... [Success]
      mycluster1-worker-0.lab.example.com... [Success]
      Details at /var/log/gphd/gphdmgr/gphdmgr-webservices.log
      Cluster ID: 5

#.  Start your cluster.

    .. parsed-literal::

      [gpadmin\@hadoopmanager-server-0 etc] -bash-4.1$ **icm_client start \\
      --clustername mycluster1**
      Starting services
      Starting cluster
      [==================================================================] 100%
      Results:
      Details at /var/log/gphd/gphdmgr/gphdmgr-webservices.log


Initialize HAWQ
===============

#.  Initialize HAWQ.

    .. parsed-literal::

      [gpadmin\@mycluster1-master-0 ~]$ **source /usr/local/hawq/greenplum_path.sh**
      [gpadmin\@mycluster1-master-0 ~]$ **gpssh-exkeys -f \\
      /mnt/scripts/isilon-hadoop-tools/etc/mycluster1-hosts.txt**
      [STEP 1 of 5] create local ID and authorize on local host

      [STEP 2 of 5] keyscan all hosts and update known_hosts file

      [STEP 3 of 5] authorize current user on remote hosts
        ... send to mycluster1-worker-0.lab.example.com
        ***
        *** Enter password for mycluster1-worker-0.lab.example.com: **\*\*\***
        ... send to mycluster1-worker-1.lab.example.com
        ... send to mycluster1-worker-2.lab.example.com

      [STEP 4 of 5] determine common authentication file content

      [STEP 5 of 5] copy authentication files to all remote hosts
        ... finished key exchange with mycluster1-worker-0.lab.example.com
        ... finished key exchange with mycluster1-worker-1.lab.example.com
        ... finished key exchange with mycluster1-worker-2.lab.example.com

      [INFO] completed successfully

      [gpadmin\@mycluster1-master-0 ~]$ **/etc/init.d/hawq init**
      20141009:06:05:35:009986 gpinitsystem:mycluster1-master-0:gpadmin-[INFO]:
      -Checking configuration parameters, please wait...
      ...
      20141009:06:06:55:009986 gpinitsystem:mycluster1-master-0:gpadmin-[INFO]:
      -HAWQ instance successfully created
      ...


.. include:: ../common/adding-a-hadoop-user.rst

.. include:: ../common/functional-tests.rst


HAWQ
----

.. parsed-literal::

  [gpadmin\@mycluster1-master-0 ~]$ **psql**
  psql (8.2.15)
  Type "help" for help.

  gpadmin=# **\\l**
                   List of databases
     Name    |  Owner  | Encoding | Access privileges
  -----------+---------+----------+-------------------
   gpadmin   | gpadmin | UTF8     |
   postgres  | gpadmin | UTF8     |
   template0 | gpadmin | UTF8     |
   template1 | gpadmin | UTF8     |
  (4 rows)

  gpadmin=# **\\c gpadmin**
  psql (8.4.20, server 8.2.15)
  WARNING: psql version 8.4, server version 8.2.
           Some psql features might not work.
  You are now connected to database "gpadmin".
  gpadmin=# **create table test (a int, b text);**
  NOTICE:  Table doesn't have 'DISTRIBUTED BY' clause -- Using column named 'a'
  as the Greenplum Database data distribution key for this table.
  HINT:  The 'DISTRIBUTED BY' clause determines the distribution of data. Make
  sure column(s) chosen are the optimal data distribution key to minimize skew.
  CREATE TABLE
  gpadmin=# **insert into test values (1, '435252345');**
  INSERT 0 1
  gpadmin=# **select * from test;**
   a |     b
  ---+-----------
   1 | 435252345
  (1 row)

  gpadmin=# **\\q**


Pivotal Command Center
----------------------

Browse to the Pivotal Command Center GUI
``https://hadoopmanager-server-0.lab.example.com:5443``.

Login using the following default account:

Username: gpadmin

Password: Gpadmin1


Additional Functional Tests
---------------------------

If you will be using other Hadoop components and applications, refer to
http://pivotalhd.docs.pivotal.io/doc/2100/RunningPHDSamplePrograms.html for additional functional tests.


.. include:: ../common/wikipedia.rst

.. include:: ../common/where-to-go-from-here.rst

.. include:: ../common/linux-tuning.rst

.. include:: ../common/odp-tuning.rst

.. include:: ../common/isilon-tuning.rst

.. include:: ../common/known-limitations.rst

.. include:: ../common/legal.rst

.. include:: ../common/references.rst

http://www.pivotal.io/

.. include:: ../common/substitutions.rst
