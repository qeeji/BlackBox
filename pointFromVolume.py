# -*- coding:utf-8 -*-

"""
Get the position information of the points that fill the inside of the selected mesh or are scattered on the surface.
Reproduced the [PointFromVolume] and [scatter] nodes of Houdini.
"""

import  random
import maya.cmds as cmds
import maya.api.OpenMaya as om


class PointFromVolume(object):
    def __init__(self):
        """
        Store the selected mesh data in meshFn
        """

        self . sel  =  om . MGlobal . getActiveSelectionList ()
        self . meshFn  =  om . MFnMesh ( self . Cell . GetDagPath ( 0 ))

    def getBoundingBox(self):
        """
        Get bounding information for selected objects
        """

        self.boundingBox = om.MBoundingBox()
        self . pointArray  =  om . MPointArray ()

        #Get location information of point
        self.pointArray = self.meshFn.getPoints(om.MSpace.kWorld)

        for  points  in  range ( len ( self . pointArray )):
            self.point = self.pointArray[points]
            self.boundingBox.expand(self.point)

        return self.boundingBox

    def setPointFromVolume(self, distance, surface=False, rand=False):
        """
        Scatter points to mesh and get position information for that point
        argument:
            distance(float): Distance between points. The smaller the value, the denser the density
            surface(bool): If True, scatter on the surface of the mesh
            rand(float): Placed in random. Numerical value becomes random strength value as it is
        """

        # Calculate the offset applied to the minimum and maximum corners of the bounding box
        self . halfVoxelDist  =  0.5  *  distance
        # Get the minimum bounding box
        self.minPoint = self.getBoundingBox().min
        self.minPoint.x += self.halfVoxelDist
        self.minPoint.y += self.halfVoxelDist
        self.minPoint.z += self.halfVoxelDist
        #Get maximum value of bounding box
        self.maxPoint = self.getBoundingBox().max
        self.maxPoint.x += self.halfVoxelDist
        self . maxPoint . y  + =  self . halfVoxelDist
        self.maxPoint.z += self.halfVoxelDist

        def floatIterator(start, stop, step):
            """
            Stores the calculated value by repeating the number within the range from start to stop for the number specified in step.
            example)
                Get the equal number of position information of the specified number (step) between the minimum value (start) and the maximum value (stop) of the bounding box.
            """
            r = start
            while r < stop:
                yield r
                r += step

        #Declare position information after calculation
        self.voxels = []
        for xCoord in floatIterator(self.minPoint.x, self.maxPoint.x, distance):
            for yCoord in floatIterator(self.minPoint.y, self.maxPoint.y, distance):
                for zCoord in floatIterator(self.minPoint.z, self.maxPoint.z, distance):

                    #Cross judgment parameters
                    self . raySource  =  om . MFloatPoint ( xCoord , yCoord , zCoord )
                    self.maxParam = 9999.0
                    self.tolerance = 0.0001
                    randX = random.uniform(-1, 1) * rand
                    randY = random.uniform(-1, 1) * rand
                    randZ = random.uniform(-1, 1) * rand

                    # Branch when setting arguments
                    if surface == True:
                        if rand != False:
                            self . raySource  + =  om . MFloatPoint (
                                randX, randY, randZ)
                            self . rayDirection  =  on . MFloatVector (
                                randX, randY, randZ)
                        elif  rand  ==  False :
                            rand  =  1
                            self . raySource  + =  om . MFloatPoint (
                                randX, randY, randZ)
                            self . rayDirection  =  on . MFloatVector (
                                randX, randY, randZ)
                    elif surface == False:
                        if rand != False:
                            self . raySource  + =  om . MFloatPoint (
                                randX, randY, randZ)
                            self . rayDirection  =  on . MFloatVector (
                                randX, randY, randZ)
                        elif  rand  ==  False :
                            self . rayDirection  =  on . MFloatVector ( 0 , 0 , - 1 )

                    #Cross judgment
                    self . ret  =  self . meshFn . allIntersections (
                        Self . RaySource ,              # RaySource ---------- Rei start point
                        Self . RayDirection ,           the direction of the # rayDirection ------- Rei
                        Om . MSpace . KWorld ,            coordinate space # coordinate space --- hit point is specified
                        Self . MaxParam ,               maximum radius consider the # maxParam ----------- hit
                        False ,                       # testBothDirections-Whether to consider negative rayDirection hits
                        tolerance = self . tolerance ,    # tolerance ---------- numerical tolerances intersection operation
                    )

                    Branch of the return value when the # argument is set
                    if surface == True:
                        if (len(self.ret[0]) % 2 == 1):
                            self.voxels.append(
                                ( self . ret [ 0 ] [ 0 ] [ 0 ], self . ret [ 0 ] [ 0 ] [ 1 ], self . ret [ 0 ] [ 0 ] [ 2 ]))
                        elif  len ( self . ret [ 0 ]) %  2  ==  0  and  len ( self . ret [ 0 ]) ! =  0 :
                            self.voxels.append(
                                ( self . ret [ 0 ] [ 0 ] [ 0 ], self . ret [ 0 ] [ 0 ] [ 1 ], self . ret [ 0 ] [ 0 ] [ 2 ]))

                    elif surface == False:
                        #If the skipped ray hits only once, it is judged to be inside the mesh, otherwise it is judged to be outside the mesh
                        if (len(self.ret[0]) % 2 == 1):
                            self.voxels.append(self.raySource)

        return self.voxels



#Sample script
"""
distance = 3
cls = PointFromVolume ()
pos = cls.setPointFromVolume(distance, surface=False, rand=0)
grp = []
for i in pos:
    loc = cmds.polyCube(w=distance,h=distance,d=distance)
    cmds.setAttr(loc[0]+".translate",i[0],i[1],i[2])
    grp.append(loc[0])
cmds.group(grp)
"""
