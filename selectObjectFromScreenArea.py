
import maya.OpenMaya as om_1
import maya.OpenMayaUI as omUI_1

currentView = omUI_1.M3dView.active3dView()


om_1.MGlobal.selectFromScreen( 0, 0, currentView.portWidth(), currentView.portHeight(), om_1.MGlobal.kReplaceList)



om_1.MGlobal.selectFromScreen( 700, 300, 800, 400, om_1.MGlobal.kReplaceList)
