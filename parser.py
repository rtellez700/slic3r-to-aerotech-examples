import numpy as np
import re

def remove_line(line):
    return '; >>> ' + line + ' ; REMOVED'
    
def parse_gcode(input_file, output_file, print_settings):
    
    d_N = print_settings['d_N']
    v_N = print_settings['v_N']
    ACCEL_DEFAULT = print_settings['ACCEL_DEFAULT']
    DECEL_DEFAULT = print_settings['DECEL_DEFAULT']

    dwell_initial = np.round(d_N/v_N * 0.7 ,2) # seconds
    dwell_initial_cmd = f'G4 P{dwell_initial}' if dwell_initial >= 0.3 else ''

    print(dwell_initial_cmd)

    TOGGLE_P_ON = 'Call togglePress P5; toggle on'
    TOGGLE_P_OFF = 'Call togglePress P5; toggle off'

    contents = open(input_file, "r").read().splitlines()

    # first pass of parsing
    for j, line in enumerate(contents):
    
        # remove Extrude `E` commands
        re_E_pattern = r"E[+-]?[0-9]+\.[0-9]+"
        contents[j] = re.sub(re_E_pattern, "", line)
        
        # remove all initial P_ON / P_OFF lines
        if 'Call togglePress P5' in line:
    #         contents[j] = remove_line(line)
            contents[j] = ""
            
        # remove initial home move
    #     if '; move to first infill point' in line:
    #         contents[j] = remove_line(line)

        # reset HOME POSITION
        if 'move to next layer (0)' in line:
            contents[j] = 'G92 X0 Y0  ; RESET X,Y HOME POSITION TO CURRENT POSITION\n' + line + '\n'

        # change acceleration / deceleration
        if 'G65 F2000;' in line:
            contents[j] = f'G65 F{ACCEL_DEFAULT}; DEFAULT ACCEL RATE'

        if 'G66 F2000' in line:
            contents[j] = f'G65 F{DECEL_DEFAULT}; DEFAULT ACCEL RATE'
            
        # remove M83,204, 201
        if ('M83' in line) or ('M201' in line) or ('M204' in line):
            contents[j] = remove_line(line)
    
    # second pass of parsing        
    pass_first_p_on = False

    for j, line in enumerate(contents):
        
        # ADD P_ON COMMAND
        # if 'move to next layer (0)' in line:
        #     contents[j] = line + '\n' + TOGGLE_P_ON + '\n'
        if 'G1 F' in line:
            contents[j] = line + '\n' + TOGGLE_P_ON + '\n'
            pass_first_p_on = True

        # ADD P_OFF COMMAND
        if ('; reset extrusion distance' in line) and (pass_first_p_on == True):
            # contents[j] = line + '\n' + TOGGLE_P_OFF + '\n'
            contents[j] = TOGGLE_P_OFF + '\n' + line + '\n'
        if ('move to next layer' in line) and (pass_first_p_on == True):
            # contents[j] = line + '\n' + TOGGLE_P_OFF + '\n'
            contents[j] = TOGGLE_P_OFF + '\n' + line + '\n'

        # if ';END gcode for filament' in line:
        #     contents[j] = line + '\n\n' + TOGGLE_P_OFF + '\n'

    count_P_ON  = np.sum([TOGGLE_P_ON in l for l in contents])
    count_P_OFF = np.sum([TOGGLE_P_OFF in l for l in contents])

    assert count_P_OFF == count_P_ON, f'Inconsistent togglePressure() commands. count_P_ON={count_P_ON} and count_P_OFF={count_P_OFF}'

    # if everything went well save to file
    with open(output_file, 'w') as f:
        for line in contents:
            f.write("%s\n" % line)