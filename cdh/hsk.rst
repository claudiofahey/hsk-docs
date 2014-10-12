
.. The following substitutions are used by the common documents.

.. |hsk_dst| replace:: cdh
.. |hsk_dst_strong| replace:: **cdh**
.. |hadoop-manager| replace:: Cloudera Manager
.. |hadoop-mapreduce-examples-jar| replace:: **/opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar**


**************************************************************************
EMC Isilon Hadoop Starter Kit for Cloudera with VMware Big Data Extensions
**************************************************************************

This document describes how to create a Hadoop environment utilizing
Cloudera Manager and an EMC Isilon Scale-Out NAS for HDFS accessible
shared storage. VMware Big Data Extensions is used to provision and
manage the compute resources.

.. note::
  The latest version of this document is available at http://hsk-cdh.readthedocs.org/.

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
deployment, and the cost of deployment leveraging
tools that can automate Hadoop cluster deployments.

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

* Cloudera Manager 5.2.0
* Cloudera CDH 5.1.3
* Isilon OneFS 7.2.0 (available 3-Nov-2014)
* VMware vSphere Enterprise 5.5.0
* VMware Big Data Extensions 2.0


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

#. Perform key functional tests.


.. include:: ../common/prereq.rst

.. include:: ../common/prepare-network-infrastructure.rst


.. include:: ../common/prepare-isilon-1.rst

.. include:: ../common/prepare-isilon-2-create-users-and-directories.rst

.. include:: ../common/prepare-isilon-3-after-users-and-directories.rst


.. include:: ../common/create-dns-records-for-isilon.rst

.. include:: ../common/prepare-nfs-clients.rst

.. include:: ../common/prepare-bde.rst

.. include:: ../common/prepare-hadoop-vm.rst


Install Cloudera Manager
========================

#.  Download Cloudera Manager 5.2.0 from
    http://www.cloudera.com/content/cloudera-content/cloudera-docs/CM5/latest/Cloudera-Manager-Quick-Start/Cloudera-Manager-Quick-Start-Guide.html,
    section *Download and Run the Cloudera Manager Server Installer*.

#.  Launch the installer.
    
    .. parsed-literal::

      [root\@c5manager-server-0 ~]# **./cloudera-manager-installer.bin**

#.  Accept all defaults and complete the installation process.

#.  Browse to ``http://hadoop-manager-server-0.example.com:7180/``.

    |image28|

#.  Login using the following account:
  
    Username: admin

    Password: admin


Deploy a Cloudera Hadoop Cluster
================================

.. note::
  **Only some of the steps are documented below.**
  Refer to the Cloudera Manager Quick Start Guide
  (http://www.cloudera.com/content/cloudera-content/cloudera-docs/CM5/latest/Cloudera-Manager-Quick-Start/Cloudera-Manager-Quick-Start-Guide.html)
  for complete details.

#.  Login to Cloudera Manager.
    
    |image30|

#.  Specify hosts for your CDH cluster installation. You can copy and
    paste from the file isilon-hadoop-tools/etc/mycluster1-hosts.txt that were
    generated by the BDE post deployment script. Be sure to also include the
    Cloudera Manager host. Do *not* specify your Isilon cluster here.

    |image32|

#.  You will likely want to install a specific version of CDH. When
    prompted to Select Repository, click More Options.

    |image34|

#.  To make CDH 5.1.3 available for selection, add the following to
    your Remote Parcel Repository URLs: ::

      http://archive.cloudera.com/cdh5/parcels/5.1.3/

    |image36|

#.  Now you can select the desired version of CDH. Then click Continue.

    |image38|

#.  Click Continue to select defaults and answer the prompts
    appropriately. When prompted to provide SSH login credentials, enter the
    same password that you typed into the Serengeti CLI when you created the
    cluster.

    |image40|

#.  When prompted to choose the CDH services that you want to install, select *Custom Services*. 
    Then check *Isilon* and any other services that you would like to install.
    Do *not* select *HDFS*.

    .. image:: cloudera-manager-5.2-custom-services-isilon.png

#.  Customize role assignments. For small clusters, the following role
    assignment can be used:

    - hadoop-manager-server-0 for all Cloudera Management Service roles

    - mycluster1-worker-\* for YARN Node Manager, HBase Region Server, Impala Daemon

    - mycluster1-master-0 for all other roles (e.g. YARN Resource Manager, Isilon Gateway)

    .. image:: view-by-host.png

#.  When prompted to review changes, here you will specify your Isilon cluster address.
  
    Default File System URI
      \hdfs://mycluster1-hdfs.lab.example.com:8020
      
    WebHDFS URL
      \http://mycluster1-hdfs.lab.example.com:8082/webhdfs/v1

    .. image:: review-changes.png

#.  Complete the installation process.

    |image46|

#.  Review Cloudera Manager for any warnings or errors.


.. include:: ../common/adding-a-hadoop-user.rst


.. include:: ../common/functional-tests.rst


Impala
------

.. parsed-literal::

  [hduser1\@mycluster1-master-0 ~]$ **impala-shell -i mycluster1-worker-0**
  [mycluster1-worker-0:21000] > **invalidate metadata;**
  Query: invalidate metadata

  Returned 0 row(s) in 1.05s

  [cdhdas2-worker-0:21000] > **show tables;**
  Query: show tables
  +-------+
  \| name  \|
  +-------+
  \| tab1 \|
  \| tab2 \|
  +-------+
  Returned 2 row(s) in 0.01s

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
  +------+-------+------------+-------------------------------+
  Returned 5 row(s) in 0.20s
  WARNINGS: Backend 0:Unknown disk id.  This will negatively affect
  performance. Check your hdfs settings to enable block location metadata.

  [mycluster1-worker-0:21000] > **quit;**

For more details regarding Impala, refer to
http://www.cloudera.com/content/cloudera-content/cloudera-docs/Impala/latest/Installing-and-Using-Impala/ciiu_tutorial.html.

.. include:: ../common/wikipedia.rst

.. include:: ../common/where-to-go-from-here.rst

.. include:: ../common/known-limitations.rst

.. include:: ../common/legal.rst

.. include:: ../common/references.rst

http://www.cloudera.com/

.. include:: ../common/substitutions.rst
