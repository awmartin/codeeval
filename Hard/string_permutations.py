import sys

def all_permutations(arr):
    if len(arr) == 1:
        return [arr]
    
    tr = []
    for i, el in enumerate(arr):
        remainder = arr[:i] + arr[i+1:]
        for permutation in all_permutations(remainder):
            tr.append(el + permutation)
    
    return tr

def compute(line):
    permutations = all_permutations(line)
    return ",".join(sorted(permutations))

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
