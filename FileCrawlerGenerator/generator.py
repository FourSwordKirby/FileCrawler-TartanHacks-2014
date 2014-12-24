import os
import zipfile
from level import *

class Crawler(object):

    EXTENSION = ".txt"

    ''' For local file
    def __init__(self, root_path=".", map_name="my_level"):
        self.map_name = map_name
        self.description = self.translate_folder(root_path, 0)
        self.floor_list = self.build_floors(self.description)
        self.tile_maps = self.build_tile_maps(self.floor_list)
    '''

    def __init__(self, ziplist=[], map_name="my_level"):
        self.map_name = map_name
        self.description = self.translate_ziplist(ziplist)
        self.floor_list = self.build_floors(self.description)
        self.tile_maps = self.build_tile_maps(self.floor_list)

    def translate_folder(self, path, depth):
        code = str(depth) + " "
        code += os.path.basename(path).replace(" ", "_") + " "
        parent_name = os.path.basename(os.path.dirname(path)).replace(" ", "_")
        if len(parent_name) == 0:
            parent_name = "@"
        code += parent_name + " "
        items = []
        folders = []
        for obj in os.listdir(path):
            obj_path = os.path.join(path, obj)
            if os.path.isdir(obj_path):
                folders.append(obj_path)
            else:
                items.append(obj_path)
        code += str(len(items)) + " " + str(len(folders))
        #for item in items:
            #print ("."*depth) + "Found item: " + item
        if folders:
            for folder in folders:
                code += "\n" + self.translate_folder(folder, depth+1)
            return code
        else:
            return code

    def is_dir(self, file_name):
        return file_name.endswith("/")

    #Returns full paths
    def list_dir(self, folder, ziplist):
        all_files = [x for x in ziplist if x.startswith(folder) and x != folder]
        right_files = []
        for x in all_files:
            half = x.rsplit("/", 1)            
            if (half[0] + "/" == folder
                or (half[1] == '' and
                    half[0].rsplit("/", 1)[0] + "/" == folder)):
                right_files.append(x)
        return right_files

    def translate_ziplist(self, ziplist):
        basename = "root"
        zipfolder = basename + "/"
        parent_name = "@"
        depth = 0
        for i in xrange(len(ziplist)):
            ziplist[i] = zipfolder + ziplist[i]
        code = str(depth) + " " + basename + " " + parent_name + " "
        
        items = []
        folders = []
        for obj in self.list_dir(zipfolder, ziplist):
            if self.is_dir(obj):
                folders.append(obj)
            else:
                items.append(obj)
        code += str(len(items)) + " " + str(len(folders))
        #for item in items:
            #print ("."*depth) + "Found item: " + item
        if folders:
            for folder in folders:
                code += "\n"
                code += self.translate_zipfolder(folder, ziplist, depth+1)
            return code
        else:
            return code
        
    def translate_zipfolder(self, zipfolder, ziplist, depth):
        code = str(depth) + " "
        s = zipfolder.rsplit("/", 2)
        basename = s[1]
        
        code += basename.replace(" ", "_") + " "
        si = s[0].rfind("/")
        parent_name = s[0] if si < 0 else s[0][si + 1:]

        code += parent_name.replace(" ", "_") + " "
        items = []
        folders = []
        for obj in self.list_dir(zipfolder, ziplist):
            if self.is_dir(obj):
                folders.append(obj)
            else:
                items.append(obj)
        code += str(len(items)) + " " + str(len(folders))
        #for item in items:
            #print ("."*depth) + "Found item: " + item
        if folders:
            for folder in folders:
                code += "\n"
                code += self.translate_zipfolder(folder, ziplist, depth+1)
            return code
        else:
            return code
        

    def build_floors(self, desc):
        floor_list = []
        parents = []
        prev_depth = -1
        floor_desc_list = desc.splitlines()
        for line_num in xrange(len(floor_desc_list)):
            info = floor_desc_list[line_num].split()
            depth = int(info[0])          #info[0] = depth
            name = info[1]           #info[1] = string of folder name
            #parent_name = info[2]
            num_items = int(info[3]) 
            num_sub = int(info[4])

            if prev_depth < 0:
                parent = None
            elif depth > prev_depth:
                parent = parents[prev_depth]
            elif depth == prev_depth:
                parents.pop()
                parent = parents[depth - 1]
            else: #info[0] < prev_depth
                while len(parents) - 1 >= depth:
                    parents.pop()
                parent = parents[depth-1]
            floor = Floor(name, num_items + num_sub + 1, parent)
            for i in xrange(num_items):
                floor.add_room(Room())
            for i in xrange(num_sub):
                floor.add_room(StairRoom())
            floor_list.append(floor)
            parents.append(floor)
            prev_depth = depth
        return floor_list

    def build_tile_maps(self, floor_list):
        return [x.get_string() for x in floor_list]

    def count_floors(self, floor_list):
        return len(floor_list)

    def get_string(self):
        s = str(self.count_floors(self.floor_list)) + "\n"
        s += self.description + "\n"
        s += ";\n"
        for tile_map in self.tile_maps:
            s += tile_map + "\n\n"
        return s

    def save_map(self):
        dest = open(self.map_name + self.EXTENSION, 'w')
        dest.write(self.get_string())
        dest.close()
        print "Successfully saved to", self.map_name + self.EXTENSION


zipFile = zipfile.ZipFile("PoE-Item-Info-v1.7.5-hazydoc-20140312.zip")
my_zip_list = zipFile.namelist()
c = Crawler(my_zip_list)
print c.get_string()
c.save_map()
