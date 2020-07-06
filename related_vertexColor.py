import maya.api.OpenMaya as om2
import numpy as np 

def getMFnMesh(inMesh):
	sList = om2.MSelectionList()
	sList.add(inMesh)
	dagPath, component = sList.getComponent(0)
	meshFn = om2.MFnMesh(dagPath)
	return meshFn 

def vtxColor_2_finalData(inMesh , inColors , div = 1.0 , defaultAlpha = 1):
	meshFn = getMFnMesh(inMesh)
	vfs = cmd.filterExpand('%s.vtxFace[*]' % inMesh, sm=70)
	#vfs_2_v_f_dict = {}
	v_2_vfs_dict = {}
	vis = []
	fis = []
	for vf in vfs:
		vi = int(vf.split('[')[1].split(']')[0])
		fi = int(vf.split('[')[2].split(']')[0])
		vis.append(vi)
		fis.append(fi)
		if vi not in v_2_vfs_dict.keys():
			v_2_vfs_dict[vi] = []
		v_2_vfs_dict[vi].append(vf)
	#print v_2_vfs_dict
	vf_2_color_dict = {}
	for i,color in enumerate(inColors):
		for vf in v_2_vfs_dict[i]:
			vf_2_color_dict[vf] = list(color)
	outColors = []
	for vf in vfs:
		color = vf_2_color_dict[vf]
		color = [x/div for x in color]
		color.append(defaultAlpha)
		outColors.append(color)
	outColors = om2.MColorArray(outColors)
	return outColors , fis , vis 

def getVertexColors(inMesh , channel = 'RGB'):
	colorOrder = ['R','G','B']
	cs = [0.0]*3
	for each in channel:
		cs[colorOrder.index(each)] = 1.0 
	cs = np.array(cs)
	colors = pm.polyColorPerVertex( '%s.vtx[*]' % inMesh , query=True , rgb = True)
	#vnum = len(colors) / 3
	colors = np.array([colors[0::3],colors[1::3],colors[2::3]]).transpose()
	colors = colors*cs
	return colors.tolist()
