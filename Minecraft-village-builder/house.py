from mcpi.minecraft import Minecraft
from mcpi import block
import math
import random

North = 1
East = 2
South = 3
West = 4

mc = Minecraft.create()
#List of all possible blocks to build house with
outerwalls = [block.BRICK_BLOCK, block.DIAMOND_BLOCK, block.WOOD_PLANKS, block.COBBLESTONE, block.STONE_BRICK, block.WOOL, block.GOLD_BLOCK]

class house:
    def __init__(self, plotx1, ploty1, plotz1, plotx2, plotz2, doorface):
        self.plotx1 = plotx1
        self.ploty1 = ploty1
        self.plotz1 = plotz1
        self.plotx2 = plotx2
        self.plotz2 = plotz2

        self.roofx1 = 0
        self.roofy1 = 0
        self.roofz1 = 0
        self.roofx2 = 0
        self.roofz2 = 0

        self.secondlevel = random.choice([True, False])
        self.outerwallblock = outerwalls[random.randint(0,6)]
        self.roofmat = outerwalls[random.randint(0,6)]
        self.doorfacing = doorface
        self.create_outer_walls()
        self.create_roof()
        self.create_inner()
        self.create_pool()
        self.create_decoations()
    
    def create_outer_walls(self):
        mc.setBlocks(self.plotx1, self.ploty1, self.plotz1, self.plotx2, self.ploty1, self.plotz2, block.STONE)
        mc.setBlocks(self.plotx1, self.ploty1+1, self.plotz1, self.plotx2, self.ploty1+20, self.plotz2, block.AIR)
        maxx = self.plotx2 - self.plotx1
        maxz = self.plotz2 - self.plotz1
        n = random.randint(8,int(maxx)-2)
        a = random.randint(8,int(maxz)-2)
        
        if self.doorfacing == West or self.doorfacing == North:
            mc.setBlocks(self.plotx1+1, self.ploty1, self.plotz1+1, self.plotx1+n+1, self.ploty1+4, self.plotz1+a+1, self.outerwallblock)
            mc.setBlocks(self.plotx1+2, self.ploty1+1, self.plotz1+2, self.plotx1+n, self.ploty1+3, self.plotz1+a, block.AIR)
            self.roofx1 = self.plotx1+1
            self.roofz1 = self.plotz1+1
            self.roofx2 = self.plotx1+n+1
            self.roofz2 = self.plotz1+a+1
            if self.secondlevel == False:
                self.roofy1 = self.ploty1+4
            else:
                mc.setBlocks(self.plotx1+1, self.ploty1+4, self.plotz1+1, self.plotx1+n+1, self.ploty1+8, self.plotz1+a+1, self.outerwallblock)
                mc.setBlocks(self.plotx1+2, self.ploty1+5, self.plotz1+2, self.plotx1+n, self.ploty1+7, self.plotz1+a, block.AIR)            
                self.roofy1 = self.ploty1+8
        else:
            mc.setBlocks(self.plotx2-1, self.ploty1, self.plotz2-1, self.plotx2-n-1, self.ploty1+4, self.plotz2-a-1, self.outerwallblock)
            mc.setBlocks(self.plotx2-2, self.ploty1+1, self.plotz2-2, self.plotx2-n, self.ploty1+3, self.plotz2-a, block.AIR)
            self.roofx1 = self.plotx2-n-1
            self.roofz1 = self.plotz2-a-1
            self.roofx2 = self.plotx2-1
            self.roofz2 = self.plotz2-1
            if self.secondlevel == False:
                self.roofy1 = self.ploty1+4
            else:
                mc.setBlocks(self.plotx2-1, self.ploty1+4, self.plotz2-1, self.plotx2-n-1, self.ploty1+8, self.plotz2-a-1, self.outerwallblock)
                mc.setBlocks(self.plotx2-2, self.ploty1+5, self.plotz2-2, self.plotx2-n, self.ploty1+7, self.plotz2-a, block.AIR)
                self.roofy1 = self.ploty1+8
        #Set door
        if self.doorfacing == North:
            xer = math.ceil((self.roofx2 - self.roofx1)/2)
            mc.setBlock(self.roofx1+xer, self.ploty1+2, self.roofz1, block.DOOR_WOOD.withData(8))
            mc.setBlock(self.roofx1+xer, self.ploty1+1, self.roofz1, block.DOOR_WOOD.withData(1))
        elif self.doorfacing == South:
            xer = math.ceil((self.roofx2 - self.roofx1)/2)
            mc.setBlock(self.roofx1+xer, self.ploty1+2, self.roofz2, block.DOOR_WOOD.withData(8))
            mc.setBlock(self.roofx1+xer, self.ploty1+1, self.roofz2, block.DOOR_WOOD.withData(3))
        elif self.doorfacing == East:
            xer = math.ceil((self.roofz2 - self.roofz1)/2)
            mc.setBlock(self.roofx2, self.ploty1+2, self.roofz1+xer, block.DOOR_WOOD.withData(8))
            mc.setBlock(self.roofx2, self.ploty1+1, self.roofz1+xer, block.DOOR_WOOD.withData(2))
        elif self.doorfacing == West:
            xer = math.ceil((self.roofz2 - self.roofz1)/2)
            mc.setBlock(self.roofx1, self.ploty1+2, self.roofz1+xer, block.DOOR_WOOD.withData(8))
            mc.setBlock(self.roofx1, self.ploty1+1, self.roofz1+xer, block.DOOR_WOOD.withData(0))

    def create_roof(self):
        xcheck1 = self.roofx1-1
        xcheck2 = self.roofx2+1
        zcheck1 = self.roofz1-1
        zcheck2 = self.roofz2+1
        ycheck = self.roofy1
        #Recursively build roof untill two ends meet
        while (xcheck2-xcheck1>1) and (zcheck2-zcheck1) >1:
            mc.setBlocks(xcheck1+1, ycheck+1, zcheck1+1, xcheck2-1, ycheck+1, zcheck2-1, self.roofmat)
            xcheck1 += 1
            xcheck2 -= 1
            zcheck1 += 1
            zcheck2 -= 1
            ycheck += 1

    def create_inner(self):
        if self.doorfacing == West or self.doorfacing == East:
            size = (self.roofz2-self.roofz1)+ 1
            if  size <= 13:
                middle = self.roofx2-self.roofx1
                middle = math.ceil(middle/2)
                mc.setBlocks(self.roofx1+middle, self.ploty1+1, self.roofz1, self.roofx1+middle, self.ploty1+3, self.roofz2, self.outerwallblock)
                #Set lights
                mc.setBlock(self.roofx1+middle-1, self.ploty1+2, self.roofz1+1, block.TORCH.withData(2))
                mc.setBlock(self.roofx1+middle-1, self.ploty1+2, self.roofz2-1, block.TORCH.withData(2))
                mc.setBlock(self.roofx1+middle+1, self.ploty1+2, self.roofz1+1, block.TORCH.withData(1))
                mc.setBlock(self.roofx1+middle+1, self.ploty1+2, self.roofz2-1, block.TORCH.withData(1))
                #Set Door
                xer = math.ceil(((self.roofz2 - self.roofz1)/3)*2)
                mc.setBlock(self.roofx1+middle, self.ploty1+2, self.roofz1+xer, block.DOOR_WOOD.withData(8))
                mc.setBlock(self.roofx1+middle, self.ploty1+1, self.roofz1+xer, block.DOOR_WOOD.withData(0))
                #Set tables
                mc.setBlock(self.roofx2-1, self.ploty1+1, self.roofz1+1, block.CRAFTING_TABLE)
                mc.setBlock(self.roofx2-1, self.ploty1+1, self.roofz1+2, block.FURNACE_INACTIVE.withData(4))
                #Set windows
                xer = math.ceil((self.roofz2 - self.roofz1)/2)
                if self.doorfacing == West:
                    mc.setBlocks(self.roofx2, self.ploty1+2, self.roofz1+xer-1, self.roofx2, self.ploty1+2,self.roofz1+xer+1, block.GLASS)
                else:
                    mc.setBlocks(self.roofx1, self.ploty1+2, self.roofz1+xer-1, self.roofx1, self.ploty1+2,self.roofz1+xer+1, block.GLASS)
                xer = math.ceil((self.roofz2 - self.roofz1)/4)
                if self.doorfacing == West:
                    mc.setBlock(self.roofx1, self.ploty1+2, self.roofz1+xer, block.GLASS)
                    mc.setBlock(self.roofx1, self.ploty1+2, self.roofz2-xer, block.GLASS)
                else:
                    mc.setBlock(self.roofx2, self.ploty1+2, self.roofz1+xer, block.GLASS)
                    mc.setBlock(self.roofx2, self.ploty1+2, self.roofz2-xer, block.GLASS)
            else:
                firsthird = math.ceil((self.roofz2-self.roofz1)/3)
                secondthird = math.ceil(((self.roofz2-self.roofz1)/3)*2)
                mc.setBlocks(self.roofx1, self.ploty1+1, self.roofz1+firsthird, self.roofx2, self.ploty1+3, self.roofz1+firsthird, self.outerwallblock)
                mc.setBlocks(self.roofx1, self.ploty1+1, self.roofz1+secondthird, self.roofx2, self.ploty1+3, self.roofz1+secondthird, self.outerwallblock)
                #Set Doors and lights
                xer = math.ceil(((self.roofx2 - self.roofx1)/3)*2)
                mc.setBlock(self.roofx1+xer, self.ploty1+2, self.roofz1+firsthird, block.DOOR_WOOD.withData(8))
                mc.setBlock(self.roofx1+xer, self.ploty1+1, self.roofz1+firsthird, block.DOOR_WOOD.withData(3))
                mc.setBlock(self.roofx2-xer, self.ploty1+2, self.roofz1+firsthird+1, block.TORCH.withData(3))
                mc.setBlock(self.roofx2-xer, self.ploty1+2, self.roofz1+firsthird-1, block.TORCH.withData(4))
                xer = math.ceil((self.roofx2 - self.roofx1)/3)
                mc.setBlock(self.roofx1+xer, self.ploty1+2, self.roofz1+secondthird, block.DOOR_WOOD.withData(8))
                mc.setBlock(self.roofx1+xer, self.ploty1+1, self.roofz1+secondthird, block.DOOR_WOOD.withData(1))
                mc.setBlock(self.roofx2-xer, self.ploty1+2, self.roofz1+secondthird-1, block.TORCH.withData(4))
                mc.setBlock(self.roofx2-xer, self.ploty1+2, self.roofz1+secondthird+1, block.TORCH.withData(3))
                #Set tables
                mc.setBlock(self.roofx1+1, self.ploty1+1, self.roofz1+1, block.CRAFTING_TABLE)
                mc.setBlock(self.roofx1+2, self.ploty1+1, self.roofz1+1, block.FURNACE_INACTIVE.withData(3))
                #Set Windwows
                xer = math.ceil((self.roofx2 - self.roofx1)/2)
                mc.setBlocks(self.roofx1+xer-1, self.ploty1+2, self.roofz1, self.roofx1+xer+1, self.ploty1+2, self.roofz1, block.GLASS)
                mc.setBlocks(self.roofx1+xer-1, self.ploty1+2, self.roofz2, self.roofx1+xer+1, self.ploty1+2, self.roofz2, block.GLASS)
                xer = math.ceil((self.roofz2 - self.roofz1)/2)
                if self.doorfacing ==  West:
                    mc.setBlock(self.roofx2, self.ploty1+2, self.roofz1+xer, block.GLASS)
                else:
                    mc.setBlock(self.roofx1, self.ploty1+2, self.roofz1+xer, block.GLASS)
            if self.secondlevel == True:
                middle = self.roofz2-self.roofz1
                middle = math.ceil(middle/2)
                mc.setBlocks(self.roofx1, self.ploty1+5, self.roofz1+middle, self.roofx2, self.ploty1+7, self.roofz1+middle, self.outerwallblock)
                #Set lights
                mc.setBlock(self.roofx1+1, self.ploty1+6, self.roofz1+middle-1, block.TORCH.withData(4))
                mc.setBlock(self.roofx2-1, self.ploty1+6, self.roofz1+middle-1, block.TORCH.withData(4))
                mc.setBlock(self.roofx1+1, self.ploty1+6, self.roofz1+middle+1, block.TORCH.withData(3))
                mc.setBlock(self.roofx2-1, self.ploty1+6, self.roofz1+middle+1, block.TORCH.withData(3))
                #Set Door
                xer = math.ceil((self.roofz2 - self.roofz1)/3)
                mc.setBlock(self.roofx1+xer, self.ploty1+6, self.roofz1+middle, block.DOOR_WOOD.withData(8))
                mc.setBlock(self.roofx1+xer, self.ploty1+5, self.roofz1+middle, block.DOOR_WOOD.withData(3))
                #Set windows
                xer = math.ceil((self.roofx2 - self.roofx1)/2)
                mc.setBlocks(self.roofx2-xer-1, self.ploty1+6, self.roofz1, self.roofx2-xer+1, self.ploty1+6, self.roofz1, block.GLASS)
                mc.setBlocks(self.roofx2-xer-1, self.ploty1+6, self.roofz2, self.roofx2-xer+1, self.ploty1+6, self.roofz2, block.GLASS)
                xer = math.ceil((self.roofz2 - self.roofz1)/4)
                mc.setBlocks(self.roofx1, self.ploty1+6, self.roofz1+xer-1, self.roofx1, self.ploty1+6, self.roofz1+xer, block.GLASS)
                mc.setBlocks(self.roofx1, self.ploty1+6, self.roofz2-xer, self.roofx1, self.ploty1+6, self.roofz2-xer+1, block.GLASS)
                #Create Stairs
                mc.setBlocks(self.roofx2-1, self.ploty1+1, self.roofz2-1, self.roofx2-3, self.ploty1+1, self.roofz2-1, self.outerwallblock)
                mc.setBlocks(self.roofx2-1, self.ploty1+2, self.roofz2-1, self.roofx2-2, self.ploty1+2, self.roofz2-1, self.outerwallblock)
                mc.setBlock(self.roofx2-1, self.ploty1+3, self.roofz2-1, self.outerwallblock)
                mc.setBlocks(self.roofx2-1, self.ploty1+4, self.roofz2-1, self.roofx2-3, self.ploty1+4, self.roofz2-1, block.AIR)
        if self.doorfacing == North or self.doorfacing == South:
            size = (self.roofx2-self.roofx1)+ 1
            if  size <= 13:
                middle = self.roofz2-self.roofz1
                middle = math.ceil(middle/2)
                mc.setBlocks(self.roofx1, self.ploty1+1, self.roofz1+middle, self.roofx2, self.ploty1+3, self.roofz1+middle, self.outerwallblock)
                #Set lights
                mc.setBlock(self.roofx1+1, self.ploty1+2, self.roofz1+middle-1, block.TORCH.withData(4))
                mc.setBlock(self.roofx2-1, self.ploty1+2, self.roofz1+middle-1, block.TORCH.withData(4))
                mc.setBlock(self.roofx1+1, self.ploty1+2, self.roofz1+middle+1, block.TORCH.withData(3))
                mc.setBlock(self.roofx2-1, self.ploty1+2, self.roofz1+middle+1, block.TORCH.withData(3))
                #Set Door
                xer = math.ceil(((self.roofx2 - self.roofx1)/3)*2)
                mc.setBlock(self.roofx1+xer, self.ploty1+2, self.roofz1+middle, block.DOOR_WOOD.withData(8))
                mc.setBlock(self.roofx1+xer, self.ploty1+1, self.roofz1+middle, block.DOOR_WOOD.withData(1))
                #Set tables
                mc.setBlock(self.roofx2-1, self.ploty1+1, self.roofz2-1, block.CRAFTING_TABLE)
                mc.setBlock(self.roofx2-2, self.ploty1+1, self.roofz2-1, block.FURNACE_INACTIVE.withData(2))
                #Set windows
                xer = math.ceil((self.roofx2 - self.roofx1)/2)
                if self.doorfacing == North:
                    mc.setBlocks(self.roofx1+xer-1, self.ploty1+2, self.roofz2, self.roofx1+xer+1, self.ploty1+2,self.roofz2, block.GLASS)
                else:
                    mc.setBlocks(self.roofx1+xer-1, self.ploty1+2, self.roofz1, self.roofx1+xer+1, self.ploty1+2,self.roofz1, block.GLASS)
                xer = math.ceil((self.roofx2 - self.roofx1)/4)
                if self.doorfacing == North:
                    mc.setBlock(self.roofx1+xer, self.ploty1+2, self.roofz1, block.GLASS)
                    mc.setBlock(self.roofx2-xer, self.ploty1+2, self.roofz1, block.GLASS)
                else:
                    mc.setBlock(self.roofx1+xer, self.ploty1+2, self.roofz2, block.GLASS)
                    mc.setBlock(self.roofx2-xer, self.ploty1+2, self.roofz2, block.GLASS)
            else:
                firsthird = math.ceil((self.roofx2-self.roofx1)/3)
                secondthird = math.ceil(((self.roofx2-self.roofx1)/3)*2)
                mc.setBlocks(self.roofx1+firsthird, self.ploty1+1, self.roofz1, self.roofx1+firsthird, self.ploty1+3, self.roofz2, self.outerwallblock)
                mc.setBlocks(self.roofx1+secondthird, self.ploty1+1, self.roofz1, self.roofx1+secondthird, self.ploty1+3, self.roofz2, self.outerwallblock)
                #Set Doors and lights
                xer = math.ceil(((self.roofz2 - self.roofz1)/3)*2)
                mc.setBlock(self.roofx1+firsthird, self.ploty1+2, self.roofz1+xer, block.DOOR_WOOD.withData(8))
                mc.setBlock(self.roofx1+firsthird, self.ploty1+1, self.roofz1+xer, block.DOOR_WOOD.withData(2))
                mc.setBlock(self.roofx1+firsthird+1, self.ploty1+2, self.roofz2-xer, block.TORCH.withData(1))
                mc.setBlock(self.roofx1+firsthird-1, self.ploty1+2,self.roofz2-xer, block.TORCH.withData(2))
                xer = math.ceil((self.roofz2 - self.roofz1)/3)
                mc.setBlock(self.roofx1+secondthird, self.ploty1+2, self.roofz1+xer, block.DOOR_WOOD.withData(8))
                mc.setBlock(self.roofx1+secondthird, self.ploty1+1, self.roofz1+xer, block.DOOR_WOOD.withData(0))
                mc.setBlock(self.roofx1+secondthird-1 , self.ploty1+2, self.roofz2-xer, block.TORCH.withData(2))
                mc.setBlock(self.roofx1+secondthird+1, self.ploty1+2, self.roofz2-xer, block.TORCH.withData(1))
                #Set tables
                mc.setBlock(self.roofx2-1, self.ploty1+1, self.roofz1+1, block.CRAFTING_TABLE)
                mc.setBlock(self.roofx2-1, self.ploty1+1, self.roofz1+2, block.FURNACE_INACTIVE.withData(4))
                #Set Windwows
                xer = math.ceil((self.roofz2 - self.roofz1)/2)
                mc.setBlocks(self.roofx1, self.ploty1+2, self.roofz1+xer-1, self.roofx1, self.ploty1+2, self.roofz1+xer+1, block.GLASS)
                mc.setBlocks(self.roofx2, self.ploty1+2, self.roofz1+xer-1, self.roofx2, self.ploty1+2, self.roofz1+xer+1, block.GLASS)
                xer = math.ceil((self.roofx2 - self.roofx1)/2)
                if self.doorfacing ==  North:
                    mc.setBlock(self.roofx1+xer, self.ploty1+2, self.roofz2, block.GLASS)
                else:
                    mc.setBlock(self.roofx1+xer, self.ploty1+2, self.roofz1, block.GLASS)
            if self.secondlevel == True:
                middle = self.roofx2-self.roofx1
                middle = math.ceil(middle/2)
                mc.setBlocks(self.roofx1+middle, self.ploty1+5, self.roofz1, self.roofx1+middle, self.ploty1+7, self.roofz2, self.outerwallblock)
                #Set Lights
                mc.setBlock(self.roofx1+middle-1, self.ploty1+6, self.roofz1+1, block.TORCH.withData(2))
                mc.setBlock(self.roofx1+middle-1, self.ploty1+6, self.roofz2-1, block.TORCH.withData(2))
                mc.setBlock(self.roofx1+middle+1, self.ploty1+6, self.roofz1+1, block.TORCH.withData(1))
                mc.setBlock(self.roofx1+middle+1, self.ploty1+6, self.roofz2-1, block.TORCH.withData(1))
                #Set Door
                xer = math.ceil((self.roofx2 - self.roofx1)/3)
                mc.setBlock(self.roofx1+middle, self.ploty1+6, self.roofz1+xer, block.DOOR_WOOD.withData(8))
                mc.setBlock(self.roofx1+middle, self.ploty1+5, self.roofz1+xer, block.DOOR_WOOD.withData(0))
                #Set windows
                xer = math.ceil((self.roofz2 - self.roofz1)/2)
                mc.setBlocks(self.roofx1, self.ploty1+6, self.roofz2-xer-1, self.roofx1, self.ploty1+6, self.roofz2-xer+1, block.GLASS)
                mc.setBlocks(self.roofx2, self.ploty1+6, self.roofz2-xer-1, self.roofx2, self.ploty1+6, self.roofz2-xer+1, block.GLASS)
                xer = math.ceil((self.roofx2 - self.roofx1)/4)
                mc.setBlocks(self.roofx1+xer-1, self.ploty1+6, self.roofz1, self.roofx1+xer, self.ploty1+6, self.roofz1, block.GLASS)
                mc.setBlocks(self.roofx2-xer, self.ploty1+6, self.roofz1, self.roofx2-xer+1, self.ploty1+6, self.roofz1, block.GLASS)
                #Create Stairs
                mc.setBlocks(self.roofx1+1, self.ploty1+1, self.roofz2-1, self.roofx1+1, self.ploty1+1, self.roofz2-3, self.outerwallblock)
                mc.setBlocks(self.roofx1+1, self.ploty1+2, self.roofz2-1, self.roofx1+1, self.ploty1+2, self.roofz2-2, self.outerwallblock)
                mc.setBlock(self.roofx1+1, self.ploty1+3, self.roofz2-1, self.outerwallblock)
                mc.setBlocks(self.roofx1+1, self.ploty1+4, self.roofz2-1, self.roofx1+1, self.ploty1+4, self.roofz2-3, block.AIR)
    
    def create_pool(self):
        if ((self.plotz2 - self.roofz2) > 7) or ((self.roofx1 - self.plotx1) > 7):
            mc.setBlocks(self.plotx1+2, self.ploty1-1, self.plotz2-2, self.plotx1+5, self.ploty1-1, self.plotz2-5, block.IRON_BLOCK)
            mc.setBlocks(self.plotx1+1, self.ploty1, self.plotz2-1, self.plotx1+6, self.ploty1, self.plotz2-6, block.IRON_BLOCK)
            mc.setBlocks(self.plotx1+1, self.ploty1+1, self.plotz2-1, self.plotx1+6, self.ploty1+1, self.plotz2-6, block.FENCE)
            mc.setBlocks(self.plotx1+2, self.ploty1, self.plotz2-2, self.plotx1+5, self.ploty1, self.plotz2-5, block.WATER)                
            mc.setBlocks(self.plotx1+2, self.ploty1+1, self.plotz2-2, self.plotx1+5, self.ploty1+1, self.plotz2-5, block.AIR)
        elif ((self.plotx2 - self.roofx2) > 7) or ((self.roofz1 - self.plotz1) > 7):
            mc.setBlocks(self.plotx2-2, self.ploty1-1, self.plotz1+2, self.plotx2-5, self.ploty1-1, self.plotz1+5, block.IRON_BLOCK)
            mc.setBlocks(self.plotx2-1, self.ploty1, self.plotz1+1, self.plotx2-6, self.ploty1, self.plotz1+6, block.IRON_BLOCK)
            mc.setBlocks(self.plotx2-1, self.ploty1+1, self.plotz1+1, self.plotx2-6, self.ploty1+1, self.plotz1+6, block.FENCE)
            mc.setBlocks(self.plotx2-2, self.ploty1, self.plotz1+2, self.plotx2-5, self.ploty1, self.plotz1+5, block.WATER)                
            mc.setBlocks(self.plotx2-2, self.ploty1+1, self.plotz1+2, self.plotx2-5, self.ploty1+1, self.plotz1+5, block.AIR)

    def create_decoations(self):
        if self.secondlevel == True:
            if self.doorfacing == West or self.doorfacing == East:
                feet_end = block.BED.withData(2)
                pillow_end = feet_end.withData(8 | feet_end.data)
                mc.setBlock(self.roofx1+1, self.ploty1+5 ,self.roofz1+1, pillow_end)
                mc.setBlock(self.roofx1+1, self.ploty1+5, self.roofz1+2, feet_end)
            else:
                feet_end = block.BED.withData(3)
                pillow_end = feet_end.withData(8 | feet_end.data)
                mc.setBlock(self.roofx2-1, self.ploty1+5 ,self.roofz1+1 , pillow_end)
                mc.setBlock(self.roofx2-2, self.ploty1+5, self.roofz1+1, feet_end)