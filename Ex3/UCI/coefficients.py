params = {
    'HHAR': {
            '222': {'icarl': '0.1', 'lucir': '0.5', 'equivalent': 135},
            '231': {'icarl': '0.1', 'lucir': '0.5', 'equivalent': 135},
            '21111': {'icarl': '0.3', 'lucir': '1.0', 'equivalent': 215},
            '3111': {'icarl': '0.3', 'lucir': '0.5', 'equivalent': 175},
            '321': {'icarl': '0.1', 'lucir': '0.5', 'equivalent': 135},
            '33': {'icarl': '0.1', 'lucir': '0.3', 'equivalent': 95},
            '42': {'icarl': '0.3', 'lucir': '0.8', 'equivalent': 95}
    },

    'MS': {
            '222': {'icarl': '1.0', 'lucir': '0.3', 'equivalent': 135},
            '231': {'icarl': '0.3', 'lucir': '0.5', 'equivalent': 135},
            '21111': {'icarl': '0.3', 'lucir': '0.5', 'equivalent': 215},
            '3111': {'icarl': '0.5', 'lucir': '0.3', 'equivalent': 175},
            '321': {'icarl': '0.5', 'lucir': '0.5', 'equivalent': 135},
            '33': {'icarl': '0.3', 'lucir': '0.5', 'equivalent': 95},
            '42': {'icarl': '0.3', 'lucir': '0.5', 'equivalent': 95},
    },

    'UCI': {
            '21111': {'icarl': '0.5', 'lucir': '0.3', 'equivalent': 215},
            '3111': {'icarl': '0.5', 'lucir': '0.3', 'equivalent': 175},
            '231': {'icarl': '0.3', 'lucir': '0.5', 'equivalent': 135},
            '321': {'icarl': '0.5', 'lucir': '0.5', 'equivalent': 135},
            '222': {'icarl': '1.0', 'lucir': '1.5', 'equivalent': 135},
            '33': {'icarl': '0.3', 'lucir': '0.5', 'equivalent': 95},
            '42': {'icarl': '0.3', 'lucir': '0.5', 'equivalent': 95},
    },

    'RW': {
            '23111': {'icarl': '0.5', 'lucir': '2.0', 'equivalent': 215},
            '32111': {'icarl': '1.0', 'lucir': '2.0', 'equivalent': 215},
            '41111': {'icarl': '1.0', 'lucir': '1.0', 'equivalent': 215},
            '2222': {'icarl': '1.0', 'lucir': '1.5', 'equivalent': 175},
            '4211': {'icarl': '1.0', 'lucir': '2.0', 'equivalent': 175},
            '422': {'icarl': '1.0', 'lucir': '2.0', 'equivalent': 135},
            '332': {'icarl': '1.0', 'lucir': '2.0', 'equivalent': 135},
            '53': {'icarl': '0.3', 'lucir': '2.5', 'equivalent': 95},
    },

    'PM': {
            '433': {'icarl': '0.1', 'lucir': '0.8', 'equivalent': 135},
            '2341': {'icarl': '0.5', 'lucir': '0.5', 'equivalent': 175},
            '4321': {'icarl': '0.1', 'lucir': '0.8', 'equivalent': 175},
            '511111': {'icarl': '1.0', 'lucir': '1.0', 'equivalent': 255},
            '22222': {'icarl': '1.0', 'lucir': '0.3', 'equivalent': 215},
            '532': {'icarl': '0.1', 'lucir': '1.0', 'equivalent': 135},
            '64': {'icarl': '0.1', 'lucir': '1.0', 'equivalent': 95},
    }
}

def get_params(dataset):
    return params[dataset]