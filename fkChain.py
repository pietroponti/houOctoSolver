scene = hou.node('/obj/tentacleRIG1').children()
bones = []
nulls = []
blends = [] 
a = 1
b = 0
c = 0


for child in scene:
    if 'chain_bone' in child.name():
        bones.append(child)

#Alterante mode using List comprehension)        
#bones = [child for child in scene if 'chain_bone' in child.name() ]

#Alternate mode to count up
#for i in range(len(bones)):
    
for bone in bones:
    newNull = hou.node('/obj/tentacleRIG1').createNode('null','nullBone1')
    newNull.parm('tz').setExpression('-ch("../chain_bone'+str(a)+'/length")')
    newNull.setInput(0,bone,0)
    nulls.append(newNull)
    a += 1   
    
for null in nulls:
    newBlend = hou.node('/obj/tentacleRIG1').createNode('blend','blendK1')
    newBlend.setInput(0,null,0)
    blends.append(newBlend)
    
    
for blend in blends:
    blend.setInput(1,bones[b],0)
    b += 1
    
    
bones.pop(0)
blends.pop()


for bone in bones:
    bone.setInput(0,blends[c],0)
    c += 1
