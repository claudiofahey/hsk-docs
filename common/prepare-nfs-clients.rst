Prepare NFS Clients
===================

To allow for scripts and other small files to be easily shared between
all servers in your environment, it is highly recommended to enable NFS
(Unix Sharing) on your Isilon cluster. By default, the entire /ifs
directory is already exported and this can remain unchanged. However,
Isilon best-practices suggest creating an NFS mount for
/ifs/*isiloncluster1*/scripts.

#.  On Isilon, create an NFS export for /ifs/*isiloncluster1*/scripts.
    Enable read/write and root access from all hosts in your lab subnet.

#.  Mount your NFS export on your workstation and the BDE server.
    (Note: The BDE post-deployment script can automatically perform these
    steps for VMs deployed using BDE.).

    .. parsed-literal::

      [root\@workstation ~]$ **yum install nfs-utils**
      [root\@workstation ~]$ **mkdir /mnt/scripts**
      [root\@workstation ~]$ **echo subnet0-pool0.isiloncluster1.lab.example.com:\\
      /ifs/isiloncluster1/scripts /mnt/scripts nfs \\
      nolock,nfsvers=3,tcp,rw,hard,intr,timeo=600,retrans=2,rsize=131072,wsize=524288 \\
      >> /etc/fstab**
      [root\@workstation ~]$ **mount -a**

#.  If you want to locate any VMDKs on an Isilon cluster instead of on
    local disks, add an NFS datastore to each of your ESXi hosts.

