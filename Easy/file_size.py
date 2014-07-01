import sys
import os

def main():
    filename = sys.argv[1]
    fileinfo = os.stat(filename)
    print str(fileinfo.st_size).replace("L", "")

if __name__ == "__main__":
    main()

