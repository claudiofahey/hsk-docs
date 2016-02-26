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
