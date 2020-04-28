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


import numpy as np
import math
import os
import sys

from dmpbbo_lib.bbo.bbo_plotting import *
from dmpbbo_lib.bbo.DistributionGaussian import DistributionGaussian

def runOptimization(cost_function, initial_distribution, updater, n_updates, n_samples_per_update,fig=None,directory=None):
    """ Run an evolutionary optimization process, see \ref page_bbo
    \param[in] cost_function The cost function to optimize
    \param[in] initial_distribution The initial parameter distribution
    \param[in] updater The Updater used to update the parameters
    \param[in] n_updates The number of updates to perform
    \param[in] n_samples_per_update The number of samples per update
    \param[in] fig Optional figure to plot the optimization.
    \param[in] directory Optional directory to save to (default: don't save)     
    \return A learning curve that has the following format
        #rows is number of optimization updates
        column 0: Number of samples at which the cost was evaluated
        column 1: The total cost 
        column 2...: Individual cost components (column 1 is their sum)
    """
    
    distribution = initial_distribution
    
    all_costs = []
    learning_curve = []
    exploration_curve = []
    
    if fig:
        ax = fig.add_subplot(131)
    
    # Optimization loop
    for i_update in range(n_updates): 
        
        # 0. Get cost of current distribution mean
        cost_eval = cost_function.evaluate(distribution.mean)
        
        # 1. Sample from distribution
        samples = distribution.generateSamples(n_samples_per_update)
    
        # 2. Evaluate the samples
        costs = []
        for i_sample in range(n_samples_per_update):
            costs.append(cost_function.evaluate(samples[i_sample,:]))
      
        # 3. Update parameters
        distribution_new, weights = updater.updateDistribution(distribution, samples, costs)
        
        # Bookkeeping and plotting
        # All the costs so far
        all_costs.extend(costs)
        # Update exploration curve
        cur_samples = i_update*n_samples_per_update
        cur_exploration = np.sqrt(distribution.maxEigenValue())
        exploration_curve.append([cur_samples,cur_exploration])
        # Update learning curve
        learning_curve.append([cur_samples])
        learning_curve[-1].extend(cost_eval)
        
        
        # Plot summary of this update
        if fig:
            highlight = (i_update==0)
            plotUpdate(distribution,cost_eval,samples,costs,weights,distribution_new,ax,highlight)
        if directory:
            saveUpdate(directory,i_update,distribution,cost_eval,samples,costs,weights,distribution_new)
        
        # Distribution is new distribution
        distribution = distribution_new
        
        
    # Plot learning curve
    if fig:
        plotExplorationCurve(exploration_curve,fig.add_subplot(132))
        plotLearningCurve(learning_curve,fig.add_subplot(133),all_costs)

    # Save learning curve to file, if necessary
    if directory:
        saveLearningCurve(directory,learning_curve)
        saveExplorationCurve(directory,exploration_curve)
        print('Saved results to "'+directory+'".')
    
    return learning_curve
