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

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletHelper
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletHeightfieldShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletSoftBodyNode
from panda3d.bullet import BulletSoftBodyConfig
from panda3d.bullet import ZUp


class CharacterController(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setupLights()
        # Input
        self.accept('escape', self.doExit)
        self.accept('r', self.doReset)
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

        #animation switches
        self.landingAnimation = False
        self.isDashing = False
        self.cdmax = 20
        self.cdmin = 10

        #keyOptions
        self.cameraAutoTurn = True

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

    def doJump(self):
        self.character.setMaxJumpHeight(5.0)
        self.character.setJumpSpeed(8.0)
        if self.character.isOnGround():
            self.actorNP.play('jump')
        self.character.doJump()
        self.isJumping = True

    def doDashJump(self):
        self.character.setMaxJumpHeight(2.0)
        self.character.setJumpSpeed(8.0)
        if self.character.isOnGround():
            self.isDashJumping = True
            self.actorNP.play('jump')
        self.character.doJump()
        self.isJumping = True

    def processInput(self, dt):
        speed = Vec3(0, 0, 0)
        omega = 0.0
        speedForce = 5.0
        if inputState.isSet('dash') and inputState.isSet('forward') and self.character.isOnGround():
            speed.setY(speedForce * 2)
            if self.isDashing is False:
                self.actorNP.setPlayRate(1.5, 'run')
                self.isDashing = True
        elif inputState.isSet('forward'):
            speed.setY(speedForce)
            self.isDashing = False
            self.actorNP.setPlayRate(1, 'run')
        if inputState.isSet('dash') and inputState.isSet('dashJump') and inputState.isSet('forward'):
            self.doDashJump()
            if inputState.isSet('dash') and inputState.isSet('forward') and self.isDashJumping:
                speed.setY(speedForce * 2)
        else: self.isDashJumping = False
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
        if (inputState.isSet('forward') or inputState.isSet('reverse') or inputState.isSet('left') or inputState.isSet('right') and self.isMoving is False and self.character.isOnGround()):
            if self.isMoving is False:
                self.actorNP.loop('run')
                self.isMoving = True
        else:
            if self.isMoving and self.character.isOnGround():
                self.isMoving = False
                self.actorNP.loop('idle')
            elif self.isJumping and self.character.isOnGround():
                self.isJumping = False
                self.isLanding = True
                self.landingAnimation = True
                taskMgr.add(self.landingAnimationTask, 'landing')
            elif self.isLanding is False and taskMgr.hasTaskNamed('landing'):
                taskMgr.remove('landing')
                self.actorNP.loop('idle')


        self.floater.setPos(self.characterNP.getPos())
        self.floater.setZ(self.characterNP.getZ() + 1.0)
        base.camera.lookAt(self.floater)

        return task.cont
    def landingAnimationTask(self, task):
        if self.landingAnimation:
            self.actorNP.play('land')
            self.landingAnimation = False
        if task.time >= 0.3 and self.isLanding:

            self.isLanding = False
        return task.cont

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
        self.sphere = self.render.attachNewNode(node)
        self.sphere.setPos(x, y, z)
        self.world.attachRigidBody(node)

        smileyFace = self.loader.loadModel("models/smiley")
        smileyFace.reparentTo(self.sphere)
        smileyFace.setScale(radius)

    def setup(self):

        # World
        self.debugNP = self.render.attachNewNode(BulletDebugNode('Debug'))
        self.debugNP.show()

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.setDebugNode(self.debugNP.node())

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

        fmodelNP = loader.loadModel('Resources/Models/ModelCollection/EnvBuildingBlocks/brick-cube/brick.egg')
        fmodelNP.reparentTo(floorNP)
        fmodelNP.setPos(0, 0, 0)
        fmodelNP.setScale(floorSize.x * 2, floorSize.y * 2, floorSize.z)

        self.createFourWalls()
        self.addBall(3, 'ball1', 3, 6, 10, 20)
        self.addBall(1.5, 'ball2', 0, 0, 12, 10)
        self.addBall(.4, 'ball3', 2, 5, 2, 0.001)
        # Stair
        origin = Point3(2, 0, 0)
        size = Vec3(2, 4.75, 1)
        shape = BulletBoxShape(size * 0.55)
        for i in range(9):
            pos = origin + size * i
            pos.setY(0)
            stairNP = self.render.attachNewNode(BulletRigidBodyNode('Stair%i' % i))
            stairNP.node().addShape(shape)
            stairNP.setPos(pos)
            stairNP.setCollideMask(BitMask32.allOn())

            modelNP = loader.loadModel('models//box.egg')
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

        # Character
        h = 4.25
        w = .6
        shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

        self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
        #    self.character.setMass(1.0)
        self.characterNP = self.render.attachNewNode(self.character)
        self.characterNP.setPos(-2, 0, 20)
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
        self.actorNP.setPos(0, 0, 0.5)
        self.actorNP.loop('idle')
        #animationspeed
        self.actorNP.setPlayRate(0.7, 'jump')
        self.actorNP.setPlayRate(0.7, 'land')


game = CharacterController()
game.run()
