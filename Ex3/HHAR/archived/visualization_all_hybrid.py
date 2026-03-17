from histogram import *
from duration_avg import *
from average_by_methods import *
from vis_all_acc import *
from average_all_classes import *
from class_accuracy_all import *

#scenarios = ['2_1_1_1_1','2_2_2','2_3_1','3_1_1_1','3_2_1','3_3','4_2']

params = {  '222': {'icarl': '0.1', 'lucir': '0.5'},
            '21111': {'icarl': '0.3', 'lucir': '1.0'},
            '231': {'icarl': '0.1', 'lucir': '0.5'},
            '3111': {'icarl': '0.3', 'lucir': '0.5'},
            '321': {'icarl': '0.1', 'lucir': '0.5'},
            '33': {'icarl': '0.1', 'lucir': '0.3'},
            '42': {'icarl': '0.3', 'lucir': '0.8'},
}

for scenario in list(params.keys()):
    all_class_acc('MS', scenario, params)
    new_old_class_acc('MS', scenario, params)
    average_all_classes('MS', scenario)
    average_by_methods('MS', scenario)
    vis_bar_accuracy('MS', scenario)
    accuracy_histogram('MS', scenario)
    duration_vis(scenario)

