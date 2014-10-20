
.. The following substitutions are used by the common documents.

.. |hsk_dst| replace:: hwx
.. |hsk_dst_strong| replace:: **hwx**
.. |hadoop-manager| replace:: Ambari
.. |hadoop-mapreduce-examples-jar| replace:: **hadoop-mapreduce-examples.jar**


*****************************************************************************
EMC Isilon Hadoop Starter Kit for Hortonworks with VMware Big Data Extensions
*****************************************************************************

This document describes how to create a Hadoop environment utilizing
the Hortonworks Data Platform and an EMC Isilon Scale-Out NAS for HDFS accessible
shared storage. VMware Big Data Extensions is used to provision and
manage the compute resources.

.. note::
  The latest version of this document is available at http://hsk-hwx.readthedocs.org/.

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
shared storage model with EMC Isilon scale out NAS and the Hortonworks Data Platform.
By leveraging Hortonworks distribution of Apache Ambari management tools 
which can automate Hadoop cluster deployments the time and cost for deployment 
can be dramatically reduced.

Audience
--------

This document is intended for IT program managers, IT architects,
Developers, and IT management to easily deploy Hortonworks Data Platform (HDP) with
automation tools and leverage EMC Isilon for HDFS shared storage. It can
be used by somebody who does not yet have an EMC Isilon cluster by
downloading the free EMC Isilon OneFS Simulator which can be installed
as a virtual machine for testing and training. However, this document
can also be used by somebody who will be installing in a production
environment as best-practices are followed whenever possible.


.. include:: ../common/apache-hadoop-projects.rst

Hortonworks Data Platform and the Ambari Manager
------------------------------------------------

The Hortonworks Data Platform (HDP) enables Enterprise Hadoop by providing the complete
set of essential Hadoop capabilities required for any enterprise.  Utilizing YARN at its
core, it provides capabilities for several functional areas including Data Management, Data
Access, Data Governance, Integration, Security and Operations.

HDP deliveres the core elements of Hadoop - scalable storage and
distributed computing – as well as all of the necessary enterprise
capabilities such as security, high availability and integration with a
broad range of hardware and software solutions.  It does so by leveraging 
the power of open source development and drives innovation exclusively through
the Apache Software Foundation process.

Apache Ambari is an open operational framework for provisioning, managing
and monitoring Apache Hadoop clusters. As of version 2.0 of the Hortonworks
Data Platform (HDP), Ambari can be used to setup and deploy Hadoop clusters
for nearly any task.  Ambari can provision, manage and monitor every aspect
of a Hadoop deployment.  Additionally, it provides a RESTful API to enable
integration with existing Enterprise management tools such as Microsoft System 
Center and many others.

More information on Hortonworks HDP and Ambari can be found at http://hortonworks.com


.. include:: ../common/intro-isilon.rst


Environment
===========

Versions
--------

The test environments used for this document consist of the following
software versions:

* Ambari Manager 1.6.1
* Hortonworks HDP 2.2
* Isilon OneFS 7.2.0 (available 3-Nov-2014)
* VMware vSphere Enterprise 5.5.0
* VMware Big Data Extensions 2.0


.. include:: ../common/environment-hosts.rst


Installation Overview
=====================

Below is the overview of the installation process that this document
will describe. If you have an existing HDP environment managed by
Ambari and you wish to integrate EMC Isilon for HDFS then you
can skip to the section titled “Connect HDP to Isilon” (step
8 below).

#. Confirm prerequisites.

#. Prepare your network infrastructure including DNS and DHCP.

#. Prepare your Isilon cluster.

#. Prepare VMware Big Data Extensions (BDE).

#. Use BDE to provision multiple virtual machines.

#. Install Ambari Server.

#. Use Ambari Manager to deploy HDP to the virtual machines.

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


Install Ambari Server
=====================

.. note::
    Install documentation for Ambari Server 1.6.1 is available from
    http://docs.hortonworks.com/HDPDocuments/Ambari-1.6.1.0/bk_using_Ambari_book/content/ambari-chap2.html    
    section *Download and Run the Ambari Server Installer*.

#.  Install the Ambari Server packages
    
    .. parsed-literal::

      [root\@hadoop-manager-server-0 ~]# **yum install ambari-server**
      [root\@hadoop-manager-server-0 ~]# **yum install ambari-agent**

#.  Start the install process

    .. parsed-literal::

      [root\@hadoop-manager-server-0 ~]# **ambari-server setup**
      
#.  Accept all defaults and complete the installation process.

#.  Start the server

    .. parsed-literal::

      [root\@hadoop-manager-server-0 ~]# **ambari-server start**

#.  Start the agent

    .. parsed-literal::

      [root\@hadoop-manager-server-0 ~]# **ambari-agent start**

#.  Browse to ``http://hadoop-manager-server-0.example.com:8080/``.

#.  Login using the following account:
  
    Username: admin

    Password: admin


Deploy a Hortonworks Hadoop Cluster with Isilon for HDFS
========================================================

You will deploy Hortonworks HDP Hadoop using the standard process defined
by Hortonworks.  Ambari Server allows for the immediate usage of an Isilon cluster
for all HDFS services (NameNode and DataNode), no reconfiguration will be necessary
once the HDP install is completed. 

.. note::
  **Only some of the steps are documented below.**
  Refer to the Hortonworks HDP Documentation
  (http://docs.hortonworks.com/HDPDocuments/Ambari-1.6.1.0/bk_using_Ambari_book/content/ambari-chap1.html)
  for complete details.

#.  Login to Ambari Server.

#.  Specify hosts for your HDP cluster installation in the Target Hosts text box.
    You can copy and paste from the files isilon-hadoop-tools/etc/\*-hosts.txt that were
    generated by the BDE post deployment script. The SmartConnect address of the Isilon cluster
    should also be included in the list of target hosts. Additionally, include the
    Ambari Server host.

#.  You may choose to install a specific version of the HDP Service Stack. When
    prompted select the most recent Stack as of this writing (2.2).

    .. image:: stack21.png

#.  Continue to select defaults and answer the prompts
    appropriately. In order to allow Ambari to automatically install the Agent on
    all hosts, provide the SSH private key of the Ambari Server when prompted after 
    updating the Host Registration Information section.

#.  When prompted to Choose Services, unselect (remove) Nagios and Ganglia from the
    list of services to install.  Ganglia will not function with an Isilon cluster
    without additional configuration beyond what is available through Ambari. 

    .. image:: choose_services.png

#.  Customize role/host assignments in the page labeled Assign Masters. For the NameNode and
    SNameNode (Secondary NameNode) components, the SmartConnect address of the Isilon cluster
    should be entered.  All other components can be assigned to any other hosts.

#.  Assign Slaves and Clients.  Select DataNode for only the Isilon cluster and
    distribute the rest of the selections over the remaining hosts.  The Isilon cluster should
    not be used for any other slave and client components.

    .. image:: slaves_clients.png

#.  Assign a password to Hive and Oozie if they have been selected as Services.
 
#.  Deploy the HDP installation.

#.  After a successful installation, Ambari will start and test all of the selected
    services. Review the Install, Start and Test page for any
    warnings or errors. It is recommended to correct any warnings or errors
    before continuing.


.. include:: ../common/adding-a-hadoop-user.rst

.. include:: ../common/functional-tests.rst

.. include:: ../common/wikipedia.rst

.. include:: ../common/where-to-go-from-here.rst

.. include:: ../common/known-limitations.rst

.. include:: ../common/legal.rst

.. include:: ../common/references.rst

http://www.hortonworks.com/

.. include:: ../common/substitutions.rst
