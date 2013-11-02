module Izhikenvich where 

import Numeric.GSL
import Numeric.LinearAlgebra
import Graphics.Plot 

xdot t [x,v] = [v, -0.95*x - 0.1v]

ts = linspace 100 (0, 20)

sol = odeSolve xdot [10,0] ts 
main = mplot (ts : toColumns sol)
