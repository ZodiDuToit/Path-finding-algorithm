import pygame, math
GRAY = (125, 125, 125)

DARK_GRAY = (200, 150, 150)

BLUE = (0, 80, 155)
LITE_BLUE = (0, 125, 125)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

LITE_GREEN = (0, 125, 0)
LITE_RED = (125, 0, 0)

START_COLOR = LITE_GREEN
END_COLOR = LITE_RED
PATH_COLOR = (238, 149, 114)
SEARCH_COLOR = (32, 178, 170)

NEIGHBOUR_COLOR = (176, 226, 255)
DEFAULT_COLOR = (180, 180, 180)
WALL_COLOR = (100, 100, 100)

BACKGROUND_COLOR = WHITE


class Node:
    def __init__(self, position, currentState=None, parent=None):

        # block variables
        self.color = DEFAULT_COLOR

        x, y = position
        self.x, self.y = x * Map.blockSize, y * Map.blockSize
        self.position = (self.x, self.y)

        self.blockPosition = position
        self.XblockPosition, self.YblockPosition = self.blockPosition

        self.parent = parent
        self.currentState = currentState

        self.blockSize = Map.blockSize

        self.rect = pygame.Rect(self.x, self.y, self.blockSize - 1,
                                self.blockSize - 1)
        # node variables
        self.g = None
        self.h = None
        self.f = None

    def calculate_cost(self):
        end_x, end_y = endNode.blockPosition

        # calculating f the cost)
        self.g = self.currentState
        self.h = math.sqrt((end_x - self.XblockPosition)**2 +
                           (end_y - self.YblockPosition)**2)

        self.f = self.g + self.h
        return self.f


class Button:
    def __init__(self,
                 position,
                 size,
                 label,
                 color=LITE_GREEN,
                 textColor=BLACK,
                 textSize=46):

        self.position = position
        self.x, self.y = self.position

        self.size = size
        self.width, self.height = self.size

        self.color = color
        self.textColor = textColor

        self.textSize = textSize

        self.label = label
        self.textFont = pygame.font.SysFont('Comic Sans MS', self.textSize)

        self.text = self.textFont.render(self.label, True, self.textColor,
                                         self.color)

        self.textRect = self.text.get_rect()
        self.textRect.center = (self.x + self.width // 2,
                                self.y + self.height // 2)

   
    def mouseOverButton(self, mouseX, mouseY):
        if self.x + self.width > mouseX > self.x and self.y + self.height > mouseY > self.y:
            return True
        return False

    def show(self):
        SCREEN.blit(self.text, self.textRect)


class Map:
    def __init__(self):
        self.blocks = {}
        self.blockSize = 0

        # map variables
        self.rows = None
        self.columns = None

    def createMap(self, rows, columns):
        self.blockSize = (WIDTH - (WIDTH // 4)) // rows

        self.rows = rows
        self.columns = columns

        x, y = 0, 0

        for i in range(self.rows):
            for j in range(self.columns):
                node = Node((x, y))
                self.blocks[(j, i)] = node
                x += 1
            y += 1
            x = 0

        return self.blocks

    def clearPath(self):
        for node in self.blocks:
            if self.blocks[node].color == PATH_COLOR or self.blocks[
                    node].color == SEARCH_COLOR or self.blocks[
                        node].color == NEIGHBOUR_COLOR:
                self.blocks[node].color = DEFAULT_COLOR

    def show(self):
        SCREEN.fill(BACKGROUND_COLOR)

        for node in self.blocks:
            pygame.draw.rect(SCREEN, self.blocks[node].color,
                             self.blocks[node].rect)
        StartButton.show()
        pygame.display.update()


def createWallsClick():

    while True:
        Map.show()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                for position in Map.blocks:
                    node = Map.blocks[position]
                    if x > node.x and x < node.x + Map.blockSize and y > node.y and y < node.y + Map.blockSize:

                        if node.color == WALL_COLOR:
                            Map.blocks[node.
                                       blockPosition].color = DEFAULT_COLOR
                            Map.show()

                        elif node.color == DEFAULT_COLOR:
                            Map.blocks[node.blockPosition].color = WALL_COLOR
                            Map.show()

                        elif node.color == START_COLOR:
                            Map.blocks[node.
                                       blockPosition].color = DEFAULT_COLOR
                            getStart()

                        elif node.color == END_COLOR:
                            Map.blocks[node.
                                       blockPosition].color = DEFAULT_COLOR
                            getEnd()

                x, y = pygame.mouse.get_pos()
                if StartButton.mouseOverButton(x, y):
                    return


def getStart():
    global startNode

    while True:
        Map.show()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                for position in Map.blocks:
                    node = Map.blocks[position]
                    if x > node.x and x < node.x + Map.blockSize and y > node.y and y < node.y + Map.blockSize and node.color != END_COLOR and node.color != WALL_COLOR:

                        Map.blocks[node.blockPosition].color = START_COLOR
                        Map.show()

                        startNode = Map.blocks[node.blockPosition]
                        return Map.blocks[node.blockPosition]
def getEnd():
    global endNode

    while True:
        Map.show()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                for position in Map.blocks:
                    node = Map.blocks[position]
                    if x > node.x and x < node.x + Map.blockSize and y > node.y and y < node.y + Map.blockSize and node.color != START_COLOR and node.color != WALL_COLOR:

                        Map.blocks[position].color = END_COLOR
                        Map.show()

                        endNode = Map.blocks[position]
                        return Map.blocks[position]


def getNeighbours(nodePosition):
    x, y = nodePosition
    neighbours = []

    if x + 1 < Map.rows:
        neighbours.append((x + 1, y))

    if x - 1 >= 0:
        neighbours.append((x - 1, y))

    if y + 1 < Map.columns:
        neighbours.append((x, y + 1))

    if y - 1 >= 0:
        neighbours.append((x, y - 1))
    return neighbours


def getPath(startNode, endNode):
    startNode.currentState = 0

    openList = [startNode]
    closedList = []

    currentIndex = 0

    while openList:
        clock.tick(60)

        x, y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and StartButton.mouseOverButton(x, y):
                return

        pygame.time.delay(100)

        currentNode = openList.pop(currentIndex)

        print("position: ", currentNode.blockPosition, " index position: ",
              currentIndex)
        print(f"f: {currentNode.f} g: {currentNode.g} h: {currentNode.h} \n")

        if Map.blocks[currentNode.
                      blockPosition].color != START_COLOR and Map.blocks[
                          currentNode.blockPosition].color != END_COLOR:

            Map.blocks[currentNode.blockPosition].color = SEARCH_COLOR
            closedList.append(currentNode.blockPosition)

        Map.show()

        if currentNode.blockPosition == endNode.blockPosition:
            path = []
            while currentNode.color != START_COLOR:

                path.append(currentNode.blockPosition)
                currentNode = currentNode.parent

            path.append(startNode.blockPosition)

            path = path[::-1]
            tempPath = path
            searchNodes = []

            for position in Map.blocks:
                node = Map.blocks[position]

                if Map.blocks[position].color == SEARCH_COLOR or Map.blocks[
                        position].color == NEIGHBOUR_COLOR:
                    searchNodes.append(position)

            i = 0
            for position in searchNodes:
                if Map.blocks[position].color != PATH_COLOR and Map.blocks[position].color != START_COLOR:
                    Map.blocks[position].color = DEFAULT_COLOR

                i += 1
                Map.show()
                pygame.time.delay(50)

                if i == (len(searchNodes) // len(tempPath)) - 1:
                    Map.blocks[tempPath.pop(1)].color = PATH_COLOR
                    Map.show()
                    pygame.time.delay(100)

                    i = 0
                    
            for position in tempPath:
                if Map.blocks[position].color != START_COLOR and Map.blocks[position].color != END_COLOR:
                    Map.blocks[position].color = PATH_COLOR
                    Map.show()
                    pygame.time.delay(50)


            while True:
                x, y = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and StartButton.mouseOverButton(x, y):

                        return path

        for position in getNeighbours(currentNode.blockPosition):
            node = Map.blocks[position]

            if node.blockPosition not in closedList and node not in openList and node.color != WALL_COLOR:

                node.parent = currentNode
                node.currentState = currentNode.currentState + 1
                node.calculate_cost()

                print("neighbour position: ", node.blockPosition)
                print(f"f: {node.f} g: {node.g} h: {node.h}")
                print()

                if Map.blocks[position].color != START_COLOR and Map.blocks[
                        position].color != END_COLOR:
                    node.color = NEIGHBOUR_COLOR

                pygame.time.delay(100)
                Map.blocks[position] = node

                openList.append(node)

        if openList:
            currentIndex = 0
            currentNode = openList[currentIndex]

            for index, node in enumerate(openList):

                currentNode.calculate_cost()
                node.calculate_cost()

                if node.f < currentNode.f:

                    currentIndex = index
                    currentNode = node

                elif node.f == currentNode.f and node.h < currentNode.h:

                    currentIndex = index
                    currentNode = node
        else:
            break


WIDTH = 750

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, WIDTH - WIDTH // 4))

Map = Map()
Map.createMap(10, 10)

StartButton = Button((WIDTH - (WIDTH // 5), WIDTH // 16),
                     (Map.blockSize * 2, Map.blockSize), "START")

clock = pygame.time.Clock()

startNode = getStart()
endNode = getEnd()

while True:
    createWallsClick()

    getPath(startNode, endNode)
    Map.clearPath()
