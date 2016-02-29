
Prepare VMware Big Data Extensions
==================================

Installing Big Data Extensions
------------------------------

Refer to `VMware Big Data Extensions documentation
<http://pubs.vmware.com/bde-2/index.jsp>`_ for complete install details.
For a typical deployment, only the steps in the following
topics need to be performed:

- Installing Big Data Extensions

  - Deploy the Big Data Extensions vApp in the vSphere Web Client

  - Install the Big Data Extensions Plug-In

  - Connect to a Serengeti Management Server

- Managing vSphere Resources for Hadoop and HBase Clusters

  - Add a Datastore in the vSphere Web Client

  - Add a Network in the vSphere Web Client

How to Login to the Serengeti CLI
---------------------------------

The Serengeti CLI is installed on your Big Data Extensions vApp server.
You will first change directory to the path that contains your BDE spec
files which define the VMs to create.

.. parsed-literal::

    [root\@bde ~]# **cd /mnt/scripts/isilon-hadoop-tools/etc**
    [root\@bde etc]# **java -jar /opt/serengeti/cli/serengeti-cli-\*.jar**
    serengeti>\ **connect --host localhost:8443**
    Enter the username: **root**
    Enter the password: **\*\*\***
    Connected

.. note::

    If you deployed BDE with VMWare SSO be sure to log into Serengi CLI\
    with your VMWare SSO credentials!!

View Resources
--------------

Use the commands below to view your BDE resources. Their names will be needed later.

.. parsed-literal::

    serengeti>\ **network list**
    serengeti>\ **datastore list**
    serengeti>\ **resourcepool list**
