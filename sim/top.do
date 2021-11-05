# Copyright 1991-2016 Mentor Graphics Corporation
# 
# Modification by Oklahoma State University
# Use with Testbench 
# James Stine, 2008
# Go Cowboys!!!!!!
#
# All Rights Reserved.
#
# THIS WORK CONTAINS TRADE SECRET AND PROPRIETARY INFORMATION
# WHICH IS THE PROPERTY OF MENTOR GRAPHICS CORPORATION
# OR ITS LICENSORS AND IS SUBJECT TO LICENSE TERMS.

# Use this run.do file to run this example.
# Either bring up ModelSim and type the following at the "ModelSim>" prompt:
#     do run.do
# or, to run from a shell, type the following at the shell prompt:
#     vsim -do run.do -c
# (omit the "-c" to see the GUI while running from the shell)

onbreak {resume}

# create library
if [file exists work] {
    vdel -all
}
vlib work

# compile source files
vlog -lint ../src/address_clock_sdr_2r1w_64.v ../src/ra_bist_ddr.v ../src/predecode_sdr_64.v ../src/ra_bist_sdr.v ../src/ra_2r1w_64x72_sdr.v ../src/ra_cfg_ddr.v ../src/regfile_2r1w_64x24.v ../src/toysram.vh ../src/ra_4r2w_64x72_ddr_1x.v ../src/ra_cfg_sdr.v ../src/regfile_4r2w_64x24.v ../src/ra_4r2w_64x72_ddr.v ../src/ra_delay.v ../src/ra_lcb_sdr.v  ../src/ra_lcb_ddr.v ../src/test_ra_ddr.v ../src/test_ra_sdr.sv ../src/test_ra_ddr_1x.v 

# start and run simulation
vsim -debugdb -voptargs=+acc work.test_ra_sdr

view wave

-- display input and output signals as hexidecimal values
# Diplays All Signals recursively
add wave -noupdate -divider -height 32 "ra_lcb_sdr"
add wave -hex -r /lcb/*
add wave -noupdate -divider -height 32 "ra_cfg_sdr"
add wave -hex -r /cfig/*
add wave -noupdate -divider -height 32 "ra_bist_sdr"
add wave -hex -r /bist/*
add wave -noupdate -divider -height 32 "ra_2r1w_64x72_sdr"
add wave -hex -r /ra/*


-- Set Wave Output Items 
TreeUpdate [SetDefaultTree]
WaveRestoreZoom {0 ps} {75 ns}
configure wave -namecolwidth 250
configure wave -valuecolwidth 400
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2

-- Run the Simulation 
run 1300ns
quit
