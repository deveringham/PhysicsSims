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
# HeatEq_1D.py
#
# Function to solve heat equation in 1 dimension with finite difference method
#
# Dylan Everingham
# 5/23/2018
#

###################################################################################################
# Dependencies
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from solver_utils import *
###################################################################################################


def parse_args(dims, resolution, bc_1, bc_2, ic):
	# Parse arguments
	print('Parsing arguments...')

	# Parse dims parameter
	dims, dims_pass = parse_array_arg(dims, [2], int)
	if not dims_pass:
		raise TypeError('Incorrectly formed dims argument')
		return (0, 0, 0)

	# Parse resolution parameter
	resolution, resolution_pass = parse_array_arg(resolution, [2], float)
	if not resolution_pass:
		raise TypeError('Incorrectly formed resolution argument')
		return (0, 0, 0)

	# Get number of each type of boundary condition
	n_bc_1 = len(bc_1)
	n_bc_2 = len(bc_2)

	# Parse type 1 (Dirichlet) boundary conditions, if present
	if (n_bc_1 > 0):		
		bc, bc_pass = parse_array_arg(bc_1[0], [dims[1]], float)
		if not bc_pass:
			raise TypeError('Incorrectly formed bc_1 argument')
			return (0, 0, 0)

		if (n_bc_2 > 1):
			bc, bc_pass = parse_array_arg(bc_1[1], [dims[1]], float)
			if not bc_pass:
				raise TypeError('Incorrectly formed bc_1 argument')
				return (0, 0, 0)

	# Parse type 2 (Neumann) boundary conditions, if present
	if (n_bc_2 > 0):
		bc, bc_pass = parse_array_arg(bc_2[0], [dims[1]], float)
		if not bc_pass:
			raise TypeError('Incorrectly formed bc_2 argument')
			return (0, 0, 0)

		if (n_bc_2 > 1):
			bc, bc_pass = parse_array_arg(bc_2[1], [dims[1]], float)
			if not bc_pass:
				raise TypeError('Incorrectly formed bc_2 argument')
				return (0, 0, 0)

	# Parse initial condition
	ic, ic_pass = parse_array_arg(ic, [dims[0]], float)
	if not ic_pass:
		raise TypeError('Incorrectly formed ic argument')
		return (0, 0, 0)

	return (1, n_bc_1, n_bc_2)



def plot_result(x_max, t_max, dx, dt, u):
	print('Plotting and animating results...')

	fig, ax = plt.subplots()
	p, = plt.plot([], [], 'ro', animated=True)
	it_text = ax.text(0.5,-0.9,'')

	def init():
		ax.set_xlim(0,x_max*dx)
		ax.set_ylim(np.amin(u),np.amax(u))
		return p,

	def update(frame_num):
		p.set_data(np.linspace(0, (x_max-1)*dx, x_max), u[:,frame_num])
		it_text.set_text('Iteration #' + str(frame_num) + ' / ' + str(t_max))
		return p,it_text

	ani = FuncAnimation(fig, update, frames=np.arange(t_max), init_func=init, blit=True, interval=1)

	plt.title('1D Heat Equation')
	plt.xlabel('Distance')
	plt.ylabel('Heat')

	plt.show()


###################################################################################################
# Solver for heat quation in 1 dimension
# Uses finite diference equations to solve explicitly
###################################################################################################
def heateq_1D(dims, resolution, bc_1, bc_2, ic, do_plot):

########################

	# Parse arguments
	parse = parse_args(dims, resolution, bc_1, bc_2, ic)
	if not parse[0]:
		return []

	# Get parameters
	x_max, t_max = dims[0], dims[1]
	dx, dt = resolution[0], resolution[1]
	n_bc_1, n_bc_2 = parse[1], parse[2]

	# Allocate results matrix
	u = np.zeros((x_max,t_max))

	# Put bcs/ics in matrix
	if (n_bc_1 > 0):
		u[x_max-1, :] = bc_1[0]

		if (n_bc_1 > 1):
			u[0, :] = bc_1[1]

	u[:, 0] = ic

########################
	# Solve
	print('Solving...')
	for t in range(1, t_max):
		for x in range(1, x_max-1):

			# Main finite difference equation
			u[x,t] = (dt / (dx * dx)) * (u[x+1][t-1] - 2*u[x][t-1] + u[x-1][t-1]) + u[x][t-1]

########################
	# Plot results
	if (do_plot):
		plot_result(x_max, t_max, dx, dt, u)

	# Return result array
	return u