"""
Template to be used
-------------------
Nomenclatures['__Group Name__'] = {
    'n': __Total number of fields__,
    'ID': '__HTML Card ID__',
    'Parameters': {
        '__Parameter Name as appear in app__': {
            'n': __orderNumber__,
            'list': {
                '__What to show on Description__': '__What to show on selection menu in app__',
                '__What to show on Description__': '__What to show on selection menu in app__',
                ....
            },
            'sep': '__the seperator required next__',
            'ID': '____HTML input ID__'
        },
        '__Parameter Name as appear in app__': {
            'n': __orderNumber__,
            'list': {
                '__What to show on Description__': '__What to show on selection menu in app__',
                '__What to show on Description__': '__What to show on selection menu in app__',
                ....
            },
            'sep': '__the seperator required next__',
            'ID': '____HTML input ID__'
        },
        .....
    }
}
"""

# import json
Nomenclatures = dict()

Nomenclatures['Fin and Tube Coil'] = {
    'n': 10,
    'ID': 'FT ',
    'Parameters': {
        'V-shape': {
            'n': 1,
            'list': {
                'v-': 'True',
                '': 'False'
            },
            'sep': '',
            'ID': 'FT_V-shape'
        },
        'Type': {
            'n': 2,
            'list': {
                'EVAP': 'EVAP (Evaporator)',
                'COND': 'COND (Condenser)',
                'RAD': 'RAD (Radiator)'
            },
            'sep': ' ',
            'ID': 'FT_Type'
        },
        'Material': {
            'n': 3,
            'list': {
                'Cu': 'Copper',
                'Al': 'Aluminium'
            },
            'sep': '-',
            'ID': 'FT_Material'
        },
        'Pattern': {
            'n': 4,
            'list': {
                '2512': '25.4x12.7 mm',
                '2516': '25.4x15.9 mm',
                '2522': '25.4x22 mm',
                '1916': '19.05x16 mm',
                '3127': '31.75x27.5 mm'
            },
            'sep': '-',
            'ID': 'FT_Pattern'
        },
        'FPI': {
            'n': 5,
            'list': '',
            'sep': '-',
            'ID': 'FT_FPI'
        },
        'Rows': {
            'n': 6,
            'list': '',
            'sep': 'R',
            'ID': 'FT_Rows'
        },
        'Tube / row': {
            'n': 7,
            'list': '',
            'sep': 'T-',
            'ID': 'FT_Tubes'
        },
        'Core, mm': {
            'n': 8,
            'list': '',
            'sep': '-',
            'ID': 'FT_Core'
        },
        'No of circuits': {
            'n': 9,
            'list': '',
            'sep': ' (',
            'ID': 'FT_circuits'
        },
        'Comment, if any': {
            'n': 10,
            'list': '',
            'sep': ')',
            'ID': 'FT_Comment'
        }
    }
}

Nomenclatures['Parallel Flow Coil'] = {
    'n': 11,
    'ID': 'PF ',
    'Parameters': {
        'Type': {
            'n': 1,
            'list': {
                'EVAP': 'EVAP (Evaporator)',
                'COND': 'COND (Condenser)',
                'RAD': 'RAD (Radiator)'
            },
            'sep': ' ',
            'ID': 'PF_Type'
        },
        'Double': {
            'n': 2,
            'list': {
                '2x': 'True',
                '': 'False'
            },
            'sep': '',
            'ID': 'PF_Parameters'
        },
        'Monifold Type': {
            'n': 3,
            'list': {
                'O': 'Round',
                'S': 'Square',
                'D': 'D-type',
                'C': 'Customized for OEM'
            },
            'sep': '',
            'ID': 'PF_Man'
        },
        'Manifold Width': {
            'n': 4,
            'list': '',
            'sep': '',
            'ID': 'PF_Width'
        },
        'Tube Width': {
            'n': 5,
            'list': '',
            'sep': '',
            'ID': 'PF_T_Width'
        },
        'Fin Hieght': {
            'n': 6,
            'list': '',
            'sep': '-',
            'ID': 'PF_F_Height'
        },
        'FPI': {
            'n': 7,
            'list': '',
            'sep': '-',
            'ID': 'PF_FPI'
        },
        'Core': {
            'n': 8,
            'list': '',
            'sep': '-',
            'ID': 'PF_Core'
        },
        'Circuit': {
            'n': 9,
            'list': '',
            'sep': '-',
            'ID': 'PF_Circuit'
        },
        'No of Passes': {
            'n': 10,
            'list': '',
            'sep': ' (',
            'ID': 'PF_Passes'
        },
        'Comment, if any': {
            'n': 11,
            'list': '',
            'sep': ')',
            'ID': 'PF_Comment'
        }
    }
}

Nomenclatures['Fitting'] = {
    'n': 7,
    'ID': 'Fitting ',
    'Parameters': {
        'Type': {
            'n': 1,
            'list': {
                'Connector': 'Connector',
                'Swivel_connector': 'Swivel connector',
                'Swivel_Nut': 'Swivel nut',
                'Crimp_Racor': 'Crimp racor',
                'Reusable_Racor': 'Reusable racor',
                'Clamp_racor': 'Clamp racor (drain hose)',
                'Adaptor': 'Adaptor',
                'Nipple': 'Nipple',
                'Tee': 'Tee (Threaded)',
                'T_racor': 'T racor',
                'Cap': 'Cap',
                'Plug': 'Plug',
                'Nut': 'Nut'
            },
            'sep': '-',
            'ID': 'Fitting_type'
        },
        'Seal type': {
            'n': 2,
            'list': {
                'Oring': 'Oring',
                'Face_Oring': 'Face Oring',
                'Flare_SAE45': 'Flare SAE45',
                'Flare_JIC37': 'Flare JIC37',
                'Clamp': 'Clamp'
            },
            'sep': '-',
            'ID': 'Fitting_Seal'
        },
        'Material': {
            'n': 3,
            'list': {
                'Al': 'Al',
                'Brass': 'Brass',
                'GSt': 'G.St.'
            },
            'sep': '-',
            'ID': 'Fitting_Material'
        },
        'Connection 1': {
            'n': 4,
            'list': {
                '5/8inch_18UNF': '5/8inch 18UNF',
                '3/4inch_16UNF': '3/4inch 16UNF',
                '7/8inch_14UNF': '7/8inch 14UNF',
                '1_1/16inch_14UNF': '1 1/16inch 14UNF',
                '1_1/8inch_12UNF': '1 1/8inch 12UNF',
                'M30x2': 'M30x2',
                '': 'Blank (if T racor,)'
            },
            'sep': '-',
            'ID': 'Fitting_conn1'
        },
        'Connection 2': {
            'n': 5,
            'list': {
                'Counterbored': 'Counterbored (connector)',
                'Counterbored_neck': 'Counterbored neck (connector)',
                'Neck': 'Neck (connector)',
                'Tube': 'Tube (Swivel Nut/connector)',
                'Hose_size': 'Hose (crimp/reusable/clamp racor)',
                '': 'Thread (adaptor/nipple)',
                '2x': '2xThread (Tee)',
                '': 'blank (cap/nut/T racor)'
            },
            'sep': ' ',
            'ID': 'Fitting_conn2'
        },
        'Conn 2 Dimension': {
            'n': 6,
            'list': '',
            'sep': ' (',
            'ID': 'Fitting_conn_dim'
        },
        'Comment, if any': {
            'n': 7,
            'list': '',
            'sep': ')',
            'ID': 'Fitting_Comment'
        }
    }
}

# print(Nomenclatures['F&T Coil']['Parameters'].keys())
# print(json.dumps(Nomenclatures))
