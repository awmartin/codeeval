import sys


def compute(line):
    current_longest = ""

    i = 0  # left start position
    k = 0  # left subtr
    j = 0  # right substr

    while i < len(line):
        char = line[i]
        j = i + 1
        substr = None
        max_substring_length = 0
        done = False

        while j < len(line):
            repeat_char = line[j]
            if char == repeat_char:
                if substr is None:
                    substr = char
                    max_substring_length = j - i
                    k = i
                else:
                    substr += char
                k += 1
                char = line[k]

                if k - i == max_substring_length or \
                        j == len(line) - 1:
                    done = True

            elif substr is not None:
                done = True
                # Don't increment j. We want to examine this character again as it might be the
                # start to a new valid subsequence.
                j -= 1

            if done:
                # Done. Reset and look for another substring.
                if len(substr) > len(current_longest) and \
                        substr.strip() != "":
                    current_longest = substr
                char = line[i]
                substr = None
                k = i
                done = False

            j += 1

        i += 1

    if current_longest.strip() == "":
        return "NONE"
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
        # Remove the trailing newline.
        if line[-1] == "\n":
            line = line[:-1]
        print compute(line)

if __name__ == "__main__":
    main()

