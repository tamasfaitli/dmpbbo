# This file is part of DmpBbo, a set of libraries and programs for the 
# black-box optimization of dynamical movement primitives.
# Copyright (C) 2014 Freek Stulp, ENSTA-ParisTech
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


class TaskSolver:
    """Interface for classes that can perform rollouts.
    
    For further information see the section on \ref sec_bbo_task_and_task_solver
    """
    
    def performRollout(self,sample):
        """ Perform rollouts, that is, given a set of samples, determine all the variables that are relevant to evaluating the cost function.         

        \param[in] sample The sample
        \return The variables relevant to computing the cost.
        """
        raise NotImplementedError('subclasses must override performRollout()!')
        
    def plotRollout(self,cost_vars,ax):
        #print("plotRollout not implemented.")
        pass

