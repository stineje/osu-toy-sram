import numpy as np

WWL = np.array([-55, 233, -7, 263])
RWL0 = np.array([-55, 95, -31, 129])
RWL1 = np.array([-31, 95, -7, 129])
RBL0 = np.array([530, -55, 545, -7])
RBL1 = np.array([-7, -55, 8, -7])
WBL = np.array([429, -55, 444, -7])
WBLb = np.array([94, -55, 109, -7])
VDD = np.array([-55, 219, -7, 233])
GND = np.array([-55, -7, -7, 7])

delta_right = np.array([580, 0, 580, 0])
delta_up = np.array([0, 270, 0, 270])

print("rlabel metal1 {} {} {} {} 1 VDD".format(VDD[0], VDD[1], VDD[2], VDD[3]))
print("port 1 ew power bidirectional abutment")
print("rlabel metal1 {} {} {} {} 1 GND".format(GND[0], GND[1], GND[2], GND[3]))
print("port 2 ew ground bidirectional abutment")

i = 1
for i in range(15):
    VDD = VDD + delta_up
    GND = GND + delta_up
    print("rlabel metal1 {} {} {} {} 1 VDD".format(VDD[0], VDD[1], VDD[2], VDD[3]))
    print("port 1 ew power bidirectional abutment")
    print("rlabel metal1 {} {} {} {} 1 GND".format(GND[0], GND[1], GND[2], GND[3]))
    print("port 2 ew ground bidirectional abutment")


i = 0
port = 3
print("rlabel poly {} {} {} {} 1 {}_{}".format(WWL[0], WWL[1], WWL[2], WWL[3], 'WWL', i))
print("port {} ew signal input".format(port))
port = port + 1
print("rlabel metal2 {} {} {} {} 1 {}_{}".format(RWL0[0], RWL0[1], RWL0[2], RWL0[3], 'RWL0', i))
print("port {} ew signal input".format(port))
port = port + 1
print("rlabel metal1 {} {} {} {} 1 {}_{}".format(RWL1[0], RWL1[1], RWL1[2], RWL1[3], 'RWL1', i))
print("port {} ew signal input".format(port))
port = port + 1
print("rlabel corelocali {} {} {} {} 1 {}_{}".format(RBL0[0], RBL0[1], RBL0[2], RBL0[3], 'RBL0', i))
print("port {} ns signal output".format(port))
port = port + 1
print("rlabel corelocali {} {} {} {} 1 {}_{}".format(RBL1[0], RBL1[1], RBL1[2], RBL1[3], 'RBL1', i))
print("port {} ns signal output".format(port))
port = port + 1
print("rlabel corelocali {} {} {} {} 1 {}_{}".format(WBL[0], WBL[1], WBL[2], WBL[3], 'WBL', i))
print("port {} ns signal input".format(port))
port = port + 1
print("rlabel corelocali {} {} {} {} 1 {}_{}".format(WBLb[0], WBLb[1], WBLb[2], WBLb[3], 'WBLb', i))
print("port {} ns signal input".format(port))
port = port + 1

i = 1
for i in range(1, 16):
    WWL = WWL + delta_up
    RWL0 = RWL0 + delta_up
    RWL1 = RWL1 + delta_up
    print("rlabel poly {} {} {} {} 1 {}_{}".format(WWL[0], WWL[1], WWL[2], WWL[3], 'WWL', i))
    print("port {} ew signal input".format(port))
    port = port + 1
    print("rlabel metal2 {} {} {} {} 1 {}_{}".format(RWL0[0], RWL0[1], RWL0[2], RWL0[3], 'RWL0', i))
    print("port {} ew signal input".format(port))
    port = port + 1
    print("rlabel metal1 {} {} {} {} 1 {}_{}".format(RWL1[0], RWL1[1], RWL1[2], RWL1[3], 'RWL1', i))
    print("port {} ew signal input".format(port))
    port = port + 1
    i = i+1


i = 1
for i in range(1, 12):
    RBL0 = RBL0   + delta_right
    RBL1 = RBL1 + delta_right
    WBL = WBL + delta_right
    WBLb = WBLb + delta_right
    print("rlabel corelocali {} {} {} {} 1 {}_{}".format(RBL0[0], RBL0[1], RBL0[2], RBL0[3], 'RBL0', i))
    print("port {} ns signal output".format(port))
    port = port + 1
    print("rlabel corelocali {} {} {} {} 1 {}_{}".format(RBL1[0], RBL1[1], RBL1[2], RBL1[3], 'RBL1', i))
    print("port {} ns signal output".format(port))
    port = port + 1
    print("rlabel corelocali {} {} {} {} 1 {}_{}".format(WBL[0], WBL[1], WBL[2], WBL[3], 'WBL', i))
    print("port {} ns signal input".format(port))
    port = port + 1
    print("rlabel corelocali {} {} {} {} 1 {}_{}".format(WBLb[0], WBLb[1], WBLb[2], WBLb[3], 'WBLb', i))
    print("port {} ns signal input".format(port))
    port = port + 1
    i = i+1



#rect1 = np.array([94, -55, 109, -7])
#rect2 = np.array([429, -55, 444, -7])
#rect3 = np.array([1110, 4313, 1125, 4361])
#rect4 = np.array([1153, 4313, 1168, 4361])
#print("\ncorelocali rects")
#i = 1
#for i in range(11):
#    rect3 = rect3 + delta_right
#    rect4 = rect4 + delta_right
#    print("rect {} {} {} {}".format(rect3[0], rect3[1], rect3[2], rect3[3]))
#    print("rect {} {} {} {}".format(rect4[0], rect4[1], rect4[2], rect4[3]))
