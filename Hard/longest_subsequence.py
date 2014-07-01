import sys

def get_char(index, string):
    if index < len(string):
        return string[index]
    return None

def get_subsequence(left, right):
    """Gets the longest CONTIGUOUS subsequence."""
    
    word = None
    current_longest = ""
    
    start_i = start_j = 0
    i = j = 0
    while i < len(left):
        lchar = get_char(i, left)
        j = 0
        while j < len(right):
            rchar = get_char(j, right)
            
            if lchar == rchar:
                word = lchar + get_subsequence(left[i+1:], right[j+1:])
                if len(word) > len(current_longest):
                    current_longest = word
                word = None
                break
            
            j += 1
        i += 1
    return current_longest
    

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
        left, right = line.split(";")
        longest = get_subsequence(left.strip(), right.strip())
        print longest.strip()
    
if __name__ == "__main__":
    main()