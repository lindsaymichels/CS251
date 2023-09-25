'''analysis.py
Run statistical analyses and plot Numpy ndarray data
YOUR NAME HERE
CS 251 Data Analysis Visualization
Spring 2023
'''
import numpy as np
import matplotlib.pyplot as plt
import math


class Analysis:
    def __init__(self, data):
        '''

        Parameters:
        -----------
        data: Data object. Contains all data samples and variables in a dataset.
        '''
        self.data = data

        # Make plot font sizes legible
        plt.rcParams.update({'font.size': 18})

    def set_data(self, data):
        '''Method that re-assigns the instance variable `data` with the parameter.
        Convenience method to change the data used in an analysis without having to create a new
        Analysis object.

        Parameters:
        -----------
        data: Data object. Contains all data samples and variables in a dataset.
        '''
        
        if not isinstance(data, np.ndarray):
            raise TypeError('Input data must be a numpy ndarray')
        if data.ndim != 2:
            raise ValueError('Input data must be a 2D array')
        if data.shape[1] != self.data.shape[1]:
            raise ValueError('Input data must have the same number of columns as the current data')

        
        self.data = data
        
    def header_index(self, header):
        '''Returns the index of the given header in the data array.'''
        try:
            return self.data.headers.index(header)
        except ValueError:
            raise ValueError(f'Header "{header}" not found in data')

    
    def min(self, headers, rows=[]):
        '''Computes the minimum of each variable in `headers` in the data object.
        Possibly only in a subset of data samples (`rows`) if `rows` is not empty.
        (i.e. the minimum value in each of the selected columns)

        Parameters:
        -----------
        headers: Python list of str.
            One str per header variable name in data
        rows: Python list of int.
            Indices of data samples to restrict computation of min over, or over all indices
            if rows=[]

        Returns
        -----------
        mins: ndarray. shape=(len(headers),)
            Minimum values for each of the selected header variables

        NOTE: There should be no loops in this method!
        '''
        if len(rows) == 0:
            data_subset = self.data.get_all_data()[:, self.data.get_header_indices(headers)]
        else:
            data_subset = self.data.select_data(headers, rows)
        return np.min(data_subset, axis=0)

    def max(self, headers, rows=[]):
        '''Computes the maximum of each variable in `headers` in the data object.
        Possibly only in a subset of data samples (`rows`) if `rows` is not empty.

        Parameters:
        -----------
        headers: Python list of str.
            One str per header variable name in data
        rows: Python list of int.
            Indices of data samples to restrict computation of max over, or over all indices
            if rows=[]

        Returns
        -----------
        maxs: ndarray. shape=(len(headers),)
            Maximum values for each of the selected header variables

        NOTE: There should be no loops in this method!
        '''
        if len(rows) != 0:
            data = self.data.select_data(headers, rows)
        else:
            data = self.data.select_data(headers)

        return {header: np.max(data[:, i]) for i, header in enumerate(headers)}
    def range(self, headers, rows=[]):
        '''Computes the range [min, max] for each variable in `headers` in the data object.
        Possibly only in a subset of data samples (`rows`) if `rows` is not empty.

        Parameters:
        -----------
        headers: Python list of str.
            One str per header variable name in data
        rows: Python list of int.
            Indices of data samples to restrict computation of min/max over, or over all indices
            if rows=[]

        Returns
        -----------
        mins: ndarray. shape=(len(headers),)
            Minimum values for each of the selected header variables
        maxes: ndarray. shape=(len(headers),)
            Maximum values for each of the selected header variables

        NOTE: There should be no loops in this method!
        '''
        if len(rows) != 0:
          
            data_subset = self.data
        else:
            data_subset = self.data.select_data(headers, rows)

        mins = np.min(data_subset, axis=0)
        maxes = np.max(data_subset, axis=0)

        return mins, maxes
    def mean(self, headers, rows=[]):
        '''Computes the mean for each variable in `headers` in the data object.
        Possibly only in a subset of data samples (`rows`).

        Parameters:
        -----------
        headers: Python list of str.
            One str per header variable name in data
        rows: Python list of int.
            Indices of data samples to restrict computation of mean over, or over all indices
            if rows=[]

        Returns
        -----------
        means: ndarray. shape=(len(headers),)
            Mean values for each of the selected header variables

        NOTE: You CANNOT use np.mean here!
        NOTE: There should be no loops in this method!
        '''
     
        data_subset = self.data.select_data(headers, rows)
        
        n = len(data_subset)
        return np.sum(data_subset, axis=0) / n
        
    
    def var(self, headers, rows=[]):
        '''Computes the variance for each variable in `headers` in the data object.
        Possibly only in a subset of data samples (`rows`) if `rows` is not empty.

        Parameters:
        -----------
        headers: Python list of str.
            One str per header variable name in data
        rows: Python list of int.
            Indices of data samples to restrict computation of variance over, or over all indices
            if rows=[]

        Returns
        -----------
        vars: ndarray. shape=(len(headers),)
            Variance values for each of the selected header variables

        NOTE: You CANNOT use np.var or np.mean here!
        NOTE: There should be no loops in this method!
        '''
        data = self.data.select_data(headers, rows)
        
         
        n = data.shape[0]

        # calculate the means
        means = np.sum(data, axis=0) / n

        # calculate the variances
        vars = np.sum((data - means)**2, axis=0) / (n - 1)

        return vars
        

    def std(self, headers, rows=[]):
        '''Computes the standard deviation for each variable in `headers` in the data object.
        Possibly only in a subset of data samples (`rows`) if `rows` is not empty.

        Parameters:
        -----------
        headers: Python list of str.
            One str per header variable name in data
        rows: Python list of int.
            Indices of data samples to restrict computation of standard deviation over,
            or over all indices if rows=[]

        Returns
        -----------
        vars: ndarray. shape=(len(headers),)
            Standard deviation values for each of the selected header variables

        NOTE: You CANNOT use np.var, np.std, or np.mean here!
        NOTE: There should be no loops in this method!
        '''
        
        data_subset = self.data.select_data(headers, rows)
    # Compute the mean of the values for each variable
        means = self.mean(headers, rows)

    # Compute the sum of the squared differences between each value and the mean for each variable
        squared_diffs_sum = np.sum((data_subset - means)**2, axis=0)

    # Compute the variance for each variable
        vars = squared_diffs_sum / (len(data_subset) - 1)

        return vars
    def show(self):
        '''Simple wrapper function for matplotlib's show function.

        (Does not require modification)
        '''
        plt.show()

    def scatter(self, ind_var, dep_var, title):
        '''Creates a simple scatter plot with "x" variable in the dataset `ind_var` and
        "y" variable in the dataset `dep_var`. Both `ind_var` and `dep_var` should be strings
        in `self.headers`.

        Parameters:
        -----------
        ind_var: str.
            Name of variable that is plotted along the x axis
        dep_var: str.
            Name of variable that is plotted along the y axis
        title: str.
            Title of the scatter plot

        Returns:
        -----------
        x. ndarray. shape=(num_data_samps,)
            The x values that appear in the scatter plot
        y. ndarray. shape=(num_data_samps,)
            The y values that appear in the scatter plot

        NOTE: Do not call plt.show() here.
        
        '''
       
        # Extract the independent and dependent variable data
        x = self.data.select_data([ind_var] )
        y = self.data.select_data([dep_var])

        # Create a scatter plot
        fig, ax = plt.subplots()
        ax.scatter(x, y)

        # Set the plot title and axis labels
        ax.set_title(title)
        ax.set_xlabel(ind_var)
        ax.set_ylabel(dep_var)

        # Return the x and y values
        return x, y
    

    def pair_plot(self, data_vars, fig_sz=(12, 12), title=''):
        '''Create a pair plot: grid of scatter plots showing all combinations of variables in
        `data_vars` in the x and y axes.

        Parameters:
        -----------
        data_vars: Python list of str.
            Variables to place on either the x or y axis of the scatter plots
        fig_sz: tuple of 2 ints.
            The width and height of the figure of subplots. Pass as a paramter to plt.subplots.
        title. str. Title for entire figure (not the individual subplots)

        Returns:
        -----------
        fig. The matplotlib figure.
            1st item returned by plt.subplots
        axes. ndarray of AxesSubplot objects. shape=(len(data_vars), len(data_vars))
            2nd item returned by plt.subplots

        TODO:
        - Make the len(data_vars) x len(data_vars) grid of scatterplots
        - The y axis of the first column should be labeled with the appropriate variable being
        plotted there.
        - The x axis of the last row should be labeled with the appropriate variable being plotted
        there.
        - There should be no other axis or tick labels (it looks too cluttered otherwise!)

        Tip: Check out the sharex and sharey keyword arguments of plt.subplots.
        Because variables may have different ranges, pair plot columns usually share the same
        x axis and rows usually share the same y axis.
        '''
        fig, axes = plt.subplots(len(data_vars), len(data_vars), figsize=fig_sz, sharex='col', sharey='row')
        fig.suptitle(title)

        for i in range (len(data_vars)):
            for j in range (len(data_vars)):
                x = self.data.select_data([data_vars[i]])
                y = self.data.select_data([data_vars[i]])
                
                if i == j:
                    axes[i, j].hist(x, bins = 20, alpha=0.5, edgecolor = 'black', linewidth = 1.2)
                else:
                    axes[i, j].scatter(x, y, alpha = 0.5, edgecolor = "black")
                    if i ==len(data_vars)-1:
                        axes[i, j].set_xlabel(data_vars[j])
                    if j==0:
                        axes[i, j].set_ylabel(data_vars[i])
                    
               

        return fig, axes