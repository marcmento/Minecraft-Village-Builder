
from mcpi.minecraft import Minecraft

mc = Minecraft.create()

class Path:
    def __init__(self, width):
        self.width = width

        
    ##creates X axis components of path.
    def xAxisPath(self, xPos, zPos, pX, pZ):
        while xPos != pX:
            xCleaner = (xPos - pX)/abs(xPos - pX)
            pathHeight = mc.getHeight(xPos, zPos)
            if self.isHouseBlock(xPos, pathHeight, zPos):
                xPos = pX
            else:
                mc.setBlocks(xPos, pathHeight, zPos - self.width, xPos, pathHeight, zPos + self.width, 208)
                xPos -= xCleaner
            if xPos % 16 == 0 and (zPos != pZ or xPos != pX):
                self.placeLantern(xPos, zPos, pX, pZ)
        return xPos

    ##creates Zaxis component of path
    def zAxisPath(self, xPos, zPos, pX, pZ):
        while zPos != pZ:
            zCleaner = (zPos - pZ)/abs(zPos - pZ)
            pathHeight = mc.getHeight(xPos, zPos)
            if self.isHouseBlock(xPos, pathHeight, zPos):
                zPos = pZ 
            else:
                mc.setBlocks(xPos - self.width, pathHeight, zPos, xPos + self.width, pathHeight, zPos, 208)
                zPos -= zCleaner
            if zPos % 16 == 0 and ((zPos != pZ) or (xPos != pX) ):
                self.placeLantern(xPos, zPos, pX, pZ)
        return zPos

  
  
    ##Builds Paths centering from position of player. combining z and x components
    def pathBuilding(self, xPos, zPos, pX, pZ):
        xPos = round(xPos)
        zPos = round(zPos)
        pX = round(pX)
        pZ = round(pZ)

        if abs(xPos - pX) > abs(zPos - pZ):
            zPos = self.zAxisPath(xPos, zPos, pX, pZ)
            xPos = self.xAxisPath(xPos, zPos, pX, pZ)
        else:
            xPos = self.xAxisPath(xPos, zPos, pX, pZ)
            zPos = self.zAxisPath(xPos, zPos, pX, pZ)
        if(self.isHouseBlock(pX, mc.getHeight(pX,pZ), pZ) == False) and (mc.getBlock(pX, mc.getHeight(pX,pZ), pZ) != 1):
            mc.setBlock(pX, mc.getHeight(pX,pZ), pZ, 208)


    ## Checks if Block is made from a house
    def isHouseBlock(self, xPos, yPos, zPos):
        house = False
        block = mc.getBlock(xPos,yPos,zPos)
        if block ==  45 or block == 5 or block == 4 or block == 98 or block == 35 or block == 41:
            house = True
        return house

    ## Function that checks where relative to the path a lantern should be placed.
    def placeLantern(self, xPos, zPos, pX, pZ):
        if xPos == pX:
            self.buildPillar(xPos + 2, zPos)  
        elif zPos == pZ:
            self.buildPillar(xPos, zPos + 2)  
        elif abs(xPos - pX) > abs(zPos - pZ):
            self.buildPillar(xPos + 2, zPos)  
        else:
            self.buildPillar(xPos, zPos + 2)  

    ## constructs a lantern in the shape of a pillar
    def buildPillar(self, xPos, zPos):
        y = mc.getHeight(xPos, zPos)
        block = mc.getBlock(xPos, y, zPos) 
        if block == 169 or block == 208:
            return
        mc.setBlocks(xPos,y + 1,zPos,xPos,y + 3,zPos,139)
        mc.setBlock(xPos,y + 4,zPos, 169)

    def buildWell(self, xPos, zPos):
        y = mc.getHeight(xPos, zPos)

        ##Checks if Well is on path
        blocks = mc.getBlocks(xPos - 2, y, zPos - 2, xPos + 2, y + 1, zPos + 2)
        isPlaceable = self.isAnyBlocksHouses(blocks)
        while isPlaceable == False:
            xPos += 2
            y = mc.getHeight(xPos, zPos)
            blocks = mc.getBlocks(xPos - 2, y, zPos - 2, xPos + 2, y, zPos + 2)
            isPlaceable = self.isAnyBlocksHouses(blocks)

        #Well building code
        mc.setBlocks(xPos - 2, y, zPos - 2, xPos + 2, y + 6, zPos + 2, 0)
        mc.setBlocks(xPos - 2, y, zPos - 2, xPos + 2, y, zPos + 2, 208)
        mc.setBlocks(xPos - 1, y + 1, zPos - 1, xPos + 1, y-9, zPos + 1, 4)
        mc.setBlocks(xPos, y + 1, zPos, xPos, y - 9, zPos, 9)
        mc.setBlock(xPos, y - 10, zPos, 88)
        self.buildPillar(xPos - 1, zPos - 1)
        self.buildPillar(xPos - 1, zPos + 1)
        self.buildPillar(xPos + 1, zPos - 1)
        self.buildPillar(xPos + 1, zPos + 1)
        mc.setBlocks(xPos - 1, y + 5, zPos - 1, xPos + 1, y + 5, zPos + 1, 4)
        return xPos, zPos

    #Checks if block is natural
    def isAnyBlocksHouses(self, blocks):
        isPlaceable = True
        for block in blocks:
            if (block != 0) and (block != 208) and (block != 2):
                isPlaceable = False
        return isPlaceable
