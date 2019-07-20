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
# solver_utils.py
#
# Contains helper functions for PDE solvers
#
# Dylan Everingham
# 5/23/2018

###################################################################################################
# Dependencies
import numpy as np
import sys

###################################################################################################

###################################################################################################
# parse_array_arg
#	Makes certain that a given array argument is well formed for the solver
###################################################################################################
def parse_array_arg(arr, expected_dims, expected_type):
	# Make sure arr is a list or a numpy array, and change array to numpy array
	# if it is native python list type
	if (isinstance(arr, list)):
		arr = np.array(arr)
	elif (not isinstance(arr, np.ndarray)):
		print('Argument was neither native python list type nor numpy ndarray type')
		return arr, False

	# Check dimensions argument
	if (isinstance(expected_dims, list)):
		expected_dims = np.array(expected_dims)
	elif(not isinstance(arr, np.ndarray)):
		print('Dims argument to parse_array_arg was not a 1D list/array of ints as expected')
		return arr, False
	for d in expected_dims:
		if not isinstance(d, np.int32):
			print('Dims argument to parse_array_arg was not a 1D list/array of ints as expected')
			return arr, False
	if len(expected_dims.shape) != 1:
		print('Dims argument to parse_array_arg was not a 1D list/array of ints as expected')
		return arr, False

	# Make sure number of dimensions is right
	if len(arr.shape) != expected_dims.shape[0]:
		print('Number array dims (' + str(len(arr.shape)) + ') does not match number of expected dims (' + str(expected_dims.shape[0]) + ')')
		return arr, False

	# Make sure dimensions match
	for i in range(len(arr.shape)):
		if arr.shape[i] != expected_dims[i]:
			print('Dimension ' + str(i+1) + ' mismatch: got ' + str(arr.shape[i]) +', expected ' + str(expected_dims[i]))
			return arr, False

	# Check array type
	if (arr.dtype != expected_type):
		print('Type mismatch: got ' + str(arr.dtype) + ', expected ' + str(expected_type))
		return arr, False

	# Passed all tests, return true
	return arr, True


###################################################################################################
# gen_bc_zero
#	Generates a boundary condition array of all 0s
###################################################################################################
def gen_bc_zero(t_max):
	return [0.0 for i in range(t_max)]

###################################################################################################
# gen_bc_const
#	Generates a boundary condition array with a constant value
###################################################################################################
def gen_bc_const(t_max, val=0.0):
	return [val for i in range(t_max)]

###################################################################################################
# gen_bc_lin
#	Generates a linear boundary condition array
###################################################################################################
def gen_bc_const(t_max, min_val=0.0, max_val=1.0):
	return [min_val+(max_val/(t_max-1))*i for i in range(t_max)]

###################################################################################################
# gen_bc_sin
#	Generates a sin wave boundary condition array
###################################################################################################
def gen_bc_sin(t_max, dt=1.0, amp=1.0, freq=1.0, phase=0.0):
	return [amp*np.sin(2*np.pi*freq*i*dt + phase) for i in range(t_max)]


###################################################################################################
# gen_bc_step
#	Generates a step function boundary condition array
###################################################################################################
def gen_bc_step(t_max, dt=1.0, step_min=0.0, step_max=1.0, width=1.0, duty_cycle=0.5, offset=0.0):
	return [step_min if (((i+offset)%(2*width))<(2*width*duty_cycle)) else step_max for i in range(t_max)]


###################################################################################################
# gen_tri_bc
#	Generates a triangle wave boundary condition array
###################################################################################################


