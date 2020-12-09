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
                'RAD': 'RAD (Radiator)',
                'HTR': 'HTR (Heater'
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
                'T': 'T (Thread)',
                'T_racor': 'T racor (for drain hoses)',
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
                'G.St': 'G.St.'
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

Nomenclatures['Subassembly (Man, side plate, header, ...)'] = {
    'n': 3,
    'ID': 'Sub ',
    'Parameters': {
        'Subassembly Name': {
            'n': 1,
            'list': '',
            'sep': '-',
            'ID': 'Sub_name'
        },
        'Parrent Name': {
            'n': 2,
            'list': '',
            'sep': ' (',
            'ID': 'Sub_parrent'
        },
        'Comment, if any': {
            'n': 3,
            'list': '',
            'sep': ')',
            'ID': 'Sub_comment'
        }
    }
}

Nomenclatures['Rivet'] = {
    'n': 6,
    'ID': 'Rivet ',
    'Parameters': {
        'Material': {
            'n': 1,
            'list': {
                'Al': 'Aluminum',
                'G.St': 'Galvanized steel'
            },
            'sep': '-',
            'ID': 'RivetMaterial'
        },
        'Head Type': {
            'n': 2,
            'list': {
                'Domed_head': 'Domed Head',
                'Countersunk_head': 'Countersunk_Head',
                'Large_Flange_head': 'Large_Flange_Head'
            },
            'sep': '-',
            'ID': 'RivetHeadType'
        },
        'Sealed': {
            'n': 3,
            'list': {
                'sealed': 'True',
                '': 'False'
            },
            'sep': '-',
            'ID': 'RivetSealed'
        },
        'Diameter': {
            'n': 4,
            'list': '',
            'sep': 'x',
            'ID': 'RivetDiameter'
        },
        'Length': {
            'n': 5,
            'list': '',
            'sep': 'mm (',
            'ID': 'RivetLength'
        },
        'Comment, if any': {
            'n': 6,
            'list': '',
            'sep': ')',
            'ID': 'RivetComment'
        }
    }
}

Nomenclatures['Washer'] = {
    'n': 5,
    'ID': 'Washer ',
    'Parameters': {
        'Material': {
            'n': 1,
            'list': {
                'Al': 'Aluminum',
                'G.St': 'Galvanized steel',
                'Rubber': 'Rubber'
            },
            'sep': '-',
            'ID': 'WasherMaterial'
        },
        'Type': {
            'n': 2,
            'list': {
                'Flat': 'Flat',
                'Spring': 'Spring',
                'Grooved': 'Grooved'
            },
            'sep': '-ID',
            'ID': 'WasherType'
        },
        'Inner Diameter': {
            'n': 3,
            'list': '',
            'sep': 'xOD',
            'ID': 'WasherID'
        },
        'Outter Diameter': {
            'n': 4,
            'list': '',
            'sep': 'mm (',
            'ID': 'WasherOD'
        },
        'Comment, if any': {
            'n': 5,
            'list': '',
            'sep': ')',
            'ID': 'WasherComment'
        }
    }
}

Nomenclatures['Nut'] = {
    'n': 5,
    'ID': 'Nut ',
    'Parameters': {
        'Material': {
            'n': 1,
            'list': {
                'Al': 'Aluminum',
                'G.St': 'Galvanized steel'
            },
            'sep': '-',
            'ID': 'NutMaterial'
        },
        'Type': {
            'n': 2,
            'list': {
                'Hex': 'Hex',
                'Nylock': 'Nylock',
                'Flange': 'Flange',
                'Wing': 'Wing',
                'Jam': 'Jam',
                'Square': 'Square'
            },
            'sep': '-M',
            'ID': 'NutType'
        },
        'Thread M size': {
            'n': 3,
            'list': '',
            'sep': 'x',
            'ID': 'NutThread'
        },
        'Thread pitch': {
            'n': 4,
            'list': '',
            'sep': 'mm (',
            'ID': 'NutPitch'
        },
        'Comment, if any': {
            'n': 5,
            'list': '',
            'sep': ')',
            'ID': 'NutComment'
        }
    }
}

Nomenclatures['Foam'] = {
    'n': 5,
    'ID': 'Foam ',
    'Parameters': {
        'Type': {
            'n': 1,
            'list': '',
            'sep': '-',
            'ID': 'FoamType'
        },
        'Name': {
            'n': 2,
            'list': '',
            'sep': '-',
            'ID': 'FoamName'
        },
        'Dimension LxWxTh mm': {
            'n': 3,
            'list': '',
            'sep': 'mm-',
            'ID': 'FoamDim'
        },
        'Where Used': {
            'n': 4,
            'list': '',
            'sep': ' (',
            'ID': 'FoamWhereUsed'
        },
        'Comment, if any': {
            'n': 5,
            'list': '',
            'sep': ')',
            'ID': 'FoamComment'
        }
    }
}
# print(Nomenclatures['F&T Coil']['Parameters'].keys())
# print(json.dumps(Nomenclatures))
