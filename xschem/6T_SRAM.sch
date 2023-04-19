v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 1100 -2670 1120 -2670 {
lab=Q_B}
N 1100 -2410 1120 -2410 {
lab=Q_B}
N 1230 -2670 1280 -2670 {
lab=Q}
N 1230 -2670 1230 -2410 {
lab=Q}
N 1230 -2410 1280 -2410 {
lab=Q}
N 1120 -2670 1150 -2670 {
lab=Q_B}
N 1150 -2670 1150 -2410 {
lab=Q_B}
N 1120 -2410 1150 -2410 {
lab=Q_B}
N 960 -2550 1060 -2550 {
lab=Q}
N 1060 -2630 1060 -2440 {
lab=Q}
N 1320 -2640 1320 -2440 {
lab=Q_B}
N 1320 -2550 1420 -2550 {
lab=Q_B}
N 930 -2660 930 -2590 {
lab=WL}
N 1450 -2660 1450 -2590 {
lab=WL}
N 1480 -2550 1520 -2550 {
lab=BL_B}
N 870 -2550 900 -2550 {
lab=BL}
N 870 -2700 870 -2550 {
lab=BL}
N 870 -2550 870 -2410 {
lab=BL}
N 1060 -2380 1060 -2350 {
lab=GND}
N 1060 -2350 1320 -2350 {
lab=GND}
N 1320 -2380 1320 -2350 {
lab=GND}
N 1060 -2720 1060 -2700 {
lab=VDD}
N 1060 -2720 1320 -2720 {
lab=VDD}
N 1320 -2720 1320 -2700 {
lab=VDD}
N 1520 -2700 1520 -2420 {
lab=BL_B}
N 1060 -2590 1230 -2590 {
lab=Q}
N 1150 -2510 1320 -2510 {
lab=Q_B}
C {sky130_fd_pr/nfet_01v8.sym} 930 -2570 1 0 {name=A1
L=0.15
W=0.21
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 1450 -2570 1 0 {name=A2
L=0.15
W=1
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 1080 -2410 2 0 {name=D1
L=0.15
W=1
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 1300 -2410 0 0 {name=D2
L=0.15
W=1
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 1080 -2670 2 0 {name=P1
L=0.15
W=1
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 1300 -2670 0 0 {name=P2
L=0.15
W=1
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {devices/gnd.sym} 1190 -2350 0 0 {name=l1 lab=GND}
C {devices/vdd.sym} 1190 -2720 0 0 {name=l2 lab=VDD}
C {devices/lab_pin.sym} 930 -2660 0 0 {name=l3 sig_type=std_logic lab=WL}
C {devices/lab_pin.sym} 870 -2700 0 0 {name=l4 sig_type=std_logic lab=BL}
C {devices/lab_pin.sym} 1450 -2660 0 0 {name=l5 sig_type=std_logic lab=WL}
C {devices/lab_pin.sym} 1520 -2700 0 0 {name=l6 sig_type=std_logic lab=BL_B}
C {devices/lab_pin.sym} 1060 -2550 2 0 {name=l7 sig_type=std_logic lab=Q}
C {devices/lab_pin.sym} 1320 -2550 0 0 {name=l8 sig_type=std_logic lab=Q_B}
