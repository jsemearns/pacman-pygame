from random import randint

WIDTH = 10
HEIGHT = 10
START_X = 0
START_Y = 0
COLORS = [['GREEN', 1], ['BLUE', 2], ['YELLOW', 3]]


class Coordinate():
    xPos = 0
    yPos = 0
    entity = None

    def __init__(self, xpos, ypos, entity=None):
        self.xPos = xpos
        self.yPos = ypos
        self.entity = entity


class PacMan():
    coordinate = None
    direction = 'right'
    points = 0

    def __init__(self, coordinate):
        self.coordinate = coordinate
        self.coordinate.entity = self

    def moveTo(self, coordinate):
        if isinstance(coordinate.entity, Wall):
            print("WALL! Cannot move.")
        else:
            if isinstance(coordinate.entity, Coin):
                self.points = self.points + coordinate.entity.getAmount()
                print("POINTS: {}".format(self.points))

            # Update pacman's coordinates
            self.coordinate.entity = None
            self.coordinate = coordinate
            self.coordinate.entity = self

        displayBoard()
        print("")


class Wall():
    name = 'wall'
    coordinate = None

    def __init__(self, coordinate):
        self.coordinate = coordinate
        self.coordinate.entity = self


class Coin():
    name = 'coin'
    color = 0
    coordinate = None

    def __init__(self, color, coordinate):
        self.color = color
        self.coordinate = coordinate
        self.coordinate.entity = self

    def getAmount(self):
        return COLORS[self.color][1]


BOARD = [[Coordinate(x, y) for y in range(WIDTH)] for x in range(HEIGHT)]
PACMAN = PacMan(BOARD[START_X][START_Y])


def setWall(x, y):
    """ Create a wall in a coordinate. """
    Wall(BOARD[x][y])


def setCoin(color, x, y):
    """ Create a coin in a coordinate. """
    Coin(color, BOARD[x][y])


def displayBoard():
    print("POINTS: {}".format(PACMAN.points))
    for y in range(HEIGHT):
        row_str = ""
        print("*************************************************************")
        for x in range(WIDTH):
            if isinstance(BOARD[x][y].entity, PacMan):
                row_str += "  X  |"
            elif isinstance(BOARD[x][y].entity, Wall):
                row_str += "||||||"
            elif isinstance(BOARD[x][y].entity, Coin):
                row_str += "  {}  |".format(BOARD[x][y].entity.getAmount())

                if BOARD[x][y].entity.getAmount() < 0:
                    # For display purposes only.
                    row_str = row_str[:-2] + "|"
            else:
                # row_str += " {},{} |".format(x, y)
                row_str += "     |"
        print("|" + row_str)
    print("*************************************************************")


def setColorValue():
    """ Generate random values between -9 to 9 for the 3 colors. """
    COLORS[0][1] = randint(-9, 9)
    COLORS[1][1] = randint(-9, 9)
    COLORS[2][1] = randint(-9, 9)
    return (COLORS[0][1], COLORS[1][1], COLORS[2][1])

def createCoins():
    """ Assign coins to coordinates with random COLORS. """
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if BOARD[x][y].entity is None:
                setCoin(randint(0, 2), BOARD[x][y].xPos, BOARD[x][y].yPos)


def createBoard():
    """ Create the walls and coins for the board. """
    setWall(1, 1)
    setWall(1, 2)
    setWall(1, 3)
    setWall(1, 4)
    setWall(1, 8)
    setWall(1, 7)
    setWall(1, 6)
    setWall(3, 8)
    setWall(2, 8)
    setWall(3, 6)
    setWall(3, 5)
    setWall(3, 3)
    setWall(4, 3)
    setWall(5, 3)
    setWall(3, 0)
    setWall(3, 1)
    setWall(5, 2)
    setWall(5, 1)
    setWall(7, 1)
    setWall(7, 2)
    setWall(7, 3)
    setWall(9, 0)
    setWall(9, 1)
    setWall(9, 2)
    setWall(9, 3)
    setWall(9, 4)
    setWall(9, 5)
    setWall(8, 5)
    setWall(8, 7)
    setWall(9, 7)
    setWall(9, 8)
    setWall(9, 9)
    setWall(8, 9)
    setWall(7, 9)
    setWall(6, 9)
    setWall(5, 9)
    setWall(5, 5)
    setWall(5, 6)
    setWall(5, 7)
    setWall(6, 5)
    setWall(6, 7)

    # Assign coins to EMPTY coordinates in the board.
    createCoins()
    displayBoard()

# CREATE BOARD NOW!
createBoard()


def loop():
    """ Function that continues the movement depending on direciton. """
    next_x = PACMAN.coordinate.xPos
    if next_x + 1 > WIDTH:
        next_x -= 1

    next_y = PACMAN.coordinate.yPos
    if next_y + 1 > HEIGHT:
        next_y -= 1

    try:
        if PACMAN.direction == 'right':
            PACMAN.moveTo(BOARD[next_x + 1][next_y])
        elif PACMAN.direction == 'left':
            PACMAN.moveTo(BOARD[next_x - 1][next_y])
        elif PACMAN.direction == 'up':
            PACMAN.moveTo(BOARD[next_x][next_y - 1])
        elif PACMAN.direction == 'down':
            PACMAN.moveTo(BOARD[next_x][next_y + 1])
    except IndexError:
        if PACMAN.direction == 'right':
            if isinstance(BOARD[0][next_y].entity, Wall):
                PACMAN.moveTo(BOARD[next_x][next_y])
            else:
                PACMAN.moveTo(BOARD[0][next_y])
        if PACMAN.direction == 'left':
            if isinstance(BOARD[WIDTH-1][next_y].entity, Wall):
                PACMAN.moveTo(BOARD[next_x][next_y])
            else:
                PACMAN.moveTo(BOARD[WIDTH-1][next_y])
        if PACMAN.direction == 'up':
            if isinstance(BOARD[next_x][HEIGHT-1].entity, Wall):
                PACMAN.moveTo(BOARD[next_x][next_y])
            else:
                PACMAN.moveTo(BOARD[next_x][HEIGHT-1])
        if PACMAN.direction == 'down':
            if isinstance(BOARD[next_x][0].entity, Wall):
                PACMAN.moveTo(BOARD[next_x][next_y])
            else:
                PACMAN.moveTo(BOARD[next_x][0])