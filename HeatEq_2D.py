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
# 7/20/2018
#

###################################################################################################
# Dependencies
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize
from solver_utils import *
###################################################################################################

###################################################################################################
# Helper function to parse arguments to heateq_2D
###################################################################################################
def parse_args(dims, resolution, bc_1, bc_2, ic):
	# Parse dims parameter
	dims, dims_pass = parse_array_arg(dims, [3], int)
	if not dims_pass:
		raise TypeError('Incorrectly formed dims argument')
		return 0

	# Parse resolution parameter
	resolution, resolution_pass = parse_array_arg(resolution, [3], float)
	if not resolution_pass:
		raise TypeError('Incorrectly formed resolution argument')
		return 0

	# Parse boundary conditions (BCs)
	# BC arcuments are an array of BCs, with an empty array in the place of absent BCs
	for d in range(len(dims)-1):
		for n in range(2):
			# The maximum number of BCs is 2 * the number of space dimensions
			i = 2*d + n

			# Parse type 1 (Dirchlet) boundary conditions, if present
			if (len(bc_1) >= i+1):
				if (bc_1[i] != []):		
					bc, bc_pass = parse_array_arg(bc_1[i], [dims[1-d], dims[-1]], float)
					if not bc_pass:
						raise TypeError('Incorrectly formed bc_1 argument')
						return 0
			
			# Parse type 2 (Neumann) boundary conditions, if present
			if (len(bc_2) >= i+1):
				if (bc_2[i] != []):
					bc, bc_pass = parse_array_arg(bc_2[i], [dims[1-d], dims[-1]], float)
					if not bc_pass:
						raise TypeError('Incorrectly formed bc_2 argument')
						return 0

			# There must be at least one BC on each boundary
			n_bcs = int(bc_1[i] != []) + int(bc_2[i] != [])
			if (n_bcs < 1):
				raise TypeError('Not enough BCs provided')
				return 0


	# Parse initial condition (IC)
	ic, ic_pass = parse_array_arg(ic, [dims[0], dims[1]], float)
	if not ic_pass:
		raise TypeError('Incorrectly formed ic argument')
		return 0

	return 1

###################################################################################################
# Helper function to plot results from heateq_2D
###################################################################################################
def plot_result(x_max, y_max, t_max, dx, dy, dt, u):
	fig, ax = plt.subplots()
	norm = Normalize(np.amin(u), np.amax(u))
	img = ax.imshow(u[:,:,0], Norm=norm)
	it_text = ax.text(0.5,-0.9,'')

	def init():
		ax.set_xlim(0,x_max-1)
		ax.set_ylim(0,y_max-1)
		return img,

	def update(frame_num):
		img = ax.imshow(u[:,:,frame_num], Norm=norm)
		#p.set_data(np.linspace(0, (x_max-1)*dx, x_max), u[:,frame_num])
		it_text.set_text('Iteration #' + str(frame_num) + ' / ' + str(t_max))
		return img,

	ani = FuncAnimation(fig, update, frames=np.arange(t_max), init_func=init, blit=True, interval=100)

	plt.title('2D Heat Equation')

	plt.show()


###################################################################################################
# Solver for heat quation in 2 dimensions
# Uses finite diference equations to solve explicitly
###################################################################################################
def heateq_2D(dims, resolution, bc_1, bc_2, ic, a, do_plot):

########################
	# Parse arguments
	print('Parsing arguments...')
	parse = parse_args(dims, resolution, bc_1, bc_2, ic)
	if not parse:
		return []

	# Get parameters
	x_max, y_max, t_max = dims[0], dims[1], dims[2]
	dx, dy, dt = resolution[0], resolution[1], resolution[2]

	# Allocate results matrix
	u = np.zeros((x_max,y_max,t_max))

	# IC
	u[:, :, 0] = ic

########################
	# Solve
	print('Solving...')
	for t in range(1, t_max):
		for x in range(x_max):
			for y in range(y_max):

				# Handle BCs
				# Corners
				if ((x in [0,x_max-1]) and (y in [0,y_max-1])):
					# Identify which corner we're looking at
					x_edge = int(x>0)
					y_edge = 2+int(y>0)

					# Identify whether type of conditions match at corner
					if ((bc_1[x_edge] != []) and (bc_1[y_edge] != [])):
						# Identify if values match at corner
						u_1 = bc_1[x_edge][y][t]
						u_2 = bc_1[y_edge][x][t]

						if (u_1 == u_2):
							u[x,y,t] = u_1
						else:
							# Values did not match at corner
							print('BC value mismatch at ' + str((x,y,t)))
							return []

					elif ((bc_2[x_edge] != []) and (bc_2[y_edge] != [])):
						# Identify if values match at corner
						#u_1 = bc_1[x_edge][int(x>1)*(y_max-1)][t]
						#u_2 = bc_1[y_edge][int(y>1)*(x_max-1)][t]

						if (u_1 == u_2):
							u[x,y,t] = u_1
						else:
							# Values did not match at corner
							print('BC value mismatch at ' + str((x,y,t)))
							return []

					else:
						# Type of conditions did not match at corner
						print('BC type mismatch at ' + str((x,y,t)))
						return []

				# X boundaries
				elif (x in [0,x_max-1]):
					# Identify which edge we're looking at
					x_edge = int(x>0)

					# Type 1 BCs take precedence over type 2
					if (bc_1[x_edge] != []):
						u[x,y,t] = bc_1[x_edge][y][t]

					#elif(bc_2[0] != []):
						# Main finite difference equation (type 2 bcs)
						#u[x,t] = (a * dt) * bc_2[0][t] + u[x][t-1]

				# Y boundaries
				elif (y in [0,y_max-1]):
					# Identify which edge we're looking at
					y_edge = 2+int(y>0)

					# Type 1 BCs take precedence over type 2
					if (bc_1[y_edge] != []):
						u[x,y,t] = bc_1[y_edge][x][t]

					#elif(bc_2[0] != []):
						# Main finite difference equation (type 2 bcs)
						#u[x,t] = (a * dt) * bc_2[0][t] + u[x][t-1]

				else:
					# Main finite difference equation (not at boundaries)
					u[x,y,t] = (a * dt) * ( ((u[x+1,y,t-1] - 2*u[x,y,t-1] + u[x-1,y,t-1]) / (dx * dx)) + ((u[x,y+1,t-1] - 2*u[x,y,t-1] + u[x,y-1,t-1]) / (dy * dy)) + u[x,y,t] )

########################
	# Plot results
	if (do_plot):
		print('Plotting and animating results...')
		plot_result(x_max, y_max, t_max, dx, dy, dt, u)

	# Return result array
	return u