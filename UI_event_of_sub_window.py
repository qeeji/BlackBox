
### this is fork from <https://groups.google.com/forum/#!topic/python_inside_maya/P3XXQnWIT9k>

import maya.OpenMayaUI as mui
from shiboken2 import wrapInstance
from PySide import  QtCore, QtWidgets



class HyperShadeEventFilter(QtCore.QObject):
    def __init__(self):
        super(HyperShadeEventFilter, self).__init__()
        ptr = mui.MQtUtil.mainWindow()

        self.Handler = Handler()
        mainWin = wrapInstance(long(ptr), QtWidgets.QWidget)
        mainWin.installEventFilter(self.Handler)        
    
                
class Handler(QtCore.QObject):
    def eventFilter(self, obj, event):
        if event.type() == event.ChildPolished:
            print event.type()

            child = event.child()
            print child.objectName()
            if 'hyperShadePanel' in child.objectName():
                print 'OPEN'

        elif event.type() == event.ChildRemoved:
            print event.type()

            child = event.child()
            if 'hyperShadePanel' in child.objectName():
                print 'CLOSE'

        return super(Handler, self).eventFilter(obj, event)
x = HyperShadeEventFilter()


### can be any sub windows name 
###
