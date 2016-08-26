.. _prereq:

Prerequisites
=============

Isilon
------

- For low-capacity, non-performance testing of Isilon, the EMC
  Isilon OneFS Simulator can be used instead of a cluster of physical
  Isilon appliances. This can be downloaded for free from
  http://www.emc.com/getisilon. Refer to the *EMC Isilon OneFS Simulator
  Install Guide* for details. Be sure to follow the section for running
  the virtual nodes in VMware ESX. Only a single virtual node is required
  but adding additional nodes will allow you to explore other features
  such as data protection, SmartPools (tiering), and SmartConnect (network
  load balancing).

- For physical Isilon nodes, you should have already completed
  the console-based installation process for your first Isilon node and
  added at least two other nodes for a minimum of 3 Isilon nodes.

- You must have OneFS version 7.1.1.0 with patch-130611
  or version 7.2.0.3 and higher.

- You must obtain a OneFS HDFS license code and install it on
  your Isilon cluster. You can get your free OneFS HDFS license from
  http://www.emc.com/campaign/isilon-hadoop/index.htm.

- It is recommended, but not required, to have a SmartConnect
  Advanced license for your Isilon cluster.

- To allow for scripts and other small files to be easily
  shared between all nodes in your environment, it is highly recommended
  to enable NFS (Unix Sharing) on your Isilon cluster. By default, the
  entire /ifs directory is already exported and this can remain unchanged in
  test or development environments.  It is best practice to close this hole for
  production use.  This document assumes that a single Isilon cluster is used
  for this NFS export as well as for HDFS. However, there is no requirement that
  the NFS export be on the same Isilon cluster that you are using for HDFS.

VMware
------

- VMware vSphere Enterprise or Enterprise Plus

- VMware vSphere vCenter should be installed and functioning.

- All hosts referenced in this document can be virtualized with
  VMware ESXi.

- At a **minimum** for non-performance testing, you will need a
  single VMware ESXi host with 72 GB of RAM.

- VMDK files we be used for the operating system and
  applications for each host. Additionally, VMDKs will be used for
  temporary files needed to process Hadoop jobs (e.g. MapReduce spill and
  shuffle files). VMDKs can be located on physical disks attached to the
  ESXi host or on a shared NFS datastore hosted on an Isilon cluster. If
  using an Isilon cluster, be aware that the VMDK I/O will compete with
  the HDFS I/O, reducing the overall performance.

- All ESXi hosts must be managed by vCenter.

- As a requirement for the VMware Big Data Extensions vApp, you
  must define a vSphere cluster.

Networking
----------

- For the best performance, a single 10 Gigabit Ethernet switch
  should connect to at least one 10 Gigabit port on each ESXi host running
  a worker VM. Additionally, the same switch should connect to at least
  one 10 Gigabit port on each Isilon node.

- A single dedicated layer-2 network can be used to connect all
  ESXi hosts and Isilon nodes. Although multiple networks can be used for
  increased security, monitoring, and robustness, it adds complications
  that should be avoided when possible.

- At least an entire /24 IP address block should be allocated
  to your lab network. This will allow a DNS reverse lookup zone to be
  delegated to your own lab DNS server.

- If not using DHCP for dynamic IP address allocation, a static
  set of IP addresses must be assigned to Big Data Extensions so that it
  may allocate them to new virtual machines that it provisions. You will
  usually need just one IP address for each virtual machine.

- If using the EMC Isilon OneFS Simulator, you will need at
  least two static IP addresses (one for the node's ext-1 interface,
  another for the SmartConnect service IP). Each additional Isilon node
  will require an additional IP address.

- At a minimum, you will need to allocate to your Isilon
  cluster one IP address per Access Zone per Isilon node. In general, you
  will need one Access Zone for each separate Hadoop cluster that will use
  Isilon for HDFS storage. For the best possible load balancing during an
  Isilon node failure scenario, the recommended number of IP addresses is
  give by the formula below. Of course, this is in addition to any IP
  addresses used for non-HDFS pools.

  ``# of IP addresses = 2 * (# of Isilon Nodes) * (# of Access Zones)``

  For example, 20 IP addresses are recommended for 5 Isilon nodes and 2
  Access Zones.

- This document will assume that Internet access is available
  to all servers to download various components from Internet
  repositories.

DHCP and DNS
-------------

- A DHCP server on this subnet is highly recommended. Although
  a DHCP server is not a requirement for a Hadoop environment, this
  document will assume that one exists.

- A DNS server is required and you must have the ability to
  create DNS records and zone delegations.

- Although not required, it is assumed in this document that a
  Windows Server 2008 R2 server is running on this subnet providing DHCP
  and DNS services. To distinguish this DNS server from a corporate or
  public DNS server outside of your lab, this will be referred to as your
  *lab* DNS server.

- It is recommended, and this document will assume, that the
  DHCP server creates forward and reverse DNS records when it provides IP
  address leases to hosts. The procedure for doing this is documented
  later in this document.

- It is recommend that a forward lookup DNS zone be delegated
  to your lab DNS server. For instance, if your company's domain is
  example.com, then DNS requests for lab.example.com, and all subdomains
  of lab.example.com, should be delegated to your lab DNS server.

- It is recommended that your DNS server delegate a subdomain
  to your Isilon cluster. For instance, DNS requests for
  subnet0-pool0.isiloncluster1.lab.example.com or
  isiloncluster1.lab.example.com should be delegated to the Service IP
  defined on your Isilon cluster.

- To allow for a convenient way of changing the HDFS Name Node
  used by all Hadoop applications and services, it is recommended to
  create a DNS record for your Isilon cluster's HDFS Name Node service.
  This should be a CNAME alias to your Isilon SmartConnect zone. Specify a
  TTL of 1 minute to allow for quick changes while you are experimenting.
  For example, create a CNAME record for mycluster1-hdfs.lab.example.com
  that targets subnet0-pool0.isiloncluster1.lab.example.com. If you later
  want to redirect all HDFS I/O to another cluster or a different pool on
  the same Isilon cluster, you simply need to change the DNS record and
  restart all Hadoop services.

Other
-----

- You will need one Linux workstation which you will use to
  perform most configuration tasks. No services will run on this
  workstation.

  - This should have a GUI and a web browser.

  - This must have Python 2.6.6 or higher 2.x version.

  - CentOS 6.5 has been used for testing but most other systems should
    also work. However, be aware that Centos 6.4, supplied with BDE 2.0,
    must be upgraded to support Python 2.6.6.

  - sshpass must be installed. This document shows how to install
    sshpass on Centos 6.x.

- Several useful scripts and file templates are provided in the
  archive file ``isilon-hadoop-tools-*x*.*x*.tar.gz``. Download the latest
  version from `Github <https://github.com/isilon/isilon_hadoop_tools/releases>`_.

- Time synchronization is critical for Hadoop. It is highly
  recommended to configure all ESXi hosts and Isilon nodes to use NTP. In
  general, you do not need to run NTP clients in your VMs.
