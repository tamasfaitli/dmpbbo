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
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with DmpBbo.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

lib_path = os.path.abspath('../../../python/')
sys.path.append(lib_path)

from dmp_bbo.Task import Task


class TaskViapoint(Task):
    
    def __init__(self, viapoint, viapoint_time=None, viapoint_radius=0.0,goal=None,goal_time=None,viapoint_weight=1.0, acceleration_weight=0.0001,goal_weight=0.0):
        if goal is not None:
            assert(goal.shape == viapoint.shape)
            
        self.viapoint_ = viapoint
        self.viapoint_time_ = viapoint_time
        self.viapoint_radius_ = viapoint_radius
        if goal_time is None:
            self.goal_ = np.zeros(viapoint.shape)
        else:
            self.goal_ = goal
        self.goal_time_ = goal_time
        self.viapoint_weight_ = viapoint_weight
        self.acceleration_weight_ = acceleration_weight
        self.goal_weight_ = goal_weight
    
    def costLabels(self):
        return ['viapoint','acceleration','goal']

    def evaluateRollout(self,cost_vars,sample):
        n_dims = self.viapoint_.shape[0]
        n_time_steps = cost_vars.shape[0]
        
        ts = cost_vars[:,0] # fff
        y = cost_vars[:,1:1+n_dims] # fff, rename to ys
        ydd = cost_vars[:,1+n_dims*2:1+n_dims*3] # fff, rename to ydds
        
        dist_to_viapoint = 0.0
        if self.viapoint_weight_>0.0:
            
            if self.viapoint_time_ is None:
                # Don't compute the distance at some time, but rather get the
                # minimum distance
                
                # Compute all distances along trajectory
                viapoint_repeat =  np.repeat(np.atleast_2d(self.viapoint_),n_time_steps,axis=0)
                dists = np.linalg.norm(y-viapoint_repeat,axis=1)
                
                # Get minimum distance
                dist_to_viapoint = dists.min()
                
            else:
                # Get integer time step at t=viapoint_time 
                viapoint_time_step = np.argmax(ts>=self.viapoint_time_)
                if viapoint_time_step==0:
                    print("WARNING: viapoint_time_step=0, maybe viapoint_time_ is too large?")
                # Compute distance at that time step
                y_via = cost_vars[viapoint_time_step,1:1+n_dims]
                dist_to_viapoint = np.linalg.norm(y_via-self.viapoint_)
                
            if self.viapoint_radius_>0.0:
                # The viapoint_radius defines a radius within which the cost is
                # always 0
                dist_to_viapoint -= self.viapoint_radius_
                if dist_to_viapoint<0.0:
                    dist_to_viapoint = 0.0
        
        sum_ydd = 0.0
        if self.acceleration_weight_>0.0:
            sum_ydd = np.sum(np.square(ydd))
        
        delay_cost_mean = 0.0
        if self.goal_weight_>0.0 and self.goal_ is not None:
            after_goal_indices = ts>=self.goal_time_
            ys_after_goal = y[after_goal_indices,:]
            n_time_steps = ys_after_goal.shape[0]
            goal_repeat = np.repeat(np.atleast_2d(self.goal_),n_time_steps,axis=0)
            delay_cost_mean = np.mean(np.linalg.norm(ys_after_goal-goal_repeat,axis=1))
            
            
        costs = np.zeros(1+3)
        costs[1] = self.viapoint_weight_*dist_to_viapoint
        costs[2] = self.acceleration_weight_*sum_ydd/n_time_steps
        costs[3] = self.goal_weight_*delay_cost_mean
        costs[0] = np.sum(costs[1:])
        return costs
        
    def plotRollout(self,cost_vars,ax):
        """Simple script to plot y of DMP trajectory"""
        n_dims = self.viapoint_.shape[0]
        t = cost_vars[:,0]
        y = cost_vars[:,1:n_dims+1]
        if n_dims==1:
            line_handles = ax.plot(t,y,linewidth=0.5)
            ax.plot(t[0], y[0], 'bo', label='start')                
            ax.plot(t[-1], y[-1], 'go', label='end')                
            ax.plot(self.viapoint_time_,self.viapoint_,'ok',label='viapoint')
            if (self.viapoint_radius_>0.0):
                r = self.viapoint_radius_
                t = self.viapoint_time_
                v = self.viapoint_[0]
                ax.plot([t,t],[v+r,v-r],'-k')
                ax.set_xlabel('time (s)')
                ax.set_ylabel('y')
                
        elif n_dims==2:
            line_handles = ax.plot(y[:,0],y[:,1],linewidth=0.5)
            ax.plot(y[0,0], y[0,1], 'bo', label='start')                
            ax.plot(y[-1,0], y[-1,1], 'go', label='end')                
            ax.plot(self.viapoint_[0],self.viapoint_[1],'ko',label='viapoint')
            if (self.viapoint_radius_>0.0):
                circle = plt.Circle(self.viapoint_,self.viapoint_radius_, color='k', fill=False)
                ax.add_artist(circle)
            ax.axis('equal')
            ax.set_xlabel('y_1')
            ax.set_ylabel('y_2')
        else:
            line_handles = []
            
        return line_handles
        
    def saveToFile(self,directory,filename):
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        my_file = open(directory+"/"+filename, 'w')
        for x in self.viapoint_:
            my_file.write(str(x)+" ")
        if self.viapoint_time_:
            my_file.write(str(self.viapoint_time_)+" ")
        else:
            my_file.write(str(-1.0)+" ")
        my_file.write(str(self.viapoint_radius_)+" ")
        
        for x in self.goal_:
            my_file.write(str(x)+" ")
        if self.goal_time_:
            my_file.write(str(self.goal_time_)+" ")
        else:
            my_file.write(str(-1.0)+" ")
            
        my_file.write(str(self.viapoint_weight_)+" ")
        my_file.write(str(self.acceleration_weight_)+" ")
        my_file.write(str(self.goal_weight_)+" ")
        my_file.close()

if __name__=='__main__':
    counter = 0
    for n_dims in [1,2,5]:
        for viapoint_time in [0.5, None]:
            viapoint = np.linspace(0.0,1.0,n_dims)
            task = TaskViapoint(viapoint, viapoint_time)
            task.saveToFile("/tmp/demoTaskViapoint/","viapoint"+str(counter)+".txt")
            counter += 1
        
        
