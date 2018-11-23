#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Wed, 23 Sep 2015, 14:36:18
#========================================
import maya.OpenMaya as OpenMaya
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def func(*args):
    print "time triggered..."

#- create time change signal, 3 is 3 seconds, you can input a float number...
time_event_id = OpenMaya.MTimerMessage.addTimerCallback (3, func)

#- delete it, don't run this with up codes..
OpenMaya.MMessage.removeCallback(time_event_id)




##################### try to add this call back to UI parent 
import maya.cmds as cmd
import maya.OpenMaya as om
import maya.OpenMayaUI as mui

from functools import partial

def func(input , *args):
    print (input +'aaa')
    
    
time_event_id = om.MTimerMessage.addTimerCallback(1 , partial(func,'bbb ') )


#om.MMessage.removeCallback(time_event_id)

def removeCallback(inID , *args):
    om.MMessage.removeCallback(inID)
    

win = cmd.window()
cmd.columnLayout()
cmd.button()
cmd.showWindow(win)

#aa = om.MString(win)
uiid = mui.MUiMessage.addUiDeletedCallback(win , partial(removeCallback ,time_event_id ))
