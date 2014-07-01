import sys

def get_char(index, string):
    if index < 0:
        return None
    if index >= len(string):
        return None
    return string[index]

def search_for(haystack, pattern):
    i = len(haystack) - 1
    j = len(pattern) - 1
    
    while i >= 0:
        char = haystack[i]
        found_wildcard = get_char(j, pattern) == "*" and get_char(j-1, pattern) != "\\"
        if char == pattern[j] or found_wildcard:
            # Found a match at the end. Look for more characters.
            is_wildcard = False
            while j >= 0:
                haystack_char = get_char(i, haystack)
                pattern_char = get_char(j, pattern)
                next_char = get_char(j - 1, pattern)
                
                if pattern_char == "*" and next_char != "\\":
                    is_wildcard = True
                
                if is_wildcard:
                    if next_char == haystack_char:
                        is_wildcard = False
                        j -= 1 # Advance past the asterisk to the next character.
                        i += 1 # Have a look at the current haystack char again.
                    if next_char is None:
                        is_wildcard = False
                        return True
                    
                else:
                    if haystack_char != pattern_char:
                        break
                    if j == 0 and haystack_char == pattern_char:
                        return True
                    j -= 1
                
                # Skip the backslashes. \*
                if next_char == "\\":
                    j -= 1
                    if j == -1 and pattern_char == '*' and haystack_char == "*":
                        return True
                i -= 1
                
        i -= 1
    
    return False

def compute(line):
    haystack, pattern = line.split(',')
    result = search_for(haystack, pattern)
    return str(result).lower()

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
