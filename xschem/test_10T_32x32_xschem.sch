v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 180 -1690 180 -1680 {
lab=VDD}
N 180 -1620 180 -1610 {
lab=GND}
C {10T_32x32_xschem.sym} 0 -160 0 0 {name=x1}
C {devices/vsource.sym} 180 -1650 0 0 {name=V1 value=1.8}
C {devices/lab_pin.sym} 180 -1690 0 0 {name=l8 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 180 -1610 0 0 {name=l9 sig_type=std_logic lab=GND}
C {devices/code_shown.sym} 290 -1550 0 0 {name=NGSPICE
only_toplevel=true
place=end
value="
.tran 1ps 30ns
"}
C {devices/code.sym} 280 -1710 0 0 {name=TT_MODELS
only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SKYWATER_MODELS/sky130.lib.spice tt

"}
