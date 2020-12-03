# This file is part of DmpBbo, a set of libraries and programs for the 
# black-box optimization of dynamical movement primitives.
# Copyright (C) 2018 Freek Stulp
#
# DmpBbo is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# DmpBbo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with DmpBbo.  If not, see <http://www.gnu.org/licenses/>.
# 

import numpy as np
import sys
import os

from dmpbbo_lib.dynamicalsystems.DynamicalSystem import DynamicalSystem#


class TimeSystem(DynamicalSystem):
    
    def __init__(self, tau, count_down=False, name="TimeSystem"):
        super().__init__(1, tau, np.zeros([1,1]), np.ones([1,1]), name)
        self.count_down_ = count_down
        self.tracking_error = 0
        if (self.count_down_):
            self.set_initial_state(np.ones([1,1]))
            self.set_attractor_state(np.zeros([1,1]))

    def differentialEquation(self, x):
        xd = np.zeros([1,1])
        alpha_x = 2
        alpha_px = 20000

        x_dot = (alpha_x*x)/((1+alpha_px*self.tracking_error)*self.tau_)
        #x_dot = 1/self.tau_

        # if x_dot < 1e-10:
        #     x_dot = 1e-10
        if self.count_down_:
            if x>0:
                xd[0] = -x_dot
        else:
            if x<1.0:
                xd[0] = x_dot
                
        return xd

    def set_tracking_error(self, e):
        self.tracking_error = e

#    def analyticalSolution(self, ts):
#        T = ts.size
#
#        # Prepare output arguments to be of right size
#        xs = np.zeros([T,self.dim_]);
#        xds = np.zeros([T,self.dim_]);
#  
#        # Find first index at which the time is larger than tau. Then velocities should be set to zero.
#        velocity_stop_index = -1;
#  int i=0;
#  while (velocity_stop_index<0 && i<ts.size())
#    if (ts[i++]>tau())
#      velocity_stop_index = i-1;
#    
#  if (velocity_stop_index<0)
#    velocity_stop_index = ts.size();
#
#  if (count_down_)
#  {
#    xs.topRows(velocity_stop_index) = (-ts.segment(0,velocity_stop_index).array()/tau()).array()+1.0;
#    xs.bottomRows(xs.size()-velocity_stop_index).fill(0.0);
#  
#    xds.topRows(velocity_stop_index).fill(-1.0/tau());
#    xds.bottomRows(xds.size()-velocity_stop_index).fill(0.0);
#  }
#  else
#  {
#    xs.topRows(velocity_stop_index) = ts.segment(0,velocity_stop_index).array()/tau();
#    xs.bottomRows(xs.size()-velocity_stop_index).fill(1.0);
#  
#    xds.topRows(velocity_stop_index).fill(1.0/tau());
#    xds.bottomRows(xds.size()-velocity_stop_index).fill(0.0);
#  }
  
