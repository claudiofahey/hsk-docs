Isilon Scale-Out NAS For HDFS
-----------------------------

EMC Isilon is the only scale-out NAS platform natively integrated with
the Hadoop Distributed File System (HDFS). Using HDFS as an
over-the-wire protocol, you can deploy a powerful, efficient, and
flexible data storage and analytics ecosystem.

In addition to native integration with HDFS, EMC Isilon storage easily
scales to support massively large Hadoop analytics projects. Isilon
scale-out NAS also offers unmatched simplicity, efficiency, flexibility,
and reliability that you need to maximize the value of your Hadoop data
storage and analytics workflow investment.

Overview of Isilon Scale-Out NAS for Big Data
---------------------------------------------

The EMC Isilon scale-out platform combines modular hardware with unified
software to provide the storage foundation for data analysis. Isilon
scale-out NAS is a fully distributed system that consists of nodes of
modular hardware arranged in a cluster. The distributed Isilon OneFS
operating system combines the memory, I/O, CPUs, and disks of the nodes
into a cohesive storage unit to present a global namespace as a single
file system.

The nodes work together as peers in a shared-nothing hardware
architecture with no single point of failure. Every node adds capacity,
performance, and resiliency to the cluster, and each node acts as a
Hadoop namenode and datanode. The namenode daemon is a distributed
process that runs on all the nodes in the cluster. A compute client can
connect to any node through HDFS.

As nodes are added, the file system expands dynamically and
redistributes data, eliminating the work of partitioning disks and
creating volumes. The result is a highly efficient and resilient storage
architecture that brings all the advantages of an enterprise scale-out
NAS system to storing data for analysis.

Unlike traditional storage, Hadoop's ratio of CPU, RAM, and disk space
depends on the workload—factors that make it difficult to size a Hadoop
cluster before you have had a chance to measure your MapReduce workload.
Expanding data sets also makes sizing decisions upfront problematic.
Isilon scale-out NAS lends itself perfectly to this scenario: Isilon
scale-out NAS lets you increase CPUs, RAM, and disk space by adding
nodes to dynamically match storage capacity and performance with the
demands of a dynamic Hadoop workload.

An Isilon cluster optimizes data protection. OneFS more efficiently and
reliably protects data than HDFS. The HDFS protocol, by default,
replicates a block of data three times. In contrast, OneFS stripes the
data across the cluster and protects the data with forward error
correction codes, which consume less space than replication with better
protection.
