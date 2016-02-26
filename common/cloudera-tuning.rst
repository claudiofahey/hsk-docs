Hadoop Tuning
-------------

DO NOT transfer values from one cluster to another cluster unless values are defaults.
Many of the below settings include memory tuning specifications that can render job failures if
work is being transferred to a cluster with lesser footprint.  In kind, if settings are transferred from an older
configuration to a newer one, with newer hardware, the performance of the new cluster is inherently limited.  For
best results tune to your cluster's unique specifications.

**Cloudera**

A similar planning utility is available for Cloudera.  `Cloudera's planning tool is available here <http://www.cloudera.com/documentation/enterprise/latest/topics/cdh_ig_yarn_tuning.html>`_
Cloudera's tool takes the form of a spreadsheet.  Just as above, take the recommendations
from the spreadsheet, search and tune for them in Cloudera Manager>Configurations.  In
most cases services restarts are required.

.. note::
  DO NOT apply values from one distribution's tool to another.  (i.e, do not use Hortonwork's output for Cloudera Tuning or reverse)
  While the core is similar, there are differences between them such as SQL Query Engines and YARN schedulers that are impacted if not tuned
  appropriately for their respective tool sets.
