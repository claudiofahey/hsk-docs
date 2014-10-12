
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
