import math
from enum import IntEnum
import numpy as np
from scipy import linalg
import time

np.set_printoptions(suppress=True)

class NodeType(IntEnum):

    ROBOT = 1

    LANDMARK = 2

class Constrain:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Edge:

    def __init__(self, parent, child, constrains):

        self.parent = parent
        self.child = child
        self.constrains = constrains


class Node:

    def __init__(self, type, id):

        self.type = type
        self.id = id
        self.edgs = []                  # 只建立单向的联系


class Graph:

    def __init__(self):

        self.recordId = 0

        self.nodeList = dict()
        self.currentNode = None
        self.landMarkList = dict()
        self.midToLandId = dict()
        self.matrixIndex = dict()
        self.position = []
        self.robotWeight = 1

        self.newNode = dict()

        self.Ax = []
        self.Ay = []
        self.Bx = []
        self.By = []

    def setInitNode(self, constrain):

        id = self.getRecordId()
        node = Node(NodeType.ROBOT, id)
        node.edgs.append(Edge(node, None, constrain))
        self.nodeList[id] = node
        self.currentNode = node

    def getRecordId(self):

        id = self.recordId
        self.recordId += 1

        return id

    def addRobotNode(self, constrains=None):

        id = self.getRecordId()
        node = Node(NodeType.ROBOT, id)
        if constrains is not None:
            preNode = self.currentNode
            edge = Edge(node, preNode, constrains)
            node.edgs.append(edge)
            self.nodeList[id] = node
        self.nodeList[id] = node
        self.newNode[id] = node
        self.currentNode = node


    def addLandMarkNode(self, constrains, mid):

        if mid not in self.midToLandId.keys():
            id = self.getRecordId()
            self.midToLandId[mid] = id
            landMark = Node(NodeType.LANDMARK, id)
            self.landMarkList[id] = landMark
        else:
            landMark = self.landMarkList[self.midToLandId[mid]]

        node = self.currentNode
        edge = Edge(landMark, node, constrains)
        node.edgs.append(edge)

    def getInitMatrix(self):

        size = len(self.matrixIndex)

        A = np.array([[0 for i in range(size)] for j in range(size)], dtype=float)
        B = np.array([0 for i in range(size)], dtype=float)

        return A, B

    def getConstrain(self, x, y):

        constrain = dict()
        constrain['x'] = x
        constrain['y'] = y

        return constrain


    def increaseMatrix(self, A, B, currentSize, increase):

        A = np.insert(A, len(A), [[0 for i in range(currentSize - increase)] for j in range(increase)], axis=1)
        A = np.insert(A, len(A), [[0 for i in range(currentSize + increase)] for j in range(increase)], axis=0)
        B = np.insert(B, len(B), [0 for i in range(increase)], axis=0)

        return A, B

    def solveQR(self, A, B):

        Q, R = linalg.qr(A)
        B = np.dot(Q.T, B)

        return R, B

    def solveRB(self, R, B):

        x = []
        size = len(R)
        for i in range(size):
            temp = 0
            for j in range(i):
                temp += x[j] * R[size-i-1][size-j-1]
            temp = (B[size-i-1] - temp) / R[size-i-1][size-i-1]
            x.append(temp)
        x.reverse()

        return x

    def solveGiven(self, A, B, row):

        for i in range(row):
            if A[row][i] != 0:
                aii = A[i][i]
                aji = A[row][i]
                k = math.sqrt(1 + (aii / aji)**2)
                cos = (-1) * aii / aji / k
                sin = 1 / k
                for k in range(len(A)):
                    aik = A[i][k]
                    ajk = A[row][k]
                    A[i][k] = cos * aik - sin * ajk
                    A[row][k] = sin * aik + cos * ajk
                bi = B[i]
                bj = B[row]
                B[i] = cos * bi - sin * bj
                B[row] = sin * bi + cos * bj

        return A, B

    def solvEdges(self, A, B, edges, attr):

        for edge in edges:
            if edge.parent.type == NodeType.ROBOT and edge.child is not None and edge.child.type == NodeType.ROBOT:
                weight = self.robotWeight
            else:
                weight = 1
            constrains = edge.constrains[attr]
            parentId = self.matrixIndex[edge.parent.id]
            A[parentId][parentId] += weight
            B[parentId] += constrains * weight
            if edge.child is not None:
                childId = self.matrixIndex[edge.child.id]
                A[parentId][childId] -= weight
                A[childId][childId] += weight
                A[childId][parentId] -= weight
                B[childId] -= constrains * weight

        return A, B

    def assignMatrixIndex(self, nodeList, isReconstrcut=False):


        if isReconstrcut:
            self.matrixIndex = dict()

        matrixRecord = len(self.matrixIndex)

        pre = matrixRecord

        for k, node in nodeList.items():
            self.matrixIndex[node.id] = matrixRecord
            matrixRecord += 1
            for edge in node.edgs:
                id = edge.parent.id
                if edge.parent.type == NodeType.LANDMARK and id not in self.matrixIndex.keys():
                    self.matrixIndex[id] = matrixRecord
                    matrixRecord += 1

        end = matrixRecord

        return pre, end

    def delLandMark(self, midList):


        deleteList = []

        for mid in midList:

            if mid not in self.midToLandId.keys():
                continue
            id = self.midToLandId[mid]
            deleteList.append(id)

        for k, node in self.nodeList.items():
            for edge in node.edgs:
                if edge.parent.type == NodeType.LANDMARK and (edge.parent.id in deleteList):
                    node.edgs.remove(edge)



    def reconstrcutGraph(self):

        self.assignMatrixIndex(self.nodeList, True)

        self.Ax, self.Bx = self.getInitMatrix()
        self.Ay, self.By = self.getInitMatrix()

        for k, node in self.nodeList.items():
            self.Ax, self.Bx = self.solvEdges(self.Ax, self.Bx, node.edgs, 'x')
            self.Ay, self.By = self.solvEdges(self.Ay, self.By, node.edgs, 'y')

        self.Ax, self.Bx = self.solveQR(self.Ax, self.Bx)
        self.Ay, self.By = self.solveQR(self.Ay, self.By)

        px = self.solveRB(self.Ax, self.Bx)
        py = self.solveRB(self.Ay, self.By)

        self.position = [(px[i], py[i]) for i in range(len(px))]

        self.newNode = {}

    def solveIncGraph(self):

        pre, end = self.assignMatrixIndex(self.newNode)
        increase = end - pre

        if increase == 0:
            print("error! please add data or reconstrctGraph first")
            return
        self.Ax, self.Bx = self.increaseMatrix(self.Ax, self.Bx, pre, increase)
        self.Ay, self.By = self.increaseMatrix(self.Ay, self.By, pre, increase)

        for k, node in self.newNode.items():
            Ax, Bx = self.solvEdges(self.Ax, self.Bx, node.edgs, 'x')
            Ay, By = self.solvEdges(self.Ay, self.By, node.edgs, 'y')

        length = end

        self.Ax[length-increase:length] = Ax[length-increase:length]
        self.Bx[length-increase:length] = Bx[length-increase:length]

        self.Ay[length-increase:length] = Ay[length-increase:length]
        self.By[length-increase:length] = By[length-increase:length]

        for i in range(increase):
            self.Ax, self.Bx = self.solveGiven(self.Ax, self.Bx, length + i - increase)
            self.Ay, self.By = self.solveGiven(self.Ay, self.By, length + i - increase)

        px = self.solveRB(self.Ax, self.Bx)
        py = self.solveRB(self.Ay, self.By)

        self.position = [(px[i], py[i]) for i in range(len(px))]


        self.newNode = {}



if __name__ == '__main__':


    grah = Graph()
    grah.setInitNode({'x': 0, 'y': 0})
    grah.addLandMarkNode({'x': 2, 'y': 2}, 0)
    grah.addRobotNode({'x': 1, 'y': 1})
    grah.addLandMarkNode({'x': 0.8, 'y': 0.8}, 0)
    # grah.addLandMarkNode({'x': 0.8, 'y': 0.8}, 10)
    grah.reconstrcutGraph()
    print(grah.position)
    # time1 = time.time()
    grah.addRobotNode(grah.getConstrain(2, 2))
    grah.addRobotNode(grah.getConstrain(2, 2))
    grah.solveIncGraph()
    grah.reconstrcutGraph()
    print(grah.position)
    grah.delLandMark([0])
    grah.reconstrcutGraph()
    print(grah.position)

    # grah.addLandMarkNode(2.1, 1)
    #
    # grah.reconstrcutGraph()
    # print(grah.position)
    # time2 = time.time()
    # print(time2 - time1)

