from random import randint

# Stores the current cell
class c_info:
    def __init__(self, c_cell):
        self.c_cell = c_cell

def main(size):
    # Maze size
    #size = 10

    # Stores maze with the following code:
    # 0 - Unvisited Cell
    # 1 - Empty space/corridor (visited)
    # 2 - Wall (visited or unvisited)
    array = []

    # Here we create a grid of isolated empty cells:
    # #########
    # #########
    # ## # # ##
    # #########
    # ## # # ##
    # #########
    # ## # # ##
    # #########
    # #########
    # Note the double thickness outside walls (to avoid literal edge-cases).
    for i in range (0, size * 2 + 3):
        if i%2 == 0 and not i == size*2+2 and not i==0:
            sub_array = [2,2]
            for j in range (0, size):
                sub_array.append(0)
                sub_array.append(2)
            sub_array.append(2)
            array.append(sub_array)
        else:
            sub_array = []
            for j in range (0, size * 2 + 3):
                sub_array.append(2)
            array.append(sub_array)
    #print(array)

    c_cell = [2,2]
    c_cell = c_info(c_cell)
    c_cell.c_cell

    # This is used later to check if the algorithm is done
    unvisited_cells_exist = True

    # The "stack" is used to track visited cells (cf. the algorithm)
    stack = [c_cell.c_cell]

    # Unused, 
    def is_at_edge(cell):
        if cell[0] == 0 or cell[1] == 0 or cell[0] == len(array) or cell[1] == len(array[0]):
            return True

    # Each of the connect_X methods should break the wall between
    # the current cell and one of the 4 surrounding cells, and set
    # the current cell to that new cell.
    def connect_1(x,y, c_cell):
        c_cell.c_cell[0] = x + 2
        array[x + 1][y] = 1
        array[x][y] = 1
        return c_cell.c_cell
        

    def connect_2(x,y, c_cell):
        c_cell.c_cell[1] = y + 2
        array[x][y + 1] = 1
        array[x][y] = 1
        return c_cell.c_cell

    def connect_3(x,y, c_cell):
        c_cell.c_cell[0] = x - 2
        array[x - 1][y] = 1
        array[x][y] = 1
        return c_cell.c_cell

    def connect_4(x,y, c_cell):
        c_cell.c_cell[1] = y - 2
        array[x][y - 1] = 1
        array[x][y] = 1
        return c_cell.c_cell

    # Used to limit iterations to avoid infinite loops.
    count = 0

    while unvisited_cells_exist:

        #print(c_cell.c_cell)

        count += 1
        #print("Loop iteration " + str(count))
        
        
        # Select one of 4 sides.
        side = randint(0,3)
        x = c_cell.c_cell[0]
        y = c_cell.c_cell[1]
        if array[x-2][y]==0 or array[x][y+2]==0 or array[x][y-2]==0 or array[x-2][y]==0:
            free_cells = True
        else:
            free_cells = False
        if free_cells:
            # This does the selecting and assures equal probability for each side.
            # Follows the following number order:
            # side = 0: 1 -> 2 -> 3 -> 4
            # side = 1: 2 -> 4 -> 1 -> 3
            # side = 2: 3 -> 1 -> 4 -> 2
            # side = 3: 4 -> 3 -> 2 -> 1
            if side == 0:
                if array[x+2][y] == 0:
                    c_cell.c_cell = connect_1(x,y, c_cell)
                elif array[x][y+2] == 0:
                    c_cell.c_cell = connect_2(x,y, c_cell)
                elif array[x-2][y] == 0:
                    c_cell.c_cell = connect_3(x,y, c_cell)
                elif array[x][y-2] == 0:
                    c_cell.c_cell = connect_4(x,y, c_cell)
            elif side == 1:
                if array[x][y+2] == 0:
                    c_cell.c_cell = connect_2(x,y, c_cell)
                elif array[x][y-2] == 0:
                    c_cell.c_cell = connect_4(x,y, c_cell)
                elif array[x+2][y] == 0:
                    c_cell.c_cell = connect_1(x,y, c_cell)
                elif array[x-2][y] == 0:
                    c_cell.c_cell = connect_3(x,y, c_cell)
            elif side == 2:
                if array[x-2][y] == 0:
                    c_cell.c_cell = connect_3(x,y, c_cell)
                elif array[x+2][y] == 0:
                    c_cell.c_cell = connect_1(x,y, c_cell)
                elif array[x][y-2] == 0:
                    c_cell.c_cell = connect_4(x,y, c_cell)
                elif array[x][y+2] == 0:
                    c_cell.c_cell = connect_2(x,y, c_cell)
            elif side == 3:
                if array[x][y-2] == 0:
                    c_cell.c_cell = connect_4(x,y, c_cell)
                elif array[x-2][y] == 0:
                    c_cell.c_cell = connect_3(x,y, c_cell)
                elif array[x][y+2] == 0:
                    c_cell.c_cell = connect_2(x,y, c_cell)
                elif array[x+2][y] == 0:
                    c_cell.c_cell = connect_1(x,y, c_cell)
            #if not stack[-1] == c_cell.c_cell:
            stack.append(list(c_cell.c_cell))
        # Stack removing part of algorithm
        elif not stack == []:
            #print(stack)
            c_cell.c_cell = stack[-1]
            del stack[-1]

        # Check if all cells have been visited.
        unvisited_cells_exist = False
        for i in array:
            for j in i:
                if j == 0:
                    unvisited_cells_exist = True
        #print(count)
        if count == 30000:
            #print("fail")
            break
        #print(str(stack[-1]))

    #print(array)

    '''def print_maze(array):
        print_array = list(array)
        for i in range (0,len(print_array)):
            print_array[i] = list(print_array[i])

        string_array = ""

        for i in range (0, len(print_array) ):
            for j in range (0, len(print_array[i]) ):
                if print_array[i][j] == 2:
                    print_array[i][j] = ""
                elif print_array[i][j] == 1:
                    print_array[i][j] = " "
                elif print_array[i][j] == 0:
                    print_array[i][j] = "X"
                string_array = string_array + print_array[i][j]
            string_array = string_array + "\n"

        #for i in print_array:
        #    print(i)
        print (string_array)'''

    #!print_maze(array)

    # Temporary hack to fix bug with random empty cells.
    for i in range(0,len(array)):
        for j in range(0,len(array[i])):
            if array[i][j] == 0:
                array[i][j] = 1

    #!print_maze(array)

    # Makes set entrance
    array[2][0] = 1
    array[2][1] = 1

    # Makes random exit
    exit_int = randint(0,size*4)

    if exit_int < size:
        array[exit_int * 2 + 1][0] = 1
        array[exit_int * 2 + 1][1] = 1
    elif exit_int < size*2:
        array[size*2 + 1][(exit_int - size)*2 + 1] = 1
        array[size*2 + 2][(exit_int - size)*2 + 1] = 1
    elif exit_int < size*3:
        array[(exit_int - size*2) * 2 + 1][size*2 + 1] = 1
        array[(exit_int - size*2) * 2 + 1][size*2 + 2] = 1
    elif exit_int < size*4:
        array[0][(exit_int - size*3) * 2 + 1] = 1
        array[1][(exit_int - size*3) * 2 + 1] = 1

    #!print_maze(array)
    return array

if __name__ == "__main__":
    while True:
        try:
            size = int(input("What size of maze do you want generated? "))
            break
        except TypeError:
            print("Please input an interger")
    main(size)
