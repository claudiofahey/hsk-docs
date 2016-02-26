Linux Tuning
------------

**Kernel Parameters**

Where possible the following should be set on the compute nodes:
  *  transparent hugepage is disabled.
  *  vm.overcommit_memory is 1
  *  vm.swappiness is ideally 0, but anything below 10 is generally accepted.  Pivotal Hawq likes this value to be 2.
