scene = hou.node('/obj/tentacleRIG1').children()
bones = []
nulls = []
fkBones = [] 
a = 1
b = 1
c = 0


for child in scene:
    if 'chain_bone' in child.name():
        bones.append(child)

for bone in bones:
    newNull = hou.node('/obj/tentacleRIG1').createNode('null','nullBone1')
    newNull.parm('tz').setExpression('-ch("../chain_bone'+str(a)+'/length")')
    newNull.setInput(0,bone,0)
    nulls.append(newNull)
    a += 1   
    
for null in nulls:
    fkBone = hou.node('/obj/tentacleRIG1').createNode('bone','fkBone1')
    fkBone.parm('length').setExpression('ch("../chain_bone'+str(b)+'/length")')
    fkBone.setInput(0,null,0)
    fkBones.append(fkBone)
    b += 1
    
    
#for blend in blends:
#    blend.setInput(1,bones[b],0)
#    b += 1
#    
#    
#bones.pop(0)
#blends.pop()
#
#
#for bone in bones:
#    bone.setInput(0,blends[c],0)
#    c += 1
