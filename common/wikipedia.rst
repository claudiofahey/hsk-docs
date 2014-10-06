
Searching Wikipedia
===================

One of the many unique features of Isilon is its multi-protocol support. This allows you, for instance, to
write a file using SMB (Windows) or NFS (Linux/Unix) and then read it using HDFS to perform Hadoop
analytics on it.

In this section, we exercise this capability to download the entire Wikipedia database (excluding media) using
your favorite browser to Isilon. As soon as the download completes, we'll run a Hadoop grep to search
the entire text of Wikipedia using our Hadoop cluster. As this search doesn't rely on a word index, your regular
expression can be as complicated as you like.

#.  First, let's connect your client (with your favorite web browser) to your Isilon cluster.
  
    #.  If you are using a Windows host or other SMB client:
      
        #.  Click Start -> Run.
        
        #.  Enter: ``\\subnet0-pool0.isiloncluster1.lab.example.com\ifs``
        
        #.  You may authenticate as *root* with your Isilon root password.
        
        #.  Browse to ``\ifs\isiloncluster1\zone1\hadoop\tmp``.
        
        #.  Create a directory here called *wikidata*. This is where you will download the Wikipedia data to.

    #.  If you are using a Linux host or other NFS client:

        #.  Mount your NFS export.

            .. parsed-literal::

              [root\@workstation ~]$ **mkdir /mnt/isiloncluster1**
              [root\@workstation ~]$ **echo subnet0-pool0.isiloncluster1.lab.example.com:\\
              /ifs /mnt/isiloncluster1 nfs \\
              nolock,nfsvers=3,tcp,rw,hard,intr,timeo=600,retrans=2,rsize=131072,wsize=524288 \\
              >> /etc/fstab**
              [root\@workstation ~]$ **mount -a**
              [root\@workstation ~]$ **mkdir -p /mnt/isiloncluser1/isiloncluster1/zone1/hadoop/tmp/wikidata**

#.  Open your favorite web browser and go to http://dumps.wikimedia.org/enwiki/latest.
    
    .. image:: ../common/images/wikipedia-browser.png
        
#.  Locate the file ``enwiki-latest-pages-articles.xml.bz2`` and download it directly to the *wikidata* folder
    on Isilon. Your web browser will be writing this file to the Isilon file system using SMB or NFS.

    .. note:: 
       This file is approximately 10 GB in size and contains the entire text of the English version of Wikipedia.
       If this is too large, you may want to download one of the smaller files such as enwiki-latest-all-titles.gz

    .. image:: ../common/images/wikipedia-save-as.png

    .. note::
       If you get an access-denied error, the quickest resolution is to SSH into any node in your
       Isilon cluster as root and run ``chmod -R a+rwX /ifs/isiloncluster1/zone1/hadoop/tmp``.

#.  Now let's run the Hadoop grep job. We'll search for all two-word phrases that begin with `EMC`.

    .. parsed-literal::

      [hduser1\@mycluster1-master-0 ~]$ **hadoop fs -ls /tmp/wikidata**
      [hduser1\@mycluster1-master-0 ~]$ **hadoop fs -rm -r /tmp/wikigrep**
      [hduser1\@mycluster1-master-0 ~]$ **hadoop jar \\**
      |hadoop-mapreduce-examples-jar| **\\
      grep /tmp/wikidata /tmp/wikigrep "EMC [^ ]*"**

#.  When the the job completes, use your favorite text file viewer to view the output file */tmp/wikigrep/part-r-00000*.
    If you are using Windows, you may open the file in Wordpad.

    .. image:: ../common/images/wikipedia-output-dir.png

    .. image:: ../common/images/wikipedia-wordpad.png

#.  That's it! Can you think of anything else to search for?

