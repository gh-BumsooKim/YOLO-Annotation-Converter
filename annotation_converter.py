try:
    import os
    import sys
    import glob
    import time
    import argparse
    from typing import *
    from pprint import pprint
except ModuleNotFoundError as e:
    print("os, sys, glob, time, and argparse library can not imported with error :", e)
    
parser = argparse.ArgumentParser(description='Converter Program')
parser.add_argument('--path', type=str, help="input directory path including \
                    obj.names file",
                    default = os.getcwd())
parser.add_argument('--want_class', type=str, help='if you want classes, \
                    input file path, having obj.names format. \
                    Default : person, bicycle, car, motorbike, bus, truck',
                    default = None)
parser.add_argument('--obj_names', type=str, help="input obj.names format file,\
                    if your obj.names format file's name is not \'obj.names\'.",
                    default = None)
parser.add_argument('--merge_carclass', type=bool, help="check if merge bus, truck to car or not",
                    default = False)
args = parser.parse_args()

if __name__ == "__main__":
    # Processing Time
    start_time: float = time.time()
    
    # Wanted Path
    PATH: str = args.path # parser path
    
    if args.obj_names is None:
        FILE_NAME: str = "obj.names"
    else:
        FILE_NAME: str = args.obj_names
    
    #DIR = "Downloads/test"
    #PATH = os.path.join(PATH, DIR)
    #PATH = os.path.join(PATH, "data")
    
    # Wanted Classes : Dictionary Format
    if args.want_class is None:
        target_class: dict = {0 : "person",     1 : "bicycle", 2 : "car",
                              3 : "motorbike",  4 : "bus",     5 : "truck"}
    else:
        target_class: dict = dict()
        with open(args.want_class) as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "\n" in line:
                    target_class[i] = str(line.replace("\n", ""))
                else: target_class[i] = str(line)
    
    # Read Source Class
    os.chdir(PATH)
    
    if os.path.isfile(FILE_NAME):
        file_list: list = list()
        with open(FILE_NAME) as f:
            lines = f.readlines()
            for line in lines:
                if "\n" in line: file_list.append(line.replace("\n", ""))
                else: file_list.append(line)
    else:
        print("\nNotFoundFile :", FILE_NAME, "in your path\n")
    
    # Extract Source Class Number about Target Class
    source_class: dict = dict()
    for i in range(len(target_class)):
        if target_class[i] in file_list:
            source_class[file_list.index(target_class[i])] = target_class[i]
    
    # Extract from_class index, to_class_index
    if args.merge_carclass:
        if 'bus' not in target_class.values():       
            if 'bus' in file_list:
                source_class[file_list.index('bus')] = 'car'
        if 'truck' not in target_class.values():       
            if 'truck' in file_list:
                source_class[file_list.index('truck')] = 'car' 
                
    # Remove and Convert Labeling Box using Target Class
    os.chdir("obj_train_data")
    os.chdir(os.listdir()[0]) 
    
    text_file_list: list = glob.glob("*.txt")
    
    reversed_target_class: dict = dict(map(reversed, target_class.items()))
    
    removed_box: int = 0
    total_box: int = 0
    old_class_count: list = [0] * len(file_list)
    new_class_count: list = [0] * len(target_class.keys())
    
    for text_file in text_file_list:
        temp_text: list = list()
        with open(text_file) as f:
            lines = f.readlines()
            for line in lines:
                # Old Class Counting
                old_idx: int = -1
                if line.split()[0] != "None":
                    old_idx = int(line.split()[0])
                    old_class_count[old_idx] += 1
                
                if old_idx in source_class.keys():
                    # Class Number Mapping / Source -> Target
                    new_idx = str(reversed_target_class[source_class[old_idx]])
                    
                    new_line = line.split()[1:]
                    new_line.insert(0, new_idx)
                    
                    temp_text.append(" ".join(new_line) + "\n")
                    
                    # New Class Counting
                    new_class_count[int(new_idx)] += 1
                else: removed_box += 1
                total_box += 1                    
                    
        with open(text_file, 'w') as f:
            for text in temp_text:
                f.write(text)
        
        print("Processing...", text_file, end='\r')
    
    end_time: float = time.time()
    
    # Simple Analysis
    print("\nDone...\nLast Text File :",text_file)
    print("Processing Time :", round(end_time - start_time, 2), "sec")
    
    print("\nTotal Labeling Box :", total_box, "Box")
    print("Removed Labeling Box :", removed_box, "Box")
    
    try:
        ratio: float = round(removed_box/total_box, 4) * 100
    except ZeroDivisionError:
        ratio: int = 0
    
    print("Removed Ratio of \'removed_box/total_box\' :", ratio, "%")
    
    os.chdir("../..")
    
    # Convert Class Number
    with open("obj.data", 'r') as f:
        lines = f.readlines()
    
    lines[0] = "classes = " + str(len(target_class)) + "\n"
    with open("obj.data", 'w') as f:
        for line in lines:
            f.write(line)
        
    with open(FILE_NAME, 'w') as f:
        for class_name in target_class.items():
            f.write(class_name[1] + '\n')
            
    print("\nPrevious Class Number Indexing :\n", source_class)
    print("Modified Class Number Indexing :\n", target_class)    
    
    print("\nPrevious BBox Counting :")
    for i, value in enumerate(file_list):
        print(i, ":", value, ":", old_class_count[i], "Box")
    print("Total Previous BBox :", total_box, "Box")
    
    print("\nModified BBox Counting :")
    for i, value in enumerate(target_class.values()):
        print(i, ":", value, ":", new_class_count[i], "Box")
    print("Total Modified BBox :", sum(new_class_count), "Box")
