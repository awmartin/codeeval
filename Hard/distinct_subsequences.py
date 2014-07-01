import sys
import re

class DistinctSubsequences(object):
    def evaluate(self, lines):
        for line in lines:
            line = Util.sanitize_line(line)
            print self.compute(line)

    def compute(self, line):

        haystack, needle = line.split(",")
        haystack = haystack.strip()
        needle = needle.strip()

        return self.find(haystack, needle)

    def find(self, haystack, needle):
        if len(needle) > len(haystack):
            return 0
        if len(needle) == len(haystack):
            if needle == haystack:
                return 1
            else:
                return 0
        if len(needle) == 1:
            if haystack.find(needle) != -1:
                pattern = re.compile(needle)
                matches = pattern.findall(haystack)
                return len(matches)
            return 0

        first_char = needle[0]
        start_pos = haystack.find(first_char)
        if start_pos == -1:
            return 0

        count = 0
        while start_pos < len(haystack):
            tr = haystack[start_pos+1:]

            count += self.find(tr, needle[1:])

            index = tr.find(first_char)
            if index == -1:
                # No more matches found for the first character in the remaining string.
                break

            start_pos = index + start_pos + 1

        return count


    def run_tests(self, test_cases):
        pass


class Util(object):
    """Utility functions for formatting and parsing."""

    @classmethod
    def sanitize_line(cls, line):

        # Remove the trailing newline.
        if line[-1] == "\n":
            line = line[:-1]

        return line

def open_input_file(filename):
    lines = None
    with open(filename) as f:
        lines = f.readlines()
    assert lines is not None and isinstance(lines, list), "File wasn't read properly."
    return lines

def parse_args():
    args = sys.argv
    assert len(args) in (2, 3), "Provide a filename or filename plus the --test flag."

    filename = args[1]

    test_flag = False
    if len(args) == 3:
        if args[2] in ('--test', '-t'):
            test_flag = True
        else:
            assert False, "First argument should be a filename and the second either --test or -t."

    return filename, test_flag

def main():
    filename, test_flag = parse_args()

    lines = open_input_file(filename)

    if test_flag:
        DistinctSubsequences().run_tests(lines)
    else:
        DistinctSubsequences().evaluate(lines)

if __name__ == "__main__":
    main()


