#!/bin/sh
CELL1=$(basename "$1" .spice)
CELL2=$(basename "$2" .spice)

netgen -noc << EOF
permute transistors
lvs "$1 $CELL1" "$2 $CELL2" $CELL1.out
quit
EOF
