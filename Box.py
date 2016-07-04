from panda3d.core import Vec3

class Box():
    def __init__(self, x, y, z, px, py, pz, blockType):
        self.size = Vec3(x, y, z)
        self.position = Vec3(px, py, pz)
        self.model = blockType
    def getSize(self):
        return self.size

    def getPosition(self):
        return self.position

    def getModel(self):
        return self.model