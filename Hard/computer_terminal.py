"""Computer Terminal - William Martin - submission on CodeEval

An solution implementation for the Computer Terminal problem on CodeEval.com.
"""

import sys

class InsertMode(object):
    pass
class OverwriteMode(object):
    pass

class Screen(object):
    def __init__(self):
        def row():
            return [' '] * 10
        
        self.chars = []
        for i in range(10):
            self.chars.append(row())
    
    def get(self, pt):
        return self.chars[pt.r][pt.c]
    
    def write(self, pt, char):
        self.chars[pt.r][pt.c] = char
    
    def get_row(self, r_index):
        return self.chars[r_index]

    def set_row(self, r_index, content):
        assert isinstance(content, list), "set_row expects a list of chars for a row"
        self.chars[r_index] = content
        
    def print_screen(self, cursor=None):
        if cursor is not None:
            char = self.chars[cursor.r][cursor.c]
            self.chars[cursor.r][cursor.c] = 'X'
        for row in self.chars:
            print "".join(row)
        if cursor is not None:
            self.chars[cursor.r][cursor.c] = char
        
    def clear(self):
        r = 0
        while r < len(self.chars):
            c = 0
            row = self.chars[r]
            while c < len(row):
                self.chars[r][c] = ' '
                c += 1
            r += 1


class Cursor(object):
    def __init__(self, r, c):
        self.r = max(min(r, 9), 0)
        self.c = max(min(c, 9), 0)
    
    def __str__(self):
        return "Cursor(%s, %s)" % (self.r, self.c)
    
    def up(self, dist=1):
        self.move_to(r=self.r - dist)
        
    def down(self, dist=1):
        self.move_to(r=self.r + dist)
        
    def left(self, dist=1):
        self.move_to(c=self.c - dist)
        
    def right(self, dist=1):
        self.move_to(c=self.c + dist)
    
    def move_to(self, r=None, c=None):
        if r is not None:
            self.r = max(min(r, 9), 0)
        if c is not None:
            self.c = max(min(c, 9), 0)

class ComputerTerminal(object):
    def __init__(self):
        self.screen = Screen()
        self.cursor = Cursor(0, 0)
        self.mode = OverwriteMode
    
    def run_tests(self, lines):
        pass
    
    def set_insert_mode(self):
        self.mode = InsertMode
    
    def set_overwrite_mode(self):
        self.mode = OverwriteMode
    
    def evaluate(self, lines):
        parser = Parser()
        
        commands = []
        for line in lines:
            line = Util.sanitize_line(line)
            if line.strip() != '':
                commands.extend(parser.parse_line(line))
        
        for command in commands:
            command.evaluate(self)
            
        self.screen.print_screen()
    
    def write(self, char):
        
        if issubclass(self.mode, OverwriteMode):
            self.screen.write(self.cursor, char)
        
        elif issubclass(self.mode, InsertMode):
            row = self.screen.get_row(self.cursor.r)
            chars_to_shift = row[self.cursor.c:]
            new_row = row[:self.cursor.c] + [char] + chars_to_shift[:-1]
            self.screen.set_row(self.cursor.r, new_row)
        
        else:
            assert False, "Unknown mode."
        
        self.cursor.right()
        

class Command(object):
    def __str__(self):
        return "Command()"
        
    def evaluate(self, terminal):
        assert False, "Subclasses implement."
    
    @classmethod
    def is_parsable_as(cls, remaining):
        """Returns whether the left of the given string is parsable as this command."""
        assert False, "Subclasses implement."
        
    @classmethod
    def parse(cls, remaining):
        """Parses the given string and returns the remaining, unconsumed string."""
        assert False, "Subclasses implement."
    
class Clear(Command):
    def __str__(self):
        return "Clear()"
    
    def evaluate(self, terminal):
        terminal.screen.clear()
    
    @classmethod
    def is_parsable_as(cls, remaining):
        return remaining[0:2] == '^c'
        
    @classmethod
    def parse(cls, remaining):
        return cls(), remaining[2:]

class Home(Command):
    def __str__(self):
        return "Home()"
    
    def evaluate(self, terminal):
        terminal.cursor.move_to(0, 0)
    
    @classmethod
    def is_parsable_as(cls, remaining):
        return remaining[0:2] == '^h'
        
    @classmethod
    def parse(cls, remaining):
        return cls(), remaining[2:]

class Beginning(Command):
    def __str__(self):
        return "Beginning()"
    
    def evaluate(self, terminal):
        terminal.cursor.move_to(c=0)
    
    @classmethod
    def is_parsable_as(cls, remaining):
        return remaining[0:2] == '^b'
        
    @classmethod
    def parse(cls, remaining):
        return cls(), remaining[2:]

class Down(Command):
    def __str__(self):
        return "Down()"
    
    def evaluate(self, terminal):
        terminal.cursor.down()
    
    @classmethod
    def is_parsable_as(cls, remaining):
        return remaining[0:2] == '^d'
        
    @classmethod
    def parse(cls, remaining):
        return cls(), remaining[2:]

class Up(Command):
    def __str__(self):
        return "Up()"
    
    def evaluate(self, terminal):
        terminal.cursor.up()
    
    @classmethod
    def is_parsable_as(cls, remaining):
        return remaining[0:2] == '^u'
        
    @classmethod
    def parse(cls, remaining):
        return cls(), remaining[2:]

class Left(Command):
    def __str__(self):
        return "Left()"
    
    def evaluate(self, terminal):
        terminal.cursor.left()
    
    @classmethod
    def is_parsable_as(cls, remaining):
        return remaining[0:2] == '^l'
        
    @classmethod
    def parse(cls, remaining):
        return cls(), remaining[2:]

class Right(Command):
    def __str__(self):
        return "Right()"
    
    def evaluate(self, terminal):
        terminal.cursor.right()
    
    @classmethod
    def is_parsable_as(cls, remaining):
        return remaining[0:2] == '^r'
        
    @classmethod
    def parse(cls, remaining):
        return cls(), remaining[2:]

class Erase(Command):
    def __str__(self):
        return "Erase()"
    
    def evaluate(self, terminal):
        row = terminal.screen.get_row(terminal.cursor.r)
        num_to_erase = 9 - terminal.cursor.r
        new_row = row[:terminal.cursor.r+1] + [' '] * num_to_erase
        terminal.screen.set_row(terminal.cursor.r, new_row)
    
    @classmethod
    def is_parsable_as(cls, remaining):
        return remaining[0:2] == '^e'
        
    @classmethod
    def parse(cls, remaining):
        return cls(), remaining[2:]

class Insert(Command):
    def __str__(self):
        return "InsertMode()"
    
    def evaluate(self, terminal):
        terminal.set_insert_mode()
    
    @classmethod
    def is_parsable_as(cls, remaining):
        return remaining[0:2] == '^i'
        
    @classmethod
    def parse(cls, remaining):
        return cls(), remaining[2:]

class Overwrite(Command):
    def __str__(self):
        return "OverwriteMode()"
    
    def evaluate(self, terminal):
        terminal.set_overwrite_mode()
    
    @classmethod
    def is_parsable_as(cls, remaining):
        return remaining[0:2] == '^o'
        
    @classmethod
    def parse(cls, remaining):
        return cls(), remaining[2:]

class Circumflex(Command):
    def __str__(self):
        return "Insert(^)"
    
    def evaluate(self, terminal):
        terminal.write('^')
    
    @classmethod
    def is_parsable_as(cls, remaining):
        return remaining[0:2] == '^^'
        
    @classmethod
    def parse(cls, remaining):
        return cls(), remaining[2:]

class Move(Command):
    def __str__(self):
        return "Move(%s, %s)" % (self.r, self.c)
    
    def __init__(self, r, c):
        self.r = r
        self.c = c
    
    def evaluate(self, terminal):
        terminal.cursor.move_to(self.r, self.c)
    
    @classmethod
    def is_parsable_as(cls, remaining):
        digits = '0123456789'
        return remaining[0] == '^' and \
            remaining[1] in digits and \
            remaining[2] in digits
        
    @classmethod
    def parse(cls, remaining):
        return cls(int(remaining[1]), int(remaining[2])), remaining[3:]

class InsertChar(Command):
    def __str__(self):
        return "Insert(%s)" % self.char
    
    def __init__(self, char):
        assert char != "^", "Unrecognized command"
        self.char = char
    
    def evaluate(self, terminal):
        terminal.write(self.char)
    
    @classmethod
    def is_parsable_as(cls, remaining):
        if remaining[0] == "^":
            assert False, "Unrecognized command at start of: %s" % remaining
        return True
        
    @classmethod
    def parse(cls, remaining):
        return cls(remaining[0]), remaining[1:]

AvailableCommands = [
    Clear, Home, Beginning, Left, Right, Up, Down, 
    Erase, Insert, Overwrite, Circumflex, Move,
    InsertChar # Keep as the last command.
    ]

class Parser(object):
    def parse_line(self, line):
        commands = []
        while len(line) > 0:
            for CommandType in AvailableCommands:
                if CommandType.is_parsable_as(line):
                    command, line = CommandType.parse(line)
                    commands.append(command)
                    break
        return commands
        


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
    #filename, test_flag = parse_args()
    filename = 'computer_terminal.txt'
    test_flag = False
    
    lines = open_input_file(filename)
    
    if test_flag:
        ComputerTerminal().run_tests(lines)
    else:
        ComputerTerminal().evaluate(lines)
        
if __name__ == "__main__":
    main()
