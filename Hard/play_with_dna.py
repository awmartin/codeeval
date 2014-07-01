import sys


class PlayWithDna(object):    
    def evaluate(self, lines):
        for line in lines:
            line = Util.sanitize_line(line)
            print self.compute(line)
        
    def run_tests(self, test_cases):
        for input, expected in test_cases:
            result = self.compute(input)
            if expected == result:
                print "Test passed: %s" % input
            else:
                print "Test failed: Expected %s and got %s" % (expected, result)
        
    def compute(self, line):
        pattern, num_mismatches, haystack = line.split(" ")
        num_mismatches = int(num_mismatches)
        
        if num_mismatches == 0:
            matches = self.find_subsequences(pattern, haystack, 0)
            return self.sort_matches(matches, pattern)

        all_subsequences = self.find_subsequences(pattern, haystack, num_mismatches)
        
        matches = self.sort_matches(all_subsequences, pattern)
        
        if len(matches) == 0:
            return "No match"
        return " ".join(matches)
    
    def sort_matches(self, matches, pattern):
        sorted_matches = []
        
        for match in matches:
            index = self.num_mismatches(pattern, match)
            sorted_matches.append((index, match))
        
        sorted_matches = sorted(sorted_matches)

        return [pair[1] for pair in sorted_matches]
        
        
    def num_mismatches(self, x, y):
        if x == y:
            return 0
        num_different = 0
        i = 0
        while i < len(x):
            if x[i] != y[i]:
                num_different += 1
            i += 1
        return num_different
        
    def find_subsequences(self, pattern, haystack, num_mismatches):
        matches = []
        
        start = 0
        while start < len(haystack) - len(pattern):
            j = 0
            mismatches_left = num_mismatches
            found = True
            match = ""
            i = start
            
            while j < len(pattern):
                char = pattern[j]
                if char != haystack[i]:
                    mismatches_left -= 1
                    if mismatches_left == -1:
                        found = False
                        break
                    match += haystack[i]
                else:
                    match += char
                j += 1
                i += 1
            
            if found:
                matches.append(match)
            
            start += 1
            
        return matches

        
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
    
    # test_flag = True
    if test_flag:
        test_cases = [
            ["CCC 1 CGCCCGAATCCAG", 'CCC CCA CCG CGC GCC TCC'],
            ['GCGAG 2 CCACGGCCTATGTATTTGCAAGGATCTGGGCCAGCTAAATCAGCACCCCTGGAACGGCAAGGTTCATTTTGTTGCGCGCATAG', 'GCAAG GCAAG GCCAG GCGCG GCGCA GCTAA'],
            ['CGGCGCC 1 ACCCCCGCAGCCATATGTCCCCAGCTATTTAATGAGGGCCCCGAACACGGGGAGTCTTACACGATCTGCCCTGGAATCGC', 'No match']
            ]
        PlayWithDna().run_tests(test_cases)
    else:
        PlayWithDna().evaluate(lines)
        
if __name__ == "__main__":
    main()
