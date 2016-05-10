#Get number of bones and name of bones without the number
numbones = raw_input('enter number of bones:')
labelbones = raw_input('enter bones label:')
axis = raw_input('enter axis:')
firstBone = raw_input('enter first affected bone:')
lastBone = raw_input('enter last affected bone:')

#Get selected node (this has to be a channel CHOP - later I might create this)
#selList = hou.selectedNodes()
#as I am using selectedNodes and its a Tuple I reduce to one item by choosing only one itme of the list
#sel = selList[0]

try:
    sel = hou.selectedNodes()[0]
except IndexError:
    print 'select something bitch'

#Set the Number of Channels to be the same as the number of bones
sel.parm('numchannels').set(numbones)

#Create parameters for animation of the sinewave
phaseSinParm = hou.FloatParmTemplate('phaseSin',('phase'),1,default_value=([0]))
freqSinParm = hou.FloatParmTemplate('freqSin',('frequency'),1,default_value=([0]))
ampSinParm = hou.FloatParmTemplate('ampSin',('amplitude'),1,default_value=([1]))

sinAnimParms = (phaseSinParm,freqSinParm,ampSinParm)

for parms in sinAnimParms:
    sel.addSpareParmTuple(parms, in_folder=(['Animate']), create_missing_folders=True)

#Set the parameters for each bone channel
for bone in range(int(numbones)):

    nameBones = labelbones+str(bone+1)+':r'
    
    sel.parm('name'+str(bone)).set(nameBones)
    sel.parm('type'+str(bone)).set(1)
    
    
for i in range(int(firstBone),int(lastBone)):

    exp = 'sin('+str(i+1)+'*ch("phaseSin")+ch("freqSin"))*ch("ampSin")'
    sel.parm('value'+ str(i) + str(axis)).setExpression(exp)
