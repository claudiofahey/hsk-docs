Hosts
-----

A typical Hadoop environment composed of many types of hosts. Below is a
description of these hosts.

|image0|

List of Hosts in Hadoop Environments

+----------------------------+----------------------------------------------------------------------------------------------------------------------------+
| Host (Host Name)           | Description                                                                                                                |
+============================+============================================================================================================================+
| DNS/DHCP Server            | It is recommended to have a DNS and DHCP server that you can                                                               |
|                            | control. This will be used by all other hosts for DNS and                                                                  |
|                            | DHCP services.                                                                                                             |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+
| VMware vCenter             | VMware vCenter will manage all ESXi hosts and their VMs. It                                                                |
|                            | is required for Big Data Extensions (BDE).                                                                                 |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+
| VMware Big Data Extensions | This will run the Serengeti components to assist in                                                                        |
| vApp Server (bde)          | deploying Hadoop clusters.                                                                                                 |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+
| VMware ESXi                | Physical machines will run the VMware ESXi operating system                                                                |
|                            | to allow virtual machines to run in them.                                                                                  |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+
| Linux workstation          | You should have a Linux workstation with a GUI that you can                                                                |
| (workstation)              | use to control everything with.                                                                                            |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+
| Isilon nodes               | You will need one or more Isilon Scale-Out NAS nodes. For                                                                  |
| (isiloncluster1-1, 2, 3,   | functional testing, you can use a single Isilon OneFS                                                                      |
| ...)                       | Simulator node instead of the Isilon appliance. The nodes                                                                  |
|                            | will be clustered together into an *Isilon Cluster*. Isilon                                                                |
|                            | nodes run the OneFS operating system.                                                                                      |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+
| Isilon InsightIQ           | This is optional licensed software from Isilon and can be                                                                  |
|                            | used to monitor the health and performance of your Isilon                                                                  |
|                            | cluster. It is recommend for any performance testing.                                                                      |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+
| |hadoop-manager|           | This host will manage your Hadoop cluster. This will run |hadoop-manager| which will deploy and monitor the Hadoop         |
| (hadoopmanager-server-0)   | components. In smaller environments, you may choose to deploy |hadoop-manager| to your Hadoop Master host.                 |
|                            |                                                                                                                            |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+
| Hadoop Master              | This host will the YARN Resource Manager, Job History                                                                      |
| (mycluster1-master-0)      | Server, Hive Metastore Server, etc.. In general,                                                                           |
|                            | it will run all "master" services except for the HDFS Name                                                                 |
|                            | Node.                                                                                                                      |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+
| Hadoop Worker              | There will be any number of worker nodes, depending on the                                                                 |
| Node (mycluster1-worker-0, | compute requirements. Each node will run the YARN Node                                                                     |
| 1, 2, ...)                 | Manager, HBase Region Server, etc.. During the                                                                             |
|                            | installation process, these nodes will run                                                                                 |
|                            | the HDFS Data Node but these will become idle like the HDFS Name Node.                                                     |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+

Due to the many hosts involved, all commands that must be typed are prefixed with the standard
system prompt identifying the user and host name. For example:

.. parsed-literal::

    [user\@workstation ~]$ **ping myhost.lab.example.com**

