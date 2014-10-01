Create DNS Records For Isilon
-----------------------------

You will now create the required DNS records that will be used to access
your Isilon cluster.

#.  Create a delegation record so that DNS requests for the zone
    isiloncluster1.lab.example.com are delegated to the Service IP that will
    be defined on your Isilon cluster. The Service IP can be any unused
    static IP address in your lab subnet.

    #.  If using a Windows Server 2008 R2 server, see the screenshot
        below to create the delegation.

        |image18|

    #.  Enter the DNS domain that will be delegated. This should identify
        your Isilon cluster. Click Next.

        |image20|

    #.  Enter the DNS domain again. Then enter the Isilon SmartConnect
        Zone Service IP address. At this time, you can ignore any warning
        messages about not being able to validate the server. Click OK. 

        |image22|

    #.  Click Next and then Finish.
        
        |image24|

#.  If you are using your own lab DNS server, you should create a
    CNAME alias for your Isilon SmartConnect zone. For example, create a
    CNAME record for mycluster1-hdfs.lab.example.com that targets
    subnet0-pool0.isiloncluster1.lab.example.com.

    |image26|

#.  Test name resolution.
    
    .. parsed-literal::

      [user\@workstation ~]$ **ping mycluster1-hdfs.lab.example.com**
      PING subnet0-pool0.isiloncluster1.lab.example.com (10.111.129.115) 56(84) 
      bytes of data.
      64 bytes from 10.111.129.115: icmp\_seq=1 ttl=64 time=1.15 ms

