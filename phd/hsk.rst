
.. The following substitutions are used by the common documents.

.. |hsk_dst| replace:: phd
.. |hsk_dst_strong| replace:: **phd**
.. |hadoop-manager| replace:: Pivotal Control Center
.. |hadoop-mapreduce-examples-jar| replace:: **/opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar**


****************************************************************************
EMC Isilon Hadoop Starter Kit for Pivotal HD with VMware Big Data Extensions
****************************************************************************

This document describes how to create a Hadoop environment utilizing
Cloudera Manager and an EMC Isilon Scale-Out NAS for HDFS accessible
shared storage. VMware Big Data Extensions is used to provision and
manage the compute resources.

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
shared storage model with EMC Isilon scale out NAS and using the
industry leader in Enterprise Hadoop, Cloudera, reduce the time to
deployment, and the cost of deployment leveraging Cloudera Manager
tool’s that can automate Hadoop cluster deployments.

Audience
--------

This document is intended for IT program managers, IT architects,
Developers, and IT management to easily deploy Cloudera Hadoop with
automation tools and leverage EMC Isilon for HDFS shared storage. It can
be used by somebody who does not yet have an EMC Isilon cluster by
downloading the free EMC Isilon OneFS Simulator which can be installed
as a virtual machine for testing and training. However, this document
can also be used by somebody who will be installing in a production
environment as best-practices are followed whenever possible.


.. include:: ../common/apache-hadoop-projects.rst


Cloudera CDH and Cloudera Manager
---------------------------------

CDH (Cloudera’s Distribution Including Apache Hadoop) is the world’s
most complete, tested, and widely deployed distribution of Apache
Hadoop. CDH is 100% open source and is the only Hadoop solution to
offer batch processing, interactive SQL, and interactive search as well
as enterprise-grade continuous availability. More enterprises have
downloaded CDH than all other distributions combined.

CDH delivers the core elements of Hadoop – scalable storage and
distributed computing – as well as all of the necessary enterprise
capabilities such as security, high availability and integration with a
broad range of hardware and software solutions

Cloudera Manager is the industry’s first and most sophisticated
management application for Apache Hadoop. Cloudera Manager sets the
standard for enterprise deployment by delivering granular visibility
into and control over every part of the Hadoop cluster — empowering
operators to improve performance, enhance quality of service, increase
compliance and reduce administrative costs.

Cloudera Manager is designed to make administration of Hadoop simple and
straightforward, at any scale. With Cloudera Manager, you can easily
deploy and centrally operate the complete Hadoop stack. The application
automates the installation process, reducing deployment time from weeks
to minutes; gives you a cluster-wide, real-time view of nodes and
services running; provides a single, central console to enact
configuration changes across your cluster; and incorporates a full range
of reporting and diagnostic tools to help you optimize performance and
utilization.

More information on Cloudera can be found on http://www.cloudera.com/.


.. include:: ../common/intro-isilon.rst


Cloudera and EMC Joint Support Statement
----------------------------------------

EMC Isilon and Cloudera are pleased to communicate a business
collaboration and intention to enable joint support for EMC Isilon
scale-out NAS and Cloudera Enterprise products to bring the value of
Cloudera Enterprise to customers using EMC Isilon storage.

EMC Isilon Scale-Out NAS storage for Hadoop currently supports the
Apache Hadoop Distributed File System (HDFS) protocol. CDH is 100% open
source and is the only Hadoop solution to offer batch processing,
interactive SQL and interactive search, as well as enterprise-grade
continuous availability.

EMC Isilon allows a customer to start using Hadoop now by using already
existing data thus eliminating extra copies and reducing associated
CAPEX costs for additional storage capacity. In addition, EMC Isilon is
the only Hadoop storage solution that allows you access to the data via
NAS (i.e. SMB) or HDFS protocols as well as providing a  POSIX-Compliant
file system for regulated environments.

EMC Isilon and Cloudera are now jointly working to support the following
two scenarios:

- Customers running Cloudera Enterprise on EMC Isilon NAS
  products.

  - Customers will be able to leverage the full Cloudera Enterprise offering
    on their existing data sets stored in EMC Isilon. Cloudera Enterprise is
    a subscription offering that combines CDH with Cloudera Manager for
    system management, Cloudera Navigator for data management, technical
    support, indemnity, and open source advocacy. Customers will be able to
    simplify storage management and reduce overall costs by managing storage
    and compute independently, with new server hardware purchases required
    only for additional compute in the case of an existing EMC Isilon
    installation.

- Customers wishing to integrate existing Cloudera Enterprise
  and EMC Isilon clusters.

  - Customers will be able to integrate existing EMC Isilon clusters with
    existing HDFS-storage based Cloudera Enterprise clusters by using
    existing Hadoop tools built for data movement. This scenario will allow
    customers to more easily ingest data into both systems, as well as
    enable use cases such as online or remote backup and disaster recovery.

EMC Isilon and Cloudera are currently working on product development and
support models, and intend to have a supported joint offering in the
market in the first half of 2014.

In addition, EMC Isilon and Cloudera are working together to advance the
ongoing joint roadmap for Cloudera Enterprise on EMC Isilon Scale-Out
NAS for subsequent releases of CDH, Cloudera manager, Cloudera Navigator
and OneFS software.

This guide illustrates the first scenario. Using an existing Isilon
cluster to integrate with Cloudera manager to allow CDH access to
existing data sets located in the Isilon cluster.

Environment
===========

Versions
--------

The test environments used for this document consist of the following
software versions:

* Cloudera Manager 5.1.0
* Cloudera CDH 4.7, 5.0.3, and 5.1.0
* Isilon OneFS 7.1.1 and 7.1.1 with patch-130611
* VMware vSphere Enterprise 5.5.0
* VMware Big Data Extensions 2.0

.. table:: Cloudera CDH and Isilon OneFS Compatibility Matrix

  +--------------------+---------------------+----------------+-------------------------------+
  |                    | OneFS Version                                                        |
  +--------------------+---------------------+----------------+-------------------------------+
  | CDH Version        | 7.0.2.2 - 7.1.0.0   | 7.1.1.0        | 7.1.1.0 + patch-130611        |
  +====================+=====================+================+===============================+
  | 4.2 - 4.7\ :sup:`3`| compatible\ :sup:`1`| compatible     | compatible                    |
  +--------------------+---------------------+----------------+-------------------------------+
  | 5.0.3              | not compatible      | not compatible | compatible                    |
  +--------------------+---------------------+----------------+-------------------------------+
  | 5.1.0              | not compatible      | not compatible | partially compatible\ :sup:`2`|
  +--------------------+---------------------+----------------+-------------------------------+

:sup:`1` Fully-compatible but commands and features described in this
document may not all apply to this version of OneFS.

:sup:`2` Impala 1.4 on CDH 5.1.0 is not compatible with OneFS.

:sup:`3` Commands and features described in this document may not all
apply to these versions of CDH.
 

.. include:: ../common/environment-hosts.rst


Installation Overview
=====================

Below is the overview of the installation process that this document
will describe. If you have an existing Cloudera environment managed by
Cloudera Manager and you wish to integrate EMC Isilon for HDFS then you
can skip to the section titled “Connect Cloudera Hadoop to Isilon” (step
8 below).

#. Confirm prerequisites.

#. Prepare your network infrastructure including DNS and DHCP.

#. Prepare your Isilon cluster.

#. Prepare VMware Big Data Extensions (BDE).

#. Use BDE to provision multiple virtual machines.

#. Install Cloudera Manager.

#. Use Cloudera Manager to deploy Cloudera CDH to the virtual machines.

#. Connect Cloudera Hadoop services and components to Isilon for all HDFS file access.

#. Perform key functional tests.


.. include:: ../common/prereq.rst

.. include:: ../common/prepare-network-infrastructure.rst

.. include:: ../common/prepare-isilon.rst

.. include:: ../common/create-dns-records-for-isilon.rst

.. include:: ../common/prepare-nfs-clients.rst

.. include:: ../common/prepare-bde.rst

.. include:: ../common/prepare-hadoop-vm.rst


Install Cloudera Manager
========================

#.  Download Cloudera Manager 5.1.0 from
    http://www.cloudera.com/content/cloudera-content/cloudera-docs/CM5/latest/Cloudera-Manager-Quick-Start/Cloudera-Manager-Quick-Start-Guide.html,
    section *Download and Run the Cloudera Manager Server Installer*.

#.  Launch the installer.
    
    .. parsed-literal::

      [root\@c5manager-server-0 ~]# **./cloudera-manager-installer.bin**

#.  Accept all defaults and complete the installation process.

#.  Browse to http://c5manager-server-0.example.com:7180/.

    |image28|

#.  Login using the following account:    
  
    Username: admin

    Password: admin


Deploy a Cloudera Hadoop Cluster
================================

You will deploy Cloudera CDH Hadoop in the traditional way, meaning you
will have an HDFS NameNode and three DataNodes. Once all software
components are installed, you will reconfigure them to use Isilon for
HDFS and the original NameNode and DataNodes will be unused and idle.

.. note::
  **Only some of the steps are documented below.**
  Refer to the Cloudera Manager Quick Start Guide
  (http://www.cloudera.com/content/cloudera-content/cloudera-docs/CM5/latest/Cloudera-Manager-Quick-Start/Cloudera-Manager-Quick-Start-Guide.html)
  for complete details.

#.  Login to Cloudera Manager.
    
    |image30|

#.  Specify hosts for your CDH cluster installation. You can copy and
    paste from the files isilon-hadoop-tools/etc/\*-hosts.txt that were
    generated by the BDE post deployment script. Be sure to also include the
    Cloudera Manager host.

    |image32|

#.  You will likely want to install a specific version of CDH. When
    prompted to Select Repository, click More Options.

    |image34|

#.  To make CDH 5.0.3 available for selection, add the following to
    your Remote Parcel Repository URLs: ::

      http://archive.cloudera.com/cdh5/parcels/5.0.3/

    |image36|

#.  Now you can select the desired version of CDH. Then click Continue.

    |image38|

#.  Click Continue to select defaults and answer the prompts
    appropriately. When prompted to provide SSH login credentials, enter the
    same password that you typed into the Serengeti CLI when you created the
    cluster.

    |image40|

#.  Click Continue to select defaults and answer the prompts appropriately.
    
    |image42|

#.  Customize role assignments. For small clusters, the following role
    assignment can be used:

    - c5manager-server-0 for all Cloudera Management Service roles

    - mycluster1-namenode-0 for HDFS NameNode

    - mycluster1-worker-\* for HDFS DataNode, YARN Node Manager, HBase Region Server, Impala Daemon, Spark Worker

    |image44|

#.  Complete the installation process.

    |image46|

#.  Log into the Hue Web UI and install all of the application examples.

#.  After a successful installation, review Cloudera Manager for any
    warnings or errors. It is recommended to correct any warnings or errors
    before continuing.


Connect Cloudera Hadoop To Isilon
=================================

Copy HDFS Files to Isilon
-------------------------

#.  Login to Cloudera Manager.

#.  Stop all Cloudera cluster services except HDFS,YARN, and Zookeeper.
    
    |image48|

#.  SSH to mycluster1-master-0 as root.

#.  Test HDFS access to your CDH cluster's NameNode.
    
    .. parsed-literal::

      [root\@mycluster1-master-0 ~]# **sudo -u hdfs hdfs dfs -ls /**
      Found 4 items
      drwxr-xr-x   - hbase hbase               0 2014-08-05 05:38 /hbase
      drwxrwxr-x   - solr  solr                0 2014-08-05 05:03 /solr
      drwxrwxrwt   - hdfs  supergroup          0 2014-08-05 05:10 /tmp
      drwxr-xr-x   - hdfs  supergroup          0 2014-08-05 05:10 /user

#.  Test HDFS access to your Isilon cluster.
    
    .. parsed-literal::

      [root\@mycluster1-master-0 ~]# **sudo -u hdfs hdfs dfs -ls \\
      hdfs://mycluster1-hdfs/**
      Found 1 items
      -rw-r--r--   1 root hadoop          0 2014-08-05 05:59 hdfs://mycluster1-hdfs/THIS\_IS\_ISILON

#.  Copy the entire CDH cluster's HDFS namespace to Isilon.
    
    .. parsed-literal::

      [root\@mycluster1-master-0 ~]# **sudo -u hdfs hadoop distcp -skipcrccheck \\
      -update -pugp / hdfs://mycluster1-hdfs/**
      ...
      [root\@mycluster1-master-0 ~]# **sudo -u hdfs hdfs dfs -ls \\
      hdfs://mycluster1-hdfs/**
      Found 5 items
      -rw-r--r--   1 root  hadoop              0 2014-08-05 05:59 hdfs://mycluster1-hdfs/THIS\_IS\_ISILON
      drwxr-xr-x   - hbase hbase             148 2014-08-05 06:06 hdfs://mycluster1-hdfs/hbase
      drwxrwxr-x   - solr  solr                0 2014-08-05 06:07 hdfs://mycluster1-hdfs/solr
      drwxrwxrwt   - hdfs  supergroup        107 2014-08-05 06:07 hdfs://mycluster1-hdfs/tmp
      drwxr-xr-x   - hdfs  supergroup        184 2014-08-05 06:07 hdfs://mycluster1-hdfs/user


Reconfigure Cloudera Services to use Isilon for HDFS
----------------------------------------------------

#.  Stop all Cloudera cluster services.
    
    |image50|

#.  Edit HDFS \\ Service-Wide \\ Advanced \\ Cluster-wide Advanced
    Configuration Snippet (Safety Valve) for core-site.xml: ::

      <property>
      <name>fs.defaultFS</name>
      <value>hdfs://mycluster1-hdfs.lab.example.com:8020</value>
      </property>

    |image52|

#.  If HBase is installed, edit HBase \\ Service-Wide \\ Advanced \\
    HBase Service Advanced Configuration Snippet (Safety Valve) for
    hbase-site.xml: ::

      <property>
      <name>hbase.rootdir</name>
      <value>hdfs://mycluster1-hdfs.lab.example.com:8020/hbase</value>
      </property>

    |image54|


#.  Edit Hue \\ Service-Wide \\ Advanced \\ Hue Service Advanced
    Configuration Snippet (Safety Valve) for hue\_safety\_valve.ini: ::

      [hadoop]
      [[hdfs_clusters]]
      [[[default]]]
      fs_defaultfs=hdfs://mycluster1-hdfs.lab.example.com:8020
      webhdfs_url=https://mycluster1-hdfs.lab.example.com:8080/webhdfs/v1

    |image56|

#.  Deploy Client Configuration.

    |image58|

#.  Restart the Cloudera cluster.

    |image60|

#.  Confirm that the Isilon is now your default Hadoop file system.
    
    .. parsed-literal::

      [root\@mycluster1-master-0 ~]# **sudo -u hdfs hdfs dfs -ls /**
      Found 5 items
      -rw-r--r--   1 root  hadoop              0 2014-08-05 05:59 /THIS_IS_ISILON
      drwxr-xr-x   - hbase hbase             148 2014-08-05 06:06 /hbase
      drwxrwxr-x   - solr  solr                0 2014-08-05 06:07 /solr
      drwxrwxrwt   - hdfs  supergroup        107 2014-08-05 06:07 /tmp
      drwxr-xr-x   - hdfs  supergroup        184 2014-08-05 06:07 /user

#.  To ensure that no services are using the CDH NameNode and
    DataNodes, you may stop the CDH HDFS services.

    |image62|

#.  Review Cloudera Manager for any warnings or errors.


.. include:: ../common/adding-a-hadoop-user.rst


.. include:: ../common/functional-tests.rst


Impala
------

.. parsed-literal::

  [hduser1\@mycluster1-master-0 ~]$ **hadoop fs -mkdir -p sample\_data/tab1**
  [hduser1\@mycluster1-master-0 ~]$ **cat - > tab1.csv
  1,true,123.123,2012-10-24 08:55:00
  2,false,1243.5,2012-10-25 13:40:00
  3,false,24453.325,2008-08-22 09:33:21.123
  4,false,243423.325,2007-05-12 22:32:21.33454
  5,true,243.325,1953-04-22 09:11:33**
  
Type <Control+D>.

.. parsed-literal::

  [hduser1\@mycluster1-master-0 ~]$ **hadoop fs -put tab1.csv sample_data/tab1**
  [hduser1\@mycluster1-master-0 ~]$ **impala-shell -i mycluster1-worker-0**
  [mycluster1-worker-0:21000] >  
  
  **DROP TABLE IF EXISTS tab1;
  CREATE EXTERNAL TABLE tab1
  (
     id INT,
     col\_1 BOOLEAN,
     col\_2 DOUBLE,
     col\_3 TIMESTAMP
  )
  ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
  LOCATION '/user/hduser1/sample\_data/tab1';
   
  DROP TABLE IF EXISTS tab3;
  -- Leaving out the EXTERNAL clause means the data will be managed
  -- in the central Impala data directory tree. Rather than reading
  -- existing data files when the table is created, we load the
  -- data after creating the table.

  CREATE TABLE tab3
  (
     id INT,
     col\_1 BOOLEAN,
     col\_2 DOUBLE,
     month INT,
     day INT
  )
  ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

  INSERT OVERWRITE TABLE tab3
  SELECT id, col\_1, col\_2, MONTH(col\_3), DAYOFMONTH(col\_3)
  FROM tab1 WHERE YEAR(col\_3) = 2012;**

  WARNINGS: Backend 0:Unknown disk id.  This will negatively affect
  performance. Check your hdfs settings to enable block location metadata.

  [mycluster1-worker-0:21000] > **select \* from tab1;**
  Query: select \* from tab1
  +------+-------+------------+-------------------------------+
  \| id   \| col\_1 \| col\_2      \| col\_3                         \|
  +------+-------+------------+-------------------------------+
  \| 1    \| true  \| 123.123    \| 2012-10-24 08:55:00           \|
  \| 2    \| false \| 1243.5     \| 2012-10-25 13:40:00           \|
  \| 3    \| false \| 24453.325  \| 2008-08-22 09:33:21.123000000 \|
  \| 4    \| false \| 243423.325 \| 2007-05-12 22:32:21.334540000 \|
  \| 5    \| true  \| 243.325    \| 1953-04-22 09:11:33           \|
  \| NULL \| NULL  \| NULL       \| NULL                          \|
  +------+-------+------------+-------------------------------+
  Returned 6 row(s) in 0.20s
  WARNINGS: Backend 0:Unknown disk id.  This will negatively affect
  performance. Check your hdfs settings to enable block location metadata.

  [mycluster1-worker-0:21000] > **select \* from tab3;**
  Query: select \* from tab3
  +----+-------+---------+-------+-----+
  \| id \| col\_1 \| col\_2   \| month \| day \|
  +----+-------+---------+-------+-----+
  \| 1  \| true  \| 123.123 \| 10    \| 24  \|
  \| 2  \| false \| 1243.5  \| 10    \| 25  \|
  +----+-------+---------+-------+-----+
  Returned 2 row(s) in 0.29s
  WARNINGS: Backend 0:Unknown disk id.  This will negatively affect
  performance. Check your hdfs settings to enable block location metadata.
  [mycluster1-worker-0:21000] > **quit;**

For more details regarding Impala, refer to
http://www.cloudera.com/content/cloudera-content/cloudera-docs/Impala/latest/Installing-and-Using-Impala/ciiu_tutorial.html.


.. include:: ../common/where-to-go-from-here.rst

.. include:: ../common/known-limitations.rst

.. include:: ../common/legal.rst

.. include:: ../common/references.rst

.. include:: ../common/substitutions.rst
