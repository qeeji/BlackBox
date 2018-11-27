import maya.OpenMaya as om
import maya.cmds as cmds
import random

def GetDagPath(nodeName):
sel = om.MSelectionList()
om.MGlobal.getSelectionListByName(nodeName, sel)

dp = om.MDagPath()

sel.getDagPath(0,dp)
return dp


def UvCoordToWorld(U, V, mesh):

mfnMesh = om.MFnMesh(GetDagPath(mesh))
numFaces = mfnMesh.numPolygons()

WSpoint = om.MPoint(0.0,0.0,0.0)

util2 = om.MScriptUtil()
util2.createFromList ((U, V),2)
float2ParamUV = util2.asFloat2Ptr()

for i in range(numFaces):
try:
mfnMesh.getPointAtUV(i,WSpoint, float2ParamUV, om.MSpace.kWorld)
break; #point is in poly
except:
continue #point not found!

return WSpoint

f = UvCoordToWorld (random.random(), random.random(), cmds.ls(sl=True,type='shape'))
print [f[0], f[1], f[2]]
