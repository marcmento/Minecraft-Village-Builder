import random
from mcpi.minecraft import Minecraft
from house import house
from terrain import Terrain
from path import Path
mc = Minecraft.create()

North = 1
East = 2
South = 3
West = 4



playerTilePos = mc.player.getTilePos()
A = Terrain(playerTilePos.x, playerTilePos.y, playerTilePos.z, 0, 75)

print("Clearing Land")
A.bulldoze(75)

print("Buidling Hills")
A.hills()

print("Making Plots")
for i in range(5):
    plotsize = random.randint(15,25)
    A.generate_plot(plotsize)


playerX, playerY, playerZ = A.centre()
pb = Path(1)

# Construct Paths from new player centrer
for i in range(len(A.plot_list)):
    print("Building Path: ", i+1)
    plotter = A.plot_list[i]
    xMid = (plotter.x1 + plotter.x2)/2
    zMid = (plotter.z1 + plotter.z2)/2
    pb.pathBuilding(xMid, zMid, playerX, playerZ)
wellX, wellZ = pb.buildWell(playerX, playerZ)  
pb.pathBuilding(wellX - 4, wellZ, playerX, playerZ)

#Teleport player above ground
mc.player.setPos(playerX, playerY+15, playerZ)

# Build Houses on Plots
for i in range(len(A.plot_list)):
    print("Building House: ", i+1)
    plotter = A.plot_list[i]
    #Moving door to closest middle axis
    xMid = (plotter.x1 + plotter.x2)/2 - playerX
    zMid = (plotter.z1 + plotter.z2)/2 - playerZ

    if abs(xMid) >= abs(zMid):
        if(zMid >= 0):
            dirc = North
        else:
            dirc = South
    else:
        if(xMid >= 0):
            dirc = West
        else:
            dirc = East

    newhouse = house(plotter.x1 , plotter.y1, plotter.z1, plotter.x2, plotter.z2, dirc)
    
