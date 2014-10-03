
Where To Go From Here
=====================

You are now ready to fine-tune the configuration and performance of your
Isilon Hadoop environment. You should consider the following areas for
fine-tuning.

- YARN NodeManager container memory

- Isilon HDFS daemon thread count (e.g. "isi hdfs settings modify --server-threads 255")

- Isilon HDFS read block size (e.g. "isi hdfs settings modify --default-block-size 512M")
