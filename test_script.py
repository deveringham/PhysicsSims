# Test script

# Dependencies
import numpy as np
from HeatEq_1D import *

# Configuration variables
x_max = 100
dx = 0.1
t_max = 10000
dt = 0.001

# Set BCs
bc_0 = gen_bc_sin(t_max, dt, 1.0, 1.0, 0.0)
bc_max = gen_bc_step(t_max, dt, -1.0, 1.0, 1000.0, 0.5, 1000.0)

# Set IC
ic = [0.0 for i in range(x_max)]

# Run the solver
result_array = heateq_1D([x_max,t_max], [dx,dt], [bc_0,bc_max], [], ic, True)