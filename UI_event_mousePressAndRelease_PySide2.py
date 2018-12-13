### fork from mottosso/mouse_monitor.py

from PySide2 import QtWidgets , QtCore



class Handler(QtCore.QObject):
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            print "Press: %s" % obj.text()
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            print "Release: %s" % obj.text()
        return super(Handler, self).eventFilter(obj, event)


class Window(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(QtWidgets.QPushButton("Hello 1"))
        layout.addWidget(QtWidgets.QPushButton("Hello 2"))
        layout.addWidget(QtWidgets.QPushButton("Hello 3"))




win = Window()
win.show()

handler = Handler()
for widget in win.children():
    if isinstance(widget, QtWidgets.QPushButton):
        print "Installing in %s" % widget.text()
        widget.installEventFilter(handler)

