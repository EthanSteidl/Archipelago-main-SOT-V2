import time

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--input_directory', dest='input_directory', type=str,
                    help='Microsoft login cookie given to www.seaofthieves.com', nargs='+')
args = parser.parse_args()
input_directory = str(args.input_directory[0])




#        32,26
        #64,52
x = 32
y = 26
width = 64-32
height = 52-26

class XY:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

dims = {
    "banana": XY(42, 0, 58-42, 37-0),
    "coconut": XY(32, 26, 64-32, 52-26),
    "mango": XY(32, 26, 64-32, 52-26),
    "pineapple": XY(32, 26, 64-32, 52-26),
    "pomegran": XY(32, 26, 64-32, 52-26),
}

for path_list, folders_list, files_list in os.walk(input_directory):

    for folder_primary in folders_list:
        foutneg = open("samples/" + folder_primary + "_negatvies", "w")
        for folder_secondary in folders_list:


            if folder_secondary == folder_primary:
                #make positives
                fout = open("samples/" +folder_primary + "_positive", "w")
                for path2, folders2, files2 in os.walk("{}\\{}".format(input_directory, folder_secondary)):
                    for found_file in files2:
                        sample_name = "{}/{}".format(folder_secondary, found_file)
                        out_dims = dims[folder_primary]
                        fout.write("{} {} {} {} {} {}\n".format(sample_name, 1, out_dims.x, out_dims.y, out_dims.width, out_dims.height))
                fout.close()
            else:
                #make positives

                for path2, folders2, files2 in os.walk("{}\\{}".format(input_directory, folder_secondary)):
                    for found_file in files2:
                        sample_name = "{}/{}/{}".format("samples",folder_secondary, found_file)
                        foutneg.write("{}\n".format(sample_name))

        foutneg.close()
