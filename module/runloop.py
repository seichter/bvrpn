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
import mathutils
import math
import os

sys.path.append(bge.logic.expandPath('//module'))

# just scene setup
scn = bge.logic.getCurrentScene()
ctl = bge.logic.getCurrentController()
obj = ctl.owner

foundVRPN = False

def checkIfCamera(obj):
   
    if isinstance(obj,bge.types.KX_Camera):
        return True
    else:
        return False

# import logic
try:
    imp.find_module('vrpn')
    import vrpn
    foundVRPN = True
except ImportError:
    foundVRPN = False
    
globalScale = 10.0
    
def applyForObject(userdata,data):
    scale = globalScale
    
    # update scale from Game properties
    if 'Scale' in obj:
        scale = obj['Scale']
    
    # update the position
    if 'position' in data:
        obj.worldPosition.x =   data['position'][0] * scale
        obj.worldPosition.y = - data['position'][2] * scale
        obj.worldPosition.z =   data['position'][1] * scale
        
        
    # get rotation
    if 'quaternion' in data:
                
        # get rotation as a quaternion
        
        quatVRPN = data['quaternion']
        
        qV = mathutils.Quaternion((quatVRPN[3],quatVRPN[0],- quatVRPN[2],quatVRPN[1]))
        obj.worldOrientation = qV
    
        
    # debug
    if 'Debug' in obj and obj['Debug']:

        obj['Info'] = str(obj.worldPosition)
    pass


def applyForCamera(userdata,data):
    
    scale = globalScale
    
    # update scale from Game properties
    if 'Scale' in obj:
        scale = obj['Scale']
    
    obj.position.x =   data['position'][0] * scale
    obj.position.y = - data['position'][2] * scale
    obj.position.z =   data['position'][1] * scale
    
    pass

# vrpn Callback
def vrpnCallback(userdata, data):
    
    if checkIfCamera(userdata):
        scn.active_camera = userdata
        applyForCamera(userdata,data)
    else:
        applyForObject(userdata,data) 

                    
        
        
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