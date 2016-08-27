#!/usr/bin/env python2.7

# External functions
import time.sleep as sleep
import random.randint as randint
import mcpi.minecraft as minecraft
import Test01.main as maze_generator
"""import anyio.GPIO as GPIO
import anyio.seg7 as display"""

# Simplifying important objects
mc = minecraft.Minecraft.create()

# Setup for the button and the display (external hardware used for the course)
"""button = 4 # the button is 4 for the 4th pin
seg7_pins = [7, 6, 14, 16, 10, 8, 9, 15] # same as above for the seg7 display pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN)
ON = False
display.setup(GPIO, seg7_pins, ON) # the display uses the data to set up the display"""


# Own functions
def go(array):
    """Teleports to coordinates' location
    (array: list or tuple)"""
    mc.player.setTilePos(array[0], array[1], array[2])


def check_contained(current_coords, array):
    """Checks if matching x, z coordinates are within a list
    (current_coords: list or tuple, array: list or tuple) -> bool"""
    for x, y, z in array:
        if x == current_coords[0] and z == current_coords[2]:
            return True
    return False


def check_adj(current_coords, counted_blocks):
    """Checks how many horizontally adjacent blocks match x, z coordinates within a list
    (current_coords: list or tuple, counted_blocks: list or tuple) -> int"""
    surrounding_coords = ((1, 0, 0), (0, 0, 1), (1, 0, 1),
                          (-1, 0, 0), (0, 0, -1), (-1, 0, -1),
                          (1, 0, -1), (-1, 0, 1))
    number_walls = 0
    for x, y, z in counted_blocks:
        for X, Y, Z in surrounding_coords:
            adj_block = (current_coords[0] + X, current_coords[1] + Y, current_coords[2] + Z)
            if adj_block[0] == x and adj_block[2] == z:
                number_walls += 1
    return number_walls


def modify_maze(maze, width, length):
    """Coverts a generated maze into a format suitable for the game
    (maze: list, width: int, length: int) -> list"""
    no_checkpoints = 0
    entrance_or_exit = []  # (outer wall gaps)

    # Converts the 1 for gaps, 2 for walls used in the generator into a binary format
    for line in maze:
        for n, i in enumerate(line):
            if i == 1:
                line[n] = "0"
            elif i == 2:
                line[n] = "1"

    for x in range(0, width):
        for y in range(0, length):
            # any gaps in the outer wall (entrance/exit) stored as coordinates
            if ((x == 0 and y == 0) or (x == width - 1 and y == length - 1) or
                        x == 0 or x == width - 1 or y == 0 or y == length - 1) and maze[x][y] == '0':
                entrance_or_exit.append((x, y))
                # print("entrance")
            # turns all the outside cells to 2's if not gaps
            elif ((x == 0 and y == 0) or (x == width - 1 and y == length - 1) or
                          x == 0 or x == width - 1 or y == 0 or y == length - 1) and maze[x][y] == '1':
                maze[x][y] = "2"
                # print("outside")
            # randomly turns inside gap blocks into checkpoints up to max of the area of the maze / 5
            elif maze[x][y] == '0' and no_checkpoints < int(round((width*length)/5)):
                # print("gap")
                if randint(1, 20) == 1:
                    maze[x][y] = "4"
                    no_checkpoints += 1
    # puts the start block on the entrance (assigns it '5') and the pillar on the exit (assigns it '3')
    for i in range(0, len(entrance_or_exit)):
        x = entrance_or_exit[i][0]
        y = entrance_or_exit[i][1]
        if i == 0:
            maze[x][y] = "5"
        else:
            maze[x][y] = "3"
    return maze


def construct_maze(maze, origin_x, origin_y, origin_z, limits_block, column_block):
    """Construct the maze using Minecraft blocks and by saving entity locations
    maze: list, origin_x: int, origin_y: int, origin_z: int, limits_block: int, column_block: int)\
    -> (list, list, list, tuple)"""
    wall_coords = []
    checkpoint_coords = []
    column_coords = []
    teleport_pos = "none"

    # New, changeable variables are created from the maze origin points
    x = origin_x
    z = origin_z
    y = origin_y

    for line in maze:
        for cell in line:
            if cell == "0":
                pass  # gaps shown by "0"
            elif cell == "1":
                pass  # inside walls shown using "1"
                wall_coords.append((x, y, z))  # coordinates set to teleport the player back if entered
            elif cell == "2":
                b = limits_block  # the outer walls shown using "2"
                wall_coords.append((x, y, z))  # coordinates set to teleport the player back if entered
                mc.setBlock(x, y, z, b)  # a marking material is placed on the same level as the player
            elif cell == "3":
                b = column_block  # the column for the exit is shown using "3"
                column_coords.append((x, y, z))  # column coordinates stored for detecting maze completion
                mc.setBlocks(x, y - 10, z, x, y + 10, z, b) # pillar created
            elif cell == "4":
                # checkpoints are shown using "4"
                checkpoint_coords.append((x, y, z)) # coordinates saved to act as a checkpoint
            elif cell == "5":  # the block labeled "5" becomes the starting place for the player if included
                go([x, y, z])
                teleport_pos = (x, y, z)

            # Creating the initial maze shape
            """mc.setBlock(x, y, z, b)
            mc.setBlock(x, y+1, z, b)
            mc.setBlock(x, y+2, z, b)
            mc.setBlock(x, y+3, z, b)
            mc.setBlock(x, y+4, z, limits)
            mc.setBlock(x, y-1, z, limits)"""

            x += 1

        x = origin_x
        z += 1
    return wall_coords, checkpoint_coords, column_coords, teleport_pos


# Main program
def main():
    # Defines the materials of the different blocks
    limits_block = 89  # The material for (TMF) the outside border of the maze
    column_block = 22  # TMF the column that marks the end of the maze
    start_block = 49  # TMF the block that the player initially stands on
    checkpoint_block = 20  # TMF the block below the player on the checkpoints
    reward_block = 57  # TMF the block the column turns into upon beating the maze

    # Counting variables
    deaths = 0
    counter = 0  # used for delays in the while loop
    seconds = 0
    minutes = 0
    maze_no = 1
    # maze_numbers = []

    # Randomises the order of the mazes
    """while len(maze_numbers) < 5:
        random_no = randint(1, 5)
        if random_no not in maze_numbers:
            maze_numbers.append(random_no)"""

    # Creates the maze
    # (try, finally is used so that the voltage for the seg7 can be returned once the function is stopped)
    try:
        while True:
            # The player's first position is set as the starting block and the place they will teleport back to at first
            pos = mc.player.getTilePos()
            teleport_pos = (pos.x, pos.y, pos.z)

            # Maze counter
            mc.postToChat("Maze number " + str(maze_no))

            # The starting point of the maze is made one block diagonal to the player
            origin_x = pos.x + 1
            origin_y = pos.y
            origin_z = pos.z + 1

            # The starting block (block below the player) is set to a certain type of block
            mc.setBlock(pos.x, pos.y - 1, pos.z, start_block)

            # Imports the maze plan
            """f = open("maze{0}.csv".format(number), "r")

            # The maze file is converted into a list and modified to fit the game
            for line in f.readlines():
                    d_line = (list(line.split(",")))
                    d_line[-1] = d_line[-1][0]
                    data.append(d_line)

            data = modify_maze(data, len(data), len(data[0]))"""

            # Generates and implements the maze
            maze_size = 10  # size is not equivalent to length or width. Maze area = (size*2+3)^2
            maze_data = maze_generator(maze_size) # generates a maze using the random generator
            """for line in maze_data:
                print(line)"""
            maze_data = modify_maze(maze_data, maze_size * 2 + 3, maze_size * 2 + 3)
            """for line in maze_data:
                print(line)"""
            list_coords = construct_maze(maze_data, origin_x, origin_y, origin_z, column_block, limits_block)
            wall_coords = list_coords[0]
            checkpoint_coords = list_coords[1]
            column_coords = list_coords[2]
            tel_pos = list_coords[3]
            if tel_pos != "none":
                teleport_pos = tel_pos # teleport is set to the starting block if included
            game_ended = False

            # The contents are done once every quarter of a second
            while True:
                pos = mc.player.getTilePos()  # get the player's position

                # Checking if on a block surrounding the column (causes game end)
                if check_adj((pos.x, pos.y, pos.z), column_coords) >= 1 and not game_ended:
                    while seconds >= 60:
                        minutes += 1
                        seconds -= 60
                    # tells the user the time they took to complete the maze
                    mc.postToChat("You have taken " + str(minutes) + " minutes and " + str(seconds) + " seconds")
                    mc.postToChat("You have died " + str(deaths) + " times")
                    # the  column becomes the reward block
                    mc.setBlocks(column_coords[0][0], column_coords[0][1] - 10, column_coords[0][2],
                                 column_coords[0][0], column_coords[0][1] + 10, column_coords[0][2], reward_block)
                    game_ended = True
                    break

                # Checking if at a checkpoint
                if check_contained((pos.x, pos.y, pos.z), checkpoint_coords) == True:
                    mc.setBlock(pos.x, origin_y - 1, pos.z,
                                checkpoint_block)  # checkpoint block is placed in the maze floor
                    teleport_pos = (pos.x, pos.y, pos.z)  # the player is set to teleport back to that point in future

                # Checking if in a wall
                elif check_contained((pos.x, pos.y, pos.z), wall_coords) == True:
                    go(teleport_pos)
                    deaths += 1
                    mc.postToChat(
                        "You have died " + str(deaths) + " times")

                # Showing number of surrounding walls
                if counter >= 2:  # Checks every 2 seconds
                    no_walls = check_adj((pos.x, pos.y, pos.z), wall_coords)
                    # display.write(str(no_walls)) # Puts the number of blocks around you on the seg7 display
                    if no_walls > 0:
                        mc.postToChat("You are surrounded by " + str(no_walls) + " wall blocks")
                    counter = 0

                sleep(0.25)  # there is a delay on running these checks
                counter += 0.25  # the counter follows the time delay
                if not game_ended:
                    seconds += 0.25

            sleep(5)
            # Teleports you back to your original position before generating the new maze
            go((origin_x - 1, origin_y, origin_z - 1))
            maze_no += 1

            # mc.postToChat("You have completed all of the mazes")

    # Once something stops the program all voltages will be returned to 0 on the breadboard
    finally:
        # GPIO.cleanup()
        pass

if __name__ == "__main__":
    main()
