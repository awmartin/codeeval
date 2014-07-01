import sys

content = """Mary had a little lamb its fleece was white as snow;
And everywhere that Mary went, the lamb was sure to go.
It followed her to school one day, which was against the rule;
It made the children laugh and play, to see a lamb at school.
And so the teacher turned it out, but still it lingered near,
And waited patiently about till Mary did appear.
"Why does the lamb love Mary so?" the eager children cry; "Why, Mary loves the lamb, you know" the teacher did reply."""

class TypeAhead(object):
    def __init__(self):
        self.words = {} # word -> next words
        
        words = content.split(" ")
        
        # Last word has no predictions.
        self.words[words[-1]] = {}
        
        i = 0
        while i < len(content) - 1:
            word = words[i]
            next_word = words[i+1]
            if word in self.words:
                if next_word in self.words[word]:
                    self.words[word][next_word] += 1
                else:
                    self.words[word][next_word] = 1
            else:
                self.words[word] = {}
                self.words[word][next_word] = 1
    
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
        
    def compute(self, word):
        next_words = self.words[word]
        
        s = 0
        for word, value in next_words:
            s += value
        
        result = []
        for word, value in next_words:
            pair = (word, float(value) / s)
            result.append(pair)
        
        result = sorted(result, key = lambda p: (-p[1], p[0]))
        
        return ";".join(["%s,%s" % pair for pair in result])


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
        test_cases = [
            ["", ''],
            ]
        TypeAhead().run_tests(test_cases)
    else:
        TypeAhead().evaluate(lines)
        
if __name__ == "__main__":
    main()
