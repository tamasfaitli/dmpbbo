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


from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt                                               
import os, sys


# Include scripts for plotting
lib_path = os.path.abspath('../../../python/')
sys.path.append(lib_path)

from functionapproximators.FunctionApproximatorLWR import *
from functionapproximators.FunctionApproximatorRBFN import *
from functionapproximators.functionapproximators_plotting import *
from functionapproximators.BasisFunction import Gaussian


if __name__=='__main__':
    """Run some training sessions and plot results."""
    # Generate training data 
    n_samples_per_dim = 25
    inputs = np.linspace(0.0, 2.0,n_samples_per_dim)
    targets = 3*np.exp(-inputs)*np.sin(2*np.square(inputs))
    
    fa_names = ["RBFN","LWR"]
    for fa_index in range(len(fa_names)):
        fa_name = fa_names[fa_index]
        
        #############################################
        # PYTHON
        
        # Initialize function approximator
        if fa_name=="LWR":
            intersection = 0.5;
            n_rfs = 9;
            fa = FunctionApproximatorLWR(n_rfs,intersection)
        else:
            intersection = 0.7;
            n_rfs = 9;
            fa = FunctionApproximatorRBFN(n_rfs,intersection)

        
        # Train function approximator with data
        fa.train(inputs,targets)
        
        # Make predictions for the targets
        outputs = fa.predict(inputs)
        
        # Make predictions on a grid
        n_samples_grid = 201
        inputs_grid = np.linspace(0.0, 2.0,n_samples_grid)
        outputs_grid = fa.predict(inputs_grid)
        if fa_name=="LWR":
            lines_grid = fa.getLines(inputs_grid)
        activations_grid = fa.getActivations(inputs_grid)
        
        # Plotting
        fig = plt.figure(fa_index,figsize=(15,5))
        fig.canvas.set_window_title(fa_name) 
        ax = fig.add_subplot(131)
        ax.set_title('Training')
        plotGridPredictions(inputs_grid,outputs_grid,ax,n_samples_grid)
        plotDataResiduals(inputs,targets,outputs,ax)
        plotDataTargets(inputs,targets,ax)
        if fa_name=="LWR":
            plotLocallyWeightedLines(inputs_grid,lines_grid,ax,n_samples_grid,activations_grid)
        if fa_name=="RBFN":
            plotBasisFunctions(inputs_grid,activations_grid,ax,n_samples_grid)
            
            
        # Perturn the function approximator's model parameters and plot
        ax = fig.add_subplot(132)
        ax.set_title('Random perturbations around trained model')
        plotGridPredictions(inputs_grid,outputs_grid,ax,n_samples_grid)
        plotDataTargets(inputs,targets,ax)
        
        values = fa.getParameterVectorSelected()

        for ii in range(5):
            # Generate random vector with values between 0.5-1.5
            rand_vector = 0.5 + np.random.random_sample(values.shape)
            fa.setParameterVectorSelected(rand_vector*values)
            outputs_grid = fa.predict(inputs_grid)
            
            line_handles = plotGridPredictions(inputs_grid,outputs_grid,ax,n_samples_grid)
            plt.setp(line_handles,linewidth=1,color='black')
            
        ax = fig.add_subplot(133)
        ax.set_title('Random perturbations around 0')
        for ii in range(5):
            # Generate random vector with values between -0.5-0.5
            rand_vector = -0.5 + np.random.random_sample(values.shape)
            fa.setParameterVectorSelected(rand_vector)
            outputs_grid = fa.predict(inputs_grid)
            
            line_handles = plotGridPredictions(inputs_grid,outputs_grid,ax,n_samples_grid)
            plt.setp(line_handles,linewidth=1,color='black')
        
    plt.show()
