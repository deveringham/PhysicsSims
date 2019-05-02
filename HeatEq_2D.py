#
# ooooooooo.   oooo                                   .oooooo..o  o8o                             
# `888   `Y88. `888                                  d8P'    `Y8  `"'                             
#  888   .d88'  888 .oo.   oooo    ooo  .oooo.o      Y88bo.      oooo  ooo. .oo.  .oo.    .oooo.o 
#  888ooo88P'   888P"Y88b   `88.  .8'  d88(  "8       `"Y8888o.  `888  `888P"Y88bP"Y88b  d88(  "8 
#  888          888   888    `88..8'   `"Y88b.            `"Y88b  888   888   888   888  `"Y88b.  
#  888          888   888     `888'    o.  )88b      oo     .d8P  888   888   888   888  o.  )88b 
# o888o        o888o o888o     .8'     8""888P'      8""88888P'  o888o o888o o888o o888o 8""888P' 
#                          .o..P'                                                                 
#                          `Y8P'                                                                  
#
# HeatEq_2D.py
#
# Function to solve heat equation in 2 dimensions with finite difference method
#
# Dylan Everingham
# 5/29/2018
#

###################################################################################################
# Dependencies
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from solver_utils import *

###################################################################################################
# heateq_2d
# 	Solver for heat quation in 2 dimensions
# 	Uses finite diference equations to solve explicitly
###################################################################################################
def heateq_2D(dims, resolution, bc_0, bc_max, ic, do_plot):

########################
	# Parse arguments
	print('Parsing arguments...')

	# Parse dims parameter
	dims, dims_pass = parse_array_arg(dims, [3], int)
	if dims_pass:
		x_max, y_max, t_max = dims[0], dims[1], dims[2]
	else:
		raise TypeError('Incorrectly formed dims argument')
		return

	# Parse resolution parameter
	resolution, resolution_pass = parse_array_arg(resolution, [3], float)
	if resolution_pass:
		dx, dy, dt = resolution[0], resolution[1], resolution[2]
	else:
		raise TypeError('Incorrectly formed resolution argument')
		return

	# If dims and resolution parse correctly, allocate results matrix
	u = np.zeros((x_max,y_max,t_max))
	
	# Parse boundary conditions and put them in results matrix
	bc_0, bc_0_pass = parse_array_arg(bc_0, [t_max], float)
	if bc_0_pass:
		u[0, :] = bc_0
	else:
		raise TypeError('Incorrectly formed bc_0 argument')
		return

	bc_max, bc_max_pass = parse_array_arg(bc_max, [t_max], float)
	if bc_max_pass:
		u[x_max-1, :] = bc_max
	else:
		raise TypeError('Incorrectly formed bc_max argument')
		return

	# Parse initial condition and put it in results matrix
	ic, ic_pass = parse_array_arg(ic, [x_max], float)
	if ic_pass:
		u[:, 0] = ic
	else:
		raise TypeError('Incorrectly formed ic argument')
		return

########################
	# Solve
	print('Solving...')

	for t in range(1, t_max):
		for x in range(1, x_max-1):
			for y in range(1, y_max-1):

				# Main finite difference equation
				u[x,y,t] = ((dt / (dx * dx)) * (u[x+1][y][t-1] - 2*u[x][y][t-1] + u[x-1][y][t-1])) + ((dt / (dy * dy)) * (u[x][y+1][t-1] - 2*u[x][y][t-1] + u[x][y-1][t-1])) + u[x][y][t-1]

########################
	# Plot results
	if (do_plot):
		print('Plotting and animating results...')

		fig, ax = plt.subplots()
		p, = plt.plot([], [], 'ro', animated=True)

		def init():
			ax.set_xlim(0,x_max*dx)
			ax.set_ylim(np.amin(u),np.amax(u))
			return p,

		def update(frame_num):
			p.set_data(np.linspace(0, (x_max-1)*dx, x_max), u[:,frame_num])
			return p,

		ani = FuncAnimation(fig, update, frames=np.arange(t_max), init_func=init, blit=True, interval=1)

		plt.show()

	# Return result array
	return u