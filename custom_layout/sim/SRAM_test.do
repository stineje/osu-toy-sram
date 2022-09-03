# Title:    SRAM_work.do
# Author:   ryan.ridley@okstate.edu
# Date:     
# Modified: 
# Purpose:  .do file script to simulate ra_2r1w_32x32_sdr.v

onbreak {resume}

# create library
if [file exists work] {
    vdel -all
}
vlib work

## compile source files
vlog ra_2r1w_32x32_sdr_tb.v ra_2r1w_32x32_sdr.v toysram.vh address_clock_sdr_2r1w_32.v regfile_2r1w_32x32.v predecode_sdr_32.v

# start and run simulation
vsim -voptargs=+acc work.tb

view list
view wave

add wave -noupdate -divider -height 32 "Control Signals"
add wave -binary -color orange /tb/clk
add wave -binary -color orange /tb/reset
add wave -binary -color orange /tb/strobe

add wave -noupdate -divider -height 32 "Write 0"
add wave -binary -color blue /tb/wr_enb_0
add wave -binary -color blue /tb/wr_adr_0
add wave -binary -color gold /tb/wr_dat_0

add wave -noupdate -divider -height 32 "Read 0"
add wave -binary -color blue /tb/rd_enb_0
add wave -binary -color blue /tb/rd_adr_0
add wave -binary -color gold /tb/rd_dat_0

add wave -noupdate -divider -height 32 "Read 1"
add wave -binary -color blue /tb/rd_enb_1
add wave -binary -color blue /tb/rd_adr_1
add wave -binary -color gold /tb/rd_dat_1

add wave -noupdate -divider -height 32 "add_clk"
add wave -binary -color blue /tb/dut/add_clk/*

add wave -noupdate -divider -height 32 "array0"
add wave -binary -color blue /tb/dut/array0/*







-- Set Wave Output Items
TreeUpdate [SetDefaultTree]
WaveRestoreZoom {0 ps} {75 ns}
configure wave -namecolwidth 150
configure wave -valuecolwidth 150 
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 5
configure wave -childrowmargin 2

-- Run the Simulation
run 99999999ns

