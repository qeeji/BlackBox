import maya.cmds as cmd


### query default attribute value 
cmd.attributeQuery('myAttribute', node='myNode', listDefault=True)


