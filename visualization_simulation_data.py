from matplotlib import pyplot as plt
import numpy as np


simulation_data = np.loadtxt('main_frederico.csv', delimiter=',', skiprows=1)


simulation_sample_header = ['linear_velocity_x',
                            'linear_velocity_y',
                            'angular_velocity_theta',
                            'current_pos_x',
                            'current_pos_y',
                            'current_pos_theta',
                            'desired_pos_x',
                            'desired_pos_y',
                            'desired_pos_theta',
                            'time_in_seconds'
                            ]

linear_velocity_x = simulation_data[:, 0]
linear_velocity_y = simulation_data[:, 1]
angular_velocity_theta = simulation_data[:, 2]

current_pos_x = simulation_data[:, 3]
current_pos_y = simulation_data[:, 4]
current_pos_theta = simulation_data[:, 5]

desired_pos_x = simulation_data[:, 6]
desired_pos_y = simulation_data[:, 7]
desired_pos_theta = simulation_data[:, 8]
time_in_seconds = simulation_data[:, 9]

plt.plot(time_in_seconds, current_pos_x, label='current pos x')
plt.plot(time_in_seconds, current_pos_y, label='current pos y')
plt.plot(time_in_seconds, desired_pos_x, label='desired pos x')
plt.plot(time_in_seconds, desired_pos_y, label='desired pos y')
plt.legend()
plt.xlabel('Tempo em segundos')
plt.ylabel('Posição em metros')
plt.draw()
plt.savefig('g1.pdf')
plt.figure(2)

plt.plot(desired_pos_x, desired_pos_y, label='desired trajectory')
plt.plot(current_pos_x, current_pos_y, label='robot trajectory')
plt.legend()
plt.xlabel('posição em metros')
plt.ylabel('Posição em metros')
plt.draw()
plt.savefig('g2.pdf')
plt.figure(3)

plt.plot(time_in_seconds, linear_velocity_x, label='robot linear velocity x')
plt.plot(time_in_seconds, linear_velocity_y, label='robot linear velocity x')
plt.legend()
plt.ylabel('Velocidade em m/s')
plt.xlabel('Tempo em segundos')
plt.draw()
plt.savefig('g3.pdf')
plt.figure(4)
plt.plot(time_in_seconds, current_pos_theta, label='Current $\\theta$ ')
plt.plot(time_in_seconds, desired_pos_theta, label='desired $\\theta$')
plt.ylabel('orientação em rads/s')
plt.xlabel('Tempo em segundos')
plt.legend()
plt.draw()
plt.savefig('g4.pdf')
plt.show()
