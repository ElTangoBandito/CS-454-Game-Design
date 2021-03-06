from math import sin, cos
import sys
import time
from direct.showbase.ShowBase import ShowBase

from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState

from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import PointLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import BitMask32
from panda3d.core import NodePath
from panda3d.core import PandaNode
from panda3d.core import TextNode
from panda3d.core import Material

from pandac.PandaModules import *

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletHelper
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import BulletHeightfieldShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletSoftBodyNode
from panda3d.bullet import BulletSoftBodyConfig
from panda3d.bullet import ZUp

from direct.gui.DirectGui import DirectCheckButton
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectFrame
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText

from math import pi, sin, cos
from Box import *
import random

class CharacterController(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)
        #self.stage3Light = False
        self.loadSounds()
        self.tasteTheRainbow = False
        self.showMenu()
        '''
        self.setupLights()
        # Input
        self.accept('escape', self.doExit)
        #self.accept('r', self.doReset)
        self.accept('f3', self.toggleDebug)
        self.accept('space', self.doJump)

        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('turnLeft', 'a')
        inputState.watchWithModifiers('turnRight', 'd')
        inputState.watchWithModifiers('cameraUp', 'arrow_up')
        inputState.watchWithModifiers('cameraDown', 'arrow_down')
        inputState.watchWithModifiers('cameraRight', 'arrow_right')
        inputState.watchWithModifiers('cameraLeft', 'arrow_left')
        inputState.watchWithModifiers('zoomOut', 'q')
        inputState.watchWithModifiers('zoomIn', 'e')
        inputState.watchWithModifiers('dash', 'shift')
        inputState.watchWithModifiers('dashJump', 'space')
        inputState.watchWithModifiers('autoCameraOn', 'p')
        inputState.watchWithModifiers('autoCameraOff', 'o')
        inputState.watchWithModifiers('helpHud', 'f1')
        inputState.watchWithModifiers('closeHelpHud', 'f2')
        inputState.watchWithModifiers('respawn', 'f8')

        #Stages
        self.stage1 = []
        #Objectives
        self.stage1Objective = {}

        # Task
        taskMgr.add(self.update, 'updateWorld')

        # time objectives
        self.timeObjectivesState = {
            "stage1objective1": False,
            "stage1objective2": False,
            "stage1objective3": False,
            "objectiveCleared": False,
            "objectiveSet": False,
            "objective2Set": False
        }

        self.respawnZValue = -60
        self.towerExterminationProtocol = False
        self.towerExterminationCurrentPositionModifier = 0
        self.towerExterminationLavaStartingPos = Vec3(0,0,0)

        #bugfixing switches
        self.stageOneCleared = False
        self.startFromStageOne = True
        self.startFromStageTwo = False
        self.startFromStageThree = False

        self.setup()
        base.setBackgroundColor(0.1, 0.1, 0.1, 1)
        base.setFrameRateMeter(True)
        base.disableMouse()
        base.camera.lookAt(self.characterNP)
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)


        #ATM state
        #self.isMoving = False
        #self.isJumping = False
        self.isLanding = False
        self.isDashJumping = False
        #self.isRunningAndJumping = False
        #self.isRunningAndJumpingAndLanding = False
        #self.isLandedFromRun = False
        #animation switches
        self.gameOver = False
        self.animationRunning = False
        self.animationDashing = False
        self.animationIdle = False
        self.animationLanding = False
        self.landingAnimation = False
        self.firstBalloonsAcquired = False
        #self.isDashing = False
        self.cdmax = 20
        self.cdmin = 10

        #keyOptions
        self.cameraAutoTurn = True

        # Player stats
        self.playerLives = 3
        self.playerScore = 0
        self.switchScoreToLife = False
        # self.playerHealth = 3
        #Pete's switches and other stuff
        #self.peteIsActive = False
        #self.peteIdentifer = 0
        #self.peteTaskAssigned = False
        self.peteState = {
            "isWalking" : False,
            "isJumping" : False
        }
        self.peteInteractions = {
            "firstTask-SFXUnknown" : False,
            "firstDialogue-Stage1" : False,
            "secondDialogue-Stage1" : False,
            "thirdDialogue-Stage1" : False,
            "fourthDialogue-stage1" : False,
            "doorDestroyed" : False,
            "bookIt" : False,
            "grandPillarSpawn" : False,
            "stage1Cleared" : False,
            "transitionDialogue1" : False,
            "transitionDoubleSwitchBegniWalk" : False,
            "transitionDoubleSwitchDoorUnlocked" : False,
            "transitionWalkingToEdge" : False,
            "onInvisiblePlatform" : False,
            "havePeteJumpInPlace" : False,
            "finishedTransitionWalk" : False,
            "stage2-third-dialogue" : False,
            "stage2-commanding-section-complete" : False
        }
        self.peteInteractionsDialogueSwitches = {
            "switch1" : False,
            "switch2" : False,
            "switch3" : False,
            "switch4" : False,
            "switch5" : False
        }

        self.peteInvisibleGuideSwitches = {
            "switch1": False,
            "switch2": False,
            "switch3": False,
            "switch4": False,
            "switch5": False,
            "switch6": False,
            "switch7": False,
            "switch8": False
        }
        self.peteCommandsSwitches = {
            "commandsEnabled" : False,
            "go" : False,
            "stop" : False,
            "going" : False
        }
        self.peteFirstTaskUnknownSFX = False
        self.peteRespawnPos = Vec3(0,0,0)

        #checkpoint
        self.respawnPoint = Vec3(self.characterNP.getX(), self.characterNP.getY(), self.characterNP.getZ())
        self.respawning = False
        self.checkPointDict = {
            "stage1-checkpoint-1" : False,
            "stage1-checkpoint-2" : False,
            "stage1-checkpoint-3" : False,
            "stage1-checkpoint-4" : False,
            "transition-checkpoint" : False,
            "stage2-checkpoint-1" : False,
            "stage2-checkpoint-2" : False,
            "stage2-checkpoint-3": False,
            "stage3-checkpoint-1" : False,
            "stage3-checkpoint-2": False,
            "stage3-checkpoint-3": False,
            "stage3-checkpoint-4": False,
            "stage3-checkpoint-5": False,
            "stage3-checkpoint-6": False
        }

        #On Screen Texts
        self.helpHudOn = False
        self.HUDTexts = []
        self.helpTexts = []
        self.textMessage = OnscreenText(text="", style=1, fg=(1,1,1,1), bg=(0.7, 0.4, 0.1, 1), pos=(0,-0.7), align = TextNode.ACenter, scale = 0.06)
        self.textMessage2 = OnscreenText(text="", style=1, fg=(1, 1, 1, 1), bg=(0.7, 0.4, 0.1, 1), pos=(0, -0.8), align=TextNode.ACenter, scale=0.06)
        self.textTimeAlert = OnscreenText(text="", style=1, fg=(1, 1, 1, 1), pos=(0.0, 0.80), align=TextNode.ACenter, scale=0.12)
        #textObject = OnscreenText(text='my text string', style = 1, fg=(1,1,0,1), pos=(-1.3, 0.95), align=TextNode.ALeft, scale=0.07)
        #textObject.destroy()
        self.displayHUD()

        taskMgr.add(self.playerStatsWatcher, "playerStatsMonitor")
        self.ATMPosX = self.characterNP.getX()
        self.ATMPosY = self.characterNP.getY()
        self.ATMPosZ = self.characterNP.getZ()
        self.ATMPos = "(" + str(self.ATMPosX) + ", " + str(self.ATMPosY) + ", " + str(self.ATMPosZ) + ")"
        self.ATMPoisitionMonitorText = OnscreenText(text=self.ATMPos, style = 1, fg=(1,1,1,1), pos = (1.3,-0.95), align=TextNode.A_right, scale = 0.08)
        taskMgr.add(self.ATMPositionMonitor, "playerPositionMonitor")


        #self.HUDTexts[1].setText("test")
        '''

    def startUp(self, stage=""):
        self.setupLights()
        # Input
        #self.accept('escape', self.doExit)
        # self.accept('r', self.doReset)
        #self.accept('f3', self.toggleDebug)
        #self.accept('space', self.doJump)

        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('turnLeft', 'a')
        inputState.watchWithModifiers('turnRight', 'd')
        inputState.watchWithModifiers('cameraUp', 'arrow_up')
        inputState.watchWithModifiers('cameraDown', 'arrow_down')
        inputState.watchWithModifiers('cameraRight', 'arrow_right')
        inputState.watchWithModifiers('cameraLeft', 'arrow_left')
        inputState.watchWithModifiers('zoomOut', 'q')
        inputState.watchWithModifiers('zoomIn', 'e')
        inputState.watchWithModifiers('dash', 'shift')
        inputState.watchWithModifiers('dashJump', 'space')
        inputState.watchWithModifiers('autoCameraOn', 'p')
        inputState.watchWithModifiers('autoCameraOff', 'o')
        inputState.watchWithModifiers('helpHud', 'f1')
        inputState.watchWithModifiers('closeHelpHud', 'f2')
        inputState.watchWithModifiers('respawn', 'f8')

        # Stages
        self.stage1 = []
        # Objectives
        self.stage1Objective = {}

        # Task
        taskMgr.add(self.update, 'updateWorld')

        # time objectives
        self.timeObjectivesState = {
            "stage1objective1": False,
            "stage1objective2": False,
            "stage1objective3": False,
            "objectiveCleared": False,
            "objectiveSet": False,
            "objective2Set": False
        }

        self.respawnZValue = -60
        self.towerExterminationProtocol = False
        self.towerExterminationCurrentPositionModifier = 0
        self.towerExterminationLavaStartingPos = Vec3(0, 0, 0)

        # bugfixing switches
        self.stageOneCleared = False
        self.startFromStageOne = True
        self.startFromStageTwo = False
        self.startFromStageThree = False
        if stage == "stage2":
            self.startFromStageTwo = True
            self.startFromStageOne = False
        elif stage == "stage3":
            self.startFromStageThree = True
            self.startFromStageOne = False


        self.setup()
        base.setBackgroundColor(0.1, 0.1, 0.1, 1)
        base.setFrameRateMeter(True)
        base.disableMouse()
        base.camera.lookAt(self.characterNP)
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

        # ATM state
        # self.isMoving = False
        # self.isJumping = False
        self.isLanding = False
        self.isDashJumping = False
        # self.isRunningAndJumping = False
        # self.isRunningAndJumpingAndLanding = False
        # self.isLandedFromRun = False
        # animation switches
        self.gameOver = False
        self.animationRunning = False
        self.animationDashing = False
        self.animationIdle = False
        self.animationLanding = False
        self.landingAnimation = False
        self.firstBalloonsAcquired = False
        # self.isDashing = False
        self.cdmax = 20
        self.cdmin = 10

        # keyOptions
        self.cameraAutoTurn = True

        # Player stats
        self.playerLives = 3
        self.playerScore = 0
        self.switchScoreToLife = False
        # self.playerHealth = 3
        # Pete's switches and other stuff
        # self.peteIsActive = False
        # self.peteIdentifer = 0
        # self.peteTaskAssigned = False
        self.peteState = {
            "isWalking": False,
            "isJumping": False
        }
        self.peteInteractions = {
            "firstTask-SFXUnknown": False,
            "firstDialogue-Stage1": False,
            "secondDialogue-Stage1": False,
            "thirdDialogue-Stage1": False,
            "fourthDialogue-stage1": False,
            "doorDestroyed": False,
            "bookIt": False,
            "grandPillarSpawn": False,
            "stage1Cleared": False,
            "transitionDialogue1": False,
            "transitionDoubleSwitchBegniWalk": False,
            "transitionDoubleSwitchDoorUnlocked": False,
            "transitionWalkingToEdge": False,
            "onInvisiblePlatform": False,
            "havePeteJumpInPlace": False,
            "finishedTransitionWalk": False,
            "stage2-third-dialogue": False,
            "stage2-commanding-section-complete": False
        }
        self.peteInteractionsDialogueSwitches = {
            "switch1": False,
            "switch2": False,
            "switch3": False,
            "switch4": False,
            "switch5": False
        }

        self.peteInvisibleGuideSwitches = {
            "switch1": False,
            "switch2": False,
            "switch3": False,
            "switch4": False,
            "switch5": False,
            "switch6": False,
            "switch7": False,
            "switch8": False
        }
        self.peteCommandsSwitches = {
            "commandsEnabled": False,
            "go": False,
            "stop": False,
            "going": False
        }
        self.peteFirstTaskUnknownSFX = False
        self.peteRespawnPos = Vec3(0, 0, 0)

        # checkpoint
        self.respawnPoint = Vec3(self.characterNP.getX(), self.characterNP.getY(), self.characterNP.getZ())
        self.respawning = False
        self.checkPointDict = {
            "stage1-checkpoint-1": False,
            "stage1-checkpoint-2": False,
            "stage1-checkpoint-3": False,
            "stage1-checkpoint-4": False,
            "transition-checkpoint": False,
            "stage2-checkpoint-1": False,
            "stage2-checkpoint-2": False,
            "stage2-checkpoint-3": False,
            "stage3-checkpoint-1": False,
            "stage3-checkpoint-2": False,
            "stage3-checkpoint-3": False,
            "stage3-checkpoint-4": False,
            "stage3-checkpoint-5": False,
            "stage3-checkpoint-6": False
        }

        # On Screen Texts
        self.helpHudOn = False
        self.HUDTexts = []
        self.helpTexts = []
        self.textMessage = OnscreenText(text="", style=1, fg=(1, 1, 1, 1), bg=(0.7, 0.4, 0.1, 1), pos=(0, -0.7),
                                        align=TextNode.ACenter, scale=0.06)
        self.textMessage2 = OnscreenText(text="", style=1, fg=(1, 1, 1, 1), bg=(0.7, 0.4, 0.1, 1), pos=(0, -0.8),
                                         align=TextNode.ACenter, scale=0.06)
        self.textTimeAlert = OnscreenText(text="", style=1, fg=(1, 1, 1, 1), pos=(0.0, 0.80), align=TextNode.ACenter,
                                          scale=0.12)
        # textObject = OnscreenText(text='my text string', style = 1, fg=(1,1,0,1), pos=(-1.3, 0.95), align=TextNode.ALeft, scale=0.07)
        # textObject.destroy()
        self.displayHUD()

        taskMgr.add(self.playerStatsWatcher, "playerStatsMonitor")
        '''
        self.ATMPosX = self.characterNP.getX()
        self.ATMPosY = self.characterNP.getY()
        self.ATMPosZ = self.characterNP.getZ()
        self.ATMPos = "(" + str(self.ATMPosX) + ", " + str(self.ATMPosY) + ", " + str(self.ATMPosZ) + ")"
        self.ATMPoisitionMonitorText = OnscreenText(text=self.ATMPos, style=1, fg=(1, 1, 1, 1), pos=(1.3, -0.95),
                                                    align=TextNode.A_right, scale=0.08)
        taskMgr.add(self.ATMPositionMonitor, "playerPositionMonitor")
        '''

        # self.HUDTexts[1].setText("test")

    def showMenu(self):
        self.playMusic(self.MenuBGM, looping=1, volume=0.1)
        self.mainFrame = DirectFrame(frameColor = (0,0,0,1), frameSize = (-1, 1, -1, 1), pos=(0,0,0))
        self.subFrame = DirectFrame(parent = self.mainFrame, frameColor = (0,0,0,1), frameSize = (-1, 1, -1, 1), pos=(0,0,-0.2))
        tasteTheRainbowButton = DirectCheckButton(parent = self.mainFrame, text = "Taste the Rainbow", scale = 0.05, pos = (0.7,0,0.93), command = self.tasteTheRainbowCheck)
        titleImage = OnscreenImage(parent=self.mainFrame, image = 'Resources/Images/A Test of Metal.png', pos=(0,0,0.5), scale=(1, 0, 0.4))
        startButton = DirectButton(parent = self.subFrame, text="Start", pos=(0, 0, 0.1), scale = .1, command = self.gameStartButton, rolloverSound = self.SFXstapler, clickSound=self.SFXpling)
        stageSelectButton = DirectButton(parent=self.subFrame, text="Stage Select", pos=(0, 0, -0.1), scale=.1, command=self.stageSelectButton, rolloverSound = self.SFXstapler, clickSound=self.SFXpling)
        quitButton = DirectButton(parent=self.subFrame, text="Quit", rolloverSound = self.SFXstapler, pos=(0, 0, -0.3), scale=.1,
                                         command=self.doExit, clickSound=self.SFXpling)
        self.stageSelectFrame = DirectFrame(parent=self.mainFrame, frameColor=(0, 0, 0, 1), frameSize=(-1, 1, -1, 1),
                                            pos=(0, 0, -0.8))
        stage1Button = DirectButton(parent=self.stageSelectFrame, text="Stage1", text_scale=(0.5), text_pos=(0,1.2,0), text_fg=(0.8,0.1,0.1,1), image = "Resources/Images/stage1.jpg", pos=(-0.6, 0, 0.5), scale=.25,
                                   command=self.stage1Button, rolloverSound=self.SFXstapler,
                                   clickSound=self.SFXpling, relief=None)
        stage2Button = DirectButton(parent=self.stageSelectFrame, text="Stage2", text_scale=(0.5), text_pos=(0,1.2,0), text_fg=(1,1,1.1,1), image = "Resources/Images/stage2.jpg", pos=(0, 0, 0.5), scale=.25,
                                         command=self.stage2Button, rolloverSound=self.SFXstapler,
                                         clickSound=self.SFXpling, relief=None)
        stage3Button = DirectButton(parent=self.stageSelectFrame, text="Stage3", text_scale=(0.5), text_pos=(0,1.2,0), text_fg=(0,0,0.8,1), image = "Resources/Images/stage3.jpg", rolloverSound=self.SFXstapler, pos=(0.6, 0, 0.5),
                                  scale=.25,
                                  command=self.stage3Button, clickSound=self.SFXpling, relief=None)
        backButton = DirectButton(parent=self.stageSelectFrame, text="Back", rolloverSound=self.SFXstapler, pos=(0, 0, 0),
                                  scale=.1,
                                  command=self.backButton, clickSound=self.SFXpling)
        self.stageSelectFrame.hide()

    def tasteTheRainbowCheck(self, status):
        if(status):
            self.tasteTheRainbow = True
        else:
            self.tasteTheRainbow = False

    def gameStartButton(self, stage=""):
        self.startUp(stage = stage)
        self.mainFrame.hide()

    def stage1Button(self):
        self.gameStartButton(stage = "stage1")

    def stage2Button(self):
        self.gameStartButton(stage = "stage2")

    def stage3Button(self):
        self.gameStartButton(stage = "stage3")

    def backButton(self):
        self.stageSelectFrame.hide()
        self.subFrame.show()

    def stageSelectButton(self):
        self.subFrame.hide()
        self.stageSelectFrame.show()

    def generateStage(self, fileName):
        counter = 1
        with open(fileName) as inputFile:
            for line in inputFile:
                parameters = []
                for value in line.strip().split(','):
                    parameters.append(value.strip())
                x = float(parameters[0])
                y = float(parameters[1])
                z = float(parameters[2])
                px = float(parameters[3])
                py = float(parameters[4])
                pz = float(parameters[5])
                blockName = fileName.replace('.txt', "") + "-" + str(counter)
                counter = counter + 1
                box = Box(x,y,z,px,py,pz, blockName)
                model = parameters[6]
                if model == "invisible":
                    self.createInvisibleBox(box, collision = True)
                else:
                    self.createBox(box, model)

    def generateSlide(self, fileName):
        counter = 1
        with open(fileName) as inputFile:
            for line in inputFile:
                parameters = []
                for value in line.strip().split(','):
                    parameters.append(value.strip())
                x = float(parameters[0])
                y = float(parameters[1])
                z = float(parameters[2])
                px = float(parameters[3])
                py = float(parameters[4])
                pz = float(parameters[5])
                blockName = fileName.replace('.txt', "") + "-" + str(counter)
                counter = counter + 1
                box = Box(x, y, z, px, py, pz, blockName)
                model = parameters[6]
                angle = float(parameters[7])
                tilt = float(parameters[8])
                self.createSlide(box, angle, tilt, model)

    def generateBalls(self, fileName):
        counter = 1
        with open(fileName) as inputFile:
            for line in inputFile:
                parameters = []
                for value in line.strip().split(','):
                    parameters.append(value.strip())
                radius = float(parameters[0])
                x = float(parameters[1])
                y = float(parameters[2])
                z = float(parameters[3])
                name = fileName.replace('.txt', "") + "-" + str(counter)
                counter = counter + 1
                mass = 10
                self.addBall(radius, name, x, y, z, mass, respawn=True)

    def generateCoins(self, fileName):
        counter = 1
        with open(fileName) as inputFile:
            for line in inputFile:
                parameters = []
                for value in line.strip().split(','):
                    parameters.append(value.strip())
                x = float(parameters[0])
                y = float(parameters[1])
                z = float(parameters[2])
                type = ""
                if len(parameters) == 4:
                    type = parameters[3]
                coinName = fileName.replace('.txt', "") + "-" + str(counter)
                self.createCoin(Vec3(x,y,z),coinName, type = type)

    def generateHazard(self, fileName):
        counter = 1
        with open(fileName) as inputFile:
            for line in inputFile:
                parameters = []
                for value in line.strip().split(','):
                    parameters.append(value.strip())
                x = float(parameters[0])
                y = float(parameters[1])
                z = float(parameters[2])
                px = float(parameters[3])
                py = float(parameters[4])
                pz = float(parameters[5])
                blockName = fileName.replace('.txt', "") + "-" + str(counter)
                counter = counter + 1
                box = Box(x, y, z, px, py, pz, blockName)
                time = float(parameters[6])
                speed = float(parameters[7])
                direction = str(parameters[8])
                moving = "yes"
                if len(parameters) == 10:
                    moving = str(parameters[9])
                self.createHazardBox(box, 'lava', time, speed, direction, moving)
        # box = Box(2, 2, 2, 240, 335, 23, 'testingmoving')
        # self.createHazardBox(box, 'lava', 4, 0.02, 'x')

    def appendToStage(self, x, y, z, px, py, pz, name):
        box = Box(x, y, z, px, py, pz, name)
        self.stage1.append(box)

    def loadSounds(self):
        #BGM
        self.BGM1 = self.loadMusic("Resources/BGM/Bramble Blast.mp3")
        #self.BGM2 = self.loadMusic("Resources/BGM/Bramble Blast (Remix).mp3")
        self.BGM2 = self.loadMusic("Resources/BGM/Path of Goddess Claire.mp3")
        self.BGM3 = self.loadMusic("Resources/BGM/Another Medium.mp3")
        self.BGM4 = self.loadMusic("Resources/BGM/Flaming Bonds are Being Tested.mp3")
        self.MenuBGM = self.loadMusic("Resources/BGM/Streetwise.mp3")
        #self.playMusic(self.BGM1, looping=1, volume = 0.1)

        #sound effectt
        self.SFXjump = self.loadSfx("Resources/Sound/Jump.mp3")
        self.SFXdashjump = self.loadSfx("Resources/Sound/Dash Jump.mp3")
        self.SFXpop = self.loadSfx("Resources/Sound/Pop.mp3")
        self.SFXclick = self.loadSfx("Resources/Sound/Click.mp3")
        self.SFXlifeUp = self.loadSfx("Resources/Sound/Life Up.wav")
        self.SFXsniffShort = self.loadSfx("Resources/Sound/Sniff Short.mp3")
        self.SFXsniffLong = self.loadSfx("Resources/Sound/Sniff Long.mp3")
        self.SFXticktock = self.loadSfx("Resources/Sound/Tick Tock.wav")
        self.SFXcheckpoint = self.loadSfx("Resources/Sound/checkpoint.wav")
        self.SFXfootstep = self.loadSfx("Resources/Sound/footstep.wav")
        self.SFXburnt = self.loadSfx("Resources/Sound/burnt.mp3")
        self.SFXexterminate = self.loadSfx("Resources/Sound/exterminate.wav")
        self.SFXgameover = self.loadSfx("Resources/Sound/Game Over.mp3")
        self.SFXpling = self.loadSfx("Resources/Sound/Pling.mp3")
        self.SFXstapler = self.loadSfx("Resources/Sound/stapler.mp3")
        self.SFXlanding = self.loadSfx("Resources/Sound/Landing.mp3")
        self.SFXfootstep.setVolume(0.3)
        self.SFXjump.setVolume(0.05)
        self.SFXdashjump.setVolume(0.05)
        self.SFXcheckpoint.setVolume(0.3)
        self.SFXpling.setVolume(0.05)
        self.SFXstapler.setVolume(0.05)
        self.SFXlanding.setVolume(0.05)

        #voice
        self.SFXballoons = self.loadSfx("Resources/Voice/balloons.wav")
        self.SFXunknown = self.loadSfx("Resources/Voice/unknown.wav")
        self.SFXacknowledged = self.loadSfx("Resources/Voice/acknowledged.wav")
        self.SFXbattery = self.loadSfx("Resources/Voice/battery.wav")
        self.SFXniceToMeetYou = self.loadSfx("Resources/Voice/nice to meet you.wav")
        self.SFXintroduction = self.loadSfx("Resources/Voice/introduction.wav")
        self.SFXhello = self.loadSfx("Resources/Voice/hello.wav")
        self.SFXaffirmative = self.loadSfx("Resources/Voice/affirmative.wav")
        self.SFXbreathe = self.loadSfx("Resources/Voice/breathe.wav")
        self.SFXsensors = self.loadSfx("Resources/Voice/sensors.wav")
        self.SFXspeedOfLight = self.loadSfx("Resources/Voice/speedoflight.wav")
        self.SFXtestOfMetal = self.loadSfx("Resources/Voice/A Test of Metal.wav")
        self.SFXfall1 = self.loadSfx("Resources/Voice/fall respawn1.wav")
        self.SFXfall2 = self.loadSfx("Resources/Voice/fall respawn2.wav")
        self.SFXfall3 = self.loadSfx("Resources/Voice/fall respawn3.wav")
        self.SFXfall4 = self.loadSfx("Resources/Voice/fall respawn4.wav")
        self.SFXfall5 = self.loadSfx("Resources/Voice/fall respawn5.wav")
        self.SFXfall6 = self.loadSfx("Resources/Voice/fall respawn6.wav")
        self.SFXfallRespawnDict = {
            "1" : self.SFXfall1,
            "2" : self.SFXfall2,
            "3" : self.SFXfall3,
            "4" : self.SFXfall4,
            "5" : self.SFXfall5,
            "6" : self.SFXfall6
        }
        self.SFXgo1 = self.loadSfx("Resources/Voice/go1.wav")
        self.SFXgo2 = self.loadSfx("Resources/Voice/go2.wav")
        self.SFXgo3 = self.loadSfx("Resources/Voice/go3.wav")
        self.SFXgo4 = self.loadSfx("Resources/Voice/go4.wav")
        self.SFXgoDict = {
            "1": self.SFXgo1,
            "2": self.SFXgo2,
            "3": self.SFXgo3,
            "4": self.SFXgo4
        }
        self.SFXstop1 = self.loadSfx("Resources/Voice/stop1.wav")
        self.SFXstop2 = self.loadSfx("Resources/Voice/stop2.wav")
        self.SFXstop3 = self.loadSfx("Resources/Voice/stop3.wav")
        self.SFXstop4 = self.loadSfx("Resources/Voice/stop4.wav")
        self.SFXstopDict = {
            "1": self.SFXstop1,
            "2": self.SFXstop2,
            "3": self.SFXstop3,
            "4": self.SFXstop4
        }

    def ATMPositionMonitor(self, task):
        self.ATMPosX = self.characterNP.getX()
        self.ATMPosY = self.characterNP.getY()
        self.ATMPosZ = self.characterNP.getZ()
        self.ATMPos = "(" + str(self.ATMPosX) + ", " + str(self.ATMPosY) + ", " + str(self.ATMPosZ) + ")"
        self.ATMPoisitionMonitorText.setText(self.ATMPos)
        return task.cont

    def displayHelpHud(self):
        self.helpTexts.append(OnscreenText(text= "[W] : Move forward", style=1, fg=(1,1,1,1), pos=(-1.3,0.90), align = TextNode.ALeft, scale = 0.06))
        self.helpTexts.append(OnscreenText(text="[A] : Rotate left", style=1, fg=(1,1,1,1), pos=(-1.3,0.85), align = TextNode.ALeft, scale = 0.06))
        self.helpTexts.append(OnscreenText(text="[D] : Rotate Right", style=1, fg=(1,1,1,1), pos=(-1.3,0.80), align = TextNode.ALeft, scale = 0.06))
        self.helpTexts.append(OnscreenText(text="[S] : Move backward", style=1, fg=(1, 1, 1, 1), pos=(-1.3, 0.75), align=TextNode.ALeft, scale=0.06))
        self.helpTexts.append(
            OnscreenText(text="[Arrow Key Up] : Tilt Camera Down", style=1, fg=(1, 1, 1, 1), pos=(-1.3, 0.65), align=TextNode.ALeft,
                         scale=0.06))
        self.helpTexts.append(
            OnscreenText(text="[Arrow Key Down] : Tilt Camera Up", style=1, fg=(1, 1, 1, 1), pos=(-1.3, 0.60), align=TextNode.ALeft,
                         scale=0.06))
        self.helpTexts.append(
            OnscreenText(text="[Arrow Key Left] : Rotate Camera left", style=1, fg=(1, 1, 1, 1), pos=(-1.3, 0.55), align=TextNode.ALeft,
                         scale=0.06))
        self.helpTexts.append(
            OnscreenText(text="[Arrow Key Right] : Rotate Camera Right", style=1, fg=(1, 1, 1, 1), pos=(-1.3, 0.50), align=TextNode.ALeft,
                         scale=0.06))
        self.helpTexts.append(
            OnscreenText(text="[Q] : Camera Zoom Out", style=1, fg=(1, 1, 1, 1), pos=(-1.3, 0.45), align=TextNode.ALeft,
                         scale=0.06))
        self.helpTexts.append(
            OnscreenText(text="[E] : Camera Zoom In", style=1, fg=(1, 1, 1, 1), pos=(-1.3, 0.40), align=TextNode.ALeft,
                         scale=0.06))
        self.helpTexts.append(
            OnscreenText(text="[Shift] : Dash", style=1, fg=(1, 1, 1, 1), pos=(0, 0.90), align=TextNode.ACenter,
                         scale=0.06))
        self.helpTexts.append(
            OnscreenText(text="[Space] : Jump", style=1, fg=(1, 1, 1, 1), pos=(0, 0.85), align=TextNode.ACenter,
                         scale=0.06))
        self.helpTexts.append(
            OnscreenText(text="[P] : Auto Camera Turn - On", style=1, fg=(1, 1, 1, 1), pos=(-1.3, 0.35), align=TextNode.ALeft,
                         scale=0.06))
        self.helpTexts.append(
            OnscreenText(text="[O] : Auto Camera Turn - Off", style=1, fg=(1, 1, 1, 1), pos=(-1.3, 0.30), align=TextNode.ALeft,
                         scale=0.06))
        self.helpTexts.append(
            OnscreenText(text="[F1] : Toggle Help - On", style=1, fg=(1, 1, 1, 1), pos=(-1.3, 0.20),
                         align=TextNode.ALeft,
                         scale=0.06))
        self.helpTexts.append(
            OnscreenText(text="[F2] : Toggle Help - Off", style=1, fg=(1, 1, 1, 1), pos=(-1.3, 0.15),
                         align=TextNode.ALeft,
                         scale=0.06))
        self.helpTexts.append(
            OnscreenText(text="[G] : Command Pete - move (Available during stage 2)", style=1, fg=(1, 1, 1, 1), pos=(-1.3, 0.05),
                         align=TextNode.ALeft,
                         scale=0.06))
        self.helpTexts.append(
            OnscreenText(text="[H] : Command Pete - hold (Available during stage 2)", style=1, fg=(1, 1, 1, 1),
                         pos=(-1.3, 0.00),
                         align=TextNode.ALeft,
                         scale=0.06))
        self.helpTexts.append(
            OnscreenText(text="[F8] : Respawn at Checkpoint", style=1, fg=(1, 1, 1, 1), pos=(-1.3, 0.10),
                         align=TextNode.ALeft,
                         scale=0.06))

    def displayHUD(self):
        lifeMsg = "Batteries: " + str(self.playerLives)
        self.HUDTexts.append(OnscreenText(text=lifeMsg, style=1, fg=(1,1,0,1), pos=(-1.3,0.95), align = TextNode.ALeft, scale = 0.06))
        scoreMsg = "Score: " + str(self.playerScore)
        self.HUDTexts.append(OnscreenText(text=scoreMsg, style=1, fg=(1,1,0,1), pos=(0.0,0.95), align = TextNode.ACenter, scale = 0.06))
        #self.HUDTexts.append(textObject1)
        #self.HUDTexts.append((textObject2))

    def playerStatsWatcher(self, task):
        if self.playerScore is not 0 and self.playerScore % 10000 is 0 and self.switchScoreToLife is False:
            self.switchScoreToLife = True
            self.updateLife(1)
        elif self.playerScore % 10000 is not 0:
            self.switchScoreToLife = False
        return task.cont

    def updateScore(self, amount):
        if self.firstBalloonsAcquired is False:
            self.firstBalloonsAcquired = True
            self.playSfx(self.SFXballoons)
        self.playerScore += amount
        scoreMsg = "Score: " + str(self.playerScore)
        self.HUDTexts[1].setText(scoreMsg)

    def updateLife(self, amount):
        if amount > 0:
            self.playSfx(self.SFXlifeUp, volume = 0.1)
        self.playerLives += amount
        lifeMsg = "Batteries: " + str(self.playerLives)
        self.HUDTexts[0].setText(lifeMsg)

    def doExit(self):
        self.cleanup()
        sys.exit(1)

    def doReset(self):
        self.cleanup()
        self.setup()

    def toggleDebug(self):
        if self.debugNP.isHidden():
            self.debugNP.show()
        else:
            self.debugNP.hide()
    '''
    def doJump(self):
        self.isRunningAndJumpingAndLanding = False
        self.character.setMaxJumpHeight(6.0)
        self.character.setJumpSpeed(10.0)
        if self.character.isOnGround():
            self.playSfx(self.SFXjump)
            self.actorNP.play('jump')
        self.character.doJump()
        self.isJumping = True

    def doDashJump(self):
        self.character.setMaxJumpHeight(2.0)
        self.character.setJumpSpeed(10.0)
        if self.character.isOnGround():
            self.isDashJumping = True
            self.playSfx(self.SFXdashjump)
            self.actorNP.play('jump')
        self.character.doJump()
        self.isJumping = True
    '''
    def doJump(self):
        #self.character.setMaxJumpHeight(6.0)
        #self.character.setJumpSpeed(11.0)
        self.character.setMaxJumpHeight(20.0)
        self.character.setJumpSpeed(18.0)
        if self.character.isOnGround():
            self.SFXfootstep.stop()
            if self.isDashJumping:
                self.playSfx(self.SFXdashjump)
            else:
                self.playSfx(self.SFXjump)
            self.actorNP.play('jump')
            self.animationDashing = False
            self.animationRunning = False
            self.animationIdle = False
            #self.isLanding = True
        self.character.doJump()

    def doJumpPete(self):
        self.pete.setMaxJumpHeight(8.0)
        self.pete.setJumpSpeed(7.0)
        if self.pete.isOnGround():
            self.playSfx(self.SFXjump)
            # self.isLanding = True
        self.pete.doJump()

    def processInput(self, dt):
        speed = Vec3(0, 0, 0)
        omega = 0.0
        speedForce = 5.0

        '''
        if inputState.isSet('dash') and inputState.isSet('forward') and self.character.isOnGround():
            speed.setY(speedForce * 2)
            if self.isDashing is False:
                self.actorNP.setPlayRate(1.5, 'run')
                self.actorNP.loop('run')
                self.isDashing = True
        elif inputState.isSet('forward'):
            speed.setY(speedForce)
            self.isDashing = False
            self.actorNP.setPlayRate(1, 'run')
        if inputState.isSet('dash') and inputState.isSet('dashJump') and inputState.isSet('forward'):
            self.doDashJump()
            if inputState.isSet('dash') and inputState.isSet('forward') and self.isDashJumping:
                speed.setY(speedForce * 2)
                #self.isJumping = False
                self.isDashing = False
                self.isMoving = False
            elif self.isDashJumping is False:
                speed.setY(speedForce)
            #elif inputState.isSet('dash') and inputState.isSet('forward'):
        '''
        #idle
        if (inputState.isSet('forward') is False) and (inputState.isSet('reverse') is False) and self.character.isOnGround() and self.animationIdle is False and self.isLanding is False and self.actorNP.getCurrentAnim() != 'land':
            self.actorNP.loop('idle')
            self.SFXfootstep.stop()
            self.animationIdle = True
            self.animationRunning = False
            self.animationDashing = False
            self.landingAnimation = False
        if self.character.isOnGround() is False and self.isLanding is False:
            self.isLanding = True
        if self.character.isOnGround() and self.animationLanding is False and self.isLanding:
            self.animationLanding = True
            #taskMgr.add(self.landingAnimationTask, 'LandingAnimation')
            self.SFXfootstep.stop()

            self.actorNP.play('land')
            self.SFXlanding.play()
            self.landingAnimation = True
            self.animationIdle = False
            self.animationRunning = False
            self.animationDashing = False
        if self.actorNP.getCurrentAnim() != 'land' and self.character.isOnGround():
            self.isLanding = False
            self.animationLanding = False
        #dashing and running on ground
        if self.character.isOnGround() is False and self.actorNP.getCurrentAnim() != "land" and self.actorNP.getCurrentAnim() != "jump":
            self.actorNP.pose('land', 1)
            if self.SFXfootstep.status() == self.SFXfootstep.PLAYING:
                self.SFXfootstep.stop()
        if inputState.isSet('dashJump') and self.actorNP.getCurrentAnim() != 'land':
            self.doJump()
        if (inputState.isSet("forward") or inputState.isSet('reverse')):
            if inputState.isSet('dash'):
                if self.character.isOnGround():
                    speed.setY(speedForce * 2)
                if self.isLanding:
                    speed.setY(speedForce * 2)
                if self.animationDashing is False and self.character.isOnGround() and self.isLanding is False and self.actorNP.getCurrentAnim() != 'land':
                    self.SFXfootstep.setPlayRate(1.5)
                    self.playSfx(self.SFXfootstep, looping=1)
                    self.actorNP.setPlayRate(1.5, 'run')
                    self.actorNP.loop('run')
                    self.landingAnimation = False
                    self.animationDashing = True
                    self.animationRunning = False
                    self.animationIdle = False
                    self.isDashJumping = True
                if inputState.isSet('dashJump') and self.isDashJumping and self.actorNP.getCurrentAnim() != 'land':
                    speed.setY(speedForce * 2)
                    self.doJump()
            else:
                if inputState.isSet('dashJump') and self.actorNP.getCurrentAnim() != 'land':
                    self.doJump()
                self.isDashJumping = False
                speed.setY(speedForce)
                self.actorNP.setPlayRate(1, 'run')
                if self.animationRunning is False and self.character.isOnGround() and self.isLanding is False and self.actorNP.getCurrentAnim() != 'land':
                    self.actorNP.loop('run')
                    self.SFXfootstep.setPlayRate(1)
                    self.playSfx(self.SFXfootstep, looping=1)
                    self.landingAnimation = False
                    self.animationIdle = False
                    self.animationRunning = True
                    self.animationDashing = False

        #else: self.isDashJumping = False
        if inputState.isSet('reverse'): speed.setY(-speedForce/2)
        if inputState.isSet('left'):    speed.setX(-speedForce)
        if inputState.isSet('right'):   speed.setX(speedForce)
        if inputState.isSet('turnLeft'):  omega = 140.0
        if inputState.isSet('turnRight'): omega = -140.0


        #additional controls
        if self.gameOver is False:
            self.character.setAngularMovement(omega)
            self.character.setLinearMovement(speed, True)

        if inputState.isSet('autoCameraOn'): self.cameraAutoTurn = True
        if inputState.isSet('autoCameraOff'): self.cameraAutoTurn = False
        if inputState.isSet("helpHud") and self.helpHudOn is False:
            self.helpHudOn = True
            self.displayHelpHud()
        elif inputState.isSet("closeHelpHud") and self.helpHudOn:
            for text in self.helpTexts:
                text.destroy()
            self.helpTexts = []
            self.helpHudOn = False

        #manual respawn
        if inputState.isSet('respawn') and self.respawning is False and self.playerLives > 1:
            self.respawnATM()

    def respawnATM(self):
        self.respawning = True
        self.updateLife(-1)
        taskMgr.doMethodLater(3, self.checkPointRespawnTask, 'manual respawn')
        self.characterNP.setPos(self.respawnPoint)
        selector = random.randint(1, len(self.SFXfallRespawnDict))
        self.playSfx(self.SFXfallRespawnDict[str(selector)])
        if self.playerLives == 0:
            self.textGameOver = OnscreenText(text="GAME OVER", style=1, fg=(1, 0, 0, 1), pos=(0, 0),
                                             align=TextNode.ACenter, scale=0.5)
            self.gameOver = True
            self.SFXgameover.play()
            taskMgr.remove("updateWorld")
            #self.cleanup()
        if self.checkPointDict["stage2-checkpoint-1"] is False and self.peteInteractions["finishedTransitionWalk"]:
            self.peteResetInvisibleGuide()
        if self.peteCommandsSwitches["commandsEnabled"] and self.peteInteractions["stage2-commanding-section-complete"] is False:
            self.peteNP.setPos(self.peteRespawnPos)
            self.pete.setLinearMovement(Vec3(0, 0, 0), True)
        if self.towerExterminationProtocol:
            if self.checkPointDict["stage3-checkpoint-6"]:
                self.towerExterminationLavaStartingPos = Vec3(self.towerExterminationLavaStartingPos.x,
                                                              self.towerExterminationLavaStartingPos.y, -5)
            elif self.checkPointDict["stage3-checkpoint-5"]:
                self.towerExterminationLavaStartingPos = Vec3(self.towerExterminationLavaStartingPos.x, self.towerExterminationLavaStartingPos.y, -80)
            self.towerMovingHazardBoxNP.setPos(self.towerExterminationLavaStartingPos)
            self.towerExterminationCurrentPositionModifier = 0

    def update(self, task):
        dt = globalClock.getDt()
        self.processInput(dt)
        self.world.doPhysics(dt, 4, 1. / 240.)

        if (inputState.isSet('cameraLeft')):
            base.camera.setX(base.camera, +30 * globalClock.getDt())
        if (inputState.isSet('cameraRight')):
            base.camera.setX(base.camera, -30 * globalClock.getDt())

        if (inputState.isSet('cameraUp')):
            base.camera.setZ(base.camera, +30 * globalClock.getDt())
        if (inputState.isSet('cameraDown')):
            base.camera.setZ(base.camera, -30 * globalClock.getDt())

        #auto camera turn
        if self.cameraAutoTurn:
            if inputState.isSet('turnLeft'):  base.camera.setX(base.camera, +45 * globalClock.getDt())
            if inputState.isSet('turnRight'): base.camera.setX(base.camera, -45 * globalClock.getDt())

        camvec = self.characterNP.getPos() - base.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()
        if (camdist > self.cdmax):
            base.camera.setPos(base.camera.getPos() + camvec * (camdist - self.cdmax))
            camdist = self.cdmax
        if (camdist < self.cdmin):
            base.camera.setPos(base.camera.getPos() - camvec * (self.cdmin - camdist))
            camdist = self.cdmin
        if (inputState.isSet("zoomIn") and self.cdmin > 4):
            self.cdmin -= .2
            self.cdmax -= .2
        if (inputState.isSet("zoomOut") and self.cdmax < 40):
            self.cdmax += .2
            self.cdmin += .2
        if abs(base.camera.getZ() - self.characterNP.getZ()) > self.cdmax:
            #if base.camera.getZ() > 0:
            base.camera.setZ(self.characterNP.getZ() + self.cdmax)
        #Atm's animations
        '''
        if (inputState.isSet('forward') or inputState.isSet('reverse') or inputState.isSet('left') or inputState.isSet('right')) and self.character.isOnGround() and self.isLanding is False:
            if self.isMoving is False:
                self.actorNP.loop('run')
                #self.playSfx(self.SFXRun)
                self.isMoving = True
                self.isJumping = False
            elif self.isMoving and self.isJumping and self.isRunningAndJumping is False:
                self.isRunningAndJumping = True
            elif self.isRunningAndJumping and self.character.isOnGround() and self.isMoving and self.isRunningAndJumpingAndLanding is False:
                self.isRunningAndJumping = False
                self.isMoving = False
                self.isRunningAndJumpingAndLanding = True
                self.isJumping = False
                self.isLanding = True
                self.landingAnimation = True
                taskMgr.add(self.landingAnimationTask, 'landing')
            else:
                pass
                #self.isRunningAndJumpingAndLanding = False

        else:
            if self.isMoving and self.character.isOnGround():
                self.isMoving = False
                self.isJumping = False
                self.actorNP.loop('idle')
            elif self.isJumping and self.character.isOnGround():
                self.isJumping = False
                self.isLanding = True
                self.landingAnimation = True
                taskMgr.add(self.landingAnimationTask, 'landing')
            elif self.isLanding is False and taskMgr.hasTaskNamed('landing'):
                taskMgr.remove('landing')
                self.actorNP.loop('idle')
        '''

        #Pete's stuff
        #print self.peteIsActive

        #checkpoints

        self.floater.setPos(self.characterNP.getPos())
        self.floater.setZ(self.characterNP.getZ() + 1.0)
        #base.camera.setZ(self.characterNP.getZ() + 5)
        base.camera.lookAt(self.floater)
        return task.cont

    def landingAnimationTask(self, task):
        if self.landingAnimation is False:
            self.actorNP.play('land')
            self.landingAnimation = True
            self.animationIdle = False
            self.animationRunning = False
            self.animationDashing = False
        if task.time >= 0.3 and self.isLanding:
            self.isLanding = False
            self.animationLanding = False
            return task.done
        return task.cont
    '''
    def landingAnimationTask(self, task):
        if self.landingAnimation:
            self.actorNP.play('land')
            self.landingAnimation = False
        if task.time >= 0.3 and self.isLanding:

            self.isLanding = False
        return task.cont
    '''
    def cleanup(self):
        taskList = taskMgr.getAllTasks()
        for task in taskList:
            taskMgr.remove(task)

        #self.world = None
        #self.render.removeNode()

    def setupLights(self):
        # Light
        alight = AmbientLight('ambientLight')
        alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
        alightNP = render.attachNewNode(alight)

        dlight = DirectionalLight('directionalLight')
        dlight.setDirection(Vec3(1, 1, -1))
        dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
        #dlight.setColor(Vec4(1, 1, 1, 1)) Full light for stage 2
        dlightNP = render.attachNewNode(dlight)

        self.render.clearLight()
        self.render.setLight(alightNP)
        self.render.setLight(dlightNP)

    def createFourWalls(self):
        wallSize = Vec3(1, 20, 5)
        wallPos = Vec3(21, 0, 4)
        texturePos = Vec3(0, -wallPos.y, -wallPos.z - 1)
        for i in range(4):
            if i is 1:
                wallPos = Vec3(-21, 0, 4)
            if i is 2:
                wallSize = Vec3(20, 1, 5)
                wallPos = Vec3(0, 21, 4)
            if i is 3:
                wallSize = Vec3(20, 1, 5)
                wallPos = Vec3(0, -21, 4)
            shape = BulletBoxShape(wallSize)
            wallNP = self.render.attachNewNode(BulletRigidBodyNode('Wall%i' % i))
            wallNP.node().addShape(shape)
            wallNP.setPos(wallPos)
            wallNP.setCollideMask(BitMask32.allOn())
            self.world.attachRigidBody(wallNP.node())

            wallmNP = loader.loadModel('Resources\Models\ModelCollection\EnvBuildingBlocks\stone-cube\stone.egg')
            wallmNP.reparentTo(wallNP)
            wallmNP.setPos(texturePos)
            wallmNP.setScale(wallSize.x * 2, wallSize.y * 2, wallSize.z * 2)

    def addBall(self, radius, name, x, y, z, mass, respawn=False):
        shape = BulletSphereShape(radius)
        node = BulletRigidBodyNode(name)
        node.setMass(mass)
        node.addShape(shape)
        sphere = self.render.attachNewNode(node)
        sphere.setPos(x, y, z)
        self.world.attachRigidBody(node)

        #models/smiley
        smileyFace = self.loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/sphere/ball.egg')
        smileyFace.reparentTo(sphere)
        smileyFace.setScale(radius)
        if respawn:
            taskMgr.add(self.ballRespawnTask, 'ballRespawn', extraArgs=[sphere, sphere.getPos()], appendTask=True)
        return sphere

    def ballRespawnTask(self, ball, startpos, task):
        if ball.getZ() <= startpos.z - 30:
            ball.node().setLinearVelocity(0)
            ball.node().setAngularVelocity(0)
            ball.setPos(startpos)
        return task.cont

    def createCoin(self, pos, name, type=""):
        shape = BulletSphereShape(0.6)
        node = BulletRigidBodyNode(name)
        node.setMass(0)
        node.addShape(shape)
        coin = self.render.attachNewNode(node)
        coin.setPos(pos)
        smileyFace = self.loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/smiley/smiley.egg')
        smileyFace.reparentTo(coin)
        smileyFace.setScale(1)
        #smileyFace.setColorScale(1,1, 0, 1)
        if type == "battery":
            smileyFace.setColorScale(0,0,1,1)
        taskMgr.add(self.coinSpinTask, "coinTask", extraArgs=[coin, type, node], appendTask = True)

    def coinSpinTask(self, coin, type, node, task):
        spinConstant = 15
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        # self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        if type == "battery":
            spinConstant = 100
        coin.setHpr(angleDegrees * spinConstant, 0, 0)
        collisions = self.world.contactTestPair(coin.node(), self.character)
        #if coinPos.getDistance(self.characterNP) <= 2:
        if len(collisions.getContacts()) > 0:
            node.removeAllChildren()
            if type == "battery":
                self.updateLife(1)
            else:
                self.updateScore(100)
                self.playSfx(self.SFXpop)
            return task.done
        return task.cont

    def createSlide(self, box, h, tilt, modelName):
        boxSize = box.getSize()
        shape = BulletBoxShape(boxSize)
        boxNP = self.render.attachNewNode(BulletRigidBodyNode(box.getModel()))
        boxNP.node().addShape(shape)
        boxNP.setR(tilt)
        boxNP.setH(h)
        boxNP.setPos(box.getPosition())
        boxNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(boxNP.node())

        boxModelNP = self.loadModel(modelName)
        boxModelNP.reparentTo(boxNP)
        boxModelNP.setPos(0, 0, - boxSize.z)
        boxModelNP.setScale(boxSize.x * 2, boxSize.y * 2, boxSize.z * 2)
        ts = TextureStage.getDefault()
        boxModelNP.setTexOffset(ts, -0.5, -0.5)
        length = boxSize.x
        width = boxSize.y
        boxModelNP.setTexScale(ts, length, width)

    def createDisk(self, box):
        boxSize = box.getSize()
        shape = BulletCylinderShape(boxSize, ZUp)
        boxNP = self.render.attachNewNode(BulletRigidBodyNode(box.getModel()))
        boxNP.node().addShape(shape)
        boxNP.setPos(box.getPosition())
        boxNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(boxNP.node())

        # boxModelNP = loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-sand/brick.egg')
        boxModelNP = self.loader.loadModel("Resources/Models/ModelCollection/EnvBuildingBlocks/cylinder/marble-cylinder.egg")
        boxModelNP.reparentTo(boxNP)
        boxModelNP.setPos(0, 0, -boxSize.z - 2)
        boxModelNP.setScale(3)
        return boxNP

    def createBox(self, box, modelName, color = ""):
        boxSize = box.getSize()
        shape = BulletBoxShape(boxSize)
        boxNP = self.render.attachNewNode(BulletRigidBodyNode(box.getModel()))
        boxNP.node().addShape(shape)
        boxNP.setPos(box.getPosition())
        boxNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(boxNP.node())

        #boxModelNP = loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-sand/brick.egg')
        boxModelNP = self.loadModel(modelName)
        #if modelName == "lava":
        if boxModelNP == "No model under that name":
            pass
        else:
            boxModelNP.reparentTo(boxNP)
            boxModelNP.setPos(0, 0, - boxSize.z)
            boxModelNP.setScale(boxSize.x * 2, boxSize.y * 2, boxSize.z * 2)
            '''
            ts = TextureStage.getDefault()
            texture = self.loadTexture(modelName)
            boxModelNP.setTexture(ts, texture)
            wrapmode = Texture.WMRepeat

            texture.setWrapU(wrapmode)
            texture.setWrapV(wrapmode)
            texture.setWrapW(wrapmode)
            boxModelNP.setTexScale(ts, boxSize.x/2, boxSize.y/2, boxSize.z/2)
            boxModelNP.reparentTo(boxNP)
            '''

            ts = TextureStage.getDefault()
            #texture = boxModelNP.getTexture(boxModelNP)
            #texture = loader.loadTexture('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-stone2/brick.png')
            #texture.setWrapU(Texture.WMRepeat)
            #texture.setWrapV(Texture.WMRepeat)
            boxModelNP.setTexOffset(ts, -0.5, -0.5)
            length = boxSize.x
            width = boxSize.y
            if boxSize.z >= 8:
                length = boxSize.z
                if boxSize.y >= boxSize.x:
                    width = boxSize.y
                elif boxSize.x >= boxSize.y:
                    width = boxSize.x
            elif boxSize.z < 8:
                width = boxSize.x
                length = boxSize.y
            elif boxSize.x == boxSize.z and boxSize.z == boxSize.y:
                length = boxSize.y
                width = boxSize.x
            boxModelNP.setTexScale(ts, width, length)

            '''
            if modelName == "stone":
                pass
            elif modelName == 'stone2':
                boxModelNP.setLight(self.directionalLightNP)
                tex = loader.loadTexture("Resources/Models/ModelCollection/EnvBuildingBlocks/brick-stone2/map.jpg")
                boxModelNP.setTexture(ts,tex)
            '''
            #boxModelNP.setTexScale(ts,boxSize.x, boxSize.z)
            #tex = loader.loadTexture('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-stone2/map.jpg')
            #boxModelNP.setTexture(texture, 1)
            #boxModelNP.setTexGen(ts, TexGenAttrib.MWorldPosition)

            #random colorize everything, just for fun
            #boxModelNP.setColorScale(random.random(), random.random(), random.random(), 1)
        if color == "orange":
            boxModelNP.setColorScale(0.8, 0.5, 0.5, 1)
        elif color == "blue":
            boxModelNP.setColorScale(0.3, 0.3, 1, 1)
        elif color == "teal":
            boxModelNP.setColorScale(0, 0.6, 0.7, 1)

        if self.tasteTheRainbow:
            boxModelNP.setColorScale(random.random(), random.random(), random.random(), 1)

        return boxNP
        # boxNP.node().removeAllChildren()
        # self.world.removeRigidBody(boxNP.node())

    def createHazardBox(self, box, modelName, time, speed, direction, moving="yes", color=""):
        boxSize = box.getSize()
        shape = BulletBoxShape(boxSize)
        boxNP = self.render.attachNewNode(BulletRigidBodyNode(box.getModel()))
        boxNP.node().addShape(shape)
        boxNP.node().setGravity(Vec3(0, 0, 0))
        boxNP.setPos(box.getPosition())
        boxNP.setCollideMask(BitMask32.allOff())
        self.world.attachRigidBody(boxNP.node())

        boxModelNP = self.loadModel(modelName)
        if boxModelNP == "No model under that name":
            pass
        else:
            boxModelNP.reparentTo(boxNP)
            boxModelNP.setPos(0, 0, - boxSize.z)
            boxModelNP.setScale(boxSize.x * 2, boxSize.y * 2, boxSize.z * 2)

            ts = TextureStage.getDefault()
            boxModelNP.setTexOffset(ts, -0.5, -0.5)
            length = boxSize.x
            width = boxSize.y
            if boxSize.z >= 8:
                length = boxSize.z
                if boxSize.y >= boxSize.x:
                    width = boxSize.y
                elif boxSize.x >= boxSize.y:
                    width = boxSize.x
            elif boxSize.z < 8:
                width = boxSize.x
                length = boxSize.y
            elif boxSize.x == boxSize.z and boxSize.z == boxSize.y:
                length = boxSize.y
                width = boxSize.x
            boxModelNP.setTexScale(ts, width, length)

        if color == "orange":
            boxModelNP.setColorScale(0.8, 0.5, 0.5, 1)
        elif color == "blue":
            boxModelNP.setColorScale(0.3, 0.3, 1, 1)
        elif color == "teal":
            boxModelNP.setColorScale(0, 0.6, 0.7, 1)
        boxNP.node().setLinearVelocity(Vec3(0, 1, 0))
        if moving == "yes":
            taskMgr.add(self.movingPlatformForwardTask, "movinghazard", extraArgs=[boxNP, time, speed, direction, Vec3(boxNP.getPos())], appendTask=True)
        elif moving == "static":
            pass
        elif moving == "tower":
            self.towerMovingHazardBoxNP = boxNP
            taskMgr.add(self.movingTowerIdleUpTask, "towerLava",
                        extraArgs=[boxNP, time, speed, direction, Vec3(boxNP.getPos())], appendTask=True)
        elif moving =="down":
            taskMgr.add(self.movingPlatformDownwardTask, "movinghazardDown", extraArgs=[boxNP, time, speed, direction, Vec3(boxNP.getPos())], appendTask=True)
        taskMgr.add(self.hazardCollisionTask, "hazardcollision", extraArgs=[boxNP], appendTask=True)
        return boxNP

    def movingTowerExterminationProtocolTask(self, boxNP, startPos, task):
        boxNP.setX(boxNP.getX() - 0.01)
        if boxNP.getX() <= startPos.x - 7.9:
            boxNP.setX(startPos.x)
        boxNP.setZ(boxNP.getZ() + 0.03)
        if boxNP.getZ() >= self.towerExterminationLavaStartingPos.z + self.towerExterminationCurrentPositionModifier:
            taskMgr.add(self.movingTowerExterminationProtocolDownTask, "exterminationProtocolUp",
                        extraArgs=[boxNP, startPos],
                        appendTask=True)
            return task.done
        return task.cont

    def movingTowerExterminationProtocolDownTask(self, boxNP, startPos, task):
        boxNP.setX(boxNP.getX() - 0.01)
        if boxNP.getX() <= startPos.x - 7.9:
            boxNP.setX(startPos.x)
        boxNP.setZ(boxNP.getZ() - 0.015)
        if boxNP.getZ() <= self.towerExterminationLavaStartingPos.z + self.towerExterminationCurrentPositionModifier - 3:
            if boxNP.getZ() < 46:
                self.towerExterminationCurrentPositionModifier += 5
            taskMgr.add(self.movingTowerExterminationProtocolTask, "exterminationProtocolDown",
                        extraArgs=[boxNP, startPos],
                        appendTask=True)
            return task.done
        return task.cont

    def movingTowerIdleUpTask(self, boxNP, time, speed, direction, startPos, task):
        if self.towerExterminationProtocol:
            taskMgr.add(self.movingTowerExterminationProtocolTask, "movingtowerextermination",
                        extraArgs=[boxNP, startPos], appendTask=True)
            self.towerExterminationLavaStartingPos = startPos
            return task.done
        boxNP.setZ(boxNP.getZ() + speed)
        boxNP.setX(boxNP.getX() - 0.01)
        if boxNP.getX() >= startPos.x + 7.9:
            boxNP.setX(startPos.x)
        if boxNP.getZ() >= startPos.z + time:
            taskMgr.add(self.movingTowerIdleDownTask, "movinghazard",
                        extraArgs=[boxNP, time, speed, direction, startPos],
                        appendTask=True)
            return task.done
        return task.cont

    def movingTowerIdleDownTask(self, boxNP, time, speed, direction, startPos, task):
        if self.towerExterminationProtocol:
            taskMgr.add(self.movingTowerExterminationProtocolTask, "movingtowerextermination",
                        extraArgs=[boxNP, startPos], appendTask=True)
            self.towerExterminationLavaStartingPos = startPos
            return task.done
        boxNP.setZ(boxNP.getZ() - speed)
        boxNP.setX(boxNP.getX() - 0.01)

        if boxNP.getX() <= startPos.x - 7.9:
            boxNP.setX(startPos.x)
        if boxNP.getZ() <= startPos.z - time:
            taskMgr.add(self.movingTowerIdleUpTask, "movinghazard",
                        extraArgs=[boxNP, time, speed, direction, startPos],
                        appendTask=True)
            return task.done
        return task.cont

    def movingPlatformDownwardTask(self, boxNP, time, speed, direction, startPos, task):
        if direction == 'x':
            boxNP.setX(boxNP.getX() - speed)
        elif direction == "y":
            boxNP.setY(boxNP.getY() - speed)
        elif direction == "z":
            boxNP.setZ(boxNP.getZ() - speed)
        if boxNP.getX() <= startPos.x - time or boxNP.getY() <= startPos.y - time or boxNP.getZ() <= startPos.z - time:
            boxNP.setPos(startPos)
        return task.cont

    def movingPlatformForwardTask(self, boxNP, time, speed, direction, startPos, task):
        if direction == 'x':
            boxNP.setX(boxNP.getX() + speed)
        elif direction == "y":
            boxNP.setY(boxNP.getY() + speed)
        elif direction == "z":
            boxNP.setZ(boxNP.getZ() + speed)
            if time == 8 and speed == 0.05 and direction == 'z':
                boxNP.setX(boxNP.getX() + 0.01)
                boxNP.setY(boxNP.getY() + 0.01)
                if boxNP.getX() >= startPos.x + 7.9:
                    boxNP.setX(startPos.x)
                    boxNP.setY(startPos.y)
        if boxNP.getX() >= startPos.x + time or boxNP.getY() >= startPos.y + time or boxNP.getZ() >= startPos.z + time:
            taskMgr.add(self.movingPlatformBackwardTask, "movinghazard", extraArgs=[boxNP, time, speed, direction, startPos],
                        appendTask=True)
            return task.done
        return task.cont

    def movingPlatformBackwardTask(self, boxNP, time, speed, direction, startPos, task):
        if direction == 'x':
            boxNP.setX(boxNP.getX() - speed)
        elif direction == "y":
            boxNP.setY(boxNP.getY() - speed)
        elif direction == "z":
            boxNP.setZ(boxNP.getZ() - speed)
            if time == 8 and speed == 0.05 and direction == 'z':
                boxNP.setX(boxNP.getX() + 0.01)
                boxNP.setY(boxNP.getY() + 0.01)
                if boxNP.getX() <= startPos.x - 7.9:
                    boxNP.setX(startPos.x)
                    boxNP.setY(startPos.y)
        if boxNP.getX() <= startPos.x - time or boxNP.getY() <= startPos.y - time or boxNP.getZ() <= startPos.z - time:
            taskMgr.add(self.movingPlatformForwardTask, "movinghazard",
                        extraArgs=[boxNP, time, speed, direction, startPos],
                        appendTask=True)
            return task.done
        return task.cont

    def movingPlatformForwardTaskOld(self, boxNP, time, speed, direction, task):
        if task.time <= time:
            if direction == 'x':
                boxNP.setX(boxNP.getX() + speed)
            elif direction =="y":
                boxNP.setY(boxNP.getY() + speed)
            elif direction =="z":
                boxNP.setZ(boxNP.getZ() + speed)
        else:
            taskMgr.add(self.movingPlatformBackwardTask, "movinghazard", extraArgs=[boxNP, time, speed, direction],
                        appendTask=True)
            return task.done
        return task.cont

    def movingPlatformBackwardTaskOld(self, boxNP, time, speed, direction, task):
        if task.time <= time:
            if direction == 'x':
                boxNP.setX(boxNP.getX() - speed)
            elif direction == "y":
                boxNP.setY(boxNP.getY() - speed)
            elif direction == "z":
                boxNP.setZ(boxNP.getZ() - speed)
        else:
            taskMgr.add(self.movingPlatformForwardTask, "movinghazard", extraArgs=[boxNP, time, speed, direction],
                        appendTask=True)
            return task.done
        return task.cont

    def hazardCollisionTask(self, boxNP, task):
        collisions = self.world.contactTestPair(boxNP.node(), self.character)
        collisions2 = self.world.contactTestPair(boxNP.node(), self.pete)
        # if coinPos.getDistance(self.characterNP) <= 2:
        if len(collisions.getContacts()) > 0 or len(collisions2.getContacts()) > 0:
            self.respawnATM()
            self.SFXburnt.play()
        return task.cont

    def loadTexture(self, modelName):
        if modelName == 'brick':
            return loader.loadCubeMap('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-cube/brick_#.png')
        elif modelName == 'iron':
            return loader.loadCubeMap('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-iron/brick_#.png')
        elif modelName == 'sand':
            return loader.loadCubeMap('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-sand/brick_#.png')
        elif modelName == 'stone':
            return loader.loadCubeMap('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-stone/brick_#.png')
        elif modelName == 'stone2':
            return loader.loadCubeMap('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-stone2/brick_#.png')
        elif modelName == 'stone3':
            return loader.loadCubeMap('Resources/Models/ModelCollection/EnvBuildingBlocks/stone-cube/stone_#.png')
        elif modelName == "techno":
            return loader.loadCubeMap('Resources/Models/ModelCollection/EnvBuildingBlocks/techno/techno_#.png')
        elif modelName == "lava":
            return loader.loadCubeMap('Resources/Models/ModelCollection/EnvBuildingBlocks/lava/lava_#.jpg')
        elif modelName == "volcano":
            return loader.loadCubeMap('Resources/Models/ModelCollection/EnvBuildingBlocks/volcano/volcano_#.jpg')
        elif modelName == "cave":
            return loader.loadCubeMap('Resources/Models/ModelCollection/EnvBuildingBlocks/cave/cave_#.jpg')
        elif modelName == "grassy":
            return loader.loadCubeMap('Resources/Models/ModelCollection/EnvBuildingBlocks/grassy/cave_#.jpg')
        elif modelName == "dry":
            return loader.loadCubeMap('Resources/Models/ModelCollection/EnvBuildingBlocks/dry/cave_#.jpg')
        else:
            print modelName
            return "No model under that name"

    def createInvisibleBox(self, box, collision=False):
        boxSize = box.getSize()
        shape = BulletBoxShape(boxSize)
        boxNP = self.render.attachNewNode(BulletRigidBodyNode(box.getModel()))
        boxNP.node().addShape(shape)
        boxNP.setPos(box.getPosition())
        boxNP.setCollideMask(BitMask32.allOff())
        if collision:
            boxNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(boxNP.node())

        # boxModelNP = loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-sand/brick.egg')
        return boxNP

    def loadModel(self, modelName):
        if modelName == 'brick':
            return loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-cube/brick.egg')
        elif modelName == 'iron':
            return loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-iron/brick.egg')
        elif modelName == 'sand':
            return loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-sand/brick.egg')
        elif modelName == 'stone':
            return loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-stone/brick.egg')
        elif modelName == 'stone2':
            return loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-stone2/brick.egg')
        elif modelName == 'stone3':
            return loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/stone-cube/stone.egg')
        elif modelName =="techno":
            return loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/techno/brick.egg')
        elif modelName == "lava":
            return loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/lava/brick.egg')
        elif modelName == "volcano":
            return loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/volcano/brick.egg')
        elif modelName == "cave":
            return loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/cave/brick.egg')
        elif modelName == "grass":
            return loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/grass/brick.egg')
        elif modelName == "dry":
            return loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/dry/brick.egg')
        elif modelName == "grassy":
            return loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/grassy/brick.egg')
        elif modelName == "flowers":
            return loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/flowers/brick.egg')
        else:
            print modelName
            return "No model under that name"

    def createCheckPoint(self, pos, name):
        boxSize = Vec3(0.2, 0.2, 3)
        shape = BulletBoxShape(boxSize)
        boxNP = self.render.attachNewNode(BulletRigidBodyNode(name))
        boxNP.node().addShape(shape)
        boxNP.setPos(pos)
        boxNP.setCollideMask(BitMask32.allOff())
        self.world.attachRigidBody(boxNP.node())

        boxModelNP = loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/spinner/spinner.egg')
        boxModelNP.reparentTo(boxNP)
        boxModelNP.setPos(0, 0, -2)
        boxModelNP.setScale(0.2, 0.2, 0.4)
        taskMgr.add(self.checkPointSpinTask, name, extraArgs=[boxNP, boxModelNP, name], appendTask=True)

    def checkPointSpinTask(self, boxNP, checkPoint, name, task):

        collision = self.world.contactTestPair(boxNP.node(), self.character)
        if len(collision.getContacts()) > 0 and self.checkPointDict[name] is False:
            self.checkPointDict[name] = True
            self.respawnPoint = boxNP.getPos()
            self.playSfx(self.SFXcheckpoint)
            #if self.checkPointDict["stage1-checkpoint-4"]:
            #    self.textGameOver = OnscreenText(text="STAGE 1 COMPLETED!", style=1, fg=(1, 1, 0, 1), pos=(0, 0),
            #                                     align=TextNode.ACenter, scale=0.2)
        if self.checkPointDict[name]:
            angleDegrees = task.time * 6.0
            checkPoint.setHpr(angleDegrees * 200, 0, 0)
        return task.cont

    def checkPointRespawnTask(self, task):
        self.respawning = False
        return task.done

    def createPete(self):
        h = 1
        w = 1.4
        #shape = BulletCapsuleShape(w, h/2 - 1, ZUp)
        shape = BulletBoxShape(Vec3(1, 1, 1))

        self.pete = BulletCharacterControllerNode(shape, 0.4, 'Pete')
        #    self.character.setMass(1.0)
        self.peteNP = self.render.attachNewNode(self.pete)
        self.peteNP.setPos(-10, 65, 10)
        self.peteNP.setH(45)
        self.peteNP.setCollideMask(BitMask32.allOn())
        self.world.attachCharacter(self.pete)

        self.peteActorNP = Actor('Resources/Models/ModelCollection/Actors/panda/panda-model.egg', {
            'walk': 'Resources/Models/ModelCollection/Actors/panda/panda-walk4.egg'})

        self.peteActorNP.reparentTo(self.peteNP)
        self.peteActorNP.setScale(0.0035)
        self.peteActorNP.setH(180)
        self.peteActorNP.setPos(0, 0, -1)
        self.peteActorNP.loop('walk')

        self.peteIdentifer = 1
        self.peteIsActive = True
        if self.startFromStageOne:
            taskMgr.add(self.peteFirstTask, 'firstPeteTask')
            taskMgr.add(self.peteGrandPillarRespawn, "peteGrandPillarRespawn")

    def peteFirstTask(self, task):
        if self.peteActorNP.getDistance(self.characterNP) <= 18:
            self.peteActorNP.lookAt(self.characterNP)
            self.peteActorNP.setHpr(self.peteActorNP.getH() + 180, 0, 0)
            self.peteNP.setH(0)
            if self.peteInteractions["firstDialogue-Stage1"] is False and self.peteInteractions["doorDestroyed"] is False:
                self.peteInteractions["firstDialogue-Stage1"] = True
                taskMgr.add(self.peteStage1FirstDialogue, "firstDialogue-Stage1")
            if self.peteInteractions["firstTask-SFXUnknown"] is False:
                self.peteInteractions["firstTask-SFXUnknown"] = True
                self.playSfx(self.SFXunknown)
        if self.peteInteractions["doorDestroyed"] is True:
            #taskMgr.add(self.peteSecondTask, "secondPeteTask")
            #self.peteInteractions["doorDestroyed"] = False
            return task.done
        if self.peteInteractions["grandPillarSpawn"] is True:
            return task.done
        return task.cont

    def peteSecondTask(self, task):
        if self.peteActorNP.getDistance(self.characterNP) <= 17:
            self.peteActorNP.lookAt(self.characterNP)
            self.peteActorNP.setHpr(self.peteActorNP.getH() + 180, 0, 0)
            if self.peteInteractions["secondDialogue-Stage1"] is False and self.peteInteractions["doorDestroyed"] is False:
                self.peteInteractions["secondDialogue-Stage1"] = True
                taskMgr.add(self.peteStage1SecondDialogue, "secondDialogue-Stage1")
        if self.peteInteractions["doorDestroyed"]:
            #self.pete.setAngularMovement(150)
            return task.done
        if self.peteInteractions["grandPillarSpawn"] is True:
            return task.done

        return task.cont

    def peteThirdTask(self, task):
        if self.peteActorNP.getDistance(self.characterNP) <= 8:
            self.peteActorNP.lookAt(self.characterNP)
            self.peteActorNP.setHpr(self.peteActorNP.getH() + 180, 0, 0)
            if self.peteInteractions["thirdDialogue-Stage1"] is False:
                self.peteInteractions["thirdDialogue-Stage1"] = True
                taskMgr.add(self.peteStage1ThirdDialogue, "peteStage1ThirdDialogue")
        if self.peteInteractions["grandPillarSpawn"]:
            #self.peteNP.setPos(-17, 383, -17)
            return task.done
        return task.cont

    def peteFourthTask(self, task):
        if self.peteActorNP.getDistance(self.characterNP) <= 8:
            self.peteActorNP.lookAt(self.characterNP)
            self.peteActorNP.setHpr(self.peteActorNP.getH() + 180, 0, 0)
            if self.peteInteractions["fourthDialogue-stage1"] is False:
                self.peteInteractions["fourthDialogue-stage1"] = True
                taskMgr.add(self.peteStage1FourthDialogue, "peteFourthDialogueStage1")
        return task.cont

    def peteWalkOutCell(self, task):
        if task.time > 10:
            self.pete.setLinearMovement(Vec3(0,0,0), True)
            self.peteInteractions["doorDestroyed"] = False
            taskMgr.add(self.peteThirdTask, 'petethirdTask')
            return task.done
        elif task.time < 4:
            self.peteActorNP.setHpr(180, 0, 0)
            self.pete.setLinearMovement(Vec3(0, 0.7, 0), True)
        return task.cont

    def peteStage1FirstDialogue(self, task):
        text = "Talking Panda: "
        if self.peteInteractionsDialogueSwitches["switch1"] is False:
            self.peteInteractionsDialogueSwitches["switch1"] = True
            self.textMessageSpeak(text + "Hey!")
        if task.time > 5 and self.peteInteractionsDialogueSwitches["switch2"] is False:
            self.peteInteractionsDialogueSwitches["switch2"] = True
            self.textMessageSpeak(text +  "It looks like you're trapped too. Its kind of hard to see in here.", line2= "Try holding  down [Q] and [E] or [F1] to see what you can do!")
        if task.time > 14 and self.peteInteractionsDialogueSwitches["switch3"] is False:
            self.peteInteractionsDialogueSwitches["switch3"] = True
            self.textMessageClear()
        if task.time > 34 and self.peteInteractionsDialogueSwitches['switch4'] is False and self.peteInteractions["doorDestroyed"] is False:
            self.peteInteractionsDialogueSwitches["switch4"] = True
            self.textMessageSpeak(text + "See that hole in the corner? It looks pretty suspicious.", line2="Try pushing that ball into it.")
        if task.time > 44 and self.peteInteractions["doorDestroyed"] is False and self.peteInteractionsDialogueSwitches["switch5"] is False:
            self.peteInteractionsDialogueSwitches["switch5"] = True
            self.textMessageClear()
        if self.peteInteractions["doorDestroyed"]:
            self.textMessageSpeak(text + "Hey! You did it!")
            taskMgr.doMethodLater(3, self.textMessageClearTask, 'clearMessage')
            self.clearPeteDialogueSwitches()
            self.peteInteractions["doorDestroyed"] = False
            taskMgr.add(self.peteSecondTask, "secondPeteTask")
            return task.done
        if self.peteInteractions["grandPillarSpawn"] is True:
            return task.done
        return task.cont

    def peteStage1SecondDialogue(self, task):
        text = "Talking Panda: "
        if self.peteInteractionsDialogueSwitches["switch1"] is False:
            self.peteInteractionsDialogueSwitches["switch1"] = True
            self.textMessageSpeak(text + "You got out! But the exit is still blocked.", line2="There should be another ball nearby...")
        if task.time > 8 and self.peteInteractionsDialogueSwitches["switch2"] is False:
            self.playSfx(self.SFXacknowledged)
            self.peteInteractionsDialogueSwitches["switch2"] = True
            self.textMessageClear()
            self.textMessageSpeak(text + "Try looking around, you can move your camera with the arrow keys.", line2="You can hold down [SHIFT] to jump further.")
        if task.time > 20 and self.peteInteractionsDialogueSwitches["switch3"] is False:
            self.peteInteractionsDialogueSwitches["switch3"] = True
            self.textMessageClear()
        if self.peteInteractions["doorDestroyed"]:
            self.textMessageSpeak(text + "Freeedoooom!")
            taskMgr.doMethodLater(3, self.textMessageClearTask, 'clearMessage')
            self.clearPeteDialogueSwitches()
            taskMgr.add(self.peteWalkOutCell, 'peteEscapeTask')
            return task.done
        if self.peteInteractions["grandPillarSpawn"] is True:
            return task.done
        return task.cont

    def peteStage1ThirdDialogue(self,task):
        text = "Talking Panda: "
        if self.peteInteractions["grandPillarSpawn"] is True:
            return task.done
        if self.peteInteractionsDialogueSwitches["switch1"] is False:
            self.peteInteractionsDialogueSwitches["switch1"] = True
            self.textMessageSpeak(text + "Hey, you are awesome! I like you, have a battery.", line2="The exit's still blocked though...")
            self.updateLife(1)
            self.playSfx(self.SFXbattery)
        if task.time > 8 and self.peteInteractionsDialogueSwitches["switch2"] is False:
            self.peteInteractionsDialogueSwitches["switch2"] = True
            self.textMessageClear()
            self.textMessageSpeak(text + "There's a button back inside my cell. It made funny noises when i stepped on it", line2="You go on ahead, this puzzle is quite puzzling to me...")
        if task.time > 16 and self.peteInteractionsDialogueSwitches["switch3"] is False:
            self.peteInteractionsDialogueSwitches["switch3"] = True
            self.peteInteractions["bookIt"] = True
            self.textMessageClear()
            return task.done
        return task.cont

    def peteStage1FourthDialogue(self, task):
        text = "Pete:"
        if self.peteInteractionsDialogueSwitches["switch1"] is False:
            self.peteInteractionsDialogueSwitches["switch1"] = True
            self.textMessageSpeak(text + " Oh! Hello. I forgot to tell you my name last time.", line2="My name is Pete.")
        if task.time > 5 and self.peteInteractionsDialogueSwitches["switch2"] is False:
            self.playSfx(self.SFXniceToMeetYou)
            self.peteInteractionsDialogueSwitches["switch2"] = True
        if task.time > 8 and self.peteInteractionsDialogueSwitches["switch3"] is False:
            self.playSfx(self.SFXintroduction)
            self.peteInteractionsDialogueSwitches["switch3"] = True
            self.textMessageClear()
        if task.time > 11 and self.peteInteractionsDialogueSwitches["switch4"] is False:
            self.peteInteractionsDialogueSwitches["switch4"] = True
            self.textMessageSpeak(text + " See that tiny bridge? Don't look down when you're on it, ATM.", line2="You got this ATM! I'll supervise you from here.")
        if task.time > 24 and self.peteInteractionsDialogueSwitches["switch5"] is False:
            self.peteInteractionsDialogueSwitches["switch5"] = True
            self.textMessageClear()
            self.updateLife(1)
            self.clearPeteDialogueSwitches()
            return task.done
        return task.cont

    def peteGrandPillarRespawn(self, task):
        if self.peteInteractions["grandPillarSpawn"]:
            self.peteNP.setPos(40, 395, 24)
            self.clearPeteDialogueSwitches()
            taskMgr.add(self.peteFourthTask, "stage1petefourthdialogue")
            return task.done
        return task.cont

    def invisiblePeteSpawnTask(self, target, task):
        if self.characterNP.getDistance(target) <= 26:
            self.peteNP.setPos(282, 327, 22)
            self.stageOneCleared = True
            return task.done
        return task.cont

    def setUpInvisiblePeteCheckPoint(self):
        box = Box(1, 1, 1, 220, 335, 35, 'invisibleCheckTransition')
        invisible = self.createInvisibleBox(box)
        taskMgr.add(self.invisiblePeteSpawnTask, "invisibleClearUp", extraArgs=[invisible], appendTask=True)

    def peteTransitionTask(self, task):
        if self.peteActorNP.getDistance(self.characterNP) <= 10 and self.peteInteractions["transitionDoubleSwitchBegniWalk"] is False and self.stageOneCleared:
            #self.peteNP.lookAt(self.characterNP)
            #self.peteActorNP.lookAt(self.characterNP)
            #self.peteActorNP.setH(self.peteActorNP.getH() + 180)
            #self.peteNP.setHpr(self.peteActorNP.getH() + 180, 0, 0)
            if self.peteInteractions["transitionDialogue1"] is False:
                self.peteInteractions["transitionDialogue1"] = True
                self.clearPeteDialogueSwitches()
                taskMgr.add(self.peteTransitionDialogue1, "PeteTransitionDialogue")
        if self.peteInteractions["transitionDoubleSwitchBegniWalk"] and self.peteState["isWalking"] is False and self.peteInteractions["finishedTransitionWalk"] is False:
            self.peteState["isWalking"] = True
            self.peteInteractions["finishedTransitionWalk"] = True
            self.peteNP.setH(0)
            self.peteActorNP.setH(90)
            #self.pete.setAngularMovement(omega)
            #self.pete.setLinearMovement(Vec3(1.3,0,0), True)
            self.pete.setLinearMovement(Vec3(1.6, 0, 0), True)
        if self.peteNP.getX() >= 300 and self.peteState:
            self.pete.setLinearMovement(Vec3(0, 0, 0), True)
            self.peteState["isWalking"] = False
        if self.peteInteractions["transitionDoubleSwitchDoorUnlocked"]:
            self.pete.setLinearMovement(Vec3(0, 0, 0), True)
            self.peteState["isWalking"] = False
            taskMgr.doMethodLater(3, self.peteTransitionTask2, "peteTransitiontask2")
            return task.done
        return task.cont

    def peteTransitionTask2(self, task):
        if self.peteState["isWalking"] is False and self.peteInteractions["transitionWalkingToEdge"] is False:
            self.peteInteractions["transitionWalkingToEdge"] = True
            self.peteState["isWalking"] = True
            self.pete.setLinearMovement(Vec3(2.3, 0, 0), True)
            self.peteActorNP.setPlayRate(2.1, "walk")
        if self.peteNP.getX() >= 329 and self.peteState["isWalking"]:
            self.peteState["isWalking"] = False
            self.pete.setLinearMovement(Vec3(0, 0, 0), True)
            self.peteActorNP.setPlayRate(1.3, "walk")
            taskMgr.add(self.peteStage2Dialogue1, "peteStage2Dialogue1")
            taskMgr.doMethodLater(3, self.peteStage2FirstTask, "peteStage2FirstTask")
            return task.done
        return task.cont

    def peteTransitionDialogue1(self, task):
        text = "Pete: "
        if self.peteInteractionsDialogueSwitches["switch1"] is False:
            self.peteInteractionsDialogueSwitches["switch1"] = True
            self.SFXhello.play()
            self.textMessageSpeak(text + "Hello! See those two switches?", line2="I tried stepping on them, but nothing happened.")
        elif task.time > 10 and self.peteInteractionsDialogueSwitches["switch2"] is False:
            self.peteInteractionsDialogueSwitches["switch2"] = True
            self.textMessageSpeak(text + "Maybe we can try stepping on both at the same time.", line2="I'll get this one, ATM.")
        elif task.time > 18 and self.peteInteractionsDialogueSwitches["switch3"] is False:
            self.peteInteractionsDialogueSwitches["switch3"] = True
            self.SFXaffirmative.play()
            self.textMessageClear()
            self.peteInteractions["transitionDoubleSwitchBegniWalk"] = True
        if self.peteInteractions["transitionDoubleSwitchDoorUnlocked"]:
            self.doJumpPete()
            self.textMessageSpeak(text + "It worked! Breath in that fresh air ATM! ")
            self.SFXbreathe.play()
            taskMgr.doMethodLater(5, self.textMessageClearTask, "textMessageClear")
            self.clearPeteDialogueSwitches()
            return task.done
        return task.cont

    def peteStage2FirstTask(self, task):
        if self.peteState["isWalking"] is False and self.peteInteractions["onInvisiblePlatform"] is False:
            self.peteState["isWalking"] = True
            self.peteInteractions["onInvisiblePlatform"] = True
            self.pete.setLinearMovement(Vec3(1.3, 0, 0), True)
            self.peteActorNP.setPlayRate(1.3, "walk")
        if self.peteNP.getX() >= 334 and self.peteState["isWalking"]:
            self.peteState["isWalking"] = False
            self.pete.setLinearMovement(Vec3(0,0,0), True)
            taskMgr.add(self.peteJumpInPlace, "peteJumpingInPlace")
            return task.done
        return task.cont

    def peteStage2SecondTask(self, task):
        if self.peteActorNP.getDistance(self.characterNP) <= 8:
            self.peteActorNP.setP(0)
            if self.peteInvisibleGuideSwitches["switch1"] is False:
                self.peteInvisibleGuideSwitches["switch1"] = True
                self.peteNP.setH(0)
                self.peteActorNP.setH(90)
                self.pete.setLinearMovement(Vec3(1.3, 0, 0), True)
                self.peteActorNP.setPlayRate(1.3, "walk")
            if self.peteInvisibleGuideSwitches["switch2"] and self.peteInvisibleGuideSwitches["switch3"] is False:
                self.peteInvisibleGuideSwitches["switch3"] = True
                self.clearPeteInvisibleGuideSwitches()
                taskMgr.doMethodLater(1, self.peteStage2ThirdTask, "invisibleG3")
                return task.done
        if self.peteInvisibleGuideSwitches["switch1"] and self.peteNP.getX() >= 342 and self.peteInvisibleGuideSwitches["switch4"] is False:
            self.peteInvisibleGuideSwitches["switch4"] = True
            self.peteNP.setH(90)
            self.peteActorNP.setH(90)
            self.pete.setLinearMovement(Vec3(0,0,0), True)
            self.peteInvisibleGuideSwitches["switch2"] = True
        return task.cont

    def peteStage2ThirdTask(self, task):
        if self.peteActorNP.getDistance(self.characterNP) <= 8:
            if self.peteInvisibleGuideSwitches["switch1"] is False:
                self.peteInvisibleGuideSwitches["switch1"] = True
                self.pete.setLinearMovement(Vec3(2, 0, 0), True)
                self.peteActorNP.setPlayRate(2, "walk")
            if self.peteInvisibleGuideSwitches["switch3"]:
                self.clearPeteInvisibleGuideSwitches()
                taskMgr.doMethodLater(1, self.peteStage2FourthTask, "invisibleG4")
                return task.done
        if self.peteInvisibleGuideSwitches["switch1"] and self.peteNP.getY() >= 331 and self.peteInvisibleGuideSwitches["switch2"] is False:
            self.peteInvisibleGuideSwitches["switch2"] = True
            self.doJumpPete()
        if self.peteNP.getY() >= 339 and self.peteInvisibleGuideSwitches["switch3"] is False:
            self.peteInvisibleGuideSwitches["switch3"] = True
            self.pete.setLinearMovement(Vec3(0, 0, 0), True)
            self.peteActorNP.setPlayRate(1.3, "walk")
            self.peteNP.setH(0)
            self.peteActorNP.setH(90)
        return task.cont

    def peteStage2FourthTask(self, task):
        if self.peteActorNP.getDistance(self.characterNP) <= 8:
            if self.peteInvisibleGuideSwitches["switch1"] is False:
                self.peteInvisibleGuideSwitches["switch1"] = True
                self.pete.setLinearMovement(Vec3(2, 0, 0), True)
                self.peteActorNP.setPlayRate(2, "walk")
            if self.peteInvisibleGuideSwitches["switch4"]:
                self.clearPeteInvisibleGuideSwitches()
                taskMgr.doMethodLater(1, self.peteStage2FifthTask, "invisibleG5")
                return task.done
        if self.peteInvisibleGuideSwitches["switch1"] and self.peteNP.getX() >= 346 and self.peteInvisibleGuideSwitches[
            "switch2"] is False:
            self.peteInvisibleGuideSwitches["switch2"] = True
            self.doJumpPete()
        if self.peteInvisibleGuideSwitches["switch2"] and self.peteNP.getX() >= 358 and self.peteInvisibleGuideSwitches[
            "switch3"] is False:
            self.peteInvisibleGuideSwitches["switch3"] = True
            self.doJumpPete()
        if self.peteNP.getX() >= 366 and self.peteInvisibleGuideSwitches["switch4"] is False:
            self.peteInvisibleGuideSwitches["switch4"] = True
            self.pete.setLinearMovement(Vec3(0, 0, 0), True)
            self.peteActorNP.setPlayRate(1.3, "walk")
            self.peteNP.setH(90)
            self.peteActorNP.setH(90)
        return task.cont

    def peteStage2FifthTask(self, task):
        if self.peteActorNP.getDistance(self.characterNP) <= 8:
            if self.peteInvisibleGuideSwitches["switch1"] is False:
                self.peteInvisibleGuideSwitches["switch1"] = True
                self.pete.setLinearMovement(Vec3(2, 0, 0), True)
                self.peteActorNP.setPlayRate(2, "walk")
            if self.peteInvisibleGuideSwitches["switch3"]:
                self.clearPeteInvisibleGuideSwitches()
                taskMgr.doMethodLater(1, self.peteStage2SixthTask, "invisibleG6")
                return task.done
        if self.peteInvisibleGuideSwitches["switch1"] and self.peteNP.getY() >= 343 and self.peteInvisibleGuideSwitches[
            "switch2"] is False:
            self.peteInvisibleGuideSwitches["switch2"] = True
            self.doJumpPete()
        if self.peteNP.getY() >= 375 and self.peteInvisibleGuideSwitches["switch3"] is False:
            self.peteInvisibleGuideSwitches["switch3"] = True
            self.pete.setLinearMovement(Vec3(0, 0, 0), True)
            self.peteActorNP.setPlayRate(1.3, "walk")
            self.peteNP.setH(0)
            self.peteActorNP.setH(90)
        return task.cont

    def peteStage2SixthTask(self, task):
        if self.peteActorNP.getDistance(self.characterNP) <= 8:
            if self.peteInvisibleGuideSwitches["switch1"] is False:
                self.peteInvisibleGuideSwitches["switch1"] = True
                self.pete.setLinearMovement(Vec3(2, 0, 0), True)
                self.peteActorNP.setPlayRate(2, "walk")
            if self.peteInvisibleGuideSwitches["switch5"] and self.checkPointDict["stage2-checkpoint-1"]:
                self.clearPeteInvisibleGuideSwitches()
                taskMgr.add(self.peteStage2Dialogue2, "peteStage2Dialogue2")
                return task.done
        if self.peteInvisibleGuideSwitches["switch1"] and self.peteNP.getX() >= 378 and self.peteInvisibleGuideSwitches[
            "switch2"] is False:
            self.peteInvisibleGuideSwitches["switch2"] = True
            self.doJumpPete()
        if self.peteInvisibleGuideSwitches["switch2"] and self.peteNP.getX() >= 390 and self.peteInvisibleGuideSwitches[
            "switch3"] is False:
            self.peteInvisibleGuideSwitches["switch3"] = True
            self.doJumpPete()
        if self.peteInvisibleGuideSwitches["switch3"] and self.peteNP.getX() >= 402 and self.peteInvisibleGuideSwitches[
            "switch4"] is False:
            self.peteInvisibleGuideSwitches["switch4"] = True
            self.doJumpPete()
        if self.peteNP.getX() >= 410 and self.peteInvisibleGuideSwitches["switch5"] is False:
            self.peteInvisibleGuideSwitches["switch5"] = True
            self.pete.setLinearMovement(Vec3(0, 0, 0), True)
            self.peteActorNP.setPlayRate(1.3, "walk")
        return task.cont

    def peteStage2Dialogue1(self, task):
        text = "Pete: "
        if self.peteInteractionsDialogueSwitches["switch1"] is False:
            self.peteInteractionsDialogueSwitches["switch1"] = True
            self.textMessageSpeak(text + "Hmmmmm... Something smells fishy here.")
            taskMgr.doMethodLater(5, self.textMessageClearTask, "messageClearTask")
            return task.done
        return task.cont

    def peteStage2Dialogue2(self, task):
        self.peteNP.lookAt(self.characterNP)
        self.peteActorNP.lookAt(self.characterNP)
        self.peteActorNP.setH(self.peteActorNP.getH() + 180)
        text = "Pete: "
        if self.peteInteractionsDialogueSwitches["switch1"] is False:
            self.peteInteractionsDialogueSwitches["switch1"] = True
            self.textMessageSpeak(text + "We made it ATM! Take this battery, I'll catch up with you later.", line2="I'm still dizzy from jumping around in the air.")
            self.updateLife(1)
            taskMgr.doMethodLater(10, self.textMessageClearTask, "messageClearTask")
            taskMgr.doMethodLater(7, self.ATMMessageSpeak, "ATMMessage", extraArgs=[self.SFXbattery], appendTask=True)
            self.clearPeteDialogueSwitches()
            return task.done
        return task.cont

    def peteJumpInPlace(self, task):
        self.peteNP.lookAt(self.characterNP)
        self.peteActorNP.lookAt(self.characterNP)
        self.peteActorNP.setH(self.peteActorNP.getH() + 180)
        #self.peteNP.setP(180)
        if self.peteInteractionsDialogueSwitches["switch5"] is False:
            self.peteInteractionsDialogueSwitches["switch5"] = True
            self.textMessageSpeak("Pete: Look ATM! I am flying!")
            taskMgr.add(self.peteJumpingInPlace, "peteJumpingInPlaceTask")
            #taskMgr.doMethodLater(4, self.textMessageClearTask, "messageClearTask")
        if task.time > 4.1 and self.peteInteractionsDialogueSwitches["switch4"] is False:
            self.peteInteractionsDialogueSwitches["switch4"] = True
            self.peteInteractions["havePeteJumpInPlace"] = True
            self.textMessageSpeak("Pete: Can't you see these walkways?")
            taskMgr.doMethodLater(4, self.textMessageClearTask, "messageClearTask")
        if task.time > 8 and self.peteInteractionsDialogueSwitches["switch2"] is False:
            self.peteInteractionsDialogueSwitches["switch2"] = True
            self.SFXsensors.play()
        if task.time > 13.5 and self.peteInteractionsDialogueSwitches["switch3"] is False:
            self.peteInteractionsDialogueSwitches["switch3"] = True
            self.textMessageSpeak("Pete: That's okay, I can guide you through.", line2="Stay close to me, ATM.")
            taskMgr.doMethodLater(10, self.textMessageClearTask, "messageClearTask")
            taskMgr.doMethodLater(4, self.ATMMessageSpeak, "ATM Message", extraArgs=[self.SFXacknowledged], appendTask=True)
            self.clearPeteDialogueSwitches()
            taskMgr.doMethodLater(5, self.peteStage2SecondTask, "invisibleG2")
            return task.done
        return task.cont

    def peteJumpingInPlace(self, task):
        self.doJumpPete()
        if task.time > 4:
            return task.done
        return task.cont

    def peteResetInvisibleGuide(self):
        taskList = taskMgr.getAllTasks()
        for task in taskList:
            if "invisibleG" in task.name:
                taskMgr.remove(task.name)
        self.peteNP.setPos(334, 327, 22)
        self.pete.setLinearMovement(Vec3(0, 0, 0), True)
        self.clearPeteInvisibleGuideSwitches()
        taskMgr.add(self.peteStage2SecondTask, "invisibleG2")

    def peteStage2SeventhTask(self, task):
        if self.peteActorNP.getDistance(self.characterNP) <= 12:
            self.peteNP.lookAt(self.characterNP)
            self.peteActorNP.lookAt(self.characterNP)
            self.peteActorNP.setH(self.peteActorNP.getH() + 180)
            if self.peteInteractions["stage2-third-dialogue"] is False:
                self.peteInteractions["stage2-third-dialogue"] = True
                taskMgr.add(self.peteStage2Dialogue3, "peteStage2Dialogue3")
        if self.peteCommandsSwitches["commandsEnabled"]:
            self.peteNP.setH(0)
            self.peteActorNP.setH(90)
            taskMgr.add(self.peteStage2CommandingTask, "peteCommandingTask")
            return task.done
        return task.cont

    def peteStage2CommandingTask(self, task):
        if self.peteInteractions["stage2-commanding-section-complete"]:
            taskMgr.add(self.peteStage2Dialogue4, "pete-stage2-Dialogue4")
            return task.done
        if self.peteCommandsSwitches["go"] and self.peteCommandsSwitches["going"] is False:
            self.peteCommandsSwitches["going"] = True
            self.peteCommandsSwitches["stop"] = False
            self.pete.setLinearMovement(Vec3(2, 0, 0), True)
            self.peteActorNP.setPlayRate(1.8, "walk")
        if self.peteCommandsSwitches["stop"] and self.peteCommandsSwitches["going"]:
            self.peteCommandsSwitches["going"] = False
            self.peteCommandsSwitches["go"] = False
            self.pete.setLinearMovement(Vec3(0, 0, 0), True)
        if self.peteNP.getX() >= 664:
            self.peteCommandsSwitches["commandsEnabled"] = False
            self.pete.setLinearMovement(Vec3(0, 0, 0), True)
            self.peteInteractions["stage2-commanding-section-complete"] = True
        return task.cont

    def peteStage2Dialogue3(self, task):
        text="Pete: "
        if self.peteInteractionsDialogueSwitches["switch1"] is False:
            self.peteInteractionsDialogueSwitches["switch1"] = True
            self.textMessageSpeak(text + "ATM! I found an entrance to an underground volcano!",
                                  line2="I see the a switch down this tunnel, but I'm too scared to go over there.")
            taskMgr.doMethodLater(10, self.textMessageClearTask, "textMessageClear")
        if task.time >= 11 and self.peteInteractionsDialogueSwitches["switch2"] is False:
            self.peteInteractionsDialogueSwitches["switch2"] = True
            self.textMessageSpeak(text + "Hey ATM, you have a brain of a robot, think you can guide me over there?")
            taskMgr.doMethodLater(5, self.ATMMessageSpeak, "ATMmessageSpeak", extraArgs=[self.SFXspeedOfLight], appendTask=True)
            taskMgr.doMethodLater(5, self.textMessageClearTask, "textMessageClear")
        if task.time >= 26 and self.peteInteractionsDialogueSwitches["switch3"] is False:
            self.peteInteractionsDialogueSwitches["switch3"] = True
            self.textMessageSpeak(text + "Okay ATM, I'll follow your command. Press [G] to command me to move.", line2="Press [H] to command me to stop.")
            taskMgr.doMethodLater(10, self.textMessageClearTask, "textMessageClearTask")
            self.peteCommandsSwitches["commandsEnabled"] = True
            self.accept('g', self.commandGo)
            self.accept('h', self.commandHold)
            self.clearPeteDialogueSwitches()
            return task.done
        return task.cont

    def peteStage2Dialogue4(self, task):
        self.peteNP.lookAt(self.characterNP)
        self.peteActorNP.lookAt(self.characterNP)
        self.peteActorNP.setH(self.peteActorNP.getH() + 180)
        text = "Pete: "
        if self.peteInteractionsDialogueSwitches["switch1"] is False:
            self.peteInteractionsDialogueSwitches["switch1"] = True
            self.textMessageSpeak(text + "Hey! I think that did it! Don't worry about me, I can probably get back out.",
                                  line2="You go on ahead ATM, I think this tunnel will lead us to freedom!")
            taskMgr.doMethodLater(10, self.textMessageClearTask, "textMessageClear")
        if task.time >= 11 and self.peteInteractionsDialogueSwitches["switch2"] is False:
            self.peteInteractionsDialogueSwitches["switch2"] = True
            self.clearPeteDialogueSwitches()
            return task.done
        return task.cont

    def peteStage3FinalDialogue(self, task):
        self.peteNP.lookAt(self.characterNP)
        self.peteActorNP.lookAt(self.characterNP)
        self.peteActorNP.setH(self.peteActorNP.getH() + 180)
        text = "Pete: "
        if self.peteActorNP.getDistance(self.characterNP) <= 16:
            taskMgr.add(self.musicFadeOut, "musicFade", extraArgs=[self.BGM4], appendTask = True)
            self.textMessageSpeak(text + "ATM! You made it! I found a shortcut when I was stuck underground.",
                                  line2="There's the exit ATM! We're finally free!!")
            taskMgr.doMethodLater(7, self.textMessageClearTask, "textMessageClear")
            taskMgr.doMethodLater(7, self.gameOverTask, "gameover")
            taskMgr.doMethodLater(4, self.ATMMessageSpeak, "ATMMessage", extraArgs=[self.SFXtestOfMetal], appendTask=True)
            render.clearFog()
            return task.done
        return task.cont

    def gameOverTask(self, task):
        self.textGameOver = OnscreenText(text="CONGRADULATIONS!", style=1, fg=(1, 0.7, 0, 1), pos=(0, 0.7),
                                             align=TextNode.ACenter, scale=0.15)

        self.livesMultiplierScore = OnscreenText(
            text="Batteries: " + str(self.playerLives) + " X 5000 = " + str(self.playerLives * 5000), style=1,
            fg=(1, 1, 1, 1), pos=(0, 0.5),
            align=TextNode.ACenter, scale=0.1)
        self.playerCurrentScore = OnscreenText(text="Current Score: " + " + " + str(self.playerScore), style=1,
                                               fg=(1, 1, 1, 1), pos=(0, 0.3),
                                               align=TextNode.ACenter, scale=0.1)
        self.underLineResult = OnscreenText(text="_____________________________", style=1,
                                            fg=(1, 1, 1, 1), pos=(0, 0.2),
                                            align=TextNode.ACenter, scale=0.1)
        self.totalScoreResult = OnscreenText(text="TOTAL SCORE: " + str(self.playerLives * 5000 + self.playerScore),
                                             style=1,
                                             fg=(0.5, 1, 0.1, 1), pos=(0, -0.2),
                                             align=TextNode.ACenter, scale=0.2)
        taskMgr.remove("updateWorld")
        self.SFXgameover.play()
        return task.done

    def commandGo(self):
        if self.peteCommandsSwitches['go'] is False and self.peteCommandsSwitches["commandsEnabled"]:
            self.peteCommandsSwitches["go"] = True
            selector = random.randint(1, len(self.SFXgoDict))
            self.playSfx(self.SFXgoDict[str(selector)])

    def commandHold(self):
        if self.peteCommandsSwitches["stop"] is False and self.peteCommandsSwitches["commandsEnabled"]:
            self.peteCommandsSwitches["stop"] = True
            selector = random.randint(1, len(self.SFXstopDict))
            self.playSfx(self.SFXstopDict[str(selector)])

    def resetPeteCommands(self):
        self.peteCommandsSwitches['go'] = False
        self.peteCommandsSwitches['stop'] = True
        self.peteCommandsSwitches['going'] = False

    def setUpStage2PeteInvisibleCheckPoint(self):
        box = Box(1, 1, 1, 576, 381, 20, 'invisibleCheckStage2')
        invisible = self.createInvisibleBox(box)
        taskMgr.add(self.stage2InvisiblePeteSpawnTask, "invisiblePeteRespawn", extraArgs=[invisible], appendTask=True)

    def stage2InvisiblePeteSpawnTask(self, target, task):
        if self.characterNP.getDistance(target) <= 26:
            self.peteNP.setPos(608, 391, 26)
            self.peteRespawnPos = Vec3(608, 391, 26)
            #self.pete.setLinearMovement(Vec3(1.3, 0, 0), True)
            #self.peteActorNP.setPlayRate(1.3, "walk")
            if taskMgr.hasTaskNamed("peteTransitionTask"):
                taskMgr.remove("peteTransitionTask")
            if taskMgr.hasTaskNamed("invisibleG6"):
                taskMgr.remove("invisibleG6")
            self.clearPeteDialogueSwitches()
            taskMgr.add(self.peteStage2SeventhTask, "stage2SeventhPeteTask")
            #taskList = taskMgr.getAllTasks()
            #for task in taskList:
            #   print task.name
            return task.done
        return task.cont

    def textMessageSpeak(self, line1, line2=""):
        self.textMessage.setText(line1)
        self.textMessage2.setText(line2)
        if line2 != "":
            self.playSfx(self.SFXsniffLong, volume = 0.1)
        else: self.playSfx(self.SFXsniffShort, volume = 0.1)

    def textMessageClear(self):
        self.textMessage.setText("")
        self.textMessage2.setText("")

    def textMessageClearTask(self, task):
        self.textMessageClear()
        return task.done

    def ATMMessageSpeak(self, voiceClip, task):
        voiceClip.play()
        return task.done

    def clearPeteDialogueSwitches(self):
        for k in self.peteInteractionsDialogueSwitches:
            self.peteInteractionsDialogueSwitches[k] = False

    def clearPeteInvisibleGuideSwitches(self):
        for switch in self.peteInvisibleGuideSwitches:
            self.peteInvisibleGuideSwitches[switch] = False

    def createATM(self):
        h = 4.25
        w = .6
        shape = BulletCylinderShape(w, h + w - 0.70, ZUp)
        self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
        #self.character.Node().setMass(1.0)
        self.characterNP = self.render.attachNewNode(self.character)
        if self.startFromStageOne:
            self.characterNP.setPos(12, 55, 4)
        elif self.startFromStageTwo:
            self.characterNP.setPos(200, 335, 24)
        elif self.startFromStageThree:
            self.characterNP.setPos(640, 391, 0)
            #self.characterNP.setPos(627, 936, 70)
            #self.setUpStage3()
        #self.characterNP.setPos(26.5, 316, 50)
        #self.characterNP.setPos(40, 395, 24)
        #stage2 spawn point
        #self.characterNP.setPos(200, 335, 24)
        #self.StageOneCleared switch need to be turned on
        #self.stageOneCleared = True
        #self.startFromStageOne = False

        #self.setUpStage2()
        #self.characterNP.setPos(664,416, 50)
        #self.setUpTransition2()
        #self.characterNP.setPos(640, 391, 0)
        #self.characterNP.setPos(640, 364, -30)
        #self.setUpStage3()
        #self.respawnZValue = -150
        #self.startFromStageThree = True

        #self.characterNP.setPos(650, 848, 70)
        #self.characterNP.setPos(656, 847, -108)
        #self.clearStage2Tasks()
        #invisible detect spawn box 5, 5, 5, 656, 798, -108, sand


        self.characterNP.setH(45)
        self.characterNP.setCollideMask(BitMask32.allOn())
        self.world.attachCharacter(self.character)
        self.character.setGravity(22)

        self.actorNP = Actor('Resources/Models/ModelCollection/Actors/robot/lack.egg', {
            'run': 'Resources/Models/ModelCollection/Actors/robot/lack-run.egg',
            'idle': 'Resources/Models/ModelCollection/Actors/robot/lack-idle.egg',
            'land': 'Resources/Models/ModelCollection/Actors/robot/lack-land.egg',
            'damage': 'Resources/Models/ModelCollection/Actors/robot/lack-damage.egg',
            'jump': 'Resources/Models/ModelCollection/Actors/robot/lack-jump.egg'})

        self.actorNP.reparentTo(self.characterNP)
        self.actorNP.setScale(0.2)
        self.actorNP.setH(180)
        self.actorNP.setPos(0, 0, 0.4)
        self.actorNP.loop('idle')
        # animationspeed
        self.actorNP.setPlayRate(0.7, 'jump')
        self.actorNP.setPlayRate(0.7, 'land')

    def ATMRespawnTask(self, task):
        if self.characterNP.getZ() <= self.respawnZValue and self.respawning is False and self.playerLives > 1:
            self.respawnATM()
            #selector = random.randint(1, len(self.SFXfallRespawnDict))
            #self.playSfx(self.SFXfallRespawnDict[str(selector)])
        elif self.characterNP.getZ() <= self.respawnZValue and self.respawning is False and self.playerLives == 1:
            self.respawnATM()
        return task.cont

    def setUpStage3(self):
        self.generateStage("Stage/stage3.txt")
        self.generateHazard("Stage/stage3lava.txt")
        self.generateCoins("Stage/stage3coins.txt")
        self.generateBalls("Stage/stage3balls.txt")
        checkpointpos = Vec3(640, 391, -97)
        self.createCheckPoint(checkpointpos, "stage3-checkpoint-1")
        checkpointpos = Vec3(620, 476, -97)
        self.createCheckPoint(checkpointpos, "stage3-checkpoint-2")
        checkpointpos = Vec3(620, 598, -126)
        self.createCheckPoint(checkpointpos, "stage3-checkpoint-3")
        checkpointpos = Vec3(656, 843, -111)
        self.createCheckPoint(checkpointpos, "stage3-checkpoint-4")
        self.setUpStage3FirstObjective()
        self.setUpStage3SecondObjective()
        self.setUpStage3ThirdObjective()
        box = Box(1, 1, 1, 656, 795, -110, 'sage3invisiblethetowercheckpoint')
        invisible = self.createInvisibleBox(box)
        taskMgr.add(self.stage3InvisibleTowerCheckPoint, "stage3towerinvisiblecheckpoint", extraArgs=[invisible], appendTask=True)
        box = Box(1, 1, 1, 656, 850, -111, 'sage3invisiblethetowercheckpoint')
        invisible = self.createInvisibleBox(box)
        taskMgr.add(self.stage3LavaFloorIntiated, "stage3lavaprotocol", extraArgs=[invisible],
                    appendTask=True)
        self.setUpStage3FourthObjective()
        self.setUpStage3FifthObjective()
        checkpointpos = Vec3(656, 852, -64)
        self.createCheckPoint(checkpointpos, "stage3-checkpoint-5")
        checkpointpos = Vec3(655, 840, 11)
        self.createCheckPoint(checkpointpos, "stage3-checkpoint-6")

    def stage3InvisibleTowerCheckPoint(self, target, task):
        if self.characterNP.getDistance(target) <= 10:
            self.respawnPoint = (Vec3(656, 843, -111))
            taskMgr.add(self.musicFadeOut, 'musicFade', extraArgs=[self.BGM3], appendTask=True)
            return task.done
        return task.cont

    def stage3LavaFloorIntiated(self, target, task):
        if self.characterNP.getDistance(target) <= 12:
            self.SFXexterminate.play()
            self.towerExterminationProtocol = True
            box = Box(5, 5, 5, 656, 798, -108, 'BlockingExit')
            self.createBox(box, 'techno')
            self.playMusic(self.BGM4, looping=1, volume=0.1)
            if self.startFromStageThree:
                self.createPete()
            self.peteNP.setPos(650, 924, 64)
            taskMgr.add(self.peteStage3FinalDialogue, "gameoverDialogue")
            return task.done
        return task.cont

    def setUpStage3FirstObjective(self):
        name = "stage3-objective1-timed1"
        switchName = name + "switch"
        #2, 8, 0.2, 643, 500, -140, sand
        box = Box(2, 8, 0.2, 643, 500, -140, name)
        switch = self.createTimeSwitch(Vec3(640, 480, -130), switchName)
        self.timeObjectivesState[switchName] = False
        self.timeObjectivesState[name] = False
        taskMgr.add(self.createTimeObjectiveReverse, name, extraArgs=[box, 'sand', switch, 6, switchName, name],
                    appendTask=True)

    def setUpStage3SecondObjective(self):
        name = "stage3-objective2-timed2"
        switchName = name + "switch"
        # 1, 1, 0.5, 644, 598, -132, sand
        box = Box(1, 1, 0.5, 644, 598, -132, name)
        switch = self.createTimeSwitch(Vec3(622, 598, -129), switchName)
        self.timeObjectivesState[switchName] = False
        self.timeObjectivesState[name] = False
        taskMgr.add(self.createTimeObjectiveReverse, name, extraArgs=[box, 'sand', switch, 6, switchName, name],
                    appendTask=True)

    def setUpStage3ThirdObjective(self):
        name = "stage3-objective3-timed3"
        switchName = name + "switch"
        # 1, 1, 0.5, 644, 598, -132, sand
        box = Box(1, 1, 0.5, 656, 606, -132, name)
        switch = self.createTimeSwitch(Vec3(656, 600, -135), switchName)
        self.timeObjectivesState[switchName] = False
        self.timeObjectivesState[name] = False
        taskMgr.add(self.createTimeObjectiveReverse, name, extraArgs=[box, 'sand', switch, 6, switchName, name],
                    appendTask=True)

    def setUpStage3FourthObjective(self):
        name = "stage3-objective4-timed4"
        switchName = name + "switch"
        box = Box(3, 3, 3, 644, 828, -89, name)
        switch = self.createTimeSwitch(Vec3(688, 828, -95.5), switchName)
        self.timeObjectivesState[switchName] = False
        self.timeObjectivesState[name] = False
        taskMgr.add(self.createTimeObjectiveReverse, name, extraArgs=[box, 'sand', switch, 21, switchName, name],
                    appendTask=True)

    def setUpStage3FifthObjective(self):
        name = "stage3-objective5-timed4"
        switchName = name + "switch"
        box = Box(2, 2, 2, 656, 871, -81, name)
        switch = self.createTimeSwitch(Vec3(618, 873, -82.5), switchName)
        self.timeObjectivesState[switchName] = False
        self.timeObjectivesState[name] = False
        taskMgr.add(self.createTimeObjectiveReverse, name, extraArgs=[box, 'sand', switch, 8, switchName, name],
                    appendTask=True)

    def setUpStage2(self):
        self.generateStage("Stage/stage2.txt")
        self.generateBalls("Stage/stage2balls.txt")
        self.generateCoins("Stage/stage2coins.txt")
        self.generateHazard("Stage/stage2lava.txt")
        checkpointpos = Vec3(418, 375, 5)
        self.createCheckPoint(checkpointpos, "stage2-checkpoint-1")
        checkpointpos = Vec3(576, 319, 20)
        self.createCheckPoint(checkpointpos, "stage2-checkpoint-2")
        checkpointpos = Vec3(608, 399, 28)
        self.createCheckPoint(checkpointpos, "stage2-checkpoint-3")
        self.setUpStage2PeteInvisibleCheckPoint()
        self.setUpStage2FirstObjective()
        self.setUpStage2SecondObjective()

    def setUpStage2FirstObjective(self):
        #4, 4, 4, 640, 391, 18, sand
        name = "stage2-objective1-destroy"
        switchName = name + "switch"
        box = Box(4, 4, 4, 640, 391, 18, name)
        boxNP = self.createBox(box, 'sand', color='orange')
        switch = self.createTimeSwitch(Vec3(664, 391, 19), switchName)
        taskMgr.add(self.destroyBoxTask, name, extraArgs=[boxNP, switch], appendTask=True)

    def setUpStage2SecondObjective(self):
        #4, 4, 4, 656, 391, 16, sand
        name = "stage2-objective2-timed1"
        switchName = name + "switch"
        box = Box(4, 4, 4, 656, 391, 16, name)
        switch = self.createTimeSwitch(Vec3(668, 419, 48), switchName)
        self.timeObjectivesState[switchName] = False
        self.timeObjectivesState[name] = False
        taskMgr.add(self.createTimeObjectiveReverse, name, extraArgs=[box, 'sand', switch, 6, switchName, name],
                    appendTask=True)

    def destroyBoxTask(self, boxNP, switch, task):
        collision = self.world.contactTestPair(switch.node(), self.pete)
        if len(collision.getContacts()) > 0:
            boxNP.node().removeAllChildren()
            self.world.removeRigidBody(boxNP.node())
            self.SFXclick.play()
            return task.done
        return task.cont

    def setUpTransition2(self):
        self.generateStage("Stage/transition2.txt")
        box = Box(1, 1, 1, 640, 391, -10, 'invisibleCheckTransition2')
        self.setUpInvisibleClearUpCheckPoint(box, stage="stage2")

    def setUpTransition(self):
        self.generateStage("Stage/transition.txt")
        self.setUpTransitionFirstObjective()
        box = Box(1, 1, 1, 280, 335, 35, 'invisibleCheckTransition')
        self.setUpInvisibleClearUpCheckPoint(box)
        self.setUpInvisiblePeteCheckPoint()
        #if taskMgr.hasTaskNamed("firstPeteTask"):
        #    taskMgr.remove("firstPeteTask")
        taskMgr.add(self.peteTransitionTask, "peteTransitionTask")
        self.setUpTransitionSecondObjective()
        checkpointpos = Vec3(325, 335, 23)
        self.createCheckPoint(checkpointpos, "transition-checkpoint")
        #box = Box(2, 2, 2, 240, 335, 23, 'testingmoving')
        #self.createHazardBox(box, 'lava', 4, 0.02, 'x')

    def clearStage1Tasks(self):
        taskList = taskMgr.getAllTasks()
        for task in taskList:
            if task.name == "coinTask":
                taskMgr.remove(task.name)
            if "stage1" in task.name:
                taskMgr.remove(task.name)
            if 'name' in task.name:
                taskMgr.remove(task.name)
            if task.name == "peteGrandPillarRespawn":
                taskMgr.remove(task.name)
        nodeList = self.render.getChildren()
        for node in nodeList:
            if "stage1" in node.getName():
                node.node().removeAllChildren()
                self.world.removeRigidBody(node.node())
        #taskList = taskMgr.getAllTasks()
        #for task in taskList:
            #print task.name
        self.setUpStage2()

    def clearStage2Tasks(self):
        taskList = taskMgr.getAllTasks()
        for task in taskList:
            if task.name == "coinTask":
                taskMgr.remove(task.name)
            if task.name == "ballRespawn":
                taskMgr.remove(task.name)
            if "hazard" in task.name:
                taskMgr.remove(task)
            if "stage2" in task.name:
                taskMgr.remove(task)
            if "transition-objective1" in task.name:
                taskMgr.remove(task)
        nodeList = self.render.getChildren()
        for node in nodeList:
            if "stage2" in node.getName() or "transition-objective1" in node.getName():
                node.node().removeAllChildren()
                self.world.removeRigidBody(node.node())
            if "transition" in node.getName():
                if "transition2" in node.getName():
                    pass
                else:
                    node.node().removeAllChildren()
                    self.world.removeRigidBody(node.node())
        #taskList = taskMgr.getAllTasks()
        #for task in taskList:
        #    print task.name
        self.setUpStage3()
        myFog = Fog("Fog Name")
        myFog.setColor(0.5, 0.5, 0.5)
        myFog.setExpDensity(0.02)
        render.setFog(myFog)

    def setUpTransitionFirstObjective(self):
        name = "transition-objective1"
        switchName = name + "switch"
        box = Box(0.5, 20, 14.5, 250, 335, 35, name)
        switch = self.createTimeSwitch(Vec3(230, 335, 20.5), switchName)
        self.timeObjectivesState[switchName] = False
        self.timeObjectivesState[name] = False
        taskMgr.add(self.createTimeObjective, name, extraArgs=[box, 'sand', switch, 5, switchName, name],
                    appendTask=True)

    def setUpTransitionSecondObjective(self):
        box = Box(0.5, 20, 14.5, 330, 335, 35, "transition-unlockdoor1")
        target = self.createBox(box, 'sand', color="teal")
        name = "transition-objective1"
        switchName = name + "switch"
        switch2Name = name + "switch2"
        switch = self.createTimeSwitch(Vec3(300, 327, 20.5), switchName)
        switch2 = self.createTimeSwitch(Vec3(300, 343, 20.5), switch2Name)
        self.timeObjectivesState[switchName] = False
        self.timeObjectivesState[name] = False
        taskMgr.add(self.objectiveDestroyBoxTwoSwitches, name, extraArgs=[switch2, switch, target],
                    appendTask=True)

    def setUpInvisibleClearUpCheckPoint(self, box, stage="stage1"):
        #box = Box(1, 1, 1, 280, 335, 35, 'invisibleCheckTransition')
        invisible = self.createInvisibleBox(box)
        taskMgr.add(self.invisibleClearUpTask, "invisibleClearUp", extraArgs=[invisible, stage], appendTask = True)

    def invisibleClearUpTask(self, target, stage, task):
        if self.characterNP.getDistance(target) <= 26:
            if stage == "stage1":
                self.clearStage1Tasks()
                taskMgr.add(self.musicFadeOut, 'musicFade', extraArgs=[self.BGM1], appendTask=True)
                #taskMgr.add(self.musicFadeOut, 'musicFade')
            if stage == "stage2":
                self.respawnZValue = -150
                self.respawnPoint = Vec3(640, 391, -0)
                self.clearStage2Tasks()
                taskMgr.add(self.musicFadeOut, 'musicFade', extraArgs=[self.BGM2], appendTask = True)
                self.playMusic(self.BGM3, looping=1, volume=0.1)
            #also set the new shit here
            return task.done
        return task.cont

    def musicFadeOut(self, BGM, task):
        if task.time > 2:
            BGM.stop()
            return task.done
        elif task.time > 1.8:
            BGM.setVolume(0.01)
        elif task.time > 1.6:
            BGM.setVolume(0.02)
        elif task.time > 1.4:
            BGM.setVolume(0.03)
        elif task.time > 1.2:
            BGM.setVolume(0.04)
        elif task.time > 1:
            BGM.setVolume(0.05)
        elif task.time > 0.8:
            BGM.setVolume(0.06)
        elif task.time > 0.6:
            BGM.setVolume(0.07)
        elif task.time > 0.4:
            BGM.setVolume(0.08)
        elif task.time > 0.2:
            BGM.setVolume(0.09)
        return task.cont

    def setUpStage1(self):
        self.generateStage("Stage/stage1.txt")
        self.generateCoins("Stage/stage1coins.txt")
        self.generateSlide("Stage/stage1slide.txt")
        self.setUpStage1FirstObjective()
        self.setUpStage1SecondObjective()
        self.setUpStage1ThirdObjective()
        self.setUpStage1FourthObjective()
        self.setUpStage1FifthObjective()
        #4, 0.2, 1.2, -17, 315, 19.8, sand
        #5, 5, 12, -2, 290, 30, sand
        box = Box(5, 5, 12, -2, 290, 30, "stage1-objective6-timed")
        switchVec = Vec3(-3, 270, 18.5)
        self.timeObjectiveReverseGeneral(box, "stage1-objective6-timed", switchVec, 31)
        #2, 8, 0.2, 48, 290, 36, sand
        box = Box(2, 8, 0.2, 48, 290, 36, "stage1-objective7-timed")
        switchVec = Vec3(44, 268, 36.2)
        self.timeObjectiveReverseGeneral(box, "stage1-objective7-timed", switchVec, 8)
        #14, 5, 0.5, -3, 253, 43, sand
        box = Box(14, 5, 0.5, -3, 253, 43, "stage1-objective8-timed")
        switchVec = Vec3(24, 247, 43.2)
        self.timeObjectiveReverseGeneral(box, "stage1-objective8-timed", switchVec, 14)
        self.setUpStage1SixthObjective()
        self.setUpStage1SeventhObjective()
        box = Box(6, 6, 6, 26.5, 316, 46, 'stage1invisiblecheckpoint1')
        invisibleBox = self.createInvisibleBox(box)
        taskMgr.add(self.setUpStage1InvisibleCheckPoint, "stage1invisiblecheckpoint1", extraArgs=[invisibleBox], appendTask = True)
        self.setUpStage1EigthObjective()

        #checkpoints
        checkpointpos = Vec3(26, 171, 3)
        self.createCheckPoint(checkpointpos, 'stage1-checkpoint-1')
        checkpointpos = Vec3(26, 383, -20)
        self.createCheckPoint(checkpointpos, 'stage1-checkpoint-2')
        checkpointpos = Vec3(100,395,22)
        self.createCheckPoint(checkpointpos, "stage1-checkpoint-3")
        checkpointpos = Vec3(160, 335, 22)
        self.createCheckPoint(checkpointpos, "stage1-checkpoint-4")

    def setUpStage1FirstObjective(self):
        box = Box(1, 5, 8, -4, 76, 8, "stage1-objective1-unlockdoor1")
        target = self.createBox(box, 'sand', color="teal")
        objectiveTest = Box(2, 3.5, 0.5, 28, 36, -1, "stage1-objblock-1")
        keyBallPosition = Vec3(3, 54, 2)
        stage1Objective1 = self.createObjective(objectiveTest, 'stage1-objective-1', self.stage1Objective,
                                                keyBallPosition, test=False)
        taskMgr.add(self.objectiveDestroyBox, 'name', extraArgs=[stage1Objective1[0], stage1Objective1[1], target], appendTask=True)

    def setUpStage1SecondObjective(self):
        #2, 1, 1.75, -10, 69, 1.75, sand
        box = Box(2, 1, 2.75, -10, 69, 2.75, "stage1-objective2-unlockdoor1")
        target = self.createBox(box, 'sand', color="teal")
        #1, 2, 1, -67, 85, -1, brick
        objectiveTest = Box(1, 2, 1, -67, 85, -1, "stage1-objblock-2")
        keyBallPosition = Vec3(-28, 67, 14)
        stage1Objective1 = self.createObjective(objectiveTest, 'stage1-objective-2', self.stage1Objective,
                                                keyBallPosition, test=False)
        taskMgr.add(self.objectiveDestroyBox, 'name', extraArgs=[stage1Objective1[0], stage1Objective1[1], target],
                    appendTask=True)

    def setUpStage1ThirdObjective(self):
        #10, 1, 9, -15, 125, 10, sand
        name = "stage1-objective3-timed1"
        switchName = name + "switch"
        box = Box(10, 1, 9, -15, 125, 10, name)
        switch = self.createTimeSwitch(Vec3(-18, 55, 1), switchName)
        self.timeObjectivesState[switchName] = False
        self.timeObjectivesState[name] = False
        taskMgr.add(self.createTimeObjective, name, extraArgs=[box, 'sand', switch, 11, switchName, name], appendTask = True)

    def setUpStage1FourthObjective(self):
        #2, 2, 1, 60, 163, 16, sand
        #95, 177, 10
        name = "stage1-objective4-timed1"
        switchName = name + "switch"
        box = Box(2, 2, 1, 60, 163, 16, name)
        switch = self.createTimeSwitch(Vec3(95, 177, 8.5), switchName)
        self.timeObjectivesState[switchName] = False
        self.timeObjectivesState[name] = False
        taskMgr.add(self.createTimeObjectiveReverse, name, extraArgs=[box, 'sand', switch, 21, switchName, name],
                    appendTask=True)

    def setUpStage1FifthObjective(self):
        #1, 1, 0.2, 62, 170, 34.5, sand
        #6, 20, 0.2, -12, 200, 0, sand
        name = "stage1-objective5-timed1"
        switchName = name + "switch"
        box = Box(6, 20, 0.2, -12, 200, 0, name)
        switch = self.createTimeSwitch(Vec3(62, 170, 34.5), switchName)
        self.timeObjectivesState[switchName] = False
        self.timeObjectivesState[name] = False
        taskMgr.add(self.createTimeObjectiveReverse, name, extraArgs=[box, 'sand', switch, 16, switchName, name],
                    appendTask=True)

    def setUpStage1SixthObjective(self):
        #5.5, 1, 4, 26.5, 316, 46, sand
        box = Box(5.5, 1, 4, 26.5, 316, 46, "stage1-objective9-unlockdoor1")
        target = self.createBox(box, 'sand', color = "teal")
        #3, 1, 1, 45, 243, 17, sand
        objectiveTest = Box(3, 1, 1, 45, 243, 17, "stage1-objblock-9")
        keyBallPosition = Vec3(46, 311, 39)
        stage1Objective1 = self.createObjective(objectiveTest, 'stage1-objective-9', self.stage1Objective,
                                                keyBallPosition, test=False)
        taskMgr.add(self.objectiveDestroyBox, 'name', extraArgs=[stage1Objective1[0], stage1Objective1[1], target],
                    appendTask=True)

    def setUpStage1SeventhObjective(self):
        # 0.5, 3, 1, -25.5, 383, -14, sand
        name = "stage1-objective10-unlockdoor1-task"
        box = Box(0.5, 3, 1, -25.5, 383, -14, "stage1-objective10-unlockdoor1")
        target = self.createBox(box, 'sand', color="teal")
        # 1, 5, 0.5, -28, 383, -24.5, sand
        objectiveTest = Box(1, 5, 0.5, -28, 383, -24.5, "stage1-objblock-10")
        keyBallPosition = Vec3(-25, 311, 42)
        stage1Objective1 = self.createObjective(objectiveTest, 'stage1-objective-10', self.stage1Objective,
                                                keyBallPosition, test=False)
        taskMgr.add(self.objectiveDestroyBox, name, extraArgs=[stage1Objective1[0], stage1Objective1[1], target],
                    appendTask=True)

    def setUpStage1EigthObjective(self):
        name = "stage1-objective9-timed1"
        switchName = name + "switch"
        box = Box(1, 16, 15, 130, 335, 20, name)
        switch = self.createTimeSwitch(Vec3(103, 335, 20), switchName)
        self.timeObjectivesState[switchName] = False
        self.timeObjectivesState[name] = False
        taskMgr.add(self.createTimeObjective, name, extraArgs=[box, 'sand', switch, 18, switchName, name],
                    appendTask=True)

    def setUpStage1InvisibleCheckPoint(self, box, task):
        collision = self.world.contactTestPair(box.node(), self.character)
        if len(collision.getContacts()) > 0:
            self.peteInteractions["grandPillarSpawn"] = True
            return task.done
        return task.cont

    def objectiveDestroyBoxTwoSwitches(self, switch1, switch2, target, task):
        collisions = self.world.contactTestPair(switch1.node(), self.character)
        collisions2 = self.world.contactTestPair(switch2.node(), self.pete)
        if len(collisions.getContacts()) > 0 and len(collisions2.getContacts()) > 0:
            self.playSfx(self.SFXclick)
            target.node().removeAllChildren()
            self.world.removeRigidBody(target.node())
            self.peteInteractions["transitionDoubleSwitchDoorUnlocked"] = True
            taskMgr.remove("background")
            self.env.removeNode()
            self.env = loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/bg/PeachSky.egg')
            self.env.reparentTo(render)
            self.env.setScale(3)
            self.plight = PointLight('plight')
            self.plnp = self.render.attachNewNode(self.plight)
            self.env.setLight(self.plnp)
            self.plnp.setPos(self.characterNP.getPos())
            self.playMusic(self.BGM2, looping=1, volume=0.1)
            taskMgr.add(self.backgroundTask, "background", extraArgs=[True], appendTask=True)
            return task.done
        else:
            return task.cont

    def timeObjectiveReverseGeneral(self, boxIn, name, switchVec, time):
        switchName = name + "switch"
        box = boxIn
        switch = self.createTimeSwitch(switchVec, switchName)
        self.timeObjectivesState[switchName] = False
        self.timeObjectivesState[name] = False
        taskMgr.add(self.createTimeObjectiveReverse, name, extraArgs=[box, 'sand', switch, time, switchName, name],
                    appendTask=True)

    def createTimeObjectiveReverse(self, box, modelName, switch, time, switchName, name, task):
        collision = self.world.contactTestPair(switch.node(), self.character)
        if len(collision.getContacts()) > 0 and self.timeObjectivesState[switchName] is False:
            self.timeObjectivesState[switchName] = True
            target = self.createBox(box, modelName, color="blue")
            taskMgr.add(self.displayRemainingTime, name + "timer", extraArgs=[time], appendTask = True)
            taskMgr.doMethodLater(time, self.destroyTimeCreatedBox, switchName + "destroy", extraArgs=[target, switchName], appendTask = True)
        return task.cont

    def destroyTimeCreatedBox(self, target, switchName, task):
        target.node().removeAllChildren()
        self.world.removeRigidBody(target.node())
        self.timeObjectivesState[switchName] = False
        return task.done

    def displayRemainingTime(self, time, task):
        timeLeft = int(time - task.time)
        self.textTimeAlert.setText(str(timeLeft))
        if timeLeft <= 3:
            self.textTimeAlert.setFg((1, 0, 0, 1))
            self.SFXticktock.setPlayRate(1.4)
        else: self.SFXticktock.setPlayRate(1)
        if self.SFXticktock.status() != self.SFXticktock.PLAYING:
            self.SFXticktock.play()
        if task.time >= time:
            if self.SFXticktock.status() == self.SFXticktock.PLAYING:
                self.SFXticktock.stop()
            self.textTimeAlert.setFg((1, 1, 1, 1))
            self.textTimeAlert.setText("")
            return task.done
        return task.cont

    def createTimeObjective(self, box, modelName, switch, time, objectiveSwitchName, name, task):
        if self.timeObjectivesState[name] is False:
            self.timeObjectivesState[name] = True
            target = self.createBox(box, modelName, color="orange")
            taskMgr.add(self.timeObject, objectiveSwitchName, extraArgs=[target, switch, time, objectiveSwitchName, name], appendTask=True)
            self.timeObjectivesState[objectiveSwitchName] = False
        return task.cont

    def timeObject(self, target, switch, time, switchName, name, task):
        collision = self.world.contactTestPair(switch.node(), self.character)
        if len(collision.getContacts()) > 0 and self.timeObjectivesState[switchName] is False:
            self.playSfx(self.SFXclick)
            self.timeObjectivesState[switchName] = True
            target.node().removeAllChildren()
            self.world.removeRigidBody(target.node())
            taskMgr.add(self.timeObjectiveTimerRespawn, switchName + "timer", extraArgs=[time, name], appendTask=True)
            return task.done
        return task.cont

    def timeObjectiveTimerRespawn(self, time, name, task):
        timeLeft = int(time - task.time)
        self.textTimeAlert.setText(str(timeLeft))
        if timeLeft <= 7 and self.peteInteractions["bookIt"]:
            self.peteInteractions["bookIt"] = False
            self.textMessageSpeak("Talking Panda: You're not gonna make it!", line2="Hold [SHIFT] and BOOK IT!")
            taskMgr.doMethodLater(6, self.textMessageClearTask, "textMessageClearTask")
        if self.SFXticktock.status() != self.SFXticktock.PLAYING:
            self.SFXticktock.play()
        if timeLeft <= 3:
            self.textTimeAlert.setFg((1,0,0,1))
            self.SFXticktock.setPlayRate(1.4)
        else: self.SFXticktock.setPlayRate(1)
        if task.time >= time:
            self.textTimeAlert.setText("")
            self.textTimeAlert.setFg((1, 1, 1, 1))
            self.timeObjectivesState[name] = False
            self.SFXticktock.stop()
            return task.done
        return task.cont

    def createTimeSwitch(self, pos, name):
        boxSize = Vec3(1, 1, 0.2)
        shape = BulletBoxShape(boxSize)
        boxNP = self.render.attachNewNode(BulletRigidBodyNode(name))
        boxNP.node().addShape(shape)
        boxNP.setPos(pos)
        boxNP.setCollideMask(BitMask32.allOff())
        self.world.attachRigidBody(boxNP.node())
        boxModelNP = self.loadModel('sand')
        boxModelNP.reparentTo(boxNP)
        boxModelNP.setPos(0, 0, - boxSize.z)
        boxModelNP.setScale(boxSize.x * 2, boxSize.y * 2, boxSize.z * 2)
        return boxNP

    def createObjective(self, box, name, tracker, ballPos, test=False):
        boxSize = box.getSize()
        shape = BulletBoxShape(boxSize)
        boxNP = self.render.attachNewNode(BulletRigidBodyNode(box.getModel()))
        boxNP.node().addShape(shape)
        boxNP.setPos(box.getPosition())
        boxNP.setCollideMask(BitMask32.allOff())
        self.world.attachRigidBody(boxNP.node())
        if test:
            boxModelNP = self.loadModel('brick')
            boxModelNP.reparentTo(boxNP)
            boxModelNP.setPos(0, 0, - boxSize.z)
            boxModelNP.setScale(boxSize.x * 2, boxSize.y * 2, boxSize.z * 2)

        sphere = self.addBall(1, name, ballPos.x, ballPos.y, ballPos.z, 1)
        result = [boxNP, sphere]
        return result

    def objectiveDestroyBox(self, box, sphere, target, task):
        collisions = self.world.contactTestPair(box.node(), sphere.node())
        #print len(collisions.getContacts())
        #if box.getDistance(sphere) <= 3:
        if len(collisions.getContacts()) > 0:
            # self.updateLife(1)
            self.playSfx(self.SFXclick)
            #self.playMusic(self.BGM2, looping=1, volumne = 0.4)
            target.node().removeAllChildren()
            self.world.removeRigidBody(target.node())
            self.peteInteractions["doorDestroyed"] = True
            # boxNP.node().removeAllChildren()
            # self.world.removeRigidBody(boxNP.node())
            return task.done
        else:
            return task.cont

    def backgroundTask(self, centerLight, task):
        if centerLight:
            self.plnp.setPos(self.characterNP.getPos())
        self.env.setPos(self.characterNP.getPos())
        self.env.setZ(self.env.getZ() + 200)
        return task.cont

    def setup(self):

        # World
        self.debugNP = self.render.attachNewNode(BulletDebugNode('Debug'))
        #self.debugNP.show()

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.setDebugNode(self.debugNP.node())

        self.createATM()
        self.createPete()

        #generate the stages
        if self.startFromStageOne:
            self.setUpStage1()
            self.setUpTransition()
            self.setUpTransition2()
            self.playMusic(self.BGM1, looping=1, volume=0.1)
        elif self.startFromStageTwo:
            self.setUpStage1()
            self.setUpTransition()
            self.setUpTransition2()
            self.playMusic(self.BGM1, looping=1, volume=0.1)
        elif self.startFromStageThree:
            self.setUpTransition2()
        taskMgr.add(self.ATMRespawnTask, 'ATMrespawnTask')
        # Floor
        # shape = BulletPlaneShape(Vec3(0, 0, 1), 0)

        #positionMP = Vec3(4, -6, 5)
        #self.createMovingPlatform(3, 3, 1, positionMP, 'moving playform 1')
        #taskMgr.add(self.movingPlatformTestTask, 'testingMove', extraArgs=[positionMP], appendTask = True)
        # Stair
        origin = Point3(2, 0, 0)
        size = Vec3(2, 4.75, 1)
        shape = BulletBoxShape(size * 0.55)
        '''
        for i in range(9):
            pos = origin + size * i
            pos.setY(0)
            stairNP = self.render.attachNewNode(BulletRigidBodyNode('Stair%i' % i))
            stairNP.node().addShape(shape)
            stairNP.setPos(pos)
            stairNP.setCollideMask(BitMask32.allOn())

            modelNP = loader.loadModel('models/box.egg')
            modelNP.reparentTo(stairNP)
            # modelNP.setPos(0, 0, 0)
            modelNP.setPos(-size.x / 2.0, -size.y / 2.0, -size.z / 2.0)
            modelNP.setScale(size)
            self.world.attachRigidBody(stairNP.node())
        for i in range(9):
            pos = origin + size * i
            pos.setY(0)
            pos.setX(pos.getX() * -1)
            stairNP = self.render.attachNewNode(BulletRigidBodyNode('Stair%i' % i))
            stairNP.node().addShape(shape)
            stairNP.setPos(pos)
            stairNP.setCollideMask(BitMask32.allOn())

            modelNP = loader.loadModel('models/box.egg')
            modelNP.reparentTo(stairNP)
            modelNP.setPos(-size.x / 2.0, -size.y / 2.0, -size.z / 2.0)
            modelNP.setScale(size)

            self.world.attachRigidBody(stairNP.node())
        '''

        #background
        #self.env = loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/bg/PeachSky.egg')
        self.env = env = loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/bg/celestial.egg')
        self.env.reparentTo(render)
        self.env.setP(90)
        self.env.setScale(3)

        taskMgr.add(self.backgroundTask, "background", extraArgs=[False], appendTask=True)

        if self.startFromStageThree:
            self.env.removeNode()
            self.env = loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/bg/PeachSky.egg')
            self.env.reparentTo(render)
            self.env.setScale(3)
            self.plight = PointLight('plight')
            self.plnp = self.render.attachNewNode(self.plight)
            self.env.setLight(self.plnp)
            self.plnp.setPos(self.characterNP.getPos())


game = CharacterController()
game.run()
