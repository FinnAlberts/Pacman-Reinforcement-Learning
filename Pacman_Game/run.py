import pygame
from pygame.locals import *
from Pacman_Game.constants import *
from Pacman_Game.pacman import Pacman
from Pacman_Game.nodes import NodeGroup
from Pacman_Game.pellets import PelletGroup
from Pacman_Game.ghosts import GhostGroup
from Pacman_Game.fruit import Fruit
from Pacman_Game.pauser import Pause
from Pacman_Game.text import TextGroup
from Pacman_Game.sprites import LifeSprites
from Pacman_Game.sprites import MazeSprites
from Pacman_Game.mazedata import MazeData
from Pacman_Game.vector import Vector2

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.background_norm = None
        self.background_flash = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.fruitCaptured = []
        self.fruitNode = None
        self.mazedata = MazeData()

    def setBackground(self):
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)
        self.background_norm = self.mazesprites.constructBackground(self.background_norm, self.level%5)
        self.background_flash = self.mazesprites.constructBackground(self.background_flash, 5)
        self.flashBG = False
        self.background = self.background_norm

    def startGame(self):      
        self.mazedata.loadMaze(self.level)
        self.mazesprites = MazeSprites("Pacman_Game/"+self.mazedata.obj.name+".txt", "Pacman_Game/"+self.mazedata.obj.name+"_rotation.txt")
        self.setBackground()
        self.nodes = NodeGroup("Pacman_Game/"+self.mazedata.obj.name+".txt")
        self.mazedata.obj.setPortalPairs(self.nodes)
        self.mazedata.obj.connectHomeNodes(self.nodes)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(*self.mazedata.obj.pacmanStart))
        self.pellets = PelletGroup("Pacman_Game/"+self.mazedata.obj.name+".txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)

        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(0, 3)))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(4, 3)))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        # RLD - Update blinky start position to same position as pinky
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))

        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)

        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.mazedata.obj.denyGhostsAccess(self.ghosts, self.nodes)

    def startGame_old(self):      
        self.mazedata.loadMaze(self.level)#######
        self.mazesprites = MazeSprites("Pacman_Game/maze1.txt", "maze1_rotation.txt")
        self.setBackground()
        self.nodes = NodeGroup("Pacman_Game/maze1.txt")
        self.nodes.setPortalPair((0,17), (27,17))
        homekey = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26))
        self.pellets = PelletGroup("Pacman_Game/maze1.txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 0+14))
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(0+11.5, 3+14))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(4+11.5, 3+14))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))

        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.nodes.denyAccessList(2+11.5, 3+14, LEFT, self.ghosts)
        self.nodes.denyAccessList(2+11.5, 3+14, RIGHT, self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.nodes.denyAccessList(12, 14, UP, self.ghosts)
        self.nodes.denyAccessList(15, 14, UP, self.ghosts)
        self.nodes.denyAccessList(12, 26, UP, self.ghosts)
        self.nodes.denyAccessList(15, 26, UP, self.ghosts)

    def update(self):
        dt = self.clock.tick(250) / 100.0    # RLD - Increased speed
        self.textgroup.update(dt)
        self.pellets.update(dt)
        if not self.pause.paused:
            self.ghosts.update(dt)      
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()

        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)
        else:
            self.pacman.update(dt)

        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.textgroup.hideText()
                            self.showEntities()
                        else:
                            self.textgroup.showText(PAUSETXT)
                            #self.hideEntities()

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            # RLD - Disable inky and clyde
            # if self.pellets.numEaten == 30:
            #     self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
            # if self.pellets.numEaten == 70:
            #     self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.startFreight()
            if self.pellets.isEmpty():
                self.flashBG = True
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.updateScore(ghost.points)                  
                    self.textgroup.addText(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    ghost.startSpawn()
                    self.nodes.allowHomeAccess(ghost)
                elif ghost.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -=  1
                        self.lifesprites.removeImage()
                        self.pacman.die()               
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.textgroup.showText(GAMEOVERTXT)
                            self.pause.setPause(pauseTime=3, func=self.restartGame)
                        else:
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)
    
    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20), self.level)
                #print(self.fruit) # RLD - Disable logging of fruits
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)
                fruitCaptured = False
                for fruit in self.fruitCaptured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruitCaptured = True
                        break
                if not fruitCaptured:
                    self.fruitCaptured.append(self.fruit.image)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.textgroup.updateLevel(self.level)

    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)
        self.lifesprites.resetLives(self.lives)
        self.fruitCaptured = []

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.showText(READYTXT)

    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        #self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)

        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))

        for i in range(len(self.fruitCaptured)):
            x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i+1)
            y = SCREENHEIGHT - self.fruitCaptured[i].get_height()
            self.screen.blit(self.fruitCaptured[i], (x, y))

        pygame.display.update()

    # RLD - Function for receiving gamestate
    def receive_gamestate(self):
        gamestate = {}
        gamestate["lives"] = self.lives
        gamestate["is_alive"] = self.pacman.alive
        gamestate["score"] = self.score
        gamestate["level"] = self.level
        gamestate["map"] = self.get_map()
        gamestate["min_ghost_distance"] = self.find_closest_ghost_distance()

        return gamestate

    # RLD - Get the distance to the closest ghost
    def find_closest_ghost_distance(self):
        distances = []
        distances.append((abs(self.ghosts.blinky.position.x - self.pacman.position.x)**2 + abs(self.ghosts.blinky.position.y - self.pacman.position.y)**2)**0.5)
        distances.append((abs(self.ghosts.pinky.position.x - self.pacman.position.x)**2 + abs(self.ghosts.blinky.position.y - self.pacman.position.y)**2)**0.5)
        
        # Clyde releases after 30 pellets have been eaten
        if self.pellets.numEaten >= 30:
            distances.append((abs(self.ghosts.clyde.position.x - self.pacman.position.x)**2 + abs(self.ghosts.blinky.position.y - self.pacman.position.y)**2)**0.5)

        # Inky releases after 70 pellets have been eaten
        if self.pellets.numEaten >= 70:
            distances.append((abs(self.ghosts.inky.position.x - self.pacman.position.x)**2 + abs(self.ghosts.blinky.position.y - self.pacman.position.y)**2)**0.5)

        # Divide closest distance by 16 (= width of a tile)
        return min(distances) / 16

    # RLD - Function for reading map
    def get_map(self):
        # Fill map with walls
        pacman_map = self.get_map_walls()

        # Set Pacman in map
        pacman_map[int(self.pacman.position.y / TILEHEIGHT) - 3][int(self.pacman.position.x / TILEWIDTH)] = 2

        # Insert pellets and powerpellets
        pellets = self.pellets.pelletList.copy()

        for pellet in pellets:
            if pellet.name == PELLET:
                pacman_map[int(pellet.position.y / TILEHEIGHT) - 3][int(pellet.position.x / TILEWIDTH)] = 3
            elif pellet.name == POWERPELLET:
                pacman_map[int(pellet.position.y / TILEHEIGHT) - 3][int(pellet.position.x / TILEWIDTH)] = 3

        # Add fruits
        if self.fruit != None:
            fruit_position = self.fruit.node.position.copy()
            pacman_map[int(fruit_position.y / TILEHEIGHT) - 3][int(fruit_position.x / TILEWIDTH)] = 3

        # Add ghosts
        pacman_map[int(self.ghosts.blinky.position.y / 16) - 3][int(self.ghosts.blinky.position.x / 16)] = 4
        pacman_map[int(self.ghosts.pinky.position.y / 16) - 3][int(self.ghosts.pinky.position.x / 16)] = 4
        pacman_map[int(self.ghosts.clyde.position.y / 16) - 3][int(self.ghosts.clyde.position.x / 16)] = 4
        pacman_map[int(self.ghosts.inky.position.y / 16) - 3][int(self.ghosts.inky.position.x / 16)] = 4

        # Return map
        return pacman_map

    
    # RLD - Function for reading map file and receiving walls
    def get_map_walls(self):
        # Define what is a wall in the maze file
        wall_map = []
        wall = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "X", "="]

        # Read the file
        maze_file = open("Pacman_Game/maze1.txt", "r")

        line_number = 0
        for line in maze_file:
            line_number += 1
            if line_number >= 4 and line_number <= 34:
                map_line = []

                line = line.replace(" ", "")
                for node in line:
                    if node == "\n":
                        break
                    if node in wall:
                        map_line.append(1)
                    else:
                        map_line.append(0)
                wall_map.append(map_line)
        
        # Return map
        return wall_map

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()



