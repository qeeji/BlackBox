# -*- coding:utf-8 -*-

"""
選択したメッシュ内部を埋め尽くす、または表面に散布されるポイントのポジション情報を取得。
Houdini の 【 PointFromVolume 】,【 scatter 】 ノードを再現。
"""

import random
import maya.cmds as cmds
import maya.api.OpenMaya as om


class PointFromVolume(object):
    def __init__(self):
        """
        meshFn に選択したメッシュデータを格納
        """

        self.sel = om.MGlobal.getActiveSelectionList()
        self.meshFn = om.MFnMesh(self.sel.getDagPath(0))

    def getBoundingBox(self):
        """
        選択したオブジェクトのバウンディング情報を取得
        """

        self.boundingBox = om.MBoundingBox()
        self.pointArray = om.MPointArray()

        # ポイントの位置情報を取得
        self.pointArray = self.meshFn.getPoints(om.MSpace.kWorld)

        for points in range(len(self.pointArray)):
            self.point = self.pointArray[points]
            self.boundingBox.expand(self.point)

        return self.boundingBox

    def setPointFromVolume(self, distance, surface=False, rand=False):
        """
        mesh にポイントを散布し、そのポイントのポジション情報を取得
        引数:
            distance(float) : ポイント間の距離。値が小さいほど密度が濃い
            surface(bool)   : True の場合、メッシュの表面に散布
            rand(float)     : random に配置。数値がそのままランダム強度値となる
        """

        # 境界ボックスの最小角と最大角に適用するオフセットを計算
        self.halfVoxelDist = 0.5 * distance
        # バウンディングボックスの最小値を取得
        self.minPoint = self.getBoundingBox().min
        self.minPoint.x += self.halfVoxelDist
        self.minPoint.y += self.halfVoxelDist
        self.minPoint.z += self.halfVoxelDist
        # バウンディングボックスの最大値を取得
        self.maxPoint = self.getBoundingBox().max
        self.maxPoint.x += self.halfVoxelDist
        self.maxPoint.y += self.halfVoxelDist
        self.maxPoint.z += self.halfVoxelDist

        def floatIterator(start, stop, step):
            """
            start ~ stop 範囲内の数値で step で指定した数分繰り返し、計算値を格納
            例)
                バウンディングボックスの最小値(start) ~ 最大値(stop) の間で指定した数(step) の均等なポジション情報を取得。
            """
            r = start
            while r < stop:
                yield r
                r += step

        # 計算後のポジション情報を宣言
        self.voxels = []
        for xCoord in floatIterator(self.minPoint.x, self.maxPoint.x, distance):
            for yCoord in floatIterator(self.minPoint.y, self.maxPoint.y, distance):
                for zCoord in floatIterator(self.minPoint.z, self.maxPoint.z, distance):

                    # 交差判定のパラメータ
                    self.raySource = om.MFloatPoint(xCoord, yCoord, zCoord)
                    self.maxParam = 9999.0
                    self.tolerance = 0.0001
                    randX = random.uniform(-1, 1) * rand
                    randY = random.uniform(-1, 1) * rand
                    randZ = random.uniform(-1, 1) * rand

                    # 引数設定時の分岐
                    if surface == True:
                        if rand != False:
                            self.raySource += om.MFloatPoint(
                                randX, randY, randZ)
                            self.rayDirection = om.MFloatVector(
                                randX, randY, randZ)
                        elif rand == False:
                            rand = 1
                            self.raySource += om.MFloatPoint(
                                randX, randY, randZ)
                            self.rayDirection = om.MFloatVector(
                                randX, randY, randZ)
                    elif surface == False:
                        if rand != False:
                            self.raySource += om.MFloatPoint(
                                randX, randY, randZ)
                            self.rayDirection = om.MFloatVector(
                                randX, randY, randZ)
                        elif rand == False:
                            self.rayDirection = om.MFloatVector(0, 0, -1)

                    # 交差判定
                    self.ret = self.meshFn.allIntersections(
                        self.raySource,             # raySource ---------- レイスタートポイント
                        self.rayDirection,          # rayDirection ------- レイの方向
                        om.MSpace.kWorld,           # coordinate space --- ヒットポイントが指定されている座標空間
                        self.maxParam,              # maxParam ----------- ヒットを考慮する最大半径
                        False,                      # testBothDirections - 負のrayDirectionのヒットも考慮する必要があるかどうか
                        tolerance=self.tolerance,   # tolerance ---------- 交差操作の数値許容差
                    )

                    # 引数設定時の戻り値の分岐
                    if surface == True:
                        if (len(self.ret[0]) % 2 == 1):
                            self.voxels.append(
                                (self.ret[0][0][0], self.ret[0][0][1], self.ret[0][0][2]))
                        elif len(self.ret[0]) % 2 == 0 and len(self.ret[0]) != 0:
                            self.voxels.append(
                                (self.ret[0][0][0], self.ret[0][0][1], self.ret[0][0][2]))

                    elif surface == False:
                        # 飛ばしたレイが1回のみ当たった場合はメッシュの中、それ以外はメッシュの外と判定
                        if (len(self.ret[0]) % 2 == 1):
                            self.voxels.append(self.raySource)

        return self.voxels



# サンプルスクリプト
"""
distance = 3
cls = PointFromVolume()
pos = cls.setPointFromVolume(distance, surface=False, rand=0)
grp = []
for i in pos:
    loc = cmds.polyCube(w=distance,h=distance,d=distance)
    cmds.setAttr(loc[0]+".translate",i[0],i[1],i[2])
    grp.append(loc[0])
cmds.group(grp)
"""
