
#.  Execute the script isilon\_create\_users.sh.
    This script will create all required users and groups for the Hadoop services
    and applications.

    .. warning::

      The script isilon\_create\_users.sh will create local
      user and group accounts on your Isilon cluster for Hadoop services. If you are using a
      directory service such as Active Directory, and you want these users and
      groups to be defined in your directory service, then DO NOT run this
      script. Instead, refer to the OneFS documentation and `EMC
      Isilon Best Practices for Hadoop Data
      Storage <http://www.emc.com/collateral/white-paper/h12877-wp-emc-isilon-hadoop-best-practices.pdf>`__.  
      
    Script Usage: isilon\_create\_users.sh --dist <DIST> [--startgid <GID>] [--startuid <UID>] [--zone <ZONE>]

    dist
      This will correspond to your Hadoop distribution - |hsk_dst|

    startgid
      Group IDs will begin with this value. For example: 501

    startuid
      User IDs will begin with this value. This is generally the same as gid_base. For example: 501

    zone
      Access Zone name. For example: System

    .. parsed-literal::

      isiloncluster1-1# **bash \\
      /ifs/isiloncluster1/scripts/isilon-hadoop-tools/onefs/isilon\_create\_users.sh \\
      --dist **\ |hsk_dst_strong|\ **--startgid 501 --startuid 501 --zone zone1**

#.  Execute the script isilon\_create\_directories.sh.
    This script will create all required directories with the appropriate ownership and permissions.

    Script Usage: isilon\_create\_directories.sh --dist <DIST> [--fixperm] [--zone <ZONE>]

    dist
      This will correspond to your Hadoop distribution - |hsk_dst|

    fixperm
      If specified, ownership and permissions will be set on existing directories.

    zone
      Access Zone name. For example: System

    .. parsed-literal::

      isiloncluster1-1# **isi_run -z 2 bash \\
      /ifs/isiloncluster1/scripts/isilon-hadoop-tools/onefs/isilon\_create\_directories.sh \\
      --dist **\ |hsk_dst_strong|\ **--fixperm --zone zone1**
