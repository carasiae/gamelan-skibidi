from model import *
from convert import *
import os
from math import *



def list_files(directory):
    try:
        # List all files in the specified directory
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        for i, file in enumerate(files):
            files[i] = os.path.join(directory, file)
        return files
    except FileNotFoundError:
        print(f"Error: The directory '{directory}' was not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ng = NGram(2)
    directory = input("Enter the directory path: ")
    files = list_files(directory)
    print(files)
    maxlen = 0
    maxset = set()
    for file in files:
        sets = process_file(file)
        print(file)
        print(sets)
        for st in sets:
            if len(st) > maxlen:
                maxlen = len(st)
                maxset = st
            ng.read(st)
    print(">><<>><<")
    print(maxset)
    print(">><<>><<")
    # for x in sorted(ng.history.keys()):
    #     print(f"{x} => {ng.history[x]}")
    res = (ng.generate(64))
    p = ng.preplexity(res)
    for i, x in enumerate(res):
        if x[0] > 7:
            res[i] = (x[0] - 7,)
        else:
            res[i] = (x[0] * -1,)
    for i, x in enumerate(res):
        print(x, end = '')
        if i % 4 == 3:
            print()
    print(p)
