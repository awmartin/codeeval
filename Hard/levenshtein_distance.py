import sys

class LevenshteinDistance(object):
    def __init__(self):
        self.words = []
    
    def evaluate(self, lines):
        cases = []
        words = []
        gathering_cases = True
        for line in lines:
            if line.strip() == "":
                continue
            line = Util.sanitize_line(line)
            if line == "END OF INPUT":
                gathering_cases = False
                continue
            if gathering_cases:
                cases.append(line)
            else:
                words.append(line)
        
        self.words = words
        
        # Caches the values computed for lev dist along the way.
        self.cache = {}
        
        for case in cases:
            print self.compute(case)
        
    def run_tests(self, lines):
        self.evaluate(lines.split("\n"))
        
    def compute(self, case):
        """Determine the size of the 'neighborhood' of the word 'case' in 'words'."""
        
        count = 0
        for word in self.words:

            # Shortcuts
            if abs(len(case) - len(word)) > 1:
                continue
            
            self.cache = {}
            dist = self.levenshtein_distance(case, word, len(case), len(word))
            if dist == 1:
                count += 1
        return count
    
    def levenshtein_distance(self, word_a, word_b, i, j):
        key = (word_a, word_b, i, j)
        if key in self.cache:
            return self.cache[key]
        
        if min(i, j) == 0:
            return max(i, j)
        else:
            deletion = self.levenshtein_distance(word_a, word_b, i - 1, j) + 1
            key = (word_a, word_b, i - 1, j)
            if key not in self.cache:
                self.cache[key] = deletion - 1

            insertion = self.levenshtein_distance(word_a, word_b, i, j - 1) + 1
            key = (word_a, word_b, i, j - 1)
            if key not in self.cache:
                self.cache[key] = insertion - 1
            
            if word_a[i - 1] == word_b[j - 1]:
                indicator = 0
            else:
                indicator = 1
            match = self.levenshtein_distance(word_a, word_b, i - 1, j - 1) + indicator
            key = (word_a, word_b, i - 1, j - 1)
            if key not in self.cache:
                self.cache[key] = match - indicator
            
            return min(deletion, insertion, match)


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
    
    #test_flag = True
    if test_flag:
        test_file = """
hello
world
END OF INPUT
helios
helicopter
hell
hellos
hellsgate
whole
whirl
worlds
        """
        LevenshteinDistance().run_tests(test_file)
    else:
        LevenshteinDistance().evaluate(lines)
        
if __name__ == "__main__":
    main()
