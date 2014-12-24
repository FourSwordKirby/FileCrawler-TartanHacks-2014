import copy
import random

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
ROOM_DIR = [(-1, 0), (0, 1), (1, 0), (0, -1)]

WALL = 1
FLOOR = 0
STAIR_UP = 2
STAIR_DOWN = 2
DOOR = 0
VOID = 9

def tile_grid_join(a, b):
    if not a:
        for row in b:
            a.append(row)
        return
    if not b:
        return
    assert(len(a) == len(b))
    for r in xrange(len(b)):
        a[r].extend(b[r])
    return

class Floor(object):
    def __init__(self, name, num_rooms=1, parent=None):
        assert(num_rooms > 0)
        self.name = name
        self.num_rooms = num_rooms
        self.parent = parent
        start = AscendRoom() if parent != None else Room()
        self.room_grid_length = rgl = (2 * (num_rooms)) / 3 + 1
        self.room_grid = [[None for i in xrange(rgl)] for i in xrange(rgl)]
        start_row = random.randint(0, rgl - 1)
        start_col = random.randint(0, rgl - 1)
        self.room_grid[start_row][start_col] = start
        self.row_range = (start_row, start_row)
        self.col_range = (start_col, start_col)

    def __str__(self):
        parent_name = "None" if self.parent == None else self.parent.name
        return ("Floor: " + self.name + "\tnum_rooms: " + str(self.num_rooms)
                + "\tparent: " + parent_name)

    def is_valid_coord(self, row, col):
        if row < 0 or row >= self.room_grid_length:
            return False
        if col < 0 or col >= self.room_grid_length:
            return False
        return True

    def is_valid_loc(self, row, col):
        if (not self.is_valid_coord(row, col)
            or self.room_grid[row][col] != None):
            return False
        for i in xrange(4):
            (r, c) = (row + ROOM_DIR[i][0], col + ROOM_DIR[i][1])
            if self.is_valid_coord(r, c) and self.room_grid[r][c] != None:
                return True
        return False

    def add_room(self, room):
        rgl = self.room_grid_length
        r_range = (max([0, self.row_range[0] - 1]),
                   min(rgl, self.row_range[1] + 1))
        c_range = (max([0, self.col_range[0] - 1]),
                   min(rgl, self.col_range[1] + 1))
        loc = (random.randint(r_range[0], r_range[1]),
               random.randint(c_range[0], c_range[1]))
        while not self.is_valid_loc(loc[0], loc[1]):
            loc = (random.randint(r_range[0], r_range[1]),
                   random.randint(c_range[0], c_range[1]))
        self.room_grid[loc[0]][loc[1]] = room
        self.row_range = (min(self.row_range[0], loc[0]),
                          max(self.row_range[1], loc[0]))
        self.col_range = (min(self.col_range[0], loc[1]),
                          max(self.col_range[1], loc[1]))
        self.connect_rooms(loc[0], loc[1])

    def connect_rooms(self, row, col):
        room = self.room_grid[row][col]
        for i in xrange(4):
            (r, c) = (row + ROOM_DIR[i][0], col + ROOM_DIR[i][1])
            if self.is_valid_coord(r, c) and self.room_grid[r][c] != None:
                contact = room.connect(self.room_grid[r][c], i)
                self.room_grid[r][c].connect(room, (i+2)%4, contact)

    def tile_grid(self):
        grid = self.strip(copy.deepcopy(self.room_grid))
        tile_grid = []
        for r in xrange(len(grid)):
            row_tile_grid = []
            for c in xrange(len(grid[r])):
                room = VoidRoom() if grid[r][c] == None else grid[r][c]
                tile_grid_join(row_tile_grid, room.tile_grid())
            for row in row_tile_grid:
                tile_grid.append(row)
        return tile_grid

    def strip(self, grid):
        empty_row = [None for i in xrange(len(grid))]
        while empty_row in grid:
            grid.remove(empty_row)
        assert(len(grid) > 0)
        for c in xrange(len(grid[0])-1, -1, -1):
            all_none = True
            for r in xrange(len(grid)):
                if grid[r][c] != None:
                    all_none = False
                    break
            if all_none:
                for row in grid:
                    row.pop(c)
        return grid

    def get_string(self):
        tile_grid = self.tile_grid()
        s = ""
        for row in tile_grid:
            for c in xrange(len(row)):
                s += str(row[c])
                if c < len(row) - 1:
                    s += ","
            s += "\n"
        return s

    def write_map(self):
        f = open(name + ".txt", 'w')
        f.write(self.get_string)
        f.close()

class Room(object):
    ROOM_HEIGHT = 12
    ROOM_WIDTH = 18

    def __init__(self, h=ROOM_HEIGHT, w=ROOM_WIDTH):
        self.height = h
        self.width = w
        self.room = self.make_room()
        self.adjacents = [None for i in xrange(4)]

    # Creates 2D array of room size filled with num
    def make_room(self, num=FLOOR):
        room = []
        for r in xrange(self.height):
            room.append([])
            assert(r < len(room))
            for c in xrange(self.width):
                room[r].append(num)
        return room

    def tile_grid(self):
        tile_grid = copy.deepcopy(self.room)
        for c in xrange(Room.ROOM_WIDTH):
            tile_grid[0][c] = tile_grid[Room.ROOM_HEIGHT-1][c] = WALL
        for r in xrange(Room.ROOM_HEIGHT):
            tile_grid[r][0] = tile_grid[r][Room.ROOM_WIDTH-1] = WALL
        for i in xrange(4):
            if self.adjacents[i] != None:
                door = self.adjacents[i][1]
                if i == NORTH:
                    tile_grid[0][door] = DOOR
                elif i == EAST:
                    tile_grid[door][Room.ROOM_WIDTH-1] = DOOR
                elif i == SOUTH:
                    tile_grid[Room.ROOM_HEIGHT-1][door] = DOOR
                else: #if i == WEST:
                    tile_grid[door][0] = DOOR
        return tile_grid

    # Adds other to adjacents list.
    def connect(self, other, dir, contact=-1):
        if contact < 0: #Random!
            if dir % 2 == 0: #North, South
                contact = random.randint(1, Room.ROOM_WIDTH-2)
            else: #East, West
                contact = random.randint(1, Room.ROOM_HEIGHT-2)
        assert(dir >= 0 and contact > 0)
        self.adjacents[dir] = (other, contact)
        return contact

class AscendRoom(Room):
    def tile_grid(self):
        tile_grid = super(AscendRoom, self).tile_grid()
        tile_grid[Room.ROOM_HEIGHT / 2][Room.ROOM_WIDTH / 2] = STAIR_UP
        return tile_grid


class VoidRoom(Room):
    def tile_grid(self):
        return super(VoidRoom, self).make_room(VOID)

class StairRoom(Room):
    def tile_grid(self):
        tile_grid = super(StairRoom, self).tile_grid()
        r = random.randint(Room.ROOM_HEIGHT / 3, Room.ROOM_HEIGHT * 2 / 3)
        c = random.randint(Room.ROOM_WIDTH / 3, Room.ROOM_WIDTH * 2 / 3)
        tile_grid[r][c] = STAIR_DOWN
        return tile_grid
    
'''
num_rooms = 5
root_floor = Floor("root", num_rooms)
lower_floor = Floor("lower", num_rooms, root_floor)
for i in xrange(num_rooms - 1):
    root_floor.add_room(Room())
    lower_floor.add_room(Room())
print root_floor.get_string()
print "floor"
print lower_floor.get_string()
'''
