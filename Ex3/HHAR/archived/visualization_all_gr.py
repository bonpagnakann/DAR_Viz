from histogram import *
from duration_avg import *
from average_by_methods import *
from vis_all_acc import *
from average_all_classes import *
from class_accuracy_all import *
from rename_vae_folders import *
from copy_results import *

scenarios = ['21111','222','231','3111','321','33','42']

for scenario in scenarios:
    #rename_vae_folders('MS', scenario)
    all_class_acc('UCI', scenario)
    new_old_class_acc('UCI', scenario)
    average_all_classes('UCI', scenario)
    average_by_methods('UCI', scenario)
    vis_bar_accuracy('UCI', scenario)
    accuracy_histogram('UCI', scenario)
    duration_vis(scenario)

copy_results(scenarios)
