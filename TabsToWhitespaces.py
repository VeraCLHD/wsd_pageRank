import sys
import fileinput

def tabsToWhitespaces(file):
    
    for line in fileinput.input(file, inplace=True):
        line = line.replace("\t", "    ")
        sys.stdout.write(line)
    
if __name__ == "__main__":
    tabsToWhitespaces(sys.argv[1])