# plain rtl + 16x12 dummy

export OR_SEED = 8675309

export DESIGN_NICKNAME = toysram_16x12_wrapper
export DESIGN_NAME = toysram_16x12_wrapper
export PLATFORM    = sky130hd
export SCRIPT_DIR = $(shell dirname $(DESIGN_CONFIG))

export SRC_DIR = $(SCRIPT_DIR)/src/array

export VERILOG_FILES_BLACKBOX = $(SCRIPT_DIR)/toysram_16x12_wrapper_gdsdummy.v

# no intermediate macro, gds/lef use vectors
export VERILOG_FILES = $(SCRIPT_DIR)/toysram_16x12_wrapper.v \
                       $(VERILOG_FILES_BLACKBOX)

export SDC_FILE      = $(SCRIPT_DIR)/constraint.sdc

export DIE_AREA   =  0  0   500 500
export CORE_AREA  = 10 10   490 490

export PLACE_DENSITY ?= 0.1
export USE_FILL =

export ABC_CLOCK_PERIOD_IN_PS = 2000
export ABC_SPEED = 1

export ADDITIONAL_GDS_FILES = $(SCRIPT_DIR)/toysram_16x12.gds
export ADDITIONAL_LEFS  = $(SCRIPT_DIR)/toysram_16x12.lef

# I/O
#export IO_CONSTRAINTS = io_constraints.tcl
# -group_pins [get_ports iBus*]
#export PLACE_PINS_ARGS = -exclude left:* -exclude right:* -exclude top:* -exclude bottom:0-300 -exclude bottom:1500-3000

export MACRO_PLACEMENT = $(SCRIPT_DIR)/macro_vec.cfg
# enforce spacing/restrict placement
export MACRO_PLACE_HALO ?= 50 50
#export MACRO_PLACE_CHANNEL ?= 100 100

export export SETUP_SLACK_MARGIN = 0.2

