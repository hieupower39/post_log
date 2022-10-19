import sys
import getopt
import warnings
import re

def init(data):
    pattern = ""
    strings = []
    isPattern = True
    for line in data:
        strings.append(line.replace("\n", ""))
        if isPattern:
            pattern = line.replace("\n", "")
            strings = []
            isPattern  = False        
    return pattern, strings

def regex_check (pattern, strings):
    results = []
    for string in strings:
        prog = re.compile(pattern)
        result = prog.match(string)
        results.append(result)
    return results

def run(data):
    pattern, strings = init(data=data)
    results = regex_check(pattern, strings)
    index = 1
    count = 0
    for result in results:
        print(str(index)+". ", end = "")
        if result == None:
            print("False")
        else:
            count += 1
            print("True")
        index += 1
    print("Matches "+str(count)+" in "+str(index-1))

def main(argv):
    warnings.filterwarnings("ignore")
    input_file = ''
    opts, args = getopt.getopt(argv,"hi:o:",["input_file="])
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py --input_file <input_file>')
            sys.exit()
        elif opt in ("--input_file"):
             input_file = arg
    run(data=open(input_file, 'r'))
    del args


if __name__ == "__main__":
    main(sys.argv[1:])
        
