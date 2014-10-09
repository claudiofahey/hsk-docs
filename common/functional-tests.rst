Functional Tests
================

The tests below should be performed to ensure a proper installation.
Perform the tests in the order shown.

You must create the Hadoop user *hduser1* before proceeding.

HDFS
----

.. parsed-literal::

  [root\@mycluster1-master-0 ~]# **sudo -u hdfs hdfs dfs -ls /**
  Found 5 items
  -rw-r--r--   1 root  hadoop              0 2014-08-05 05:59 /THIS_IS_ISILON
  drwxr-xr-x   - hbase hbase             148 2014-08-05 06:06 /hbase
  drwxrwxr-x   - solr  solr                0 2014-08-05 06:07 /solr
  drwxrwxrwt   - hdfs  supergroup        107 2014-08-05 06:07 /tmp
  drwxr-xr-x   - hdfs  supergroup        184 2014-08-05 06:07 /user
  [root\@mycluster1-master-0 ~]# **sudo -u hdfs hdfs dfs -put -f /etc/hosts /tmp**
  [root\@mycluster1-master-0 ~]# **sudo -u hdfs hdfs dfs -cat /tmp/hosts**
  127.0.0.1 localhost
  [root\@mycluster1-master-0 ~]# **sudo -u hdfs hdfs dfs -rm -skipTrash /tmp/hosts**
  [root\@mycluster1-master-0 ~]# **su - hduser1**
  [hduser1\@mycluster1-master-0 ~]$ **hdfs dfs -ls /**
  Found 5 items
  -rw-r--r--   1 root  hadoop              0 2014-08-05 05:59 /THIS_IS_ISILON
  drwxr-xr-x   - hbase hbase             148 2014-08-05 06:28 /hbase
  drwxrwxr-x   - solr  solr                0 2014-08-05 06:07 /solr
  drwxrwxrwt   - hdfs  supergroup        107 2014-08-05 06:07 /tmp
  drwxr-xr-x   - hdfs  supergroup        209 2014-08-05 06:39 /user
  [hduser1\@mycluster1-master-0 ~]$ **hdfs dfs -ls**

YARN / MapReduce
----------------

.. parsed-literal::

  [hduser1\@mycluster1-master-0 ~]$ **hadoop jar \\**
  |hadoop-mapreduce-examples-jar| **\\
  pi 10 1000**
  ...
  Estimated value of Pi is 3.14000000000000000000
  [hduser1\@mycluster1-master-0 ~]$ **hadoop fs -mkdir in**

You can put any file into the *in* directory. It will be used the
datasource for subsequent tests.

.. parsed-literal::

  [hduser1\@mycluster1-master-0 ~]$ **hadoop fs -put -f /etc/hosts in**
  [hduser1\@mycluster1-master-0 ~]$ **hadoop fs -ls in**
  [hduser1\@mycluster1-master-0 ~]$ **hadoop fs -rm -r out**
  [hduser1\@mycluster1-master-0 ~]$ **hadoop jar \\**
  |hadoop-mapreduce-examples-jar| **\\
  wordcount in out**
  [hduser1\@mycluster1-master-0 ~]$ **hadoop fs -ls out**
  Found 4 items
  -rw-r--r--   1 hduser1 hduser1          0 2014-08-05 06:44 out/_SUCCESS
  -rw-r--r--   1 hduser1 hduser1         24 2014-08-05 06:44 out/part-r-00000
  -rw-r--r--   1 hduser1 hduser1          0 2014-08-05 06:44 out/part-r-00001
  -rw-r--r--   1 hduser1 hduser1          0 2014-08-05 06:44 out/part-r-00002
  [hduser1\@mycluster1-master-0 ~]$ **hadoop fs -cat out/part\***
  localhost     1
  127.0.0.1     1

Browse to the YARN Resource Manager GUI
``http://mycluster1-master-0.lab.example.com:8088/``.

Browse to the MapReduce History Server GUI
``http://mycluster1-master-0.lab.example.com:19888/``.
In particular, confirm that you can view the complete logs for task attempts.

Hive
----

.. parsed-literal::

  [hduser1\@mycluster1-master-0 ~]$ **hadoop fs -mkdir -p sample\_data/tab1**
  [hduser1\@mycluster1-master-0 ~]$ **cat - > tab1.csv
  1,true,123.123,2012-10-24 08:55:00
  2,false,1243.5,2012-10-25 13:40:00
  3,false,24453.325,2008-08-22 09:33:21.123
  4,false,243423.325,2007-05-12 22:32:21.33454
  5,true,243.325,1953-04-22 09:11:33**
  
Type <Control+D>.

.. parsed-literal::

  [hduser1\@mycluster1-master-0 ~]$ **hadoop fs -put -f tab1.csv sample_data/tab1**
  [hduser1\@mycluster1-master-0 ~]$ **hive**
  hive> 
  **DROP TABLE IF EXISTS tab1;
  CREATE EXTERNAL TABLE tab1
  (
     id INT,
     col\_1 BOOLEAN,
     col\_2 DOUBLE,
     col\_3 TIMESTAMP
  )
  ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
  LOCATION '/user/hduser1/sample\_data/tab1';

  DROP TABLE IF EXISTS tab2;
  
  CREATE TABLE tab2
  (
     id INT,
     col\_1 BOOLEAN,
     col\_2 DOUBLE,
     month INT,
     day INT
  )
  ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

  INSERT OVERWRITE TABLE tab2
  SELECT id, col\_1, col\_2, MONTH(col\_3), DAYOFMONTH(col\_3)
  FROM tab1 WHERE YEAR(col\_3) = 2012;**
  ...
  OK
  Time taken: 28.256 seconds

  hive> **show tables;**
  OK
  tab1
  tab2
  Time taken: 0.889 seconds, Fetched: 2 row(s)

  hive> **select \* from tab1;**
  OK
  1      true   123.123       2012-10-24 08:55:00
  2      false  1243.5        2012-10-25 13:40:00
  3      false  24453.325     2008-08-22 09:33:21.123
  4      false  243423.325    2007-05-12 22:32:21.33454
  5      true   243.325       1953-04-22 09:11:33
  Time taken: 1.083 seconds, Fetched: 5 row(s)

  hive> **select \* from tab2;**
  OK
  1      true   123.123       10     24
  2      false  1243.5        10     25
  Time taken: 0.094 seconds, Fetched: 2 row(s)  

  hive> **exit;**

Pig
---

.. parsed-literal::

  [hduser1\@mycluster1-master-0 ~]$ **pig**
  grunt> **a = load 'in';**
  grunt> **dump a;**
  ...
  Success!
  ...
  grunt> **quit;**

HBase
-----

.. parsed-literal::

  [hduser1\@mycluster1-master-0 ~]$ **hbase shell**
  hbase(main):001:0> **create 'test', 'cf'**
  0 row(s) in 3.3680 seconds
  => Hbase::Table - test
  hbase(main):002:0> **list 'test'**
  TABLE                                                                                                                                                                                               
  test                                                                                                                                                                                                 
  1 row(s) in 0.0210 seconds
  => ["test"]
  hbase(main):003:0> **put 'test', 'row1', 'cf:a', 'value1'**
  0 row(s) in 0.1320 seconds
  hbase(main):004:0> **put 'test', 'row2', 'cf:b', 'value2'**
  0 row(s) in 0.0120 seconds
  hbase(main):005:0> **scan 'test'**
  ROW                         COLUMN+CELL                                                                                                                                      
   row1                        column=cf:a,timestamp=1407542488028,value=value1
   row2                        column=cf:b,timestamp=1407542499562,value=value2
  2 row(s) in 0.0510 seconds
  hbase(main):006:0> **get 'test', 'row1'**
  COLUMN                      CELL
   cf:a                        timestamp=1407542488028,value=value1
  1 row(s) in 0.0240 seconds
  hbase(main):007:0> **quit**

