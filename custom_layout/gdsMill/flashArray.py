#!/usr/bin/env python
import sys
import gdsMill

input_path = "../../virtuoso/gds/"
output_path = "../gds/"

if len(sys.argv) > 1:
    numCols = int(sys.argv[1])
else:
    numCols = 1024
if len(sys.argv) > 2:
    numRows = int(sys.argv[2])
else:
    numRows = 1024
if len(sys.argv) > 3:
    blockSize = int(sys.argv[3])
else: blockSize = 32

out_name = "flash_array_" + str(numCols) + "x" + str(numRows)

# Size of cells
SIDE_WIDTH = 2.515
MID_WIDTH = 1.44
END_HEIGHT = 2.96
CELL_HEIGHT = 0.86
MID_HEIGHT = 1.61

# Location of labels
BL_end_x = 2.875
BL_BL_x = .72
WL_x = 0.26

y_offset = 0

cellMidLayout = gdsMill.VlsiLayout()
cellLeftLayout = gdsMill.VlsiLayout()
cellRightLayout = gdsMill.VlsiLayout()

endMidLayout = gdsMill.VlsiLayout()
endLeftLayout = gdsMill.VlsiLayout()
endRightLayout = gdsMill.VlsiLayout()

botMidLayout = gdsMill.VlsiLayout()
botLeftLayout = gdsMill.VlsiLayout()
botRightLayout = gdsMill.VlsiLayout()

BLMidLayout = gdsMill.VlsiLayout()
BLLeftLayout = gdsMill.VlsiLayout()
BLRightLayout = gdsMill.VlsiLayout()

SLMidLayout = gdsMill.VlsiLayout()
SLLeftLayout = gdsMill.VlsiLayout()
SLRightLayout = gdsMill.VlsiLayout()

reader = gdsMill.Gds2reader(cellMidLayout)
reader.loadFromFile(input_path + "flash_cell_2x2.gds")
reader = gdsMill.Gds2reader(cellLeftLayout)
reader.loadFromFile(input_path + "flash_left_2.gds")
reader = gdsMill.Gds2reader(cellRightLayout)
reader.loadFromFile(input_path + "flash_right_2.gds")

reader = gdsMill.Gds2reader(endMidLayout)
reader.loadFromFile(input_path + "flash_end_2.gds")
reader = gdsMill.Gds2reader(endLeftLayout)
reader.loadFromFile(input_path + "flash_end_left.gds")
reader = gdsMill.Gds2reader(endRightLayout)
reader.loadFromFile(input_path + "flash_end_right.gds")

reader = gdsMill.Gds2reader(botMidLayout)
reader.loadFromFile(input_path + "flash_bot_2.gds")
reader = gdsMill.Gds2reader(botLeftLayout)
reader.loadFromFile(input_path + "flash_bot_left.gds")
reader = gdsMill.Gds2reader(botRightLayout)
reader.loadFromFile(input_path + "flash_bot_right.gds")

reader = gdsMill.Gds2reader(BLMidLayout)
reader.loadFromFile(input_path + "flash_midBL_2.gds")
reader = gdsMill.Gds2reader(BLLeftLayout)
reader.loadFromFile(input_path + "flash_midBL_left.gds")
reader = gdsMill.Gds2reader(BLRightLayout)
reader.loadFromFile(input_path + "flash_midBL_right.gds")

reader = gdsMill.Gds2reader(SLMidLayout)
reader.loadFromFile(input_path + "flash_midSL_2.gds")
reader = gdsMill.Gds2reader(SLLeftLayout)
reader.loadFromFile(input_path + "flash_midSL_left.gds")
reader = gdsMill.Gds2reader(SLRightLayout)
reader.loadFromFile(input_path + "flash_midSL_right.gds")

newLayout = gdsMill.VlsiLayout(name=out_name)

def placeTopRow(block):
    x_offset = 0
    global y_offset

    mirror = None
    BL_y = 2.155
    fnpass_y = 0.42

    psub_x = 1.765
    # psub_y = 1.645
    psub_y = 9.325

    newLayout.addInstance(endLeftLayout,
                          offsetInMicrons=(x_offset,y_offset),
                          mirror = mirror)
    newLayout.addBox(layerNumber=68,
                     dataType=20,
                     offsetInMicrons=(x_offset + psub_x,y_offset-psub_y),
                     width=.1,
                     height=.1,
                     center=True)
    newLayout.addText(text = "VBPW",
                      layerNumber=68,
                      purposeNumber=16,
                      offsetInMicrons=(x_offset + psub_x,y_offset - psub_y))
    x_offset += SIDE_WIDTH
    for i in range(numCols/2):
        newLayout.addInstance(endMidLayout,
                              offsetInMicrons=(x_offset,y_offset),
                              mirror=mirror)
        newLayout.addBox(layerNumber=68,
                         dataType=20,
                         offsetInMicrons=(x_offset + BL_BL_x/2,y_offset - BL_y),
                         width = .1,
                         height=.1,
                         center=True)
        newLayout.addText(text = "BL[" + str(2*i) + "]",
                          layerNumber=68,
                          purposeNumber=16,
                          offsetInMicrons=(x_offset + BL_BL_x/2,y_offset - BL_y))
        x_offset += MID_WIDTH
        newLayout.addBox(layerNumber=68,
                         dataType=20,
                         offsetInMicrons=(x_offset - BL_BL_x/2,y_offset - BL_y),
                         width = .1,
                         height=.1,
                         center=True)
        newLayout.addText(text = "BL[" + str(2*i+1) + "]",
                                  layerNumber=68,
                                  purposeNumber=16,
                                  offsetInMicrons=(x_offset - BL_BL_x/2,y_offset - BL_y))

    newLayout.addInstance(endRightLayout,
                          offsetInMicrons= (x_offset,y_offset),
                          mirror = mirror)
    
    y_offset-=END_HEIGHT
    newLayout.addBox(layerNumber=67,
                     dataType=20,
                     offsetInMicrons=(x_offset + WL_x,y_offset + fnpass_y),
                     width = .1,
                     height=.1,
                     center=True)
    newLayout.addText(text = "SSL[" + str(block) + "]",
                      layerNumber=67,
                      purposeNumber=16,
                      offsetInMicrons=(x_offset + WL_x,y_offset + fnpass_y))

def placeBotRow(block):
    x_offset = 0
    global y_offset

    mirror = None
    fnpass_y = 0.42
    m1_x = 0.2
    gnd1 = 7.202
    gnd2 = 13.142
    vddy = 10.18
    sen1_1 = 4.37
    sen1_2 = 15.995
    sen2_1 = 4.00
    sen2_2 = 16.365

    out_enx = 0.2
    out_eny = 17.32
    out_evx = 0.6
    out_evy = 16.835
    out_oddx = 1.3
    out_oddy = 17.35

    newLayout.addInstance(botLeftLayout,
                          offsetInMicrons=(x_offset,y_offset),
                          mirror = mirror)
    x_offset += SIDE_WIDTH
    for i in range(numCols/2):
        ### Label output pins
        newLayout.addInstance(botMidLayout,
                              offsetInMicrons=(x_offset,y_offset),
                              mirror=mirror)
        newLayout.addBox(layerNumber=69,
                         dataType=20,
                         offsetInMicrons=(x_offset + out_enx,y_offset - out_eny),
                         width = .1,
                         height=.1,
                         center=True)
        newLayout.addText(text = "out_en[" + str(i) + "]",
                         layerNumber=69,
                         purposeNumber=16,
                         offsetInMicrons=(x_offset + out_enx,y_offset - out_eny))

        newLayout.addBox(layerNumber=69,
                         dataType=20,
                         offsetInMicrons=(x_offset + out_oddx,y_offset - out_oddy),
                         width = .1,
                         height=.1,
                         center=True)
        newLayout.addText(text = "out[" + str(2*i + 1) + "]",
                         layerNumber=69,
                         purposeNumber=16,
                         offsetInMicrons=(x_offset + out_oddx,y_offset - out_oddy))

        newLayout.addBox(layerNumber=67,
                         dataType=20,
                         offsetInMicrons=(x_offset + out_evx,y_offset - out_evy),
                         width = .1,
                         height=.1,
                         center=True)
        newLayout.addText(text = "out[" + str(2*i) + "]",
                         layerNumber=67,
                         purposeNumber=16,
                         offsetInMicrons=(x_offset + out_evx,y_offset - out_evy))
        
        x_offset += MID_WIDTH

    newLayout.addInstance(botRightLayout,
                          offsetInMicrons= (x_offset,y_offset),
                          mirror = mirror)
    
    newLayout.addBox(layerNumber=67,
                     dataType=20,
                     offsetInMicrons=(x_offset + WL_x,y_offset - fnpass_y),
                     width = .1,
                     height=.1,
                     center=True)
    newLayout.addText(text = "SSL[" + str(block) + "]",
                      layerNumber=67,
                      purposeNumber=16,
                      offsetInMicrons=(x_offset + WL_x,y_offset - fnpass_y))

    ### Label power lines
    newLayout.addBox(layerNumber=68,
                     dataType=20,
                     offsetInMicrons=(x_offset - m1_x,y_offset - gnd1),
                     width = .1,
                     height=.1,
                     center=True)
    newLayout.addText(text = "GND",
                      layerNumber=68,
                      purposeNumber=16,
                      offsetInMicrons=(x_offset - m1_x,y_offset - gnd1))
    # newLayout.addBox(layerNumber=68,
    #                  dataType=20,
    #                  offsetInMicrons=(x_offset - m1_x,y_offset - gnd2),
    #                  width = .1,
    #                  height=.1,
    #                  center=True)
    # newLayout.addText(text = "vssd1",
    #                   layerNumber=68,
    #                   purposeNumber=16,
    #                   offsetInMicrons=(x_offset - m1_x,y_offset - gnd2))

    newLayout.addBox(layerNumber=68,
                     dataType=20,
                     offsetInMicrons=(x_offset - m1_x,y_offset - vddy),
                     width = .1,
                     height=.1,
                     center=True)
    newLayout.addText(text = "VDD",
                      layerNumber=68,
                      purposeNumber=16,
                      offsetInMicrons=(x_offset - m1_x,y_offset - vddy))

    ### Label sen control lines
    newLayout.addBox(layerNumber=68,
                     dataType=20,
                     offsetInMicrons=(x_offset - m1_x,y_offset - sen1_1),
                     width = .1,
                     height=.1,
                     center=True)
    newLayout.addText(text = "sen1",
                      layerNumber=68,
                      purposeNumber=16,
                      offsetInMicrons=(x_offset - m1_x,y_offset - sen1_1))
    # newLayout.addBox(layerNumber=68,
    #                  dataType=20,
    #                  offsetInMicrons=(x_offset - m1_x,y_offset - sen1_2),
    #                  width = .1,
    #                  height=.1,
    #                  center=True)
    # newLayout.addText(text = "sen1",
    #                   layerNumber=68,
    #                   purposeNumber=16,
    #                   offsetInMicrons=(x_offset - m1_x,y_offset - sen1_2))
    newLayout.addBox(layerNumber=68,
                     dataType=20,
                     offsetInMicrons=(x_offset - m1_x,y_offset - sen2_1),
                     width = .1,
                     height=.1,
                     center=True)
    newLayout.addText(text = "sen2",
                      layerNumber=68,
                      purposeNumber=16,
                      offsetInMicrons=(x_offset - m1_x,y_offset - sen2_1))
    # newLayout.addBox(layerNumber=68,
    #                  dataType=20,
    #                  offsetInMicrons=(x_offset - m1_x,y_offset - sen2_2),
    #                  width = .1,
    #                  height=.1,
    #                  center=True)
    # newLayout.addText(text = "sen2",
    #                   layerNumber=68,
    #                   purposeNumber=16,
    #                   offsetInMicrons=(x_offset - m1_x,y_offset - sen2_2))
    # y_offset-=END_HEIGHT

def placeBLRow(block):
    x_offset = 0
    global y_offset

    fnpass_y = 0.47

    newLayout.addInstance(BLLeftLayout,
                          offsetInMicrons=(x_offset,y_offset))
    x_offset += SIDE_WIDTH
    for i in range(numCols/2):
        newLayout.addInstance(BLMidLayout,
                              offsetInMicrons=(x_offset,y_offset))
        x_offset += MID_WIDTH

    newLayout.addInstance(BLRightLayout,
                          offsetInMicrons= (x_offset,y_offset))
    newLayout.addBox(layerNumber=67,
                     dataType=20,
                     offsetInMicrons=(x_offset + WL_x,y_offset - fnpass_y),
                     width = .1,
                     height=.1,
                     center=True)
    newLayout.addText(text = "SSL[" + str(block-1) + "]",
                      layerNumber=67,
                      purposeNumber=16,
                      offsetInMicrons=(x_offset + WL_x,y_offset - fnpass_y))
    y_offset-=MID_HEIGHT
    newLayout.addBox(layerNumber=67,
                     dataType=20,
                     offsetInMicrons=(x_offset + WL_x,y_offset + fnpass_y),
                     width = .1,
                     height=.1,
                     center=True)
    newLayout.addText(text = "SSL[" + str(block) + "]",
                      layerNumber=67,
                      purposeNumber=16,
                      offsetInMicrons=(x_offset + WL_x,y_offset + fnpass_y))

def placeSLRow(block):
    x_offset = 0
    global y_offset

    fnpass_y = 0.47

    newLayout.addInstance(SLLeftLayout,
                          offsetInMicrons=(x_offset,y_offset))
    x_offset += SIDE_WIDTH
    newLayout.addBox(layerNumber=67,
                     dataType=20,
                     offsetInMicrons=(x_offset - WL_x,y_offset - fnpass_y),
                     width = .1,
                     height=.1,
                     center=True)
    newLayout.addText(text = "GSL[" + str(block-1) + "]",
                      layerNumber=67,
                      purposeNumber=16,
                      offsetInMicrons=(x_offset - WL_x,y_offset - fnpass_y))
    newLayout.addBox(layerNumber=67,
                     dataType=20,
                     offsetInMicrons=(x_offset - WL_x,y_offset + fnpass_y - MID_HEIGHT),
                     width =.1,
                     height=.1,
                     center=True)
    newLayout.addText(text = "GSL[" + str(block) + "]",
                      layerNumber=67,
                      purposeNumber=16,
                      offsetInMicrons=(x_offset - WL_x,y_offset + fnpass_y - MID_HEIGHT))
    for i in range(numCols/2):
        newLayout.addInstance(SLMidLayout,
                              offsetInMicrons=(x_offset,y_offset))
        x_offset += MID_WIDTH

    newLayout.addInstance(SLRightLayout,
                          offsetInMicrons= (x_offset,y_offset))
    
    newLayout.addBox(layerNumber=67,
                     dataType=20,
                     offsetInMicrons=(x_offset - BL_BL_x/2,y_offset - MID_HEIGHT/2),
                     width =.1,
                     height=.1,
                     center=True)
    newLayout.addText(text = "SL",
                      layerNumber=67,
                      purposeNumber=16,
                      offsetInMicrons=(x_offset - BL_BL_x/2,y_offset - MID_HEIGHT/2))

    y_offset-=MID_HEIGHT

                      

def placeCellRow(block,row,orientation):
    x_offset = 0
    global y_offset

    if orientation:
        mirror = None
        WL0_y = -0.215
        WL1_y = 0.215 - CELL_HEIGHT
    else:
        mirror  = "x"
        WL0_y = 0.215
        WL1_y = CELL_HEIGHT - 0.215
        y_offset-=CELL_HEIGHT
        row = blockSize/2 - row - 1

    newLayout.addInstance(cellLeftLayout,
                          offsetInMicrons=(x_offset,y_offset),
                          mirror = mirror)
    x_offset += SIDE_WIDTH
    newLayout.addBox(layerNumber=67,
                     dataType=20,
                     offsetInMicrons=(x_offset - WL_x,y_offset + WL0_y),
                     width = .1,
                     height=.1,
                     center=True)
    newLayout.addText(text = "WL" + str(block) + "[" + str(2*row) + "]",
                      layerNumber=67,
                      purposeNumber=16,
                      offsetInMicrons=(x_offset - WL_x,y_offset + WL0_y))
    for i in range(numCols/2):
        newLayout.addInstance(cellMidLayout,
                              offsetInMicrons=(x_offset,y_offset),
                              mirror=mirror)
        x_offset += MID_WIDTH

    newLayout.addInstance(cellRightLayout,
                          offsetInMicrons= (x_offset,y_offset),
                          mirror = mirror)
    
    newLayout.addBox(layerNumber=67,
                     dataType=20,
                     offsetInMicrons=(x_offset + WL_x,y_offset + WL1_y),
                     width = .1,
                     height=.1,
                     center=True)
    newLayout.addText(text = "WL" + str(block) + "[" + str(2*row+1) + "]",
                      layerNumber=67,
                      purposeNumber=16,
                      offsetInMicrons=(x_offset + WL_x,y_offset + WL1_y))
    if orientation:
        y_offset-=CELL_HEIGHT
    

def placeCellBlock(block,orientation,size=(0,0)):
    global y_offset
    for row in range(size[1]/2):
        placeCellRow(block,row,orientation)

for block in range(numRows/blockSize):
    if (block % 2) == 0:
        if block: #if block is not 0
            placeBLRow(block)
        else:
            placeTopRow(block)
        placeCellBlock(block,True, size=(numCols,blockSize))
    else:
        placeSLRow(block)
        placeCellBlock(block,False, size=(numCols,blockSize))
placeBotRow(numRows/blockSize - 1)

writer = gdsMill.Gds2writer(newLayout)
writer.writeToFile(output_path + out_name + ".gds")
