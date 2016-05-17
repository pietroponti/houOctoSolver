  ####################################
 ######################################
# DEFINE FUNCTIONS FOR PROCEDURAL ANIM #
 ######################################
  ####################################

def makeChannels():
    #Declare variables from HDA parameters
    sel=hou.pwd()
    children=sel.children()
    
    proceduralSolver = hou.node(sel.parm('kinChop').eval())
    numBones = 0
    
    for child in children:
        if 'chain_bone' in child.name():
            numBones += 1
            
            
    proceduralSolver.parm('numchannels').set(numBones)
            
    #Set the parameters for each bone channel
    for bone in range(int(numBones)):

        nameBones = 'chain_bone'+str(bone+1)+':r'
    
        proceduralSolver.parm('name'+str(bone)).set(nameBones)
        proceduralSolver.parm('type'+str(bone)).set(1)
        
    sel.parm('numberOfBones').set(str(numBones))
    
    


def applySineWave():

    #Declare variables from HDA parameters
    import scipy.optimize
    sel=hou.pwd()
    children=sel.children()
    numBones = sel.parm('numberOfBones').eval()
    firstBone = sel.parm('firstBone').eval()
    lastBone = sel.parm('lastBone').eval()
    procSineWave = hou.node(sel.path()+'/KIN_Chops/KIN_proceduralAnimSine')
    chooseRotation = sel.parm('rotationOrder').eval()
    chooseAxis = sel.parm('chooseAxis').eval()
    ramp = sel.parm('sineRamp').eval()
    if chooseAxis == 0:
        chooseAxis = 'x'
    elif chooseAxis == 1:
        chooseAxis = 'y'
    elif chooseAxis == 2:
        chooseAxis = 'z'
    axis=['x','y','z']
        
    for i in range(int(numBones)):
        for axi in axis:
            procSineWave.parm('value'+str(i)+axi).deleteAllKeyframes()
            procSineWave.parm('value'+str(i)+axi).set(0)
            procSineWave.parm('rOrd'+str(i)).set(int(chooseRotation))
        
    for i in range(int(firstBone)-1,int(lastBone)):
        # Define Expression for Sine Wave
        expSineWave = '(sin('+str(i)+'*ch("../../freqSin")+(rand('+str(i)+'*ch("../../randSeed"))*ch("../../randIntensityFreq"))+ch("../../compSin"))*ch("../../ampSin"))*chramp("../../sineRamp",fit('+str(i)+',ch("../../firstBone"),ch("../../lastBone"),0,1),0)'
        procSineWave.parm('value'+str(i)+chooseAxis).setExpression(expSineWave)
        
    sel.parm('sinewaveStatus').set('Sine Wave available between Bone " '+str(firstBone)+' " and Bone " '+str(lastBone)+' " '+' on the " '+str.capitalize(chooseAxis)+' " Axis.')

    
def applyRollWave():

    #Declare variables from HDA parameters
    sel=hou.pwd()
    children=sel.children()
    numBones = sel.parm('numberOfBones').eval()
    firstBone = sel.parm('firstBone').eval()
    lastBone = sel.parm('lastBone').eval()
    procRollWave = hou.node(sel.path()+'/KIN_Chops/KIN_proceduralRoll')
    chooseRotation = sel.parm('rotationOrder').eval()
    chooseAxis = sel.parm('chooseAxis').eval()
    if chooseAxis == 0:
        chooseAxis = 'x'
    elif chooseAxis == 1:
        chooseAxis = 'y'
    elif chooseAxis == 2:
        chooseAxis = 'z'
    axis=['x','y','z']
    
    for i in range(int(numBones)):
        for axi in axis:
            procRollWave.parm('value'+str(i)+axi).deleteAllKeyframes()
            procRollWave.parm('value'+str(i)+axi).set(0)
            procRollWave.parm('rOrd'+str(i)).set(int(chooseRotation))
        
    for i in range(int(firstBone)-1,int(lastBone)):
        # Define Expression for Roll Wave  
        expRollWave = str(i+1)+'*ch("../../rollWave")*chramp("../../rollRamp",fit('+str(i)+',ch("../../firstBone"),ch("../../lastBone"),0,1),0)'
        procRollWave.parm('value'+str(i)+chooseAxis).setExpression(expRollWave)
        
    sel.parm('rollwaveStatus').set('Roll Wave available between Bone " '+str(firstBone)+' " and Bone " '+str(lastBone)+' " '+' on the " '+str.capitalize(chooseAxis)+' " Axis.')


def applyBoneRoll():

    #Declare variables from HDA parameters
    sel=hou.pwd()
    children=sel.children()
    numBones = sel.parm('numberOfBones').eval()
    firstBone = sel.parm('firstBone').eval()
    lastBone = sel.parm('lastBone').eval()
    chooseAxis = sel.parm('chooseAxis').eval()
    if chooseAxis == 0:
        chooseAxis = 'x'
    elif chooseAxis == 1:
        chooseAxis = 'y'
    elif chooseAxis == 2:
        chooseAxis = 'z'
    nulls=[child for child in children if 'nullBone' in child.name()]
    axis=['x','y','z']
        
    # Reset all rotation channels to 0
    for null in nulls:
        for axi in axis:
            null.parm('r'+axi).deleteAllKeyframes()
            null.parm('r'+axi).set(0)
    
    # Assign expressions to selected axis               
    for i in range(int(firstBone)-1,int(lastBone)-1):
        # Define Expression for Bones Roll
        expRoll = '(ch("../rollBones")*'+str(i+1)+')*chramp("../boneRollRamp",fit('+str(i)+',ch("../firstBone"),ch("../lastBone"),0,1),0)'
        nulls[i].parm('r'+chooseAxis).setExpression(expRoll)
        
    sel.parm('rollStatus').set('Bone Roll available between Bone " '+str(firstBone)+' " and Bone " '+str(lastBone)+' " '+' on the " '+str.capitalize(chooseAxis)+' " Axis.')

        
def clearAll():
    #Declare variables from HDA parameters
    sel=hou.pwd()
    children=sel.children()
    numBones = sel.parm('numberOfBones').eval()
    procSineWave = hou.node(sel.path()+'/KIN_Chops/KIN_proceduralAnimSine')
    procRollWave = hou.node(sel.path()+'/KIN_Chops/KIN_proceduralRoll')
    nulls=[child for child in children if 'nullBone' in child.name()]
    axis=['x','y','z']

    # Reset all values to 0 in Channels CHOP
    for i in range(int(numBones)):
        for axi in axis:
            procSineWave.parm('value'+str(i)+axi).deleteAllKeyframes()
            procSineWave.parm('value'+str(i)+axi).set(0)
        
    # Reset all values to 0 in Channels CHOP
    for i in range(int(numBones)):
        for axi in axis:
            procRollWave.parm('value'+str(i)+axi).deleteAllKeyframes()
            procRollWave.parm('value'+str(i)+axi).set(0)
        
    # Reset all rotation channels to 0 for Nulls
    for null in nulls:
        for axi in axis:
          null.parm('r'+axi).deleteAllKeyframes()
          null.parm('r'+axi).set(0)
    
    sel.parm('sinewaveStatus').set('No Procedural Animation Applied.')
    sel.parm('rollwaveStatus').set('No Procedural Animation Applied.')
    sel.parm('rollStatus').set('No Procedural Animation Applied.')

  #####################################
 #######################################
#-DEFINE FUNCTIONS FOR KEYABLE CONTROLS-#
 #######################################
  #####################################

#_MAIN CONTROLS_# 
      
#Select all the main controls        
def selectCtrls():
    sel=hou.pwd()
    children=sel.children()
    for i in children:
        if 'mainCtrl' in i.name():
            i.setSelected(1)
            
#Hide all the main controls        
def hideCtrls():
    sel=hou.pwd()
    children=sel.children()
    for i in children:
        if 'mainCtrl' in i.name():
            if i.isDisplayFlagSet() == True:
                hidden = 0
            else:
                hidden = 1
            i.setDisplayFlag(hidden)
            
            
#Key all the main controls        
def keyCtrls():
    a=1
    sel=hou.pwd()
    children=sel.children()
    axis = ['_tx','_ty','_tz','_rx','_ry','_rz']
    ctrls = [i.name() for i in children if 'mainCtrl' in i.name()]
    currentFrame = hou.frame()
    setKey = hou.Keyframe()
    
    for ctrl in range(len(ctrls)):
    
        setKey.setFrame(currentFrame)
        
        for ax in axis:
            parmAtFrame = sel.parm('ctrl'+str(a)+ax).eval()
            setKey.setValue(parmAtFrame)        
            sel.parm('ctrl'+str(a)+ax).setKeyframe(setKey)
            
        a+=1
        
#Remove Key all the main controls        
def rmKeyCtrls():
    a=1
    sel=hou.pwd()
    children=sel.children()
    axis = ['_tx','_ty','_tz','_rx','_ry','_rz']
    ctrls = [i.name() for i in children if 'mainCtrl' in i.name()]
    currentFrame = hou.frame()
    
    for ctrl in range(len(ctrls)):
     
        for ax in axis:
            sel.parm('ctrl'+str(a)+ax).deleteKeyframeAtFrame(currentFrame)
            
        a+=1
        
#Set to 0 all the main controls        
def resetCtrls():
    a=1
    sel=hou.pwd()
    children=sel.children()
    axis = ['_tx','_ty','_tz','_rx','_ry','_rz']
    ctrls = [i.name() for i in children if 'mainCtrl' in i.name()]
    
    for ctrl in range(len(ctrls)):
     
        for ax in axis:
            sel.parm('ctrl'+str(a)+ax).set(0)
            
        a+=1

#_SHAPE CONTROLS_#

#Select all the shape controls             
def selectShapeCtrls():
    sel=hou.pwd()
    children=sel.children()
    for i in children:
        if 'ctrl' in i.name():
            i.setSelected(1)   
            
#Hide all the shape controls        
def hideSCtrls():
    sel=hou.pwd()
    children=sel.children()
    for i in children:
        if 'ctrl' in i.name():
            if i.isDisplayFlagSet() == True:
                hidden = 0
            else:
                hidden = 1
            i.setDisplayFlag(hidden)

#Key all the shape controls        
def keySCtrls():
    a=1
    sel=hou.pwd()
    children=sel.children()
    axis = ['_tx','_ty','_tz','_rx','_ry','_rz']
    ctrls = [i.name() for i in children if 'ctrl' in i.name()]
    ctrls.pop(0)
    currentFrame = hou.frame()
    setKey = hou.Keyframe()
    
    for ctrl in range(len(ctrls)):
    
        setKey.setFrame(currentFrame)
        
        for ax in axis:
            parmAtFrame = sel.parm('sCtrl'+str(a)+ax).eval()
            setKey.setValue(parmAtFrame)        
            sel.parm('sCtrl'+str(a)+ax).setKeyframe(setKey)
            
        a+=1
        
#Remove Key all the shape controls        
def rmKeySCtrls():
    a=1
    sel=hou.pwd()
    children=sel.children()
    axis = ['_tx','_ty','_tz','_rx','_ry','_rz']
    ctrls = [i.name() for i in children if 'ctrl' in i.name()]
    ctrls.pop(0)
    currentFrame = hou.frame()
    
    for ctrl in range(len(ctrls)):
     
        for ax in axis:
            sel.parm('sCtrl'+str(a)+ax).deleteKeyframeAtFrame(currentFrame)
            
        a+=1
        
#Set to 0 all the shape controls        
def resetSCtrls():
    a=1
    sel=hou.pwd()
    children=sel.children()
    axis = ['_tx','_ty','_tz','_rx','_ry','_rz']
    ctrls = [i.name() for i in children if 'ctrl' in i.name()]
    
    for ctrl in range(len(ctrls)):
     
        for ax in axis:
            sel.parm('sCtrl'+str(a)+ax).set(0)
            
        a+=1
