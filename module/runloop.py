#
# Simple Blender VRPN integration
# 
# (c) 2015 Hartmut Seichter
# 
# Graphics+Interaction Laboratory
# Schmalkalden University of Applied Sciences
# 

import bge
import imp
import sys
import bpy
import mathutils
import math

sys.path.append(bpy.path.abspath("//module"))

foundVRPN = False

# import logic
try:
    imp.find_module('vrpn')
    import vrpn
    foundVRPN = True
except ImportError:
    foundVRPN = False

# just scene setup
scn = bge.logic.getCurrentScene()
ctl = bge.logic.getCurrentController()
obj = ctl.owner

# modify this scale according to units in the file    


# vrpn Callback
def vrpnCallback(userdata, data):

    scale = 1.0

    if 'Scale' in obj:
        scale = obj['Scale']
    
    # update the position
    if 'position' in data:
        obj.worldPosition.x = data['position'][0] * scale
        obj.worldPosition.y = data['position'][1] * scale
        obj.worldPosition.z = data['position'][2] * scale
        
        
    # get rotation
    if 'quaternion' in data:
                
        # get rotation as a quaternion
        qR = mathutils.Quaternion(data['quaternion'])
        
        # set as world orientation 
        obj.worldOrientation = qR.to_matrix()
        
    # debug
    if 'Debug' in obj and obj['Debug']:

        obj['Info'] = str(obj.worldPosition)
                    
        
        
if foundVRPN:

    # check if we installed the callback
    if not "vrpn_tracker_instance" in obj:
        
        obj["vrpn_tracker_instance"] = vrpn.receiver.Tracker(obj['VRPN'])
        obj["vrpn_tracker_instance"].register_change_handler(obj, vrpnCallback, "position")

    else:
        # need to call multiple times
        for x in range(1,5):
            obj["vrpn_tracker_instance"].mainloop()
else:
    
    print("Error: no VRPN module found!")