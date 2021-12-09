*
.include "/home/tdene/Public/skywater-src-nda/s8_spice_models/models.all"

.include "/home/tdene/Public/skywater-src-nda/s8_spice_models/tt_discrete.cor"
.include "/home/tdene/Public/skywater-src-nda/s8_spice_models/ttcell.cor"

.include "/home/tdene/Public/skywater-src-nda/s8_spice_models/npd.pm3"
.include "/home/tdene/Public/skywater-src-nda/s8_spice_models/npass.pm3"
.include "/home/tdene/Public/skywater-src-nda/s8_spice_models/ppu.pm3"

*** Define power and ground
vvdd vdd 0 DC 1.8V
vgnd gnd 0 DC 0V

.SUBCKT invM A1 O 
M_1 O A1 vdd vdd ppu w=0.14 l=0.15
M_2 O A1 gnd gnd npd w=0.21 l=0.15
.ENDS

* start main CELL 10T-toy
.SUBCKT MEM10T-toy RBL0 RBL1 RWL0 RWL1 WBL WBLb WWL 
XinvM net_1 net_4 invM 
M_1 net_1 WWL WBL gnd npass w=0.14 l=0.15
M_2 WBLb WWL net_4 gnd npass w=0.14 l=0.15 
M_3 net_2 RWL0 RBL0 gnd npd w=0.21 l=0.15 
M_4 gnd net_1 net_2 gnd npass w=0.14 l=0.15 
M_5 RBL1 RWL1 net_3 gnd npd w=0.21 l=0.15 
M_6 net_3 net_4 gnd gnd npass w=0.14 l=0.15
XInv net_4 net_1 invM 
.ENDS

* Starts low
* Allows for a write at 5ns
* Goes back low at 10ns
* Allows for another write at 20ns
* Goes back low at 25ns
vWWL WWL gnd pwl 0ns 0V 4.9ns 0V 5ns 1.8V 9.9ns 1.8V 10ns 0V 19.9ns 0V 20ns 1.8V 24.9ns 1.8V 25ns 0V
* Starts low
* At the 5ns write, we set this high
* Goes back low at 10ns
* At the 20ns write, we set this low
* Goes back low at 25ns
vWBL  WBL  gnd pwl 0ns 0V 4.9ns 0V 5n 1.8V 9.9ns 1.8V 10ns 0V 19.9ns 0V 20ns 0V   24.9ns   0V 25ns 0V
vWBLb WBLb gnd pwl 0ns 0V 4.9ns 0V 5n 0.0V 9.9ns 0.0V 10ns 0V 19.9ns 0V 20ns 1.8V 24.9ns 1.8V 25ns 0V
* Starts low
* At the 5ns write, stays low
* Goes high at 10ns to read
* At the 20ns write, goes low
* Goes high at 25ns to read
vRWL0 RWL0 gnd pwl 0ns 0V 4.9ns 0V 5ns 0.0V 9.9ns 0.0V 10ns 1.8V 19.9ns 1.8V 20ns 0.0V 24.9ns 0.0V 25ns 1.8V
vRWL1 RWL0 RWL1 0V

X1 RBL0 RBL1 RWL0 RWL1 WBL WBLb WWL MEM10T-toy
*X1 WWL Out invM

.tran 1ps 30ns

.print DC V(WWL) V(RBL0) V(RBL1) V(RWL0) V(RWL1) V(RBL) V(RBLb)   
.print tran V(WWL) V(RBL0) V(RBL1) V(RWL0) V(RWL1) V(RBL) V(RBLb)   
.probe V(WWL) V(RBL0) V(RBL1) V(RWL0) V(RWL1) V(RBL) V(RBLb) 
.op
.options probe post measout captab
.end
