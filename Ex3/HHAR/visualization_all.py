
from duration_avg import *
from average_by_methods import *

from average_all_classes import *
from class_accuracy_all import *
from copy_results import *
import histogram_equi, vis_all_acc_equiv, vis_all_acc, histogram
from coefficients import *


dataset = 'HHAR'
params = get_params(dataset)
for scenario in list(params.keys()):
    #all_class_acc(dataset, scenario, params)
    #new_old_class_acc(dataset, scenario, params)
    #average_all_classes(dataset, scenario)
    #average_by_methods(dataset, scenario)
    #vis_all_acc.vis_bar_accuracy(dataset, scenario)
    #histogram.accuracy_histogram(dataset, scenario)
    vis_all_acc_equiv.vis_bar_accuracy(dataset, scenario, params[scenario]['equivalent'])
    histogram_equi.accuracy_histogram(dataset, scenario, params[scenario]['equivalent'])
    #duration_vis(dataset, scenario, icarl= params[scenario]['icarl'], lucir= params[scenario]['lucir'])

# Define the base source and destination directories
#scenarios = ["222","231","321","21111","3111","42","33"]  # Replace with the correct path to the source directory

#copy_results(list(params.keys()))
