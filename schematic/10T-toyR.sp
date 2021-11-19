.include "/home/tdene/Public/skywater-src-nda/s8_spice_models/models.all"
.include "/home/tdene/Public/skywater-src-nda/s8_spice_models/tt_discrete.cor"

*** Define power and ground
vvdd vdd 0 DC 1.8V
vgnd gnd 0 DC 0V

.SUBCKT invM A1 O 
M_1 O A1 vdd vdd ppu w=0.14u l=0.15u
M_2 O A1 gnd gnd npd w=0.21u l=0.15u
.ENDS

* start main CELL 10T-toy
.SUBCKT MEM10T-toy RBL0 RBL1 RWL0 RWL1 WBL WBLb WWL 
XinvM net_1 net_4 invM 
M_1 net_1 WWL WBL gnd npd w=0.21u l=0.15u
M_2 WBLb WWL net_4 gnd npd w=0.21u l=0.15u 
M_3 net_2 RWL0 RBL0 gnd npd w=0.21u l=0.15u 
M_4 gnd net_1 net_2 gnd npd w=0.21u l=0.15u 
M_5 RBL1 RWL1 net_3 gnd npd w=0.21u l=0.15u 
M_6 net_3 net_4 gnd gnd npd w=0.21u l=0.15u 
XInv net_4 net_1 invM 
.ENDS

vin1 WWL gnd pulse 0 1.8V 0ns 750ps 750ps 14.8ns 30ns
vin2 RWL1 gnd 0V
vin3 RWL0 gnd 0V
*X1 RBL0 RBL1 RWL0 RWL1 WBL WBLb WWL MEM10T-toy
X1 WWL Out invM

.tran 1ns 45ns

.print DC V(WWL) V(RBL0) V(RBL1) V(RWL0) V(RWL1) V(RBL) V(RBLb)   
.print tran V(WWL) V(RBL0) V(RBL1) V(RWL0) V(RWL1) V(RBL) V(RBLb)   
.probe V(WWL) V(RBL0) V(RBL1) V(RWL0) V(RWL1) V(RBL) V(RBLb)   
.op
.options probe post measout captab
.end
