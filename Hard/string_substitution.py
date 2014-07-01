import sys

class StringSubstitution(object):
    def evaluate(self, lines):
        for line in lines:
            line = Util.sanitize_line(line)
            print self.compute(line)
        
    def compute(self, line):
        haystack, replacements_str = line.split(";")
        
        replacements_flat = replacements_str.split(",")
        i = 0
        while i < len(replacements_flat) / 2:
            to_replace = replacements_flat[i*2]
            substitute = replacements_flat[i*2+1]
            haystack = self.substitute(haystack, to_replace, substitute)
            i += 1
        
        return haystack.replace("2", "0").replace("3", "1")
        
    def substitute(self, haystack, to_replace, substitute):
        two_three_sub = substitute.replace("0", "2").replace("1", "3")
        return haystack.replace(to_replace, two_three_sub)
    
    def run_tests(self):
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
    #test_flag = False
    
    lines = open_input_file(filename)
    #lines = ['10011011001;0110,1001,1001,0,10,11']
    
    if test_flag:
        StringSubstitution().run_tests(lines)
    else:
        StringSubstitution().evaluate(lines)
        
if __name__ == "__main__":
    main()
