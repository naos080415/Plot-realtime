
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)

#dev_r = usbcontroller.USBController('/dev/ttyUSB0', baud=1000000, reconnect=False)
#dev_l = usbcontroller.USBController('/dev/ttyUSB1', baud=1000000, reconnect=False)
dev_l=usbcontroller.USBController('/dev/ttyUSB0')#モーターのアドレス 参照 usb-simple-connection.py　★
dev_r=usbcontroller.USBController('/dev/ttyUSB1')#モーターのアドレス 参照 usb-simple-connection.py　★
dev_r.enable_action()#安全装置。初めてモーターを動作させる場合に必ず必要。
dev_l.enable_action()#安全装置。初めてモーターを動作させる場合に必ず必要。

start_time = time.perf_counter() # プログラム開始時の現在の時刻

tr1 = 0
tl1 = 0
pr1 = 0
pl1 = 0
v_r = 0
v_l = 0
diff_r = 0
diff_l = 0


Theta = [0]
V=0
dv=0
# v0=25
while True:
a = ser.readline()

try:
A = a.decode().strip()
#print(A)
l = A.split(',')
print("l",l)
x = l[0]
h = l[1]
s = l[2]
print('x:',int(x))
# print('h',int(h))
print('s:',int(s))
#x座標の中心からのずれ
dx = 158-int(x)
print('dx:',dx)

#キョリを求める
D= 1092.9/(int(s)**0.466)
print('D:',D)
#角度を求める
theta = math.atan(dx/D)
#theta = math.degrees(math.atan(dx/D))
Theta.append(theta)
print(Theta)

#P制御
k = 7
V += (Theta[0]-Theta[1])* k
Theta.pop(0)
print("V:",V,'Theta',Theta)

dk = 0.6
dv = (D-20)*dk
print('dv',dv)

"""
mr = dev_r.read_motor_measurement()
tr = mr['torque']
# print("mr",mr)
# print("mr",mr['velocity'])
ml = dev_l.read_motor_measurement()
tl = mr['torque']
# print("ml",ml)
# print("ml",ml['velocity'])
print("mr",mr['torque'], 'ml', ml['torque'])
if tr >= 0.1 or tl <= -0.1:
print("torque")
dev_r.set_led(1, 200, 0, 200)
dev_l.set_led(1, 200, 0, 200)
dev_r.free_motor()
dev_l.free_motor()
mr = dev_r.read_motor_measurement()
tr = mr['torque']
ml = dev_l.read_motor_measurement()
tl = mr['torque']
"""

mr1 = dev_r.read_motor_measurement()
tr1 = mr1['velocity']
pr1 = mr1['position']
# print("mr",mr)
# print("mr",mr['velocity'])
ml1 = dev_l.read_motor_measurement()
tl1 = ml1['velocity']
pl1 = ml1['position']
# print("ml",ml)
# print("ml",ml['velocity'])
print("mr1",tr1, 'ml1', tl1)
"""
if tr > 0 or tl < 0:
print("velocity")
dev_r.set_led(1, 200, 0, 200)
dev_l.set_led(1, 200, 0, 200)
dev_r.free_motor()
dev_l.free_motor()
print("free")
# mr = dev_r.read_motor_measurement()
# tr = mr['torque']
# ml = dev_l.read_motor_measurement()
# tl = mr['torque']
"""


if D < 30:
dev_r.set_led(1, 200, 0, 0)
dev_l.set_led(1, 200, 0, 0)
dev_r.free_motor()
dev_l.free_motor()

else:
"""
if tr > 0 or tl < 0:
print("velocity")
dev_r.set_led(1, 200, 0, 200)
dev_l.set_led(1, 200, 0, 200)
dev_r.free_motor()
dev_l.free_motor()
print("free")
continue
"""
vl = V+dv#★
vr = V-dv#★
v_l = utils.rpm2rad_per_sec(vl)
v_r = utils.rpm2rad_per_sec(vr)
dev_r.set_led(1, 200-V*5, 200, 200+V*5)
dev_l.set_led(1, 200+V*5, 200, 200-V*5)
# dev_r.set_speed(utils.rpm2rad_per_sec(vr))#rpm -> radian/sec
dev_r.set_speed(v_r)#rpm -> radian/sec
#dev_r.set_speed(utils.rpm2rad_per_sec(0))#rpm -> radian/sec
# dev_l.set_speed(utils.rpm2rad_per_sec(vl))#rpm -> radian/sec
dev_l.set_speed(v_l)#rpm -> radian/sec

dev_r.run_forward()
dev_l.run_forward()
if dx > 0:
print("left",dx)
print("vr:",vr, utils.rpm2rad_per_sec(vr))
print("vl",vl)
else:
print("right",dx)
print("vr:",vr)
print("vl:",vl)
#sleep(0.1)

mr = dev_r.read_motor_measurement()
print("mr",mr)
print("mr",mr['velocity'])
ml = dev_l.read_motor_measurement()
print("ml",ml)
print("ml",ml['velocity'])

diff_r = mr['velocity'] - v_r
diff_l = ml['velocity'] - v_l


sleep(0.1)

except Exception:
print("Stop")
dev_r.set_led(1, 200, 0, 0)
dev_l.set_led(1, 200, 0, 0)

mr = dev_r.read_motor_measurement()
ml = dev_l.read_motor_measurement()


diff_r = mr['velocity'] - v_r
diff_l = ml['velocity'] - v_l


dev_r.free_motor()
dev_l.free_motor()

# グラフ描画
new_data = mr['torque']
# graphWin.update()
graphWin.data_update(new_data=new_data)
print(type(new_data))


with open('/home/cpslabo/robot/robot/mainA2P_writer.csv', 'a') as f:
# with open('ドキュメント//serial/mainA2P_writer.csv', 'a') as f:
writer = csv.writer(f)
# writer.writerow([time.perf_counter() - start_time, mr['velocity'], ml['velocity']])
writer.writerow([time.perf_counter() - start_time, mr['torque'], ml['torque'], tr1, tl1,v_r,v_l , mr['velocity'], ml['velocity'], diff_r, diff_l, pr1, pl1,mr['position'], ml['position']])
"""
# グラフ描画
new_data = mr['torque']
graphWin.original_update(new_data=new_data)
"""

ser.close()
