
.. The following substitutions are used by the common documents.

.. |hsk_dst| replace:: phd3
.. |hsk_dst_strong| replace:: **phd3**
.. |hadoop-manager| replace:: Ambari
.. |hadoop-mapreduce-examples-jar| replace:: **/usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar**


*****************************************************************************
EMC Isilon Hadoop Starter Kit for Pivotal HD 3.0 with VMware Big Data Extensions
*****************************************************************************

This document describes how to create a Hadoop environment utilizing
Pivotal HD and an EMC Isilon Scale-Out NAS for HDFS accessible
shared storage. VMware Big Data Extensions is used to provision and
manage the compute resources.

#RememberRuddy

.. note::
  The latest version of this document is available at `ReadTheDocs <http://hsk-phd3.readthedocs.org/>`_.

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
distributed by several vendors including Pivotal, Pivotal, and
Cloudera with proprietary extensions. In addition to these
distributions, Apache distributes a free open source version. From an
infrastructure perspective many Hadoop deployments start outside the IT
data center and do not leverage the existing IT automation, storage
efficiency, and protection capabilities. Many customers cited the time
it took IT to deploy Hadoop as the primary reason to start with a
deployment outside of IT.

This guide is intended to simplify Hadoop deployments by creating a
shared storage model with EMC Isilon scale out NAS and using an
industry leader in Enterprise Hadoop, Pivotal, reduce the time to
deployment, and the cost of deployment leveraging
tools that can automate Hadoop cluster deployments.

Audience
--------

This document is intended for IT program managers, IT architects,
Developers, and IT management to easily deploy Pivotal HD (PHD) with
automation tools and leverage EMC Isilon for HDFS shared storage. It can
be used by somebody who does not yet have an EMC Isilon cluster by
downloading the free EMC Isilon OneFS Simulator which can be installed
as a virtual machine for testing and training. However, this document
can also be used by somebody who will be installing in a production
environment as best-practices are followed whenever possible.


.. include:: ../common/apache-hadoop-projects.rst


Pivotal HD, HAWQ, and the Ambari Manager
------------------------------------------------

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

For more information on `Pivotal HD and HAWQ <http://pivotal.io/big-data/pivotal-big-data-suite>`_.

Apache Ambari is an open operational framework for provisioning, managing
and monitoring Apache Hadoop clusters. As of version 3.0 of the Pivotal
HD (PHD), Ambari can be used to setup and deploy Hadoop clusters
for nearly any task.  Ambari can provision, manage and monitor every aspect
of a Hadoop deployment.  Additionally, it provides a RESTful API to enable
integration with existing Enterprise management tools such as Microsoft System
Center and many others.

For more information on `Pivotal PHD and Ambari <http://pivotalhd.docs.pivotal.io/docs/install-ambari.html>`_.


.. include:: ../common/intro-isilon.rst


Environment
===========

Versions
--------

The test environments used for this document consist of the following
software versions:

* Apache Ambari 1.7
* Pivotal PHD 3.0.0
* Isilon OneFS 7.2.0.3 or higher
* VMware vSphere Enterprise 5.5.0
* VMware Big Data Extensions 2.0


.. include:: ../common/environment-hosts.rst


Installation Overview
=====================

Below is the overview of the installation process that this document
will describe. If you have an existing PHD environment managed by
Ambari and you wish to integrate EMC Isilon for HDFS then you
can skip to the section titled “Connect PHD to Isilon” (step
8 below).

#. Confirm prerequisites.

#. Prepare your network infrastructure including DNS and DHCP.

#. Prepare your Isilon cluster.

#. Prepare VMware Big Data Extensions (BDE).

#. Use BDE to provision multiple virtual machines.

#. Install Ambari Server.

#. Use Ambari Manager to deploy PHD to the virtual machines.

#. Perform key functional tests.


.. include:: ../common/prereq.rst

.. include:: ../common/prepare-network-infrastructure.rst

.. include:: ../common/prepare-isilon-1.rst

.. include:: ../common/create-dns-records-for-isilon.rst

.. include:: ../common/prepare-nfs-clients.rst

.. include:: ../common/prepare-bde.rst

.. include:: ../common/prepare-hadoop-vm.rst


Install Ambari Server
=====================

.. note::
  **Only some of the steps are documented below.**
  Follow the instructions in the `Pivotal HD Installation Guide <http://pivotalhd.docs.pivotal.io/docs/install-ambari.html>`_
  through section 3.3 before continuing:

.. note::
  Ambari Server is the management interface for Pivotal PHD. A single instance of
  Ambari Server will manage exactly one PHD cluster. Therefore, you may choose to
  deploy it onto your cluster's master node (mycluster1-master-0) instead of the
  dedicated Hadoop management node (hadoopmanager-server-0).

#.  Browse to ``http://hadoopmanager-server-0.lab.example.com:8080/``.

#.  Login using the following account:

    Username: admin

    Password: admin

Deploy a Pivotal Hadoop Cluster with Isilon for HDFS
========================================================

You will deploy Pivotal PHD Hadoop using the standard process defined
by Pivotal.  Ambari Server allows for the immediate usage of an Isilon cluster
for all HDFS services (NameNode and DataNode), no reconfiguration will be necessary
once the PHD install is completed.

.. note::
  **Only some of the steps are documented below.**
  Refer to the `Pivotal PHD Documentation <http://pivotalhd.docs.pivotal.io/docs/install-ambari.html>`_
  for complete details.

#. Configure the Ambari Agent on Isilon.

   .. parsed-literal::

    isiloncluster1-1# **isi zone zones modify zone1 --hdfs-ambari-namenode \\
    mycluster1-hdfs.lab.example.com**
    isiloncluster1-1# **isi zone zones modify zone1 --hdfs-ambari-server \\
    hadoopmanager-server-0.lab.example.com**

#.  Login to Ambari Server.

#.  After logging into Ambari select the **Launch Installation Wizard** to enter the
    cluster configuration wizard utility.

#.  **Get Started:** name your cluster *mycluster1*.

#.  **Select Stack:** Select the PHD 3.0 stack.

    .. image:: phdStack.png

    The values that are provided in the initial installation must be replaced with the actual URLs of the
    stack that repositories you installed earlier. Replace ``http://set\_repo\_url/`` with the repository URL
    you recorded when running the ``setup_repo.sh`` script for each stack. If you did not record the URLs, you
    can obtain the correct URLs by examining the ``/etc/yum.repos.d/<STACK>-<VERSION>.repo`` file.

#.  **Install Options:**

    .. note::
      You will register your hosts with Ambari in two steps. First you will deploy
      the Ambari agent to your Linux hosts that will run PHD. Then you will go *back*
      one step and add Isilon.

    .. note::
      You may ignore any warnings about ntpd not running on VMware VMs.
      Time is synchronized using VMware Tools instead of ntpd.

    #.  Specify your Linux hosts that will run PHD for your PHD cluster installation
        in the Target Hosts text box.  You can copy and paste from the file
        isilon-hadoop-tools/etc/mycluster1-hosts.txt that was generated by the BDE
        post deployment script.  Do *not* include the Ambari Server host unless
        it is installed on your master host (mycluster1-master-0).

        Copy and paste your SSH private key into the Host Registration Information
        section.  You can view your SSH private key with the following command.

        .. parsed-literal::

          [user\@workstation ~]$ **cat ~/.ssh/id_rsa**
          -----BEGIN RSA PRIVATE KEY-----
          MIIEogIBAAKCAQEAxLJBOta8T/j7tbzHHPZgpH3FUnmJakV52wjqEPIZL0a3cDJ3
          ...
          G5//RWQCkWIcAcTGIhol5LaO6UutrZbY413OdDKvq9g8TlgQNEs=
          -----END RSA PRIVATE KEY-----

        .. image:: phdInstallOptions.png

        Click the **Next** button to deploy the Ambari Agent to your Linux hosts
        and register them.


    #.  Once the Ambari Agent has been deployed and registered on your Linux
        hosts, click the **Back** button.

        Now you will add the SmartConnect address of the Isilon cluster (mycluster1-hdfs.lab.example.com)
        to your list of target hosts.

        Check the box to "Perform manual registration on hosts and do not use SSH."

        Click the **Next** button. You should see that Ambari agents on all hosts, including your Linux hosts
        and Isilon, become registered.

#.  **Choose Services:** When prompted to Choose Services, unselect (remove) Nagios,
    Ganglia, and Knox from the list of services to install.  Ganglia will not function
    with an Isilon cluster without additional configuration beyond what is available
    through Ambari.

    .. image:: phdChooseServices.png

#.  **Assign Masters:**

    Assign NameNode and SNameNode components to the Isilon SmartConnect address
    mycluster1-hdfs.lab.example.com.

    ZooKeeper should be installed on mycluster1-master-0 and any two workers.

    All other master components can be assigned to mycluster1-master-0.


#.  **Assign Slaves and Clients:**

    Assign NodeManager, RegionServer, and Supervisor to all worker nodes (mycluster1-worker-\*).

    Assign DataNode to the Isilon SmartConnect address mycluster1-hdfs.lab.example.com.

    Assign Client to the mycluster1-master-0.


#.  **Customize Services:**

    Assign passwords to Hive, Oozie, and any other selected services that require them.

    Check that all local data directories are within /data/1, /data/2, etc..
    The following settings should be checked.

    -  YARN Node Manager log-dirs
    -  YARN Node Manager local-dirs
    -  HBase local directory
    -  ZooKeeper directory
    -  Oozie Data Dir
    -  Storm storm.local.dir


    In YARN, set the following parameters in YARN>Configs:
      #.  ``yarn.timeline-service.store-class`` to **org.apache.hadoop.yarn.server.timeline.LeveldbTimelineStore**
      #.  ``yarn.scheduler.capacity.node-locality-delay`` to **-1**

    If deploying HAWQ, set the following parameters in HAWQ>Configs
      #.  ``hawq.segments.per.node`` to **2** (you may consider adding more later but this value is a sufficient start)
      #.  ``hawq.master.port`` to **10432** if the target HAWQ master server is also running other postgresql database servers
      #.  ``hawq.temp.directory`` to include the paths to all of your local **tmp** directories are within
          /data/1, data/2, etc... so HAWQ has spill space when performing joins and sorts.


#.  **Review:** Carefully review your configuration and then click Deploy.


#.  After a successful installation, Ambari will start and test all of the selected
    services. Review the Install, Start and Test page for any
    warnings or errors. It is recommended to correct any warnings or errors
    before continuing.


#.  **Post Install Configuration:**  Now that the cluster is functional there is one
    last item that remains.

    #.  HAWQ requires ``dfs.blocksize`` be set for 134217728.  To make this
        change in Ambari, choose HDFS Service>Configs, and then search for ``dfs.blocksize``.
        Enter the parameter value above and choose save.  Ambari will promp to restart
        the HDFS service on the PHD Cluster.

        .. image::  phdSetBlocksizeForHawq.png

.. include:: ../common/adding-a-hadoop-user.rst


.. include:: ../common/functional-tests.rst

HAWQ
--------------------

#.  To validate HAWQ was installed, ssh to your HAWQ master node and execute:

  .. parsed-literal::
     $ su - gpadmin
     $ psql

#.  To validate PXF was installed, ssh to your HAWQ master node and execute:

  .. parsed-literal::
     su - gpadmin
     gpconfig -c pxf_isilon -v 1 --skipvalidation
     gpstop -r
     psql
     show pxf_isilon;

  The output of which should display:

  .. parsed-literal::
     pxf_isilon
     ------------
     on
     (1 row)

#.  If you plan to use PL/R, PL/Java, MADlib, or other HAWQ components, follow the
    instructions in `Installing Additional HAWQ Components in the HAWQ 1.3 documentation <http://hawq.docs.pivotal.io/130/docs-hawq/topics/InstallingtheHAWQComponents.html>`_
    to install them.

Ambari Service Check
--------------------

Ambari has built-in functional tests for each component.
These are executed automatically when you install your cluster with Ambari.
To execute them after installation, select the service in Ambari, click
the *Service Actions* button, and select *Run Service Check*.


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
