Known Limitations
=================

OneFS only provides WebHDFS over HTTPS but not HTTP.
Some Hadoop services and applications require WebHDFS on HTTP. Note that having a trusted SSL
certificate on the Isilon cluster may correct this problem, although this has not been tested.

Although Kerberos is supported by OneFS, this document
does not address a Hadoop environment secured with Kerberos. Instead,
refer to `EMC Isilon Best Practices for Hadoop Data
Storage <http://www.emc.com/collateral/white-paper/h12877-wp-emc-isilon-hadoop-best-practices.pdf>`__.

