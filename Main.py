from math import sin, cos
import sys
import time
from direct.showbase.ShowBase import ShowBase

from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState

from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import BitMask32
from panda3d.core import NodePath
from panda3d.core import PandaNode
from panda3d.core import TextNode

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletHelper
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import BulletHeightfieldShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletSoftBodyNode
from panda3d.bullet import BulletSoftBodyConfig
from panda3d.bullet import ZUp
from direct.gui.OnscreenText import OnscreenText

from math import pi, sin, cos
from Box import *

class CharacterController(ShowBase):
    def __init__(self):

        ShowBase.__init__(self)
        self.loadSounds()
        self.setupLights()
        # Input
        self.accept('escape', self.doExit)
        self.accept('r', self.doReset)
        self.accept('f3', self.toggleDebug)
        #self.accept('space', self.doJump)
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

        self.setup()
        base.setBackgroundColor(0.1, 0.1, 0.8, 1)
        base.setFrameRateMeter(True)
        base.disableMouse()
        #base.camera.setPos(self.characterNP.getX(), self.characterNP.getY() + 10, 4)
        # base.camera.setHpr(self.characterNP.getHpr())
        base.camera.lookAt(self.characterNP)
        # Create a floater object.  We use the "floater" as a temporary
        # variable in a variety of calculations.
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

        #ATM state
        self.isMoving = False
        self.isJumping = False
        self.isLanding = False
        self.isDashJumping = False
        self.isRunningAndJumping = False
        self.isRunningAndJumpingAndLanding = False
        self.isLandedFromRun = False

        #animation switches
        self.firstSpawned = True
        self.animationRunning = False
        self.animationDashing = False
        self.animationIdle = False
        self.animationLanding = False
        self.landingAnimation = False
        self.isDashing = False
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
        self.peteIdentifer = 0
        self.peteTaskAssigned = False
        self.peteFirstTaskUnknownSFX = False


        #checkpoint
        self.checkPointTouched = False
        self.respawnPoint = Vec3(self.characterNP.getX(), self.characterNP.getY(), self.characterNP.getZ())
        self.respawning = False

        #On Screen Texts
        self.helpHudOn = False
        self.HUDTexts = []
        self.helpTexts = []
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

        #movingplatforms

        #Music & Sounds
        #self.BGM1 = self.loadMusic("Resources/BGM/Bramble Blast.mp3")
        #self.playMusic(self.BGM1, looping=1)
        #self.SFXjump = self.loadSfx("Resources/Sound/Jump.mp3")
        #self.SFXdashjump = self.loadSfx("Resources/Sound/Dash Jump.mp3")
        #self.SFXRun = self.loadSfx("Resources/Sound/running.mp3")

    #Stage1Stuff
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
                self.createBox(box, model)

    def appendToStage(self, x, y, z, px, py, pz, name):
        box = Box(x, y, z, px, py, pz, name)
        self.stage1.append(box)

    def loadSounds(self):
        #BGM
        self.BGM1 = self.loadMusic("Resources/BGM/Bramble Blast.mp3")
        self.BGM2 = self.loadMusic("Resources/BGM/Bramble Blast (Remix).mp3")
        self.playMusic(self.BGM1, looping=1)

        #sound effects
        self.SFXjump = self.loadSfx("Resources/Sound/Jump.mp3")
        self.SFXdashjump = self.loadSfx("Resources/Sound/Dash Jump.mp3")
        self.SFXpop = self.loadSfx("Resources/Sound/Pop.mp3")
        self.SFXclick = self.loadSfx("Resources/Sound/Click.mp3")
        self.SFXlifeUp = self.loadSfx("Resources/Sound/Life Up.wav")

        #voice
        self.SFXunknown = self.loadSfx("Resources/Voice/unknown.wav")

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
            OnscreenText(text="[F8] : Respawn at Checkpoint", style=1, fg=(1, 1, 1, 1), pos=(-1.3, 0.10),
                         align=TextNode.ALeft,
                         scale=0.06))

    def displayHUD(self):
        lifeMsg = "Lives: " + str(self.playerLives)
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
        self.playerScore += amount
        scoreMsg = "Score: " + str(self.playerScore)
        self.HUDTexts[1].setText(scoreMsg)

    def updateLife(self, amount):
        if amount > 0:
            self.playSfx(self.SFXlifeUp)
        self.playerLives += amount
        lifeMsg = "Lives: " + str(self.playerLives)
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
        self.character.setMaxJumpHeight(6.0)
        self.character.setJumpSpeed(11.0)
        if self.character.isOnGround():
            self.playSfx(self.SFXjump)
            self.actorNP.play('jump')
            self.animationDashing = False
            self.animationRunning = False
            self.animationIdle = False
            #self.isLanding = True
        self.character.doJump()

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
        if (inputState.isSet('forward') is False) and (inputState.isSet('reverse') is False) and self.character.isOnGround() and self.animationIdle is False and self.isLanding is False:
            self.actorNP.loop('idle')
            self.animationIdle = True
            self.animationRunning = False
            self.animationDashing = False
            self.landingAnimation = False
        if self.character.isOnGround() is False and self.isLanding is False:
            self.isLanding = True
        if self.character.isOnGround() and self.animationLanding is False and self.isLanding:
            self.animationLanding = True
            taskMgr.add(self.landingAnimationTask, 'LandingAnimation')
        #dashing and running on ground

        if (inputState.isSet("forward") or inputState.isSet('reverse')):
            if inputState.isSet('dash'):
                if self.character.isOnGround():
                    speed.setY(speedForce * 2)
                if self.animationDashing is False and self.character.isOnGround() and self.isLanding is False:
                    self.actorNP.setPlayRate(1.5, 'run')
                    self.actorNP.loop('run')
                    self.landingAnimation = False
                    self.animationDashing = True
                    self.animationRunning = False
                    self.animationIdle = False
                    self.isDashJumping = True
                if inputState.isSet('dashJump') and self.isDashJumping:
                    speed.setY(speedForce * 2)
                    self.doJump()
            else:
                self.isDashJumping = False
                speed.setY(speedForce)
                self.actorNP.setPlayRate(1, 'run')
                if self.animationRunning is False and self.character.isOnGround() and self.isLanding is False:
                    self.actorNP.loop('run')
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
        if inputState.isSet('autoCameraOn'): self.cameraAutoTurn = True
        if inputState.isSet('autoCameraOff'): self.cameraAutoTurn = False
        self.character.setAngularMovement(omega)
        self.character.setLinearMovement(speed, True)
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
            self.respawning = True
            self.updateLife(-1)
            taskMgr.doMethodLater(3, self.checkPointRespawnTask, 'manual respawn')
            self.characterNP.setPos(self.respawnPoint)

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

        # If the camera is too far from ralph, move it closer.
        # If the camera is too close to ralph, move it farther.
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
        if self.peteIsActive and self.peteTaskAssigned is False:
            self.peteTaskAssigned = True
            taskMgr.add(self.peteFirstTask, 'firstPeteTask')

        #checkpoints
        if self.checkPointTouched is False and self.checkpoint.getDistance(self.characterNP) <= 2:
            self.checkPointTouched = True
            taskMgr.add(self.checkPointSpinTask, 'checkpoint1task', extraArgs=[self.checkpoint], appendTask = True)
            self.respawnPoint = self.checkpointPhysical.getPos()


        self.floater.setPos(self.characterNP.getPos())
        self.floater.setZ(self.characterNP.getZ() + 1.0)
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
        self.world = None
        self.render.removeNode()

    def setupLights(self):
        # Light
        alight = AmbientLight('ambientLight')
        alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
        alightNP = render.attachNewNode(alight)

        dlight = DirectionalLight('directionalLight')
        dlight.setDirection(Vec3(1, 1, -1))
        dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
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

    def addBall(self, radius, name, x, y, z, mass):
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
        return sphere

    def createCoin(self, pos, name):
        shape = BulletSphereShape(3)
        node = BulletRigidBodyNode(name)
        node.setMass(0)
        node.addShape(shape)
        coin = self.render.attachNewNode(node)
        coin.setPos(pos)
        smileyFace = self.loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/smiley/smiley.egg')
        smileyFace.reparentTo(coin)
        smileyFace.setScale(1)
        taskMgr.add(self.coinSpinTask, "coinTask1", extraArgs=[coin, smileyFace, node], appendTask = True)

    def coinSpinTask(self, coin, coinPos, node, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        # self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        coin.setHpr(angleDegrees * 15, 0, 0)
        if coinPos.getDistance(self.characterNP) <= 2:
            node.removeAllChildren()
            self.updateScore(100)
            self.playSfx(self.SFXpop)
            return task.done
        return task.cont

    def createSlide(self, box, h, modelName):
        boxSize = box.getSize()
        shape = BulletBoxShape(boxSize)
        boxNP = self.render.attachNewNode(BulletRigidBodyNode(box.getModel()))
        boxNP.node().addShape(shape)
        boxNP.setR(-50)
        boxNP.setH(h)
        boxNP.setPos(box.getPosition())
        boxNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(boxNP.node())

        boxModelNP = self.loadModel(modelName)
        boxModelNP.reparentTo(boxNP)
        boxModelNP.setPos(0, 0, - boxSize.z)
        boxModelNP.setScale(boxSize.x * 2, boxSize.y * 2, boxSize.z * 2)

    def createBox(self, box, modelName):
        boxSize = box.getSize()
        shape = BulletBoxShape(boxSize)
        boxNP = self.render.attachNewNode(BulletRigidBodyNode(box.getModel()))
        boxNP.node().addShape(shape)
        boxNP.setPos(box.getPosition())
        boxNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(boxNP.node())

        #boxModelNP = loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-sand/brick.egg')
        boxModelNP = self.loadModel(modelName)
        if boxModelNP == "No model under that name":
            pass
        else:
            boxModelNP.reparentTo(boxNP)
            boxModelNP.setPos(0, 0, - boxSize.z)
            boxModelNP.setScale(boxSize.x * 2, boxSize.y * 2, boxSize.z * 2)
        return boxNP
        # boxNP.node().removeAllChildren()
        # self.world.removeRigidBody(boxNP.node())

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
        else:
            print modelName
            return "No model under that name"

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

    def createMovingPlatform(self, x, y, z, pos, name):
        boxSize = Vec3(x,y,z)
        shape = BulletBoxShape(boxSize)
        #boxNP = BulletGhostNode(name)
        boxNP = BulletRigidBodyNode(name)
        boxNP.setMass(99999999999)
        boxNP.addShape(shape)
        boxNP.setGravity(Vec3(0,0,0))
        box = self.render.attachNewNode(boxNP)
        box.setPos(pos)
        #box.setCollideMask(BitMask32.allOff())
        self.world.attachRigidBody(boxNP)
        #self.world.attachGhost(boxNP)
        self.movingPlatformTest = boxNP
        self.movingPlatformTestModel = box
        #self.world.removeRigidBody(boxNP)

    def movingPlatformTestTask(self, startPos, task):
        #speed = Vec3(0, 0.1, 0.2)
        self.movingPlatformTest.setLinearVelocity(Vec3(0, 1, 0))
        return task.cont

    def createCheckPoint(self, pos, name):
        boxSize = Vec3(0, 0, 0)
        shape = BulletBoxShape(boxSize)
        boxNP = self.render.attachNewNode(BulletRigidBodyNode(name))
        boxNP.node().addShape(shape)
        boxNP.setPos(pos)
        boxNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(boxNP.node())

        boxModelNP = loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/spinner/spinner.egg')
        boxModelNP.reparentTo(boxNP)
        boxModelNP.setPos(0, 0, 0)
        boxModelNP.setScale(0.2, 0.2, 0.4)
        self.checkpoint = boxModelNP
        self.checkpointPhysical = boxNP

    def checkPointSpinTask(self, checkPoint, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        #self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        checkPoint.setHpr(angleDegrees * 100, 0, 0)
        return task.cont

    def checkPointRespawnTask(self, task):
        self.respawning = False
        return task.done

    def createPete(self):
        h = 1
        w = 1.4
        shape = BulletCapsuleShape(w, h/2, ZUp)

        self.pete = BulletCharacterControllerNode(shape, 0.4, 'Pete')
        #    self.character.setMass(1.0)
        self.peteNP = self.render.attachNewNode(self.pete)
        self.peteNP.setPos(-10, 60, 10)
        self.peteNP.setH(45)
        self.peteNP.setCollideMask(BitMask32.allOn())
        self.world.attachCharacter(self.pete)

        self.peteActorNP = Actor('Resources/Models/ModelCollection/Actors/panda/panda-model.egg', {
            'walk': 'Resources/Models/ModelCollection/Actors/panda/panda-walk4.egg'})

        self.peteActorNP.reparentTo(self.peteNP)
        self.peteActorNP.setScale(0.0035)
        self.peteActorNP.setH(180)
        self.peteActorNP.setPos(0, 0, -1.45)
        self.peteActorNP.loop('walk')

        self.peteIdentifer = 1
        self.peteIsActive = True

    def peteFirstTask(self, task):
        if self.peteActorNP.getDistance(self.characterNP) <= 10:
            self.peteActorNP.lookAt(self.characterNP)
            self.peteActorNP.setHpr(self.peteActorNP.getH() + 180, 0, 0)
            if self.peteFirstTaskUnknownSFX is False:
                self.peteFirstTaskUnknownSFX = True
                self.playSfx(self.SFXunknown)
        return task.cont

    def createATM(self):
        h = 4.25
        w = .6
        shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

        self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
        #self.character.Node().setMass(1.0)
        self.characterNP = self.render.attachNewNode(self.character)
        self.characterNP.setPos(11, 50, 5)
        self.characterNP.setH(45)
        self.characterNP.setCollideMask(BitMask32.allOn())
        self.world.attachCharacter(self.character)

        self.actorNP = Actor('Resources/Models/ModelCollection/Actors/robot/lack.egg', {
            'run': 'Resources/Models/ModelCollection/Actors/robot/lack-run.egg',
            'idle': 'Resources/Models/ModelCollection/Actors/robot/lack-idle.egg',
            'land': 'Resources/Models/ModelCollection/Actors/robot/lack-land.egg',
            'damage': 'Resources/Models/ModelCollection/Actors/robot/lack-damage.egg',
            'jump': 'Resources/Models/ModelCollection/Actors/robot/lack-jump.egg'})

        self.actorNP.reparentTo(self.characterNP)
        self.actorNP.setScale(0.2)
        self.actorNP.setH(180)
        self.actorNP.setPos(0, 0, 0.3)
        self.actorNP.loop('idle')
        # animationspeed
        self.actorNP.setPlayRate(0.7, 'jump')
        self.actorNP.setPlayRate(0.7, 'land')

    def setUpStage1Objectives(self):
        self.setUpStage1FirstObjective()

    def setUpStage1FirstObjective(self):
        box = Box(1, 5, 8, -4, 76, 8, "stage1-objective1-unlockdoor1")
        target = self.createBox(box, 'sand')
        objectiveTest = Box(2, 3.5, 0.5, 28, 36, -1, "stage1-objblock-1")
        keyBallPosition = Vec3(20, 38, 2)
        stage1Objective1 = self.createObjective(objectiveTest, 'stage1-objective-1', self.stage1Objective,
                                                keyBallPosition, test=False)
        taskMgr.add(self.objectiveDestroyBox, 'name', extraArgs=[stage1Objective1[0], stage1Objective1[1], target], appendTask=True)

    def objectiveDestroyBox(self, box, sphere, target, task):
        if box.getDistance(sphere) <= 3:
            # self.updateLife(1)
            self.playSfx(self.SFXclick)
            self.playMusic(self.BGM2, looping=1)
            target.node().removeAllChildren()
            self.world.removeRigidBody(target.node())
            # boxNP.node().removeAllChildren()
            # self.world.removeRigidBody(boxNP.node())
            return task.done
        else:
            return task.cont

    def setup(self):

        # World
        self.debugNP = self.render.attachNewNode(BulletDebugNode('Debug'))
        self.debugNP.show()

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.setDebugNode(self.debugNP.node())

        self.createATM()
        self.createPete()

        #generate the stages
        #stage 1
        self.generateStage("stage1.txt")
        #Stage1Objectives
        self.setUpStage1Objectives()

        # Floor
        # shape = BulletPlaneShape(Vec3(0, 0, 1), 0)
        floorPos = Vec3(0, 0, -2)
        floorSize = Vec3(20, 20, 1)
        shape = BulletBoxShape(floorSize)
        floorNP = self.render.attachNewNode(BulletRigidBodyNode('Floor'))
        floorNP.node().addShape(shape)
        floorNP.setPos(floorPos)
        floorNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(floorNP.node())
        #textures brick, brown(disk), cylinder(cloud), ball(metal) nice floor looking texture, spinner
        fmodelNP = loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-cube/brick.egg')
        fmodelNP.reparentTo(floorNP)
        fmodelNP.setPos(0, 0, 0)
        fmodelNP.setScale(floorSize.x * 2, floorSize.y * 2, floorSize.z)

        #Boxes
        testBox = Box(5, 2, 3, -6, 15, 2, "hello")
        testBox2 = Box(2, 2, 2, 10, 10, 2, "hello2")
        self.createBox(testBox, 'brick')
        self.createBox(testBox2, 'stone3')

        #slider
        testSlide = Box(8, 3, 1, -6, -6, 8, "testSlide")
        self.createSlide(testSlide, 5, 'iron')

        self.createFourWalls()
        self.addBall(3, 'ball1', -5, 6, 10, 0.000000000000001)
        self.addBall(1.5, 'ball2', 0, 0, 5, 10)
        self.addBall(.4, 'ball3', 2, 5, 2, 0.001)

        #coins
        positionCoin = Vec3(3, -6, 3)
        self.createCoin(positionCoin, "coin1")
        positionCoin = Vec3(3, -9, 3)
        self.createCoin(positionCoin, "coin2")
        positionCoin = Vec3(3, -12, 3)
        self.createCoin(positionCoin, "coin2")

        #moving platform NOT WORKING ATM
        positionMP = Vec3(4, -6, 5)
        self.createMovingPlatform(3, 3, 1, positionMP, 'moving playform 1')
        taskMgr.add(self.movingPlatformTestTask, 'testingMove', extraArgs=[positionMP], appendTask = True)
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
        # Character
        checkpointpos = Vec3(4, 2, 0)
        self.createCheckPoint(checkpointpos, 'testcheck')

        #background
        #self.env = loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/bg/env.egg')
        #self.env.reparentTo(render)
        #self.env.setScale(7000)


game = CharacterController()
game.run()
