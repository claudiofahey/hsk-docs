
13. Map the *hdfs* user to the Isilon superuser. This will allow the
    *hdfs* user to chown (change ownership of) all files.

    .. warning::

      The command below will restart the HDFS service on Isilon to ensure
      that any cached user mapping rules are flushed. This will temporarily
      interrupt any HDFS connections coming from other Hadoop clusters.

    .. parsed-literal::

      isiloncluster1-1# **isi zone zones modify --user-mapping-rules="hdfs=>root" \\
      --zone zone1**
      isiloncluster1-1# **isi services isi\_hdfs\_d disable ; \\
      isi services isi\_hdfs\_d enable**
      The service 'isi\_hdfs\_d' has been disabled.
      The service 'isi\_hdfs\_d' has been enabled.

#.  Set the owner and permissions for the HDFS root directory.
    You first need to determine the access zone ID. 
    Then we will run the ``chown`` command in the context of this access zone.

    .. parsed-literal::

      isiloncluster1-1# **isi zone zones view zone1**
      ...
                        Zone ID: 2
      isiloncluster1-1# **isi_run -z 2 chown hdfs:hadoop \\
      /ifs/isiloncluster1/zone1/hadoop**

