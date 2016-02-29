
.. The following substitutions are used by the common documents.

.. |hsk_dst| replace:: ibm
.. |hsk_dst_strong| replace:: **ibm**
.. |hadoop-manager| replace:: Ambari
.. |hadoop-mapreduce-examples-jar| replace:: **/usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar**


*************************************************************************************
EMC Isilon Hadoop Starter Kit for IBM BigInsights 4.0 with VMware Big Data Extensions
*************************************************************************************

This document describes how to create a Hadoop environment utilizing
the IBM BigInsights and an EMC Isilon Scale-Out NAS for HDFS accessible
shared storage. VMware Big Data Extensions is used to provision and
manage the compute resources.

#RememberRuddy

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
distributed by several vendors including Pivotal, BigInsights, and
Cloudera with proprietary extensions. In addition to these
distributions, Apache distributes a free open source version. From an
infrastructure perspective many Hadoop deployments start outside the IT
data center and do not leverage the existing IT automation, storage
efficiency, and protection capabilities. Many customers cited the time
it took IT to deploy Hadoop as the primary reason to start with a
deployment outside of IT.

This guide is intended to simplify Hadoop deployments by creating a
shared storage model with EMC Isilon scale out NAS and using an
industry leader in Enterprise Hadoop, BigInsights, reduce the time to
deployment, and the cost of deployment leveraging
tools that can automate Hadoop cluster deployments.

Audience
--------

This document is intended for IT program managers, IT architects,
Developers, and IT management to easily deploy IBM BigInsights (BI) with
automation tools and leverage EMC Isilon for HDFS shared storage. It can
be used by somebody who does not yet have an EMC Isilon cluster by
downloading the free EMC Isilon OneFS Simulator which can be installed
as a virtual machine for testing and training. However, this document
can also be used by somebody who will be installing in a production
environment as best-practices are followed whenever possible.


.. include:: ../common/apache-hadoop-projects.rst


IBM BigInsights and the Ambari Manager
------------------------------------------------

The IBM® Open Platform with Apache Hadoop is comprised of entirely Apache Hadoop open
source components, such as Apache Ambari, YARN, Spark, Knox, Slider, Sqoop, Flume, Hive,
Oozie, HBase, ZooKeeper, and more.

After installing IBM Open Platform, you can install additional IBM value-add service
modules. These value-add service modules are installed separately, and they include
IBM BigInsights® Analyst, IBM BigInsights Data Scientist, and the IBM BigInsights
Enterprise Management module to provide enhanced capabilities to IBM Open Platform
to accelerate the conversion of all types of data into business insight and action.

Apache Ambari is an open operational framework for provisioning, managing
and monitoring Apache Hadoop clusters. As of version 4.0 of IBM Open Platform,
Ambari can be used to setup and deploy Hadoop clusters for nearly any task.
Ambari can provision, manage and monitor every aspect of a Hadoop deployment.
Additionally, it provides a RESTful API to enable integration with existing
Enterprise management tools such as Microsoft System Center and many others.

For more information on `BigInsights <http://www-03.ibm.com/software/products/en/ibm-biginsights-for-apache-hadoop>`_

.. include:: ../common/intro-isilon.rst


Environment
===========

Versions
--------

The test environments used for this document consist of the following
software versions:

* Apache Ambari 1.7.0_IBM
* IBM Open Platform v4.0.0.0
* Isilon OneFS 7.2.0.3 with patch-159065 or higher
* All of IBM BigInsights v 4.0 value packs, i.e. Business Analyst,
  Data Scientist, and Enterprise Management
* VMware vSphere Enterprise 5.5.0
* VMware Big Data Extensions 2.0


.. include:: ../common/environment-hosts.rst


Installation Overview
=====================

Below is the overview of the installation process that this document
will describe. If you have an existing BI environment managed by
Ambari and you wish to integrate EMC Isilon for HDFS then you
can skip to the section titled “Connect BI to Isilon” (step
8 below).

#. Confirm prerequisites.

#. Prepare your network infrastructure including DNS and DHCP.

#. Prepare your Isilon cluster.

#. Prepare VMware Big Data Extensions (BDE).

#. Use BDE to provision multiple virtual machines.

#. Download and configure an IBM Open Platform Repository

#. Install Ambari Server.

#. Use Ambari Manager to deploy BI to the virtual machines.

#. Perform key functional tests.


.. include:: ../common/prereq.rst

.. include:: ../common/prepare-network-infrastructure.rst

.. include:: ../common/prepare-isilon-1.rst

.. include:: ../common/create-dns-records-for-isilon.rst

.. include:: ../common/prepare-nfs-clients.rst

.. include:: ../common/prepare-bde.rst

.. include:: ../common/prepare-hadoop-vm.rst


Download and configure an IBM Open Platform Repository
======================================================

The IBM Open Platform with Apache Hadoop uses the repository-based Ambari installer.
You have two options for specifying the location of the repository from which Ambari
obtains the component packages.

The IBM Open Platform with Apache Hadoop installation includes OpenJDK 1.7.0. During
installation, you can either install the version provided or make sure Java™ 7 is
installed on all nodes in the cluster.

Log into the IBM Passport Advantage web portal with your IBM assigned credentials and
download the following packages onto the designated Ambari server node:

* BI-AH-1.0.0.1-IOP-4.0.x86_64.bin
* IOP-4.0.0.0.x86_64.rpm
* iop-4.0.0.0.x86_64.tar.gz
* iop-utils-1.0-iop-4.0.x86_64.tar.gz

#.  Log in to your Linux cluster as ``root``, or as a user with root privileges.
#.  Ensure that the ``nc`` package is installed on all nodes.  **Required**

    .. parsed-literal::
      yum install -y nc

#.  Locate the ``IOP-4.0.0.0.x86_64.rpm`` file you downloaded from the download site and
    run the following command to install the ambari.repo file into ``/etc/yum.repos.d``:

    .. parsed-literal::
      yum install IOP-4.0.0.0x86_64rpm

    Once complete there is the option of using a mirror repository by editing ``/etc/yum.repols.d/ambari.repo``
    and replacing ``baseurl=http://ibm-open-platform.ibm.com/repos/Ambari/RHEL6/x86_64/1.7`` with your preferred mirror.
    For example:  ``baseurl=http://<web.server>/repos/Ambari/RHEL6/x86_64/1.7/`` where ``<web.server>`` is the
    preferred mirror.

    Disable the ``gpgcheck`` in the ``ambari.repo`` file.  Change ``gpgcheck=1`` to ``gpgcheck=0``

    Alternatively, you can keep ``gpgcheck`` on and change the public key file location to the mirror repository.
    To do this, change the following ``gpgkey=http://ibm-open-platform.ibm.com/repos/Ambari/RHEL6/x86_64/1.7/BI-GPG-KEY.public``
    to ``gpgkey=http://<web.server>/repos/Ambari/RHEL6/x86_64/1.7/BI-GPG-KEY.public``.

#.  Clean the yum cache on each node so the right packages from the remote repository are seen by your local yum.

    .. parsed-literal::
      #sudo yum clean all

#.  Install the Ambari server on the intended management node, using the following command:

    .. parsed-literal::
      #sudo yum install ambari-sever

    Accept the installation defaults

#.  If using a mirror repository, after installing the Ambari server, update ``/var/lib/ambari-server/resources/stacks/BigInsights/4.0/repos/repoinfo.xml``
    with the mirror repository URLs.

    In the file, change this:

    .. parsed-literal::
      <os type="redhat6">
      <repo>
      <baseurl> http://ibm-open-platform.ibm.com/repos/IOP/RHEL6/x86_64/4.0</baseurl>
      <repoid>IOP-4.0</repoid>
      <reponame>IOP</reponame>
      </repo>
      <repo>
      <baseurl> http://ibm-open-platform.ibm.com/repos/IOP-UTILS/RHEL6/x86_64/1.0</baseurl>
      <repoid>IOP-UTILS-1.0</repoid>
      <reponame>IOP-UTILS</reponame>
      </repo>
      </os>

    To this, where ``<web.server>`` is your preferred repo.

    .. parsed-literal::
      <os type="redhat6">
      <repo>
      <baseurl> http://<web.server>/repos/IOP/RHEL6/x86_64/4.0</baseurl>
      <repoid>IOP-4.0</repoid>
      <reponame>IOP</reponame>
      </repo>
      <repo>
      <baseurl> http://<web.server>/repos/IOP-UTILS/RHEL6/x86_64/1.0</baseurl>
      <repoid>IOP-UTILS-1.0</repoid>
      <reponame>IOP-UTILS</reponame>
      </repo>
      </os>


    Next, edit ``/etc/ambari-server/conf/ambari.properties`` and change the this:

    .. parsed-literal::
      jdk1.7.url=http://ibm-open-platform.ibm.com/repos/IOP-UTILS/RHEL6/x86_64/1.0/openjdk/jdk-1.7.0.tar.gz

    To this:

    .. parsed-literal::
      jdk1.7.url=http://<web.server>/repos/IOP-UTILS/RHEL6/x86_64/1.0/openjdk/jdk-1.7.0.tar.gz


Install Ambari Server
=====================


.. note::
  Ambari Server is the management interface for BigInsights BI. A single instance of Ambari Server
  will manage exactly one BI cluster. Therefore, you may choose to deploy it onto your cluster's
  master node (mycluster1-master-0) instead of the dedicated Hadoop management node (hadoopmanager-server-0).


#.  Setup Ambari Server.

    .. parsed-literal::

      [root\@hadoopmanager-server-0 ~]# **ambari-server setup**

    Accept the setup preferences.

    A Java JDK is installed as part of the Ambari server setup.  However, the Ambari
    server setup also allows for the reuse of an existing JDK.  To reuse an existing
    JDK issue ``ambari-server setup -j /full/path/to/JDK`` where ``/full/path/to/JDK``
    is the full path to the existing JDK.  **This must be run on all linux servers
    in the hadoop cluster.**

#.  Start the server.

    .. parsed-literal::

      [root\@hadoopmanager-server-0 ~]# **ambari-server start**

#.  Browse to ``http://hadoopmanager-server-0.lab.example.com:8080/``.

#.  Login using the following account:

    Username: admin

    Password: admin

Deploy a BigInsights Hadoop Cluster with Isilon for HDFS
========================================================

You will deploy BigInsights BI Hadoop using the standard process defined
by BigInsights.  Ambari Server allows for the immediate usage of an Isilon cluster
for all HDFS services (NameNode and DataNode), no reconfiguration will be necessary
once the BI install is completed.


#. Configure the Ambari Agent on Isilon.

   .. parsed-literal::

    isiloncluster1-1# **isi zone zones modify zone1 --hdfs-ambari-namenode \\
    mycluster1-hdfs.lab.example.com**
    isiloncluster1-1# **isi zone zones modify zone1 --hdfs-ambari-server \\
    hadoopmanager-server-0.lab.example.com**

#.  Choose **Launch Install Wizard** in Ambari.

#.  **Welcome:** Specify the name of your cluster *mycluster1*.

#.  **Select Stack:** Select BigInsights™ 4.0

#.  **Install Option:**

    .. note::
      You will register your hosts with Ambari in two steps. First you will deploy the Ambari agent to your
      Linux hosts that will run BI. Then you will go *back* one step and add Isilon.

    .. note::
      You may ignore any warnings about ntpd not running on VMware VMs.
      Time is synchronized using VMware Tools instead of ntpd.

    #.  Specify your Linux hosts that will run BI for your BI cluster installation in the Target Hosts text box.
        You can copy and paste from the file isilon-hadoop-tools/etc/mycluster1-hosts.txt that was
        generated by the BDE post deployment script.
        Do *not* include the Ambari Server host unless it is installed on your master host (mycluster1-master-0).

        Copy and paste your SSH private key into the Host Registration Information section.
        You can view your SSH private key with the following command.

        .. parsed-literal::

          [user\@workstation ~]$ **cat ~/.ssh/id_rsa**
          -----BEGIN RSA PRIVATE KEY-----
          MIIEogIBAAKCAQEAxLJBOta8T/j7tbzHHPZgpH3FUnmJakV52wjqEPIZL0a3cDJ3
          ...
          G5//RWQCkWIcAcTGIhol5LaO6UutrZbY413OdDKvq9g8TlgQNEs=
          -----END RSA PRIVATE KEY-----

        .. image:: install_options.png

        Click the **Next** button to deploy the Ambari Agent to your Linux hosts and register them.

    #.  Once the Ambari Agent has been deployed and registered on your Linux hosts, click the **Back** button.

        Now you will add the SmartConnect address of the Isilon cluster (mycluster1-hdfs.lab.example.com)
        to your list of target hosts.

        Check the box to "Perform manual registration on hosts and do not use SSH."

        Click the **Next** button. You should see that Ambari agents on all hosts, including your Linux hosts
        and Isilon, become registered.

#.  **Choose Services:** When prompted to Choose Services, unselect (remove) Nagios and Ganglia from the
    list of services to install.  Ganglia will not function with an Isilon cluster
    without additional configuration beyond what is available through Ambari.

    .. image:: choose_services.png

#.  **Assign Masters:**

    Assign NameNode and SNameNode components to the Isilon SmartConnect address mycluster1-hdfs.lab.example.com.

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

    In YARN, set yarn.timeline-service.store-class to ``org.apache.hadoop.yarn.server.timeline.LeveldbTimelineStore``.

#.  **Review:** Carefully review your configuration and then click Deploy.

#.  After a successful installation, Ambari will start and test all of the selected
    services. Review the Install, Start and Test page for any
    warnings or errors. It is recommended to correct any warnings or errors
    before continuing.


.. include:: ../common/adding-a-hadoop-user.rst


.. include:: ../common/functional-tests.rst

Ambari Service Check
--------------------

Ambari has built-in functional tests for each component.
These are executed automatically when you install your cluster with Ambari.
To execute them after installation, select the service in Ambari, click the *Service Actions* button, and select *Run Service Check*.


.. include:: ../common/wikipedia.rst

Installing IBM Value Packages
=============================

Preface
-------

Please note that “BigInsights Analyst” and “BigInsights Data Scientist” value package
have been sanity tested on EMC Isilon, but have not been performance profiled and tested
under load with Isilon 7.2.0.3 version. EMC and IBM BigInsights plan to validate these
components under load as part of future integration efforts. Please refer to EMC – IBM
BigInsights Joint Support Statement for further details.

You must acquire the software from Passport Advantage. The acquired software has a
*.bin extension. The name of the *.bin file depends on whether the BigInsights Analyst
or the BigInsights Data Scientist module was downloaded.

When you run the *.bin file, configuration files are copied to appropriate locations
to enable Ambari to see that value-add services as available. When adding the value-add
services through Ambari, additional software packages can be downloaded. If the Hadoop
cluster cannot directly access the internet, a local mirror repository can be created.

Where you perform the following steps depends on whether the Hadoop cluster has
direct internet access.

* If the Hadoop cluster has direct access to the internet, perform the steps from the
  Ambari server of the Hadoop cluster.
* If the Hadoop cluster does not have direct internet access, perform the steps from a
  Linux host with direct internet access. Then, transfer the files, as required,
  to a local repository mirror

Installation Prework Procedure
------------------------------

#.  Apply execution permissions ``chmod +x <package_name>.bin`` on the downloaded *.bin file.

#.  Run the ``bin`` file ``./<package_name>.bin`` to extract and install the services
    in the module where ``<package_name>`` is ``BI-Analyst-xxxxx.bin`` for **Analyst Module**
    or ``BI-DS-xxxxx.bin`` for the **Data Scientist Module**

#.  At the prompt agree to the license terms.  Reply ``yes | y`` to continue.

#.  After the prompt, choose **online** (1) or **offline** (2) install.

    * Online install will lay out the Ambari service configuration files and update
      the repository locations in the Ambari server file.  **Proceed directoy to step 6.**
    * Offline install initiates a download of files and sets up a local repository mirror.
      A subdirectory called ``BigInsights`` will be created with RPMs and located in
      the ``BigInsights/packages`` directory.

#.  Setup a local repository

    A local repository is required if the Hadoop cluster cannot connect directly
    to the internet, or if you wish to avoid multiple downloads of the same software
    when installing services across multiple nodes. In the following steps, the host
    that performs the repository mirror function is called the repository server.
    If you do not have an additional Linux host, you can use one of the Hadoop
    management nodes. The repository server must be accessible over the network
    by the Hadoop cluster. The repository server requires an HTTP web server.
    The following instructions describe how to set up a repository server by
    using a Linux host with an Apache HTTP server.

    #.  Install ``httpd`` on the **repository server** ``yum install httpd``
    #.  Install ``createrepo`` on the **repository server** ``yum install createrepo``
    #.  Create a directory for value-add repositories, such as ``<http_web_root>/repos/valueadds``.
        The default location for httpd document root is ``/var/www/html/repos``.  Using that example,
        ``mkdir /var/www/html/repos/valueadds``.
    #.  By selecting **Option 2** in step 4, RPMs were downloaded to a subdirectory called ``BigInsights/packages``.
        Copy all of the RPMs to the mirror web serverlocation.  ``cp BigInsights/pacakges/* /var/www/html/repos/valueadds``
    #.  Start the web server by ``apachect start`` or ``service httpd start`` depending on your
        Linux distribution.
    #.  Test your local repository by browsing to the web directory ``http://<your_mirror_server>/repos/valueadds``.
        You should see all of the copied files.
    #.  Run ``createrepo /var/www/html/repos/valueadds`` to initialize the repository.
    #.  Find the RPM to install on the **Ambari Server** in the ``BigInsights/packages`` directory.
        The file for the BigInsights Data Scientists is ``BI-DS-x.x.x.x-IOP-x.x.x86_64.rpm``.  The file
        for BigInsights Analyst is ``BI-Analyst-x.x.x.x-IOP-x.x.x86_64.rpm``.

        .. note::
          The BigInsights Data Scientist module also entitles you to the features of the
          BigInsights Analyst module. Therefore, consider doing the yum install for both
          of the RPM packages.

    #.  Copy these files to the Ambari Server host and install the RPMs using ``sudo yum install BI*.rpm``
    #.  If the ``/var/lib/ambari-server/resources/stacks/BigInsights/<version_number>/repos/repoinfo.xml`` on
        the Ambari Server does not exist then create it.  ``touch /var/lib/ambari-server/resources/stacks/BigInsights/<version_number>/repos/repoinfo.xml``
    #.  Edit the ``/var/lib/ambari-server/resources/stacks/BigInsights/<version_number>/repos/repoinfo.xml`` file
        to ensure it contains:

        ..  parsed-literal::
          <repo>
          <baseurl> http://<your.mirror.web.server>/repos/valueadds </baseurl>
          <repoid>BIGINSIGHTS-VALUEPACK</repoid>
          <reponame>BIGINSIGHTS-VALUEPACK</reponame>
          </repo>

        .. note::
          The new <repo> section might appear as a single line.

        .. note::
          If errors are later found with this file, make sure to issue ``yum clean all`` then restart the ambari server.

    #.  When the modules are both installed ``ambari-server restart`` to restart Ambari.
    #.  Open the Ambari interface ``http://<ambari_server>:8080`` with username ``admin`` and password ``admin``
    #.  From the Ambari Dashboard choose **Actions > Add Service**

Install BigInsights Services to the Cluster Overview
----------------------------------------------------

Select the service that you want to install and deploy. Even though your module
might contain multiple services, install the specific service that you want and
the BigInsights™ Home service. Installing one value-add service at a time is recommended.
Follow the service specific installation instructions for more information. At the
conclusion of installing all the IBM BigInsights Services, the Ambari GUI Software
List should have green check marks next to each service as shown below:

.. image:: ibmServices.png


Installing BigInsights Home
---------------------------

The BigInsights Home service is the main interface to launch BigInsights - BigSheets,
BigInsights - Text Analytics, and BigInsights - Big SQL.

.. note::
  The BigInsights Home service requires Knox to be installed, configured and started.

#.  In the Ambari dashboard, click **Actions > Add Service**.

#.  In the **Add Service Wizard > Choose Services**, select the **BigInsights – BigInsights Home service**.

    .. note::
      If you do not see the option for BigInsights – BigInsights Home,
      follow the instructions described in Installing the BigInsights value-add packages.

#.  Click **Next**.
#.  In the Assign Masters page, select a Management node (edge node) that your
    users can communicate with. BigInsights Home is a web application that your
    users must be able to open with a web browser.

#.  In the Assign Slaves and Clients page, make selections to assign slaves and clients.
    The nodes that you select will have ``JSQSH`` (an open source, command line interface
    to SQL for Big SQL and other database engines) and ``SFTP client``. Select nodes that
    might be used to ingest data as an ``SFTP client``, where you might want to work with
    Big SQL scripts, or other databases interactively.

#.  Click **Next** to review any options that you might want to customize.

#.  Click **Deploy**.

.. note::
  If the BigInsights – BigInsights Home service fails to install, run the
  ``remove_value_add_services.sh`` cleanup script located in ``/usr/ibmpacks/bin/<version>/remove_value_add_services.sh``

For more informaton about cleaning the value-add service environment, see Removing BigInsights value-add services


Configure Knox
---------------

The Apache Knox gateway is a system that provides a single point of authentication
and access for Apache Hadoop services on the compute nodes in a cluster; however
authentication to HDFS services is completely controlled by Isilon OneFS only.

The Knox gateway simplifies Hadoop security for users that access the cluster and
execute jobs and operators that control access and manage the cluster. The gateway
runs as a server, or a cluster of servers, providing centralized access to one or
more Hadoop clusters.

In IBM® Open Platform with Apache Hadoop, Knox is a service that you start, stop,
and configure in the Ambari web interface.

Users access the following BigInsights™ value added components through Knox by going
to the IBM BigInsights home service.

* BigSheets
* Text Analytics
* BigSQL

Knox supports only REST API calls for the following Hadoop services:

* WebHCAT
* Oozie
* HBase
* Hive
* YARN

**To Configure**

#.  Click the Knox service from the Ambari web interface to see the summary page.
#.  Select **Service Actions > Restart All** to restart it and all of its components.

.. note::
  If using LDAP, LDAP must be running

#.  Click the BigInsights Home service in the Ambari User Interface.

#.  Select Service Actions > Restart All to restart it and all of its components.
    Open the BigInsights Home page from a web.

#.  The URL for BigInsights Home is: ``https://<knox_host>:<knox_port>/<knox_gateway_path>/default/BigInsightsWeb/index.html``

    where

    * ``knox_host`` is the host running Knox
    * ``knox_port`` is the port where Knox is listening (8443 by default)
    * ``knox_gateway_path`` the value entered in the gateway.path field in the Ambari>Knox>Configs.  (normally this is 'gateway')


    An example URL might look like ``https://myhost.company.com:8443/gateway/default/BigInsightsWeb/index.html``

    .. note::
      If using the Knox Demo LDAP, a default user ID and password were already created.  When accessing this page,
      use the following credentials:

      username ``guest``
      password ``guest-password``


BigSheets
---------

To extend the power of the Open Platform for Apache Hadoop, install and deploy the
BigInsights BigSheets service, which is the IBM spreadsheet interface for big data.

#.  Click **Actions>Add Service** from the Ambari Dashboard.
#.  Select **BigInsights-BigSheets** service

    .. note::
      If you do not see **BigInsights-BigSheets**, make sure you installed the appropriate
      modules from the **Prework** section and restart Ambari.

#.  Click **Next**
#.  In the **Assign Masters** page, decide which node will run the BigSheets master.
#.  In the **Assign Slaves and Clients** page, all the defaults are automatically accepted.  The next
    page automatically appears.  **BigSheets** does not have any slaves or clients.  The
    **Assign Slaves and Clients** page will briefly show, and them immediately proceed.  This
    is expected behavior.
#.  In the **Customize Services** page, accept the recommended configuraitons for the BigShets service, or customize
    the configuration by expanding the configuration files and modifying their values.  In
    the **Advanced BigSheets-user-config** section, make sure of the following:

    #.  Leave the default username ``bigsheets`` in the ``bigsheets.user`` field.
    #.  Type a valid password in the ``bigsheets.password`` field.
    #.  Enter a ``bigsheets.userid`` that is unique across all nodes in the cluster.
    #.  Click **Next**
#.  Enter the **Ambari Admin** password in the ``ambari.password`` field.
#.  Review your changes before accepting them.  If for any reason errors are found
    or additional configuraiton is necessary, choose the **Back** button.
#.  When satistifed with all configuration changes, click **Deploy**
#.  **Test** the **BigSheets** service when the installation is complete.
#.  Click **Complete**

    .. note::
      If the **BigSheets** service fails to install, run the ``remove_value_add_services.sh`` cleanup script
      located in ``/usr/ibmpacks/bin/<version>``

#.  After BigSheets starts for the first time, the following services need to be restarted:

    * HDFS
    * MapReduce2
    * YARN
    * Knox
    * Nagios (if that is installed)
    * Ganglia (If that is installed)
    * BigInsights Home


#.  The URL for BigInsights Home is: ``https://<knox_host>:<knox_port>/<knox_gateway_path>/default/BigInsightsWeb/index.html``

    where

    * ``knox_host`` is the host running Knox
    * ``knox_port`` is the port where Knox is listening (8443 by default)
    * ``knox_gateway_path`` the value entered in the gateway.path field in the Ambari>Knox>Configs.  (normally this is 'gateway')


    An example URL might look like ``https://myhost.company.com:8443/gateway/default/BigInsightsWeb/index.html``

    .. note::
      If using the Knox Demo LDAP, a default user ID and password were already created.  When accessing this page,
      use the following credentials:

      username ``guest``
      password ``guest-password``


BigSQL
------

To extend the power of the Open Platform for Apache Hadoop, install and deploy the
BigInsights - Big SQL service, which is the IBM SQL interface to the Hadoop-based
platform, IBM Open Platform with Apache Hadoop.

#.  In the Ambari web interface, click **Actions > Add Service**.
#.  In the **Add Service Wizard**, Choose **Services**, select the **BigInsights - Big SQL service**,
    and the **BigInsights Home** service.

    .. note::
      If you do not see **BigInsights-BigSheets**, make sure you installed the appropriate
      modules from the **Prework** section and restart Ambari.

#.  Click **Next**.
#.  In the Assign Masters page, decide which nodes of your cluster you want to run
    the specified components, or accept the default nodes. Follow these guidelines:

    * For the Big SQL monitoring and editing tool, make sure that the Data Server
      Manager (DSM) is assigned to the same node that is assigned to the Big SQL Head node.

#.  Click **Next**.
#.  In the Assign Slaves and Clients page, accept the defaults, or make specific assignments
    for your nodes. Follow these guidelines:

    * Select the non-head (worker) nodes for the Big SQL Worker components. You must select at
      least one node as the worker node.
    * Select all nodes for the CLIENT. This puts JSqsh and SFTP clients on the nodes.

#.  In the Customize Services page, accept the recommended configurations for the Big SQL
    service, or customize the configuration by expanding the configuration files and modifying
    the values. Make sure that you have a valid ``bigsql_user`` and ``bigsql_user_password``
    *(see reference screen below)* and ``user_id`` (created by the ``bi_create_users.sh`` script)
    in the appropriate fields in the **Advanced bigsql-users-env** section.

    .. image::  bigsqlAdvUsers.png

#.  **Review** configuration changes before accepting.  Should any values require modification
    hit the **Back** button.  When satisfied, click **Deploy**
#.  In the **Install**, **Start and Test page**, the Big SQL service is installed and
    verified. If you have multiple nodes, you can see the progress on each node.
    When the installation is complete, either view the errors or warnings by clicking
    the link, or click **Next** to see a summary and then the new service added to the
    list of services.

    .. note::
      If the **BigInsights – Big SQL** service fails to install, run the ``remove_value_add_services.sh``
      cleanup script.

#.  A web application interface for Big SQL monitoring and editing is available
    to your end-users to work with Big SQL. You access this monitoring utility from
    the IBM BigInsights Home service. If you have not added the BigInsights Home
    service yet, do that now.
#.  Restart the **Knox** Service. Also start the Knox Demo LDAP service if you have not
    configured your own LDAP.
#.  Restart the **BigInsights Home** services.
#.  To run SQL statements from the Big SQL monitoring and editing tool, type the following
    address in your browser to open the BigInsights Home service:  ``https://<knox_host>:<knox_port>/<knox_gateway_path>/default/BigInsightsWeb/index.html``

    where

    * ``knox_host`` is the host running Knox
    * ``knox_port`` is the port where Knox is listening (8443 by default)
    * ``knox_gateway_path`` the value entered in the gateway.path field in the Ambari>Knox>Configs.  (normally this is 'gateway')


    An example URL might look like ``https://myhost.company.com:8443/gateway/default/BigInsightsWeb/index.html``

    .. note::
      If using the Knox Demo LDAP, a default user ID and password were already created.  When accessing this page,
      use the following credentials:

      username ``guest``
      password ``guest-password``


#.  If the **BigInsights - Big SQL** service shows as ``unavailable``, there might have been
    a problem with post-installation configuration. Run the following commands as **root**
    (or **sudo**) where the ``Big SQL monitoring utility (DSM)`` server is installed:

    #.  Run the ``dsmKnoxSetup``

        .. parsed-literal::
          cd /usr/ibmpacks/bigsql/<version-number>/dsm/1.1/ibm-datasrvrmgr/bin/
          ./dsmKnoxSetup.sh -knoxHost <knox-host>

        where ``<knox-host>`` is the node where the Knox gateway service is running.

    #.  Make sure that you do not stop and restart the Knox gateway service within
        Ambari. If you do, then run the ``dsmKnoxSetup`` script again.
    #.  Restart the **BigInsights Home** service so that the **Big SQL monitoring utility (DSM)**
        can be accessed from the **BigInsights Home** interface.

#.  For HBase, do the following post-installation steps:

    For all nodes where HBase is installed, check that the symlinks to hive-serde.jar
    and hive-common.jar in the hbase/lib directory are valid.

    #.  To verify the symlinks are created and valid:

        * ``namei /usr/iop/<version-number>/hbase/lib/hive-serde.jar``
        * ``namei /usr/iop/<version-number>/hbase/lib/hive-common.jar``

    #.  If they are not valid, do the following steps:

        * ``cd /usr/iop/<version-number>/hbase/lib``
        * ``rm -rf hive-serde.jar``
        * ``rm -rf hive-common.jar``
        * ``ln -s /usr/iop/<version-number>/hive/lib/hive-serde.jar hive-serde.jar``
        * ``ln -s /usr/iop/<version-number>/hive/lib/hive-common.jar hive-common.jar``

    .. note::
      After installing the Big SQL service, and fixing the symlinks, restart the HBase
      service from the Ambari web interface.

.. note::
  After you add Big SQL worker nodes **restart** the **Hive** service.


**Connecting to BigSQL**

You can run Big SQL queries from Java SQL Shell (JSqsh), or from the IBM Data Server
Manager. You can also run queries from a client application, such as IBM Data Studio,
that uses JDBC or ODBC drivers. You must identify a running Big SQL server and configure
either a JDBC or ODBC driver.

For more information about JSqsh, or IBM Data Studio, see the related topics in the
IBM® BigInsights™ Knowledge Center.

**Running JSqsh**

``JSqsh`` is installed in ``/usr/ibmpacks/common-utils/current/jsqsh/bin``. Change to that
directory and type ``./jsqsh`` to open the ``JSqsh`` shell:

.. parsed-literal::
  cd /usr/ibmpacks/common-utils/current/jsqsh/bin
  ./jsqsh

You can then run any ``JSqsh`` commands from the prompt.

**Connection setup**

To use the ``JSqsh`` command shell, you can use the default connections or define and test
a connection to the Big SQL server.

#.  The first time that you open the ``JSqsh`` command shell, a configuration wizard is started.
    When you are at the ``Jsqsh`` command prompt, type ``\drivers`` to determine the available drivers.

    #.  On the driver selection screen, select the ``Big SQL`` instance that you want to run

        .. note::
          Big SQL is designated as DB2 in this example


        .. parsed-literal::
              Name   Target   Class
              ------ -------- ------------------------------------
          ... 2 *db2 IBM Data Server(DB2 com.ibm.db2.jcc.DB2Driver

    #.  Verify the ``port``, ``server``, and ``user name``. Run ``\setup`` and click ``C`` to define
        a ``password`` for the connection. The *username* must have database administration
        privileges, or must be granted those privileges by the Big SQL administrator.
    #.  Test the connection to the Big SQL server.
    #.  Save and name this connection.

#.  Generally, you can access ``JSqsh`` from ``/usr/ibmpacks/common-utils/current/jsqsh/bin``
    with the following command:

    .. parsed-literal::
      ./jsqsh --driver=db2 --user=<username> --password=<user_password>

#.  Open the saved configuration wizard any time by typing ``\setup`` while in the
    command interface, or ``./jsqsh --setup`` when you open the command interface.
#.  Specify the following connection name in the ``JSqsh`` command shell to establish a connection:

    .. parsed-literal::
      ./jsqsh *name*

#.  Use the ``\connect`` command when you are already inside the ``JSqsh`` shell to establish
    a connection at the ``JSqsh`` prompt:

    .. parsed-literal::
      \connect name


**Commands and Queries**

At the ``JSqsh`` command prompt, you can run ``JSqsh`` commands or database server
commands. ``JSqsh`` commands usually begin with a backslash ``\`` character.

JSqsh commands accept command-line arguments and allow for common shell
activities, such as I/O redirection and pipes.

For example, consider this set of commands:

.. parsed-literal::
  1> select * from t1
  2> where c1 > 10
  3> \go --style csv > /tmp/t1.csv

Because the commands do not begin with a backslash character, the first two
commands are assumed to be SQL statements, and are sent to the Big SQL server.

The ``\go`` command sends the statements to run on the server. The ``\go`` command has
a built-in alias so that you can omit the backslash. Additionally, you can specify
a *trailing semicolon* to indicate that you want to run a statement, for example:

.. parsed-literal::
  1> select * from t1
  2> where c1 > 10;

The ``--style`` option in the ``\go`` command indicates that the display shows
comma-separated values (CSV). The ``\go`` form is most useful if you provide
additional arguments to affect how the query is run. Changing the display style
is an example of this feature.

The redirection operator ``>``specifies that the results of the command are sent
to a file called ``/tmp/t1.csv``.

A set of frequently run commands does not require the leading backslash. Any
``JSqsh`` command can bealiased to another name *(without a leading backslash, if
you choose)*, by using the ``\alias`` command. For example, if you want to be able to
type ``bye``, to leave the ``JSqsh`` shell, you establish that word as the alias for the
``\quit`` command:

.. parsed-literal::
  \\alias bye='quit'

You can run a script that contains one or more SQL statements. For example, assume
that you have a file called mySQL.sql. That file contains these statements:

.. parsed-literal::
  select tabschema, tabname from syscat.tables fetch first 5 rows only;
  select tabschema, colname, colno, typename, length from syscat.columns fetch first 10 rows only;

You can start JSqsh and run the script at the same time with this command:

.. parsed-literal::
  /usr/ibmpacks/common-utils/current/jsqsh/bin/jsqsh bigsql < /home/bigsql/mySQL.sql

The ``redirection operator`` specifies to ``JSqsh`` to get the commands from the file located
in the ``/home/bigsqldirectory``, and then run the statements within the file.

**Command and Query Edit**

The ``JSqsh`` command shell uses the ``JLine2`` library, which allows you to edit previously
entered commands and queries. You use the command-line edit features to move the arrow
keys and to edit the command or query on the current line.

The ``JLine2`` library provides the same key bindings *(vi and emacs)* as the ``GNU Readline
library``. In addition, it attempts to apply any custom key maps that you created in
a ``GNU Readline`` configuration file, *(.inputrc)* in the local file system ``$HOME/`` directory.

In addition to individual line editing, the ``JSqsh`` command shell remembers the 50
most recently run statements, which you can view by using the ``\history`` command:

.. parsed-literal::
  1> \\history
  (1) use tpch;
  (2) select count(*) from lineitem

Previously run statements are prefixed with a number in parentheses. You use this
number to recall that query by using the JSqsh recall operator (!), for example:

.. parsed-literal::
  1> !2
  1> select count(*) from lineitem
  2>

The ``!`` recall operator has the following behavior:
  * ``!!`` Recalls the previously run statement.
  * ``!5`` Recalls the fifth query from history.
  * ``!-2`` Recalls the query from two prior runs.

You can also edit queries that span multiple lines by using the ``\buf-edit`` command,
which pulls the current query into an external editor, for example:

.. parsed-literal::
  1> select id, count(*)
  2> from t1, t2
  3> where t1.c1 = t2.c2
  4> \\buf-edit

The query is opened in an external editor *(vi by default)*. However, you
can specify a different editor on the environment variable ``$EDITOR``. When you close
the editor, the edited query is entered at the ``JSqsh`` command shell prompt.

The ``JSqsh`` command shell provides built-in aliases, ``vi`` and ``emacs``, for the ``\buf-edit``
command. The following commands, for example, open the query in the ``vi`` editor:

.. parsed-literal::
  1> select id, count(*)
  2> from t1, t2
  3> where t1.c1 = t2.c2
  4> vi

**Configuration Variables**

You can use the ``\set`` command to list or define values for a number of configuration
variables, for example:

.. parsed-literal::
  1> \\set

If you want to redefine the prompt in the command shell, you run the following
command with the prompt option:

.. parsed-literal::
  1> \\set prompt='foo $lineno> '
  foo 1>

Every ``JSqsh`` configuration variable has built-in help available:

.. parsed-literal::
  1> \\help prompt

If you want to permanently set a specific variable, you can do so by editing
your ``$HOME/.jsqsh/sqshrc`` file and including the appropriate ``\set`` command
in it.


Text Analytics
--------------

The Text Analytics service provides powerful text extraction capabilities. You
can extract structured information from unstructured and semi-structured text.

It is recommended that you make sure that the ``python-paramiko`` package is installed
prior to installing the Text Analytics service.

.. parsed-literal::
  yum instsall python-paramiko

You will be selecting a Master node for Text Analytics, and this node should
contain the ``python-paramiko`` package. The master node is the node where Text
Analytics Web Tooling and Text Analytics Runtime are both installed.

#.  In the Ambari dashboard, click **Actions > Add Service**.
#.  In the **Add Service** Wizard, Choose **Services**, select the **BigInsights - Text Analytics**
    service.

    .. note::
      If you do not see the option to select the **BigInsights - Text Analytics** service,
      complete the steps in **Prework** section of this document.

#.  Click **Next**
#.  To assign master nodes, select the **Text Analytics Master** server Node.
#.  Click **Next**. The Assign Slaves and Clients page displays.
#.  Assign slave and client components to the hosts on which you want them to
    run. An asterisk (*) after a host name indicates the host is assigned a
    master component.

    #.  To assign slaves nodes and clients, click All on the Clients column.

        * The client package that is installed contains runtime binaries that
          are needed to run Text Analytics. This client needs to be installed
          on all datanodes that belong to your cluster.
        * Client nodes will install only the Text Analytics Runtime
          artifacts. ``/usr/ibmpacks/current/text-analytics-runtime``. Choose
          one or more clients. You do not have to choose the Master node as a
          client since it already installs Text Analytics Runtime.

#.  Click **Next** and select **BigInsights - Text Analytics**.
#.  Expand Advanced **ta-database-config** and enter the ``password`` in the
    ``database.password`` field.  Recommended configurations for the service are
    completed automatically but you can edit these default settings as desired.

    By default, the database server is MySQL. There are two options:

    #.  ``database.create.new = Yes`` (default)

        * You must enter the password for the database.
        * You must ensure that the default port, 32050 is free.
          You can change the port to any free port.
        * You can change the ``database.username``, but any changes to the
          ``database.hostnameare`` ignored.

    #.  ``database.create.new = N``

        * You must enter the database.hostname, database.port
          (where the existing database server instance is running), ``database.user``
          and ``database.password``. Ensure that the user and password have full
          access to create a database in the existing database server instance
          you specify. Especially if it is a remote MySQL server instance, ensure
          that all permissions are given to the user and password to access this
          remote instance. Ensure that the server instance is up and running so
          that the Text Analytics service can be started successfully.

#.  Click **Next** and in the Review screen that opens, click **Deploy**.
#.  After installation is complete, click **Next > Complete**.
#.  After the installation is successful, click **Next** and **Complete**.

    .. note::
      If the **BigInsights - Text Analytics** service fails to install, run
      the ``remove_value_add_services.sh`` cleanup script.

#.  The Text Analytics directory on all nodes where Text Analytics components
    are installed is created with world-writable permissions, which are not
    required. Change the permissions to ``rwxr-x-r-x`` on all nodes to improve
    security:

    .. parsed-literal::
      chmod go-w /usr/ibmpacks/text-analytics-runtime

#.  Restart the **Knox** service. If you have not configured LDAP service,
    start the **Knox Demo LDAP** service.

    .. image::  knoxRestart.png

#.  Open the **BigInsights Home** and launch **Text Analytics** at the following
    address:

    ``https://<knox_host>:<knox_port>/<knox_gateway_path>/default/BigInsightsWeb/index.html``

    where

    * ``knox_host`` is the host running Knox
    * ``knox_port`` is the port where Knox is listening (8443 by default)
    * ``knox_gateway_path`` the value entered in the gateway.path field in the Ambari>Knox>Configs.  (normally this is 'gateway')


    An example URL might look like ``https://myhost.company.com:8443/gateway/default/BigInsightsWeb/index.html``

    .. note::
      If using the Knox Demo LDAP, a default user ID and password were already created.  When accessing this page,
      use the following credentials:

      username ``guest``
      password ``guest-password``

    .. note::
      If you do not see the **Text Analytics** service from **BigInsights Home**,
      restart the **BigInsights Home** service in Ambari.

At this point, IBM BigHome should show all three Big Insights Services as shown below:

.. image::  textAnalytics.png


Big R
-----

To extend the power of the Open Platform for Apache Hadoop, install and deploy the
Big R service, which is the IBM R extension, to the Hadoop-based platform, IBM
Open Platform with Apache Hadoop.

.. note::
  This sectinon covers the installation of two services.  The ``R`` service and
  the ``Big R`` service.  Complete the instructions all the way through to ensure
  all requirements are met.

**Install R Service**

#.  In the Ambari web interface, click **Actions > Add Service.**
#.  In the **Add Service Wizard**, Choose **Services**, select the ``R`` service.
#.  Click *Next*
#.  In the **Assign Slaves and Clients** page, for client nodes, mark all of the
    nodes as the R Clientnode.
#.  Click **Next**
#.  In the **Customize Services** page, accept the recommended configurations for the
    ``R`` service, or customize the configuration by expanding the configuration files
    and modifying the values.

    #.  Make sure that you read the ``R`` license, and indicate acceptance by
        typing ``Y`` in the ``fieldaccept.R.Licenses``. **The value is case sensitive**, so
        make sure you type an uppercaseletter. The ``R`` Licenses field contains a
        URL where you can find the licensing information.
    #.  In the ``user.R.packages`` you must ensure that the following required
        packages are listed:  ``base64enc``, ``rJava``, and ``data.table``.
    #.  In the ``user.R.repository`` field, enter the preferred repository. The
        default is ``epel-release``, which uses the ``EPEL repository``, but you can also
        type a different repository by entering a URL, such as
        ``http://repos.domain.com/repos``.

        .. note::
           When installing R from the EPEL repository, you might have the
           following GPG key error: ``GPG key retrieval failed: [Errno 14]
           Could not open/read``

           If you receive this error, you can import the
           key with the following rpm command, then retry: ``rpm --import``

#.  Click **Next** and in the Review Page that opens, click **Deploy**.
#.  If ``R`` deployment fails, review and correct the errors before reattempting
    the installation. Remove the ``R`` service from Ambari and delete the RSERV
    server by using the following command:

    .. parsed-literal::
      curl -u [uid]:[pwd] -H "X-Requested-By: ambari" -X DELETE http://[hostname]:8080/api/v1/clusters/[cluster name]/services/RSERV

    where

    * ``[uid:[pwd]]`` = The Ambari Administrator User ID and Password
    * ``[hostname]`` = The correct hostname for your environment
    * ``8080`` = The port number 8080 is the default. Modify this according to your environment.
    * ``[cluster name]`` = The correct name of your cluster.

    Here is an example:

    .. parsed-literal::
      curl -u admin:admin -H "X-Requested-By: ambari" -X DELETE http://my_host.localdomain:8080/api/v1/clusters/my_cluster/services/RSERV

#.  In the Summary page, click **Complete**. When you return to the Ambari
    Dashboard Services tab, you notice that the ``R`` service is now listed.


**Install Big R Service**

#.  In the Ambari web interface, click **Actions > Add Service.**
#.  In the **Add Service** Wizard, Choose **Services**, select the ``Big R``
    service and click **Next**.
#.  In the **Assign Masters** page, decide which nodes of your cluster you want to
    run the specified components, or accept the default nodes. You must assign
    the ``Big R Connector`` to the same node that is running the MapReduce2 Client
    service, which is a required service that runs MapReduce2 Hadoop jobs. Click
    **Next**.
#.  In the **Assign Slaves and Clients** page, accept the defaults, or make
    specific assignments for your nodes. For client nodes, mark all of the
    nodes as the ``Big R Client`` node and click **Next**.
#.  In the **Customize Services** page, default ``Big R`` environment variables are
    set in the ``bigr-env template`` field. Review these entries for accuracy and
    completeness. Make any necessary changes and click **Next**
#.  You can review your selections in the **Review** page before accepting them.
    If you want to modify any values, click the **Back** button. If you are
    satisfied with your setup, click **Deploy**.
#.  In the **Install, Start and Test** page, the ``Big R`` service is installed and
    verified. If you have multiple nodes, you can see the progress on each
    node. When the installation is complete, either view the errors or
    warnings by clicking the link, or click **Next** to see a summary and then
    the new service added to the list of services.

    .. note::
      If the **BigInsights – Big R** service fails to install, run
      the ``remove_value_add_services.sh`` cleanup script.

#.  In the Summary page, click **Complete**.

Running BigInsights - Big R as the YARN application master
----------------------------------------------------------

You must update the ``Linux Container Executor`` as the default executor in the
yarn-site.xml file to change the owner to the ``bigr`` server user
*(the application process owner)*.  This must be edited from Ambari.  Ambari
overwrites any changes not made from Ambari.

#.  In the Ambari web interface, from the **YARN** service **Configs** page, scroll
    down to find the **Advanced yarn-site** and expand it.
#.  Change the ``yarn.nodemanager.container-executor.class`` property to have
    the following value: ``org.apache.hadoop.yarn.server.nodemanager.LinuxContainerExecutor``
#.  In the **Custom yarn-site** section, click **Add Property** to add the
    following properties:

    +----------------------------------------------------------------------+-------+
    | Property Name                                                        | Value |
    +======================================================================+=======+
    | yarn.nodemanager.linux-container-executor.nonsecure-mode.local-user  | Yarn  |
    +----------------------------------------------------------------------+-------+
    | yarn.nodemanager.linux-container-executor.nonsecure-mode.limit-users | False |
    +----------------------------------------------------------------------+-------+

#.  Make sure that the property ``yarn.nodemanager.linux-container-executor.group`` has
    the value ``hadoop``.
#.  Click **Save** in the Configs page to save your configuration changes.
#.  Make sure that the directories on ALL the nodes set in the **Node Manager**
    section for the properties ``yarn.nodemanager.local-dirs`` and
    ``yarn.nodemanager.log-dirs`` have permissions ``yarn:hadoop``.  On ALL nodes
    run the following commands:

    .. parsed-literal::
      $ echo "yarn.nodemanager.linux-container-executor.group=hadoop" >> /etc/hadoop/conf/container-executor.cfg
      $ echo "banned.users=hdfs,yarn,mapred,bin" >> /etc/hadoop/conf/container-executor.cfg
      $ echo "min.user.id=1000" >> /etc/hadoop/conf/container-executor.cfg
      $ chown root:hadoop /etc/hadoop/conf/container-executor.cfg
      $ chown root:hadoop /usr/iop/4.0.0.0/hadoop-yarn/bin/container-executor
      $ chmod 6050 /usr/iop/4.0.0.0/hadoop-yarn/bin/container-executor

#.  Make sure that the ``user ID`` with which the ``BigR`` connection is
    made (by using ``bigr.connect``) is present on ALL nodes, and that the user
    belongs to groups ``users`` and ``hadoop``.  If the user does not exist,
    run the following command as the root user on ALL nodes:  ``$ useradd -G users,hadoop someuser``
#.  Change the ``SystemML`` configuration file, ``/usr/ibmpacks/current/bigr/machine-learning/SystemML-config.xml``

    .. parsed-literal::
      dml.yarn.appmaster
      value: true

#.  You can optionally update the MapReduce configuration to get better performance:
    #.  In the Ambari web interface, from the **MapReduce2** service **Configs**
        page, scroll down to find the **Advanced map-red site** section and expand it.
    #.  Update the property ``mapreduce.task.io.sort.mb`` to ``384``.  With **BigInsights**
        this should be approximately three times the HDFS block size.

        .. note::
          If the property is not available, add it to the **Custom map-red site**.

#.  Click **Save** in the Configs page to save your configuration changes.



Big Insights Online Tutorials
=============================

Learn how to use BigInsights™ by completing `online tutorials <https://www-01.ib
m.com/support/knowledgecenter/SSPT3X_4.0.0/com.ibm.swg.im.infosphere.biginsights
.tut.doc/doc/tut_Introduction.html>`_, which use real data and teach you to run
applications. Complete the tutorials in any order.

You can find additional information, tutorials, and articles about BigInsights,
Hadoop, and related components at `Hadoop Dev <http://developer.ibm.com/hadoop/
docs/tutorials/>`_.

To isolate and resolve problems with BigInsights®, you can use the `troubleshoot
ing and support information <https://www-01.ibm.com/support/knowledgecenter/SSPT
3X_4.1.0/com.ibm.swg.im.infosphere.biginsights.trb.doc/doc/troubleshooting.html>`_
online. This information contains instructions for using the problem-determination
resources that are provided with BigInsights.


.. include:: ../common/where-to-go-from-here.rst

.. include:: ../common/linux-tuning.rst

.. include:: ../common/odp-tuning.rst

.. include:: ../common/isilon-tuning.rst

.. include:: ../common/known-limitations.rst

.. include:: ../common/legal.rst

.. include:: ../common/references.rst

http://www-03.ibm.com/software/products/en/ibm-biginsights-for-apache-hadoop

.. include:: ../common/substitutions.rst
