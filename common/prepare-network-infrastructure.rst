Prepare Network Infrastructure
==============================

Configure DHCP and DNS on Windows Server 2008 R2
------------------------------------------------

DHCP and DNS servers are often configured incorrectly in a lab
environment. This section will show you some key steps to configure a
Windows Server 2008 R2 server for DHCP and DNS. Other operating systems
can certainly be used as long as they operate the same way from the
client perspective.

#. Open Server Manager.

#. Forward Lookup Zone

   #. Create a forward lookup zone for your lab domain (lab.example.com).

      |image2|

   #. To avoid possible DNS dynamic update issues, select the option to
      allow unsecure dynamic updates. This may not be required in your
      environment and the best settings for a production deployment should be
      carefully considered.

      |image4|

#. Create a reverse lookup zone for your lab subnet
   (128.111.10.in-addr.arpa). If you have multiple subnets, this will be
   the subnet used by your worker VMs.

#. Configure your DHCP server for dynamic DNS.

   #. Right-click on IPv4 (see the screen shot below), then click Properties.

      |image6|

   #. Configure the DNS settings as shown below. These settings will
      allow the DHCP server to automatically create DNS A and PTR records for
      DHCP clients.

      |image8|

   #. Specify the credential used by the DHCP service to communicate with the DNS server.
      
      |image10|

#. Create a new DHCP scope for your lab subnet.

   #. Set the following scope options for your environment.
      
      |image12|

#. Test for a proper installation.

    #. A CentOS or Redhat Linux machine configured for DHCP should
       specify the DHCP\_HOSTNAME parameter. In particular, the file
       /etc/sysconfig/network should contain "DHCP\_HOSTNAME=myhost" and it
       should **not** specify "HOSTNAME=myhost". It is this setting that allows
       the DHCP server to automatically create DNS records for the host. After
       editing this file, restart the network with "service network restart".

    #. A Windows machine only needs to be configured for DHCP on an
       interface.

    #. Confirm that the forward DNS record myhost.lab.example.com is
       dynamically created on your DNS server. You should be able to ping the
       FQDN from all hosts in your environment.

       .. parsed-literal::

        [user\@workstation ~]$ **ping myhost.lab.example.com**
        PING myhost.lab.example.com (10.111.128.240) 56(84) bytes of data.
        64 bytes from myhost.lab.example.com (10.111.128.240): icmp\_seq=1 
        ttl=64 time=1.47 ms

    #. Confirm that the reverse DNS record for that IP address can be
       properly resolved to myhost.lab.example.com.

       .. parsed-literal::

        [user\@workstation ~]$ **dig +noall +answer -x 10.111.128.240**
        240.128.111.10.in-addr.arpa. 900 IN      PTR    myhost.lab.example.com.

