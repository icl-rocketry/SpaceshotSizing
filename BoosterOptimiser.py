import xlwings as xw
import pandas as pd
import numpy as np
from ambiance import Atmosphere as atmo
from matplotlib import pyplot as plt

def mach(velocity, height):
    if(height < 81020):
        return np.abs(velocity) / atmo(height).speed_of_sound[0]
    else:
        return np.abs(velocity) / atmo(81020).speed_of_sound[0]
    
def density(height):
    if(height < 81020):
        return atmo(height).density[0]
    else:
        return 0
    
def pressure(height):
    if(height < 81020):
        return atmo(height).pressure[0]
    else:
        return 0
    
def metrictog(x):
    return x / 9.80665


def gtometric(x):
    return x * 9.80665

diameters = np.arange(6, 8.5, 0.5)
throatdiameters = np.arange(0.7, 1.21, 0.1)
#throatdiameters = [0.7]

wb = xw.Book('HalfCatSim_v1.3.4.xlsx')
sheet = wb.sheets['Motor Simulation']
mathsheet = wb.sheets['Math']
mlist = [13.3, 14.4, 15.7, 17, 18.5]
#for index, diameter in enumerate(diameters):
#    hmax_list = []
fig, ax = plt.subplots(3, 1, figsize=(40, 20))
for throatindex, throatdiameter in enumerate(throatdiameters):
    diameter = 8
    sheet['G3'].value = diameter
    sheet['K4'].value = diameter
    sheet['C13'].value = throatdiameter
    impulse = sheet['O18'].value

    data = mathsheet.range('BC2:BC2000').value
    num = data.index(0)
    thrust_thrust = data[:num]
    thrust_time = mathsheet.range(f"A2:A{num}")
    
    spaceshot = pd.read_csv(f"aero2m8inthroat/throat{str(int(round(throatdiameter*10))).zfill(2)}.csv")
    #testdata = pd.read_csv("Flight Test.CSV")
    # Read data from sheet column BC1 to BC100
    #thrustdata = pd.read_csv('spaceshot.eng', sep=" ", skiprows=1, header=None, nrows=721)

    t = 0
    dt = 0.1
    h = 2000 / 3.32808
    v = 0

    propmass = sheet['K44'].value
    m = propmass + mlist[4]
    g = 9.806
    isp = impulse / propmass / g

    h_list = np.array([h])
    t_list = np.array([0])
    a_list = np.array([0])
    d_list = np.array([0])
    while t <= 300 and h > -0.1:
        if np.round(t / 0.05) < num:
            massthrust = thrust_thrust[int(t / 0.05)]
            thrust = massthrust + 0.03175**2 * np.pi * (pressure(0) - pressure(h))
            Cd = spaceshot['CD Power-On'][np.round(mach(v,h)*100)]
        else:
            massthrust = 0
            thrust = 0
            Cd = spaceshot['CD Power-Off'][np.round(mach(v,h)*100)]
        #Cd = testdata['CD'][np.round(t/dt)]
        F = thrust - np.sign(v) * 0.5 * density(h) * v * v * 0.075 * 0.075 * np.pi * Cd - m*g
        m = m - massthrust / isp / g * dt
        #m = testdata['Weight (lb)'][np.round(t / dt)] * 0.453592

        v = v + F / m * dt
        h = h + v * dt
        t += dt
        t_list = np.append(t_list,[t])
        h_list = np.append(h_list,[h])
        d_list = np.append(d_list,[0.5 * density(h) * v * v * 0.075 * 0.075 * np.pi * Cd])
        a_list = np.append(a_list,[F/m])
    print(f"For tank OD {diameter}, Throat size {throatdiameter}, Impulse = {impulse}, Max Altitude = {h_list.max() - h_list[0]}")
    #hmax_list.append(h_list.max() - h_list[0])
    ax[0].plot(t_list, h_list - h_list[0], label=f"Throat Diameter {throatdiameter:.1f}")
    ax[1].plot(t_list, a_list, label=f"Throat Diameter {throatdiameter:.1f}")
    ax[2].plot(t_list, d_list, label=f"Throat Diameter {throatdiameter:.1f}")
ax[0].set(ylabel = "Altitude (m)")
ax[1].set(ylabel = "Acceleration (m/s^2)")
secax = ax[1].secondary_yaxis('right', functions=(metrictog, gtometric))
secax.set_ylabel('gs')
ax[2].set(ylabel = "Drag (N)")
ax[0].legend()
ax[1].legend()
ax[2].legend()
ax[0].grid()
ax[1].grid()
ax[2].grid()
plt.show()

# tank_OD = 7

# tank_OD = 6.5
# sheet['G3'].value = tank_OD
# sheet['K4'].value = tank_OD
# print(f"For tank OD {tank_OD}, Impulse = {sheet['O18'].value}")
# wb.close()



        


# t_list = np.array([0])
# a_list = np.array([0])
# d_list = np.array([0])

# v_list = np.array([0])
# cd_list = np.array([0])
# m_list = np.array([0])
# mach_list = np.array([0])
# thrust_list = np.array([thrustdata[1][0]])
# while t <= 300 and h > -0.1:
#     #print(h)
#     if np.round(t / 0.05) < np.size(thrustdata[1]):
#         massthrust = thrustdata[1][np.round(t/ 0.05)]
#         thrust = massthrust + 0.03175**2 * np.pi * (pressure(0) - pressure(h))
#         Cd = spaceshot['CD Power-On'][np.round(mach(v,h)*100)]
#     else:
#         massthrust = 0
#         thrust = 0
#         Cd = spaceshot['CD Power-Off'][np.round(mach(v,h)*100)]
#     #Cd = testdata['CD'][np.round(t/dt)]
#     F = thrust - np.sign(v) * 0.5 * density(h) * v * v * 0.075 * 0.075 * np.pi * Cd - m*g
#     m = m - massthrust / isp / g * dt
#     #m = testdata['Weight (lb)'][np.round(t / dt)] * 0.453592
        
#     v = v + F / m * dt
#     h = h + v * dt
#     t += dt
    
#     if np.round(t / dt) % 0.1 / dt:
#         t_list = np.append(t_list,[t])
#         h_list = np.append(h_list,[h])
#         v_list = np.append(v_list,[v])
#         d_list = np.append(d_list,[0.5 * density(h) * v * v * 0.075 * 0.075 * np.pi * Cd])
#         cd_list = np.append(cd_list,[Cd])
#         a_list = np.append(a_list,[F/m])
#         mach_list = np.append(mach_list,[mach(v, h)])
#         thrust_list = np.append(thrust_list,thrust)
#         m_list = np.append(m_list,[m])
    
# fig, ax = plt.subplots(6, 1, figsize=(20, 20))
# ax[0].plot(t_list, h_list - h_list[0] )
# ax[0].plot(testdata['Time (sec)'], testdata['Altitude (ft)'] / 3.2808 )
# ax[1].plot(t_list, v_list)
# ax[1].plot(testdata['Time (sec)'], testdata['Vel-V (ft/sec)'] / 3.2808)
# ax[2].plot(t_list, mach_list)#* 0.224809)
# ax[2].plot(testdata['Time (sec)'], testdata['Mach Number'])
# ax[3].plot(t_list, d_list)
# ax[3].plot(testdata['Time (sec)'], testdata['Drag (lb)'] / 0.224809)
# ax[4].plot(t_list, thrust_list)
# ax[4].plot(testdata['Time (sec)'], testdata['Thrust (lb)'] / 0.224809)
# ax[5].plot(t_list, m_list)
# ax[5].plot(testdata['Time (sec)'], testdata['Weight (lb)'] * 0.453592)
    
# ax[5].set(xlabel="Time")
# ax[0].set(ylabel = "Altitude (m)")
# ax[1].set(ylabel="Velocity (m/s)")
# ax[2].set(ylabel="Mach Number")
# ax[3].set(ylabel="Drag (N)")
# ax[4].set(ylabel="Thrust (N)")
# ax[5].set(ylabel="Mass (kg)")

# plt.show()