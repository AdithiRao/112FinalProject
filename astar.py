import numpy

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(board, start, end):
    startingNode = Node(None, start)
    startingNode.g = startingNode.h = startingNode.f = 0
    endingNode = Node(None, end)
    endingNode.g = endingNode.h = endingNode.f = 0
    list1 = []
    list2 = []
    list1.append(startingNode)
    while len(list1) > 0:
        currNode = list1[0]
        currInd = 0
        for index, item in enumerate(list1):
            if item.f < currNode.f:
                currNode = item
                currInd = index
        list1.pop(currInd)
        list2.append(currNode)
        if currNode == endingNode:
            path = []
            current = currNode
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        branch = []
        for move in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nodePos = (currNode.position[0] + move[0], currNode.position[1] + move[1])
            if nodePos[0] > (len(board) - 1) or nodePos[0] < 0 or nodePos[1] > (len(board[len(board)-1]) -1) or nodePos[1] < 0:
                continue
            if board[nodePos[0]][nodePos[1]] != 0:
                continue
            newNode = Node(currNode, nodePos)
            branch.append(newNode)
        for subBranch in branch:
            for item in list2:
                if subBranch == item:
                    continue
            subBranch.g = currNode.g + 1
            subBranch.h = ((subBranch.position[0] - endingNode.position[0]) ** 2) \
            + ((subBranch.position[1] - endingNode.position[1]) ** 2)
            subBranch.f = subBranch.g + subBranch.h
            for open_node in list1:
                if subBranch == open_node and subBranch.g > open_node.g:
                    continue
            list1.append(subBranch)


def createPath(x1, y1, x2, y2):
    board = numpy.zeros((893,627))
    board = board.tolist()
    for i in range(len(board)):
        for j in range(len(board[0])):
            board[i][j] = int(board[i][j])
    for i in range(315,400):
        for j in range(305, 440):
            board[i][j] = 1

    start = (x1, y1)
    end = (x2, y2)

    path = astar(board, start, end)
    return path
