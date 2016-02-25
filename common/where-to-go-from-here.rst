
Where To Go From Here
=====================

You are now ready to fine-tune the configuration and performance of your
Isilon Hadoop environment. You should consider the following areas for
fine-tuning.

- Linux Tuning
- Hadoop Tuning
- Isilon Tuning
- Universally applicable settings

Linux Tuning
------------

**Kernel Parameters**

Where possible the following should be set on the compute nodes:
  *  transparent hugepage is disabled.
  *  vm.overcommit_memory is 1
  *  vm.swappiness is ideally 0, but anything below 10 is generally accepted.  Pivotal Hawq likes this value to be 2.

.. note::
  Cloudera Manager will provide directions for setting these values during installation.

Hadoop Tuning
-------------

DO NOT transfer values from one cluster to another cluster unless values are defaults.
Many of the below settings include memory tuning specifications that can render job failures if
work is being transferred to a cluster with lesser footprint.  In kind, if settings are transferred from an older
configuration to a newer one, with newer hardware, the performance of the new cluster is inherently limited.  For
best results tune to your cluster's unique specifications.

**ODP (Hortonworks, Pivotal, IBM, etc...)**

ODP distributions start with Hortonworks Data Platform as their core.  Hortonworks makes
a nice tool available to help determine what the appropriate YARN and Mapreduce settings should
be for a given environment.  `See this site for details <http://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.3.2/bk_installing_manually_book/content/determine-hdp-memory-config.html>`_

An example of the Hortonworks tool is as follows, where the system has 20 cores, 256G of ram,
was not using HBase, and had 18 disks (36 drive Isilon divided by 2 compute hosts)

.. parsed-literal::
  $ python yarn-utils.py  -c 20 -m 256 -d 18 --hbase=False
  Using cores=20 memory=256GB disks=18 hbase=False
  Profile: cores=20 memory=229376MB reserved=32GB usableMem=224GB disks=18
  Num Container=33
  Container Ram=6656MB
  Used Ram=214GB
  Unused Ram=32GB
  yarn.scheduler.minimum-allocation-mb=6656
  yarn.scheduler.maximum-allocation-mb=219648
  yarn.nodemanager.resource.memory-mb=219648
  mapreduce.map.memory.mb=6656
  mapreduce.map.java.opts=-Xmx5324m
  mapreduce.reduce.memory.mb=6656
  mapreduce.reduce.java.opts=-Xmx5324m
  yarn.app.mapreduce.am.resource.mb=6656
  yarn.app.mapreduce.am.command-opts=-Xmx5324m
  **mapreduce.task.io.sort.mb=2662**

Simply take these values, search and tune for them in Ambari>Configs.  In most cases
service restarts are required.

.. note::
  In some cases the value for **mapreduce.task.io.sort.mb** will exceed 2048.  A value
  in excess of 2048 will return job failures, explicitly calling out this value exceeds 2048.  If
  the value given for your configuration exceeds 2048, use 2048.

**Cloudera**

A similar planning utility is available for Cloudera.  `Cloudera's planning tool is available here <http://www.cloudera.com/documentation/enterprise/latest/topics/cdh_ig_yarn_tuning.html>`_
Cloudera's tool takes the form of a spreadsheet.  Just as above, take the recommendations
from the spreadsheet, search and tune for them in Cloudera Manager>Configurations.  In
most cases services restarts are required.

.. note::
  DO NOT apply values from one distribution's tool to another.  (i.e, do not use Hortonwork's output for Cloudera Tuning or reverse)
  While the core is similar, there are differences between them such as SQL Query Engines and YARN schedulers that are impacted if not tuned
  appropriately for their respective tool sets.

Isilon Tuning
-------------

**Socket Cache Re-use**

If running OneFS 7.2, disable socket cache re-use in Hadoop.  OneFS 7.2 does not support
socket cache re-use.  To disable, ``dfs.client.socketcache.capacity = 0``  The default
value is ``16``.  OneFS 8 fully supports socket cache re-use, rendering this tweak unnecesary.

**IP Pools**

In order to provide the best aggregate throughput from Isilon configure isilon per the best practice of using
one Dynamic IP Pool for Name Node Connections, and another or several Static IP Pools for Data Node Connections.
Using one pool is enticing, however it does not really benefit a failed task in so far as YARN
will attempt a retry on a failed static pool, vs the task will failover in a dynamic pool.  In either case
the job will continue.  The difference being a reduced risk data node connections are unbalanced, which can
occur during periods of high activity with dynamic data node pools.  Use Static for data node pools for best results.

**I/O Pattern**

OneFS provides the ability to alter the disk layout and caching algorithms for data via
tunable parameter known as io pattern.  This parameter can be set on files or directories, with or without
inheritance.  Generally speaking, data associated with MapReduce tasks should be set for Streaming.  Data
expected to be used primarily for interactive SQL query should use Concurrency.  IF the same data
will be accessed in both forms use Concurrency.

**SSD Strategy**

Isilon systems with SSD's can use a number of default SSD Strategies.  L3 Caching, Metadata Read, or Metadata Read
and Write.  Best results with OneFS 7.x systems are obtained with either Metadata Read or Metadata Read and Write.
The latter option performs best but requires more SSD space.  L3 for Hadoop, with OneFS 7.2 is discouraged.  In OneFS8 the
observed differences between these policies is nearly equal.

**HDFS Threads**

OneFS 7.x provided a means of tuning the available number of HDFS threads per node.  Values had a max of 256, and
and Auto setting of 80.  It is best to leave the HDFS threads to 80 from 7.2.0.3 and higher.  OneFS8 saw a significant
redesign in this area and the threading option was removed entirely.  The same subsystem that handles SMB and NFS threads now
also services HDFS threads, with the result being far more threads than ever was before.

**TCP Buffer Sysctls**

Isilon networking can be tweaked in the following ways to provide an appropriate set of
tcp buffers.  These are issued as sysctl's.  In testing we've found the ``Half`` values perform
well in most circumstances.

These are the Defaults:
  *  kern.ipc.maxsockbuf=2097152
  *  net.inet.tcp.sendbuf_max=262144
  *  net.inet.tcp.recvbuf_max=262144
  *  net.inet.tcp.sendbuf_inc=8192
  *  net.inet.tcp.recvbuf_inc=16384
  *  net.inet.tcp.sendspace=131072
  *  net.inet.tcp.recvspace=131072

These are about Half of Max:
  *  kern.ipc.maxsockbuf=8388608
  *  net.inet.tcp.sendbuf_max=8388608
  *  net.inet.tcp.recvbuf_max=8388608
  *  net.inet.tcp.sendbuf_inc=16384
  *  net.inet.tcp.recvbuf_inc=16384
  *  net.inet.tcp.sendspace=524288
  *  net.inet.tcp.recvspace=524288

These are the Max:
  *  kern.ipc.maxsockbuf=16777216
  *  net.inet.tcp.sendbuf_max=16777216
  *  net.inet.tcp.recvbuf_max=16777216
  *  net.inet.tcp.sendbuf_inc=16384
  *  net.inet.tcp.recvbuf_inc=16384
  *  net.inet.tcp.sendspace=1048576
  *  net.inet.tcp.recvspace=1048576

Universally Applicable
----------------------

**Jumbo Frames**

Hadoop does well with Jumbo Frames between the compute node interfaces and the Isilon
Storage Interfaces.  Ensure all storage interfaces on the hadoop nodes, all Isilon interfaces of interest,
and all switch ports, are all configured appropriately.  **Mistmatches cost performance.**
