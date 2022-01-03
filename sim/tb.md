# **``ra_sdr`` Testbench Explanation**

The purpose of this document is to explain how the testbench for ``test_ra_sdr.sv``.

This is an elementary testbench that drives set values in order to write and read the SDR memory. Discrete and unique values are written to unique addresses in the
memory array, and then 2 addresses each are read at the same time until all values are outputted.

at line 120 of ``test_ra_sdr.sv`` is when the test starts. all values were chosen to be unique so they can clearly be identified in the ModelSim runs. outputs should be
seen in ``rd_dat_0`` and ``rd_dat_1``.


###### Peter Tikalsky, 2022
