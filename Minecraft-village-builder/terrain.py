from mcpi.minecraft import Minecraft
import random as random
import math
import numpy as np
from mcpi import block
from path import Path

mc = Minecraft.create()
paths = Path(1)


playerTilePos = mc.player.getTilePos()


class Plot:
    #minimum of x15, z15 to max x20, z20
    def __init__(self, x1: int, x2: int, y1: int, y2: int, z1: int, z2: int):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2

class Terrain:
    def __init__(self, x, y, z, height, length):
        self.x = x
        self.y = y
        self.z = z
        self.height = height
        self.min_max = {}
        self.min_land_height = 0
        self.max_land_height = 0
        # Boundaries of the terrain
        self.x_min = playerTilePos.x - length
        self.x_max = playerTilePos.x + length
        self.z_min = playerTilePos.z - length
        self.z_max = playerTilePos.z + length
        # Amplitude options
        self.amplitude = [1, 1.2, 1.25, 1.5]
        # Wavelength options
        self.wavelength = [20, 25, 30]
        # Scale options
        self.scale = [4.5, 5, 5.5, 6]
        self.terrain_amp = random.sample(self.amplitude, 2)
        self.terrain_wave = random.sample(self.wavelength, 2)
        self.terrain_scale = random.choice(self.scale)
        # list of Plot objects that contain co-ords of the plots
        self.plot_list = []
        
    def getLandHeight(self, x, z):
        # functions to generate hill landscape
        a = self.terrain_amp[0] * np.sin(x/ self.terrain_wave[0]) 
        b = self.terrain_amp[1] * np.cos(z / self.terrain_wave[1]) 
        height = self.terrain_scale * (a * b)
        
        # creates a set of all the heights (y) in the terrain
        self.min_max.update({math.ceil(height):0})
        
        # assigns the minimum and maximum heights of the terrain 
        self.min_land_height = min(self.min_max.keys())
        self.max_land_height = max(self.min_max.keys())

        return height


    def bulldoze(self, size: int):
        """
        method to flatten terrain from the location of the player.
        base layer to be GRASS, and everything above to be AIR
        """
        pos = mc.player.getTilePos()
        s = int(size)
        mc.setBlocks(pos.x - s, self.height, pos.z - s, pos.x + s, self.height, pos.z + s, block.GRASS)
        mc.setBlocks(pos.x - s, self.height + 1, pos.z - s, pos.x + s, self.height + 64, pos.z + s, block.AIR)
    
    def hills(self):
        for x in range(self.x_min, self.x_max):
            for z in range(self.z_min, self.z_max):
                mc.setBlocks(x, self.height, z, x, self.getLandHeight(x,z), z , block.GRASS)
                mc.setBlocks(x, self.getLandHeight(x,z) + 1, z, x, 64, z , block.AIR)
    
    def generate_plot(self, plot_size: int):
        # generate plot co-ords and create co-ord values
        plot_x1 = random.randint(self.x_min, self.x_max - plot_size)
        plot_x2 = plot_x1 + plot_size
        plot_z1 = random.randint(self.z_min, self.z_max - plot_size)
        plot_z2 = plot_z1 + plot_size
        # check if plot can be built
        if self.check_plot(plot_x1, plot_x2, plot_z1, plot_z2) is True: 
            self.generate_plot(plot_size)
        # builts when check_plot returns False
        else: 
            print(plot_x1, plot_x2, plot_z1, plot_z2)
            self.build_plot(plot_x1, plot_x2, plot_z1, plot_z2)
            

    def build_plot(self, x1, x2, z1, z2):
        y_x1_z1 = mc.getHeight(x1,z1)
        y_x1_z2 = mc.getHeight(x1,z2)
        y_x2_z1 = mc.getHeight(x2,z1)
        y_x2_z2 = mc.getHeight(x2,z2)

        # get max height of the plot
        max_height = max(y_x1_z1, y_x1_z2, y_x2_z1, y_x2_z2)

        mc.setBlocks(x1, max_height, z1, x2 , max_height, z2 , block.STONE)
        self.plot_list.append(Plot(x1, x2, max_height, max_height,z1 ,z2))

        mc.setBlocks(x1, max_height + 1, z1, x2, max_height + 10, z2, block.AIR)
        self.landfill_plot(x1 - 1, max_height - 1, z1 - 1, x2 + 1, z2 + 1)

    # recursive function to fill land under plot
    def landfill_plot(self, x_min, y, z_min, x_max, z_max):
        i = 0
        while i < 15:
            mc.setBlocks(x_min, y-10, z_min, x_max, y, z_max, block.GRASS) 
            x_min -=1
            x_max +=1
            z_min -=1
            z_max +=1
            y -= 1
            i += 1
    
    def check_plot(self, x1, x2, z1, z2):
        # we need to check all corners of the plot to see whether they are within the range of an existing plot
        # checking the co-ords of (x1, z1), (x1, z2) (x2, z1) and (x2, z2)
        # if plot list is empty, can built first plot
        if not self.plot_list:
            return False
        else:
            # for each conflict in the corners of the plot co-ords to check
            for plot in self.plot_list:
                # check if x1 & z1 are within an existing plot
                if (plot.x1-10 <= x1 <= plot.x2+10) and (plot.z1-10 <= z1 <= plot.z2+10):
                    return True
                # check if x1 & z2 are within an existing plot
                if (plot.x1-10 <= x1 <= plot.x2+10) and (plot.z1-10 <= z2 <= plot.z2+10):
                    return True
                # check if x2 & z1 are within an existing plot
                if (plot.x1-10 <= x2 <= plot.x2+10) and (plot.z1-10 <= z1 <= plot.z2+10):
                    return True
                # check if x2 & z2 are within an existing plot
                if (plot.x1-10 <= x2 <= plot.x2+10) and (plot.z1-10 <= z2 <= plot.z2+10):
                    return True
            return False 


    def centre(self):
        sumX = 0
        sumZ = 0
        for i in range(len(self.plot_list)):
            sumX += (self.plot_list[i].x1 + self.plot_list[i].x2)/2
            sumZ += (self.plot_list[i].z1 + self.plot_list[i].z2)/2
        div_num = len(self.plot_list)
        x = sumX/div_num
        z = sumZ/div_num
        y = mc.getHeight(x, z)
        return x, y, z
