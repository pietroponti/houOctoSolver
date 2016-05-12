#Should do this as OnCreate not as part of the homModule
def makeChannels():
    #Declare variables from HDA parameters
    sel=hou.pwd()
    children=sel.children()
    
    proceduralSolver = hou.node(sel.path()+'/KIN_Chops/KIN_proceduralAnim')
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
    sel=hou.pwd()
    children=sel.children()
    numBones = sel.parm('numberOfBones').eval()
    firstBone = sel.parm('firstBone').eval()
    lastBone = sel.parm('lastBone').eval()
    proceduralSolver = hou.node(sel.path()+'/KIN_Chops/KIN_proceduralAnim')
    chooseRotation = sel.parm('rotationOrder').eval()
    chooseAxis = sel.parm('chooseAxis').eval()
    if chooseAxis == 0:
        chooseAxis = 'x'
    elif chooseAxis == 1:
        chooseAxis = 'y'
    elif chooseAxis == 2:
        chooseAxis = 'z'
        
    

    
    for i in range(int(numBones)):
        proceduralSolver.parm('value'+str(i)+'x').deleteAllKeyframes()
        proceduralSolver.parm('value'+str(i)+'x').set(0)
        proceduralSolver.parm('value'+str(i)+'y').deleteAllKeyframes()
        proceduralSolver.parm('value'+str(i)+'y').set(0)
        proceduralSolver.parm('value'+str(i)+'z').deleteAllKeyframes()
        proceduralSolver.parm('value'+str(i)+'z').set(0)
        proceduralSolver.parm('rOrd'+str(i)).set(int(chooseRotation))
        
    for i in range(int(firstBone)-1,int(lastBone)):
        # Define Expression for Sine Wave  
        expSineWave = 'sin('+str(i+1)+'*ch("../../freqSin")+ch("../../compSin"))*ch("../../ampSin")'
        proceduralSolver.parm('value'+str(i)+chooseAxis).setExpression(expSineWave)
        
    sel.parm('sinewaveStatus').set('Sine Wave available between Bone " '+str(firstBone)+' " and Bone " '+str(lastBone)+' " '+' on the " '+str.capitalize(chooseAxis)+' " Axis.')


def applyRoll():

    #Declare variables from HDA parameters
    sel=hou.pwd()
    children=sel.children()
    numBones = sel.parm('numberOfBones').eval()
    firstBone = sel.parm('firstBone').eval()
    lastBone = sel.parm('lastBone').eval()
    proceduralSolver = hou.node(sel.path()+'/KIN_Chops/KIN_proceduralAnim')
    chooseRotation = sel.parm('rotationOrder').eval()
    chooseAxis = sel.parm('chooseAxis').eval()
    if chooseAxis == 0:
        chooseAxis = 'x'
    elif chooseAxis == 1:
        chooseAxis = 'y'
    elif chooseAxis == 2:
        chooseAxis = 'z'
    nulls=[]
    for child in children:
        if 'nullBone' in child.name():
            nulls.append(child)
        
        
    # Reset all rotation channels to 0
    for null in nulls:
        null.parm('rx').deleteAllKeyframes()
        null.parm('rx').set(0)
        null.parm('ry').deleteAllKeyframes()
        null.parm('ry').set(0)
        null.parm('rz').deleteAllKeyframes()
        null.parm('rz').set(0)
    
    # Assign expressions to selected axis               
    for i in range(int(firstBone)-1,int(lastBone)):
        # Define Expression for Roll
        expRoll = 'ch("../rollBones")*'+str(i+1)
        nulls[i].parm('r'+chooseAxis).setExpression(expRoll)
        
    sel.parm('rollStatus').set('Roll available between Bone " '+str(firstBone)+' " and Bone " '+str(lastBone)+' " '+' on the " '+str.capitalize(chooseAxis)+' " Axis.')

        
def clearAll():
    #Declare variables from HDA parameters
    sel=hou.pwd()
    children=sel.children()
    numBones = sel.parm('numberOfBones').eval()
    proceduralSolver = hou.node(sel.path()+'/KIN_Chops/KIN_proceduralAnim')
    nulls=[]
    for child in children:
        if 'nullBone' in child.name():
            nulls.append(child)

    # Reset all values to 0 in Channels CHOP
    for i in range(int(numBones)):
        proceduralSolver.parm('value'+str(i)+'x').deleteAllKeyframes()
        proceduralSolver.parm('value'+str(i)+'x').set(0)
        proceduralSolver.parm('value'+str(i)+'y').deleteAllKeyframes()
        proceduralSolver.parm('value'+str(i)+'y').set(0)
        proceduralSolver.parm('value'+str(i)+'z').deleteAllKeyframes()
        proceduralSolver.parm('value'+str(i)+'z').set(0)
        
    # Reset all rotation channels to 0 for Nulls
    for null in nulls:
        null.parm('rx').deleteAllKeyframes()
        null.parm('rx').set(0)
        null.parm('ry').deleteAllKeyframes()
        null.parm('ry').set(0)
        null.parm('rz').deleteAllKeyframes()
        null.parm('rz').set(0)
    
    sel.parm('sinewaveStatus').set('No Procedural Animation Applied.')
    sel.parm('rollStatus').set('No Procedural Animation Applied.')

        
        
def selectCtrls():
    sel=hou.pwd()
    children=sel.children()
    for i in children:
        if 'mainCtrl' in i.name():
            i.setSelected(1)
            print i.name()
            
def selectShapeCtrls():
    sel=hou.pwd()
    children=sel.children()
    for i in children:
        if 'ctrl' in i.name():
            i.setSelected(1)
            print i.name()    
