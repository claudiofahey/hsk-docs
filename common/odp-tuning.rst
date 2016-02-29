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

.. note::
  DO NOT apply values from one distribution's tool to another.  (i.e, do not use Hortonwork's output for Cloudera Tuning or reverse)
  While the core is similar, there are differences between them such as SQL Query Engines and YARN schedulers that are impacted if not tuned
  appropriately for their respective tool sets.
