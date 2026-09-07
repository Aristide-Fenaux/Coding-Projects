import numpy as np 
import matplotlib.pyplot as plt 
import sys

# Car/System Parameters
car_mass = 80
driver_mass = 70
m = car_mass + driver_mass
r = 0.25 # wheel radius
rolling_resistance_factor = 0.015
efficiency = 0.8 # transmission efficiency
Cd = 0.3 # drag coefficient
A = 0.25 # frontal area
rho = 1.225 # fluid density
slope_degrees = 0.5 # simulates road bumps
slope = slope_degrees*np.pi/180
track_length = 100 # in meters

# Motor Parameters
Max_torque = 11.5 # motor output torque at 0 rpm
No_load_torque = 0.4 # internal friction torque 
Max_rpm = 2200 # rpm ceiling
rated_speed = 2100 # rated operating point in rpm
rated_current = 15 # rated operating point in Amps
Voltage = 24 # nominal battery voltage

Ke = 24/(Max_rpm*np.pi/30)
i_a_0 = No_load_torque/Ke

EMF_rated = Ke*rated_speed*np.pi/30 # back EMF at the rated operating point

R_a = (Voltage-EMF_rated)/rated_current # Motor armature resistance


def mechanical_power(torque, motor_rpm) : 
    return torque*motor_rpm*np.pi/30

def motor_torque(rpm_motor) :
    return max(0, Max_torque - 0.005*rpm_motor)

def resistance_force(v) : 
    aero_drag = 0.5*Cd*A*rho*v**2
    rolling_resistance = rolling_resistance_factor*m*9.81
    slope_resistance = m*9.81*np.sin(slope)
    total_resistance = aero_drag + rolling_resistance + slope_resistance
    return total_resistance

def drive_force(v) : 
    T_wheel = motor_torque(speed_to_motor_rpm(v))*G*efficiency
    F_drive = T_wheel/r
    return F_drive

def speed_to_motor_rpm(v) : 
    if v < 0 : 
        sys.exit("Not enough torque to move with the lowest reduction ratio, probably won't happen in reality so reduce resistance")
    else : 
        return min(Max_rpm, rpm_(v/r)*G)

def rpm_(rad) : 
    return rad*30/np.pi

final_time_hist, final_velo_hist = [],[]

# Defining top speed per regulations
Speed_limit_kph = 25

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(16, 9))
fig.suptitle("Drivetrain gear ratio sweep", fontsize=14)

ratios = [ratio for ratio in np.arange(7,10,0.5)]
colors = plt.get_cmap('viridis')(np.linspace(0, 1, len(ratios)))

for i, ratio in enumerate(ratios) :
    time_hist, rpm_hist, dist_hist, velo_hist, acce_hist, torq_hist, F_hist, resistance_force_hist, drive_force_hist, mechanical_power_hist, motor_efficiency_hist, current_hist = [0],[0],[0],[0],[0],[Max_torque],[],[],[],[0],[0],[i_a_0]
    G= ratio
    dt = 0.001
    s,t,v = 0,0,0
    while s < track_length :
        F_net = drive_force(v)- resistance_force(v)
        resistance_force_hist.append(resistance_force(v))
        drive_force_hist.append(drive_force(v))
        a = F_net/m  # using Newton's Second Law
        v += a*dt  # using Forward Euler Numerical Method
        s += v*dt
        t += dt
        rpm_motor = speed_to_motor_rpm(v)
        T_out = motor_torque(rpm_motor)
        P_mech = mechanical_power(T_out, rpm_motor)
        i_a = T_out/Ke + i_a_0
        v_a = (Ke*rpm_motor*np.pi/30)+i_a*R_a
        F_hist.append(F_net)
        torq_hist.append(T_out)
        acce_hist.append(a)
        time_hist.append(t)
        dist_hist.append(s)
        velo_hist.append(v*3.6)
        mechanical_power_hist.append(P_mech)
        current_hist.append(i_a)
        rpm_hist.append(rpm_motor)
        motor_efficiency_hist.append(P_mech/(v_a*i_a))

    final_velo_hist.append(max(velo_hist))
    final_time_hist.append(max(time_hist))

    eff_curve = [e*100 for e in motor_efficiency_hist]

    # Plotting
    ax1.plot(time_hist, dist_hist, color=colors[i], label=f"G = {ratio:g}", linewidth=1.3)
    ax2.plot(time_hist, velo_hist, color=colors[i], label=f"G = {ratio:g}", linewidth=1.3)
    ax3.plot(time_hist, mechanical_power_hist, color=colors[i], label=f"G = {ratio:g}", linewidth=1.3)
    ax4.plot(rpm_hist, eff_curve, color=colors[i], alpha=0.85, linewidth=1.3)
    ax4.scatter([rpm_motor], [eff_curve[-1]], color=colors[i], marker="x", s=60, zorder=5)

ax5.plot(ratios, final_velo_hist, marker="o", color="black", linewidth=1.3)
ax6.plot(ratios, final_time_hist, marker="o", color="black", linewidth=1.3)

# fastest finish time among ratios that keep top speed under the limit
qualifying = [(g, t, vmax) for g, t, vmax in zip(ratios, final_time_hist, final_velo_hist) if vmax < Speed_limit_kph]
if qualifying :
    best_ratio, best_time, best_top_speed = min(qualifying, key=lambda c: c[1])
    print(f"Best ratio : {best_ratio:g}  (finish time {best_time:.3f} s, top speed {best_top_speed:.1f} km/h)")
    best_idx = ratios.index(best_ratio)
else :
    best_ratio = None
    print("No tested ratio keeps top speed under the limit")

ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Distance (m)")
ax1.grid(True)

ax2.axhline(Speed_limit_kph, color="red", linestyle="--", linewidth=1, label=f"{Speed_limit_kph} km/h limit")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Velocity (km/h)")
ax2.grid(True)

ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Mechanical power (W)")
ax3.grid(True)

ax4.set_xlabel("Motor speed (rpm)")
ax4.set_ylabel("Motor efficiency (%)")
ax4.grid(True)
ax4.text(
    0.02, 0.02, "x = final rpm reached per ratio",
    transform=ax4.transAxes, fontsize=8, va="bottom", ha="left"
)

ax5.axhline(Speed_limit_kph, color="red", linestyle="--", linewidth=1, label=f"{Speed_limit_kph} km/h limit")
ax5.set_xlabel("Gear ratio G")
ax5.set_ylabel("Top speed (km/h)")
ax5.grid(True)
ax5.legend(fontsize=8)

if best_ratio is not None :
    ax6.scatter([best_ratio], [final_time_hist[best_idx]], color="red", zorder=5, label=f"Best ratio = {best_ratio:g}")
    ax6.legend(fontsize=8)
ax6.set_xlabel("Gear ratio G")
ax6.set_ylabel(f"Time to cover {track_length} m (s)")
ax6.grid(True)

handles, labels = ax2.get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", ncol=len(ratios)+1, fontsize=9, bbox_to_anchor=(0.5, 0.965))

fig.text(
    0.01, 0.01,
    f"Driver weight = {driver_mass} kg | Rolling resistance = {rolling_resistance_factor*100:g}% | "
    f"Transmission efficiency = {efficiency*100:g}% | Cd = {Cd} | Slope = {slope_degrees}°",
    fontsize=9, ha="left", va="bottom"
)

fig.tight_layout(rect=[0, 0.03, 1, 0.93])
fig.savefig("drivetrain_sweep_results.png", dpi=150)
plt.show()
