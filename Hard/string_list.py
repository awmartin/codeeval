import sys

def all_combinations(chars, length):
    if isinstance(chars, str):
        chars = list(set([x for x in chars]))
    if length == 1:
        return chars
    
    ret = []
    for char in chars:
        for combination in all_combinations(chars, length - 1):
            word = char
            word += combination
            ret.append(word)
    return ret

def compute(line):
    length, string = line.split(",")
    combinations = all_combinations(string, int(length))
    return ",".join(sorted(list(combinations)))

def main():
    args = sys.argv
    assert len(args) == 2, "Please specify one file as an argument."
    filename = args[1]
    
    lines = None
    with open(filename) as f:
        lines = f.readlines()
    assert lines is not None and isinstance(lines, list), "File wasn't read properly."
    
    for line in lines:
        if len(line.strip()) == 0:
            continue
        print compute(line.strip())
    
if __name__ == "__main__":
    main()
