"""Advanced Calculator for CodeEval

Contains classes that convert a calculator expression into an evaluatable data structure. These
classes include:

* ParseToken - Converts symbols in the expression string into objects that represent meaningful
    patterns of symbols.
* Expression - Expressions represent individual computations, and the base class includes
    methods that convert ParseTokens into Expressions.
* Parser - Takes strings and converts them into ParseTokens.
* Calculator - The actual calculator that takes a series of expression strings and evaluates them.
    Also includes a testing harness that attempts to convert the strings into their Python equivalents
    and evaluates the expressions against their Python expressions.
"""

# For testing purposes.
from __future__ import division
import re

# Needed for the Calculator.
import sys
import math


# ---------------------------------------------------------------------------------------------
# Parsing engine.

class ParseException(Exception):
    pass


class ParseToken(object):
    """Base class for all the parsed symbols and objects."""

    def __init__(self):
        pass

    def __str__(self):
        return "ParseToken()"

    @classmethod
    def parse(cls, string):
        """Parses the given string into an instance of this ParseToken type.

        Should return a tuple containing a ParseToken instance and the unparsed portion of the
        given string.
        """
        assert False, "Subclasses should implement."

    @classmethod
    def parsable(cls, string):
        """Determines whether the given string can be parsed as this ParseToken type."""
        assert False, "Subclasses should implement."


class Group(ParseToken):
    """A Group ParseToken represents symbols grouped by paired delimiters, like parens or pipes."""

    def __init__(self, inner, separators):
        assert isinstance(inner, ParseToken), "Group inner token should be a ParseToken subclass instance."
        assert isinstance(separators, str), "Group separators should be a string of two characters."

        # Another ParseToken object.
        self.inner = inner

        # A string holding the separating characters, e.g. "()"
        self.separators = separators

    def __str__(self):
        return "Group(%s, %s)" % (self.separators, self.inner)

    @classmethod
    def parsable(cls, string):
        return string[0] in "("

    valid_group_tokens = "()|"

    @classmethod
    def parse(cls, chars):
        start_char = chars[0]
        if start_char == "(":
            end_char = ")"
        else:
            assert False, "Got an unparsable group: %s" % chars

        left_count = 1
        right_count = 0

        # Look for the end of the parentheses.
        i = 1
        while i < len(chars):
            char = chars[i]

            if char == start_char and start_char != end_char:
                left_count += 1
            elif char == end_char:
                right_count += 1

            if left_count == right_count:
                # Parse the contents.
                contents = chars[1:i]
                token = Parser.parse_string_to_tokens(contents)
                return cls(token, start_char + end_char), chars[i+1:]

            i += 1

        assert False, "Mismatched character: %s" % chars


class Sequence(ParseToken):
    """Represents a list of ParseTokens, typically alternating between Symbols and other tokens."""

    def __init__(self, tokens):
        # A list of tokens to group into a sequence.
        assert isinstance(tokens, list), "Sequence.init requires a list of tokens."
        self.tokens = tokens

    def __str__(self):
        token_strings = [str(token) for token in self.tokens]
        return "Sequence(%s)" % (", ".join(token_strings))


class SymbolToken(ParseToken):
    """Represents operator-like symbols: +, -, *, /, mod, etc."""

    valid_symbols = '*/_+-^!|'

    def __init__(self, chars):
        self.chars = chars

    def __str__(self):
        return "SymbolToken(%s)" % self.chars

    @classmethod
    def parsable(cls, string):
        return string[:1] in cls.valid_symbols or \
                string[:3] == 'mod'

    @classmethod
    def parse(cls, string):
        if string[:1] in cls.valid_symbols:
            token = cls(string[:1])
            return token, string[1:]

        elif string[:3] == 'mod':
            token = cls(string[:3])
            return token, string[3:]

        else:
            assert False, "Attempted to parse an operator but failed: %s" % string


class ConstantToken(ParseToken):
    """Holds number literal."""

    number_tokens = '0123456789.'

    def __init__(self, digits):
        self.digits = digits

    def __str__(self):
        return "ConstantToken(%s)" % self.digits

    @classmethod
    def parsable(cls, string):
        return string[:2] == "Pi" or \
                string[:1] == 'e' or \
                string[:1] in cls.number_tokens

    @classmethod
    def parse(cls, chars):
        if chars[:2] == "Pi":
            return cls('Pi'), chars[2:]
        elif chars[:1] == 'e':
            return cls('e'), chars[1:]

        i = 0
        digits = ""

        while i < len(chars):
            char = chars[i]
            # While we're in the midst of valid characters, collect them.
            if char in cls.number_tokens:
                digits += char
            else:
                # Otherwise, wrap them in a ConstantToken and return.
                num_digits = len(digits)
                return cls(digits), chars[num_digits:]
            i += 1

        # Parsed a number that went to the end of the string.
        num_digits = len(digits)
        return cls(digits), chars[num_digits:]


class FunctionToken(ParseToken):
    """Used for function-call-like expressions, like sin(...)."""

    def __init__(self, name, group):
        # The name of the function, e.g. 'sqrt'.
        self.name = name
        # The ParseToken of the contents of the parens following the function name.
        self.group = group

    def __str__(self):
        return "Function(%s|%s)" % (self.name, self.group)

    @classmethod
    def parse(cls, string):
        name = cls.get_function_name(string)
        assert name is not None, "Invalid function name: %s" % string

        token_length = len(name)

        # Holds the parenthetical part after the function name. e.g. sin(12.0) -> (12.0)
        group_str = string[token_length:]

        # Parse the contents of (...) into a group.
        group, remaining = Group.parse(group_str)

        return cls(name, group), remaining

    @classmethod
    def get_function_name(cls, string):
        if string[:4] == 'sqrt':
            return 'sqrt'
        elif string[:3] in ('sin', 'cos', 'tan'):
            return string[:3]
        elif string[:2] in ('lg', 'ln'):
            return string[:2]
        return None

    @classmethod
    def parsable(cls, string):
        return cls.get_function_name(string) is not None


class Parser(object):
    """The Parser class provides mechanisms to convert expression strings into ParseToken objects.

    Use this class to take the input string and produce the input to the Expression class, which
    produces Expression trees with 'parse_token_to_expression'.
    """

    @classmethod
    def get_token_type(cls, string):
        """Returns the class that should parse the given string correctly."""

        token_types = (
                Group,
                SymbolToken,
                ConstantToken,
                FunctionToken,
                )

        for token_type in token_types:
            if token_type.parsable(string):
                return token_type
        raise ParseException("Found an invalid character: %s" % string)

    @classmethod
    def parse_string_to_tokens(cls, string):
        """Takes a given string and returns a ParseToken instance."""

        # Holds the list of tokens gathered from the string.
        tokens = []

        # Given the remainder of the string being parsed, this creates a token for the leftmost end
        # of the string. So 1+2 will result in a Number(1) token, and a remaining string '+2', which
        # will then be parsed into a SymbolToken(+) plus '2', and so on.
        remaining_string = string
        def get_token():
            token_type = cls.get_token_type(remaining_string)
            token, remaining = token_type.parse(remaining_string)
            tokens.append(token)
            return remaining

        # Loop over the entire string and populate the 'tokens' list.
        remaining_string = get_token()
        while len(remaining_string) > 0:
            remaining_string = get_token()

        # Wrap all collections of tokens in a Sequence instance.
        if len(tokens) > 1:
            return Sequence(tokens)
        return tokens[0]


# ---------------------------------------------------------------------------------------------
# Computable Expressions


class Expression(object):
    """Base class for all computable expressions. Includes methods that convert ParseTokens into Expressions.

    Most expressions are trees of other expressions, the leaves of which are numbers. Calling
    'compute' on any expression evaluates it's children and returns a combined value.
    """

    def __init__(self):
        pass

    def compute(self):
        """Computes the given expression, returning a float which is the value of the expression."""
        assert False, "Subclasses should implement."

    @classmethod
    def parse_token_to_expression(cls, token):
        """Given a ParseToken return an Expression tree to evaluate."""

        # An expression may get mixed in with the bunch during the translation process. If we get
        # one, just return it back to the caller.
        if isinstance(token, Expression):
            return token

        if isinstance(token, Group):
            if token.separators == '()':
                inner_expr = cls.parse_token_to_expression(token.inner)
                return Parentheses(inner_expr)
            elif token.separators == '||':
                inner_expr = cls.parse_token_to_expression(token.inner)
                return AbsoluteValue(inner_expr)

        elif isinstance(token, ConstantToken):
            if token.digits == "Pi":
                return Pi()
            elif token.digits == "e":
                return E()
            else:
                return Number(token.digits)

        elif isinstance(token, SymbolToken):
            # Produce empty expressions by initializing them with 'None' to start. The conversion
            # process from ParseToken to Expression will populate them according to the precedence
            # order.
            if token.chars == '*':
                return Multiply(None, None)
            elif token.chars == '/':
                return Divide(None, None)
            elif token.chars == 'mod':
                return Mod(None, None)
            elif token.chars == '+':
                return Add(None, None)
            elif token.chars == '-':
                # At this point, we don't know if it's a Negate or Subtract.
                return Minus()
            elif token.chars == '^':
                return Exponent(None, None)
            elif token.chars == '!':
                return Factorial(None)
            assert False, "Invalid symbol: %s" % token

        elif isinstance(token, FunctionToken):
            inner_expr = cls.parse_token_to_expression(token.group)
            if token.name == 'sqrt':
                return Sqrt(inner_expr)
            elif token.name == 'sin':
                return Sin(inner_expr)
            elif token.name == 'cos':
                return Cos(inner_expr)
            elif token.name == 'tan':
                return Tan(inner_expr)
            elif token.name == 'lg':
                return Log10(inner_expr)
            elif token.name == 'ln':
                return Log(inner_expr)
            assert False, "Function not defined: %s" % token

        elif isinstance(token, Sequence):
            # Loop through the tokens and tree-ify according to the presence of operators.

            # Absolute value tokens are a special case, since the pipes can't be matched easily.
            tokens = cls.group_absolute_values(token.tokens)

            # A first pass on the tokens to expressions converts all the Groups, the first level of
            # precedence for all expressions.
            expressions = [cls.parse_token_to_expression(t) for t in tokens]

            # Handle the unary operators, ! and - (negate).
            expressions = cls.collapse_factorial_operators(expressions)
            expressions = cls.collapse_negate_operators(expressions)

            # Parse all the binary operators in order of precedence.
            expressions = cls.collapse_binary_operators(expressions, ('Exponent',))
            expressions = cls.collapse_binary_operators(expressions, ('Multiply', 'Divide', 'Mod'))
            expressions = cls.collapse_binary_operators(expressions, ('Add', 'Subtract', 'Minus'))

            assert len(expressions) == 1, "Sequences should parse to a single expression: %s" % expressions

            return expressions[0]

        assert False, "Didn't know what to do with token: %s" % token

    @classmethod
    def group_absolute_values(cls, tokens):
        """Groups all pipe SymbolTokens (|) into Groups that represent the absolute value operation."""

        # First, attempt to distinguish between the beginning and end of the absolute value
        # expression. Uses context to determine whether a pipe is at the beginning or end.

        is_pipe = lambda token: isinstance(token, SymbolToken) and token.chars == '|'
        is_nonfactorial_symbol = lambda token: isinstance(token, SymbolToken) and token.chars != "!"

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if is_pipe(token):
                if i == 0:
                    # Pipes found at the start are definitely StartPipes.
                    tokens[i] = StartPipe()
                else:
                    prev_token = tokens[i - 1]

                    # If the previous token is a SymbolToken, this likely means that we're looking
                    # at the start of another absolute value expression, e.g. ... + |-10|
                    # The exception is factorial, which occurs at the end of a number literal:
                    # e.g. |-6!|
                    if is_nonfactorial_symbol(prev_token) or \
                            isinstance(prev_token, StartPipe):
                        tokens[i] = StartPipe()
                    else:
                        tokens[i] = EndPipe()
            i += 1

        # Check to see that we've counted the absolute value delimiters correctly.
        start_count = 0
        end_count = 0
        for token in tokens:
            if isinstance(token, StartPipe):
                start_count += 1
            elif isinstance(token, EndPipe):
                end_count += 1

        if start_count != end_count:
            raise ParseException("Absolute value delimiters weren't balanced: %s" % [str(t) for t in tokens])

        # Loop over the tokens again and recombine to produce Group tokens.

        new_tokens = tokens
        def group():
            """Finds one pair of pipes and returns a new list of tokens with that pair as a Group."""

            i = 0
            done = False
            start = None    # Index of the StartPipe instance.
            found = False   # Whether a pair was replaced.
            tr = []

            while not done:
                token = new_tokens[i]
                if isinstance(token, StartPipe):
                    # Just record where the last known StartPipe is.
                    start = i

                elif isinstance(token, EndPipe) and start is not None:
                    # Attempt to combine the space between this pipe and the last found pipe into a
                    # Group object, which will later become an AbsoluteValue Expression instance.

                    tokens_to_group = new_tokens[start+1:i]
                    assert len(tokens_to_group) > 0, "Absolute value tokens were adjacent."

                    if len(tokens_to_group) == 1:
                        inner = tokens_to_group[0]
                    else:
                        inner = Sequence(tokens_to_group)
                    abs_token = Group(inner, '||')

                    # Note that this excludes tokens at 'start' and 'i'.
                    tr = new_tokens[:start] + [abs_token] + new_tokens[i + 1:]
                    start = None
                    done = True
                    found = True
                i += 1
                if i == len(tokens):
                    done = True

            return tr, found

        # Continue to loop over the list of tokens until there are no more pipes left.
        found = True
        while found:
            new_tokens, found = group()
            if found:
                tokens = new_tokens

        return tokens


    @classmethod
    def collapse_operator_to_expression(cls, array, index):
        """Takes the token at the index and takes the left and right."""

        expr = array[index]
        # Here, we know that the operator should be a Subtract operation instead of a Negate.
        if isinstance(expr, Minus):
            expr = Subtract(None, None)

        left = array[index - 1]
        right = array[index + 1]

        expr.left = cls.parse_token_to_expression(left)
        expr.right = cls.parse_token_to_expression(right)

        # Remove 'left' and 'right', as they're now part of the tree as branches of 'expr'.
        return array[:index-1] + [expr] + array[index+2:]

    @classmethod
    def collapse_factorial_operators(cls, expressions):
        """Looks for factorial (e..g 6!) operations and replaces them with a Factorial expression."""

        i = 0
        done = False
        while not done:
            expr = expressions[i]

            if isinstance(expr, Factorial):
                expr.expr = expressions[i-1]
                # Remove the previous expression.
                expressions = expressions[:i-1] + [expr] + expressions[i+1:]

            i += 1
            if i >= len(expressions):
                done = True

        return expressions

    @classmethod
    def collapse_negate_operators(cls, expressions):
        """Looks for Minus (-) symbols and converts them to Negate operations."""

        i = 0
        done = False
        while not done:
            expr = expressions[i]

            if isinstance(expr, Minus):
                if i == 0 or isinstance(expressions[i-1], BinaryOperator):
                    expr = Negate(expressions[i+1])
                    expressions = expressions[:i] + [expr] + expressions[i+2:]

            i += 1
            if i >= len(expressions):
                done = True

        return expressions

    @classmethod
    def collapse_binary_operators(cls, expressions, operators_to_collapse):
        is_empty = lambda expr: expr.left is None and expr.right is None
        should_collapse = lambda expr: expr.name in operators_to_collapse
        is_operator = lambda expr: isinstance(expr, BinaryOperator) or isinstance(expr, Minus)

        i = 0
        done = False
        while not done:
            expr = expressions[i]
            if isinstance(expr, Minus):
                expr = Subtract(None, None)
            if is_operator(expr) and \
                    is_empty(expr) and \
                    should_collapse(expr):
                expressions = cls.collapse_operator_to_expression(expressions, i)
                i -= 2

            i += 1
            if i >= len(expressions):
                done = True

        return expressions


class Constant(Expression):
    pass

class Number(Constant):
    number_tokens = '0123456789.'

    def __init__(self, value_str):
        try:
            if '.' in value_str:
                self.value = float(value_str)
            else:
                self.value = int(value_str)
        except:
            assert False, "Number parser got on invalid string to convert: %s" % value_str

    def __str__(self):
        return "Number(%s)" % self.value

    def compute(self):
        return self.value

    @classmethod
    def parse(cls, tokens):
        # Inherently not greedy.
        i = 0
        digits = ""
        while i < len(tokens):
            token = tokens[i]
            if token in cls.number_tokens:
                digits += token
            else:
                return cls(digits), len(digits)
            i += 1
        return cls(digits), len(digits)

class Pi(Constant):
    def __str__(self):
        return "Pi"

    def compute(self):
        return math.pi

class E(Constant):
    def __str__(self):
        return "E"

    def compute(self):
        return math.e

class Function(Expression):
    name = "Function"

    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return "%s(%s)" % (self.name, self.expr)

class Sqrt(Function):
    name = "Sqrt"
    def compute(self):
        return math.sqrt(self.expr.compute())

class Sin(Function):
    name = "Sin"
    def compute(self):
        return math.sin(self.expr.compute())

class Cos(Function):
    name = "Cos"
    def compute(self):
        return math.cos(self.expr.compute())

class Tan(Function):
    name = "Tan"
    def compute(self):
        return math.tan(self.expr.compute())

class Log10(Function):
    name = "Log10"
    def compute(self):
        return math.log10(self.expr.compute())

class Log(Function):
    name = "Log"
    def compute(self):
        return math.log(self.expr.compute())

class Parentheses(Expression):
    def __init__(self, inner):
        self.inner = inner

    def __str__(self):
        return "Parentheses(%s)" % self.inner

    def compute(self):
        return self.inner.compute()


class AbsoluteValue(Expression):
    def __init__(self, inner):
        self.inner = inner

    def __str__(self):
        return "AbsoluteValue(%s)" % self.inner

    def compute(self):
        return abs(self.inner.compute())


class BinaryOperator(Expression):
    name = "BinaryOperator"

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "%s(%s, %s)" % (self.name, self.left, self.right)

class Add(BinaryOperator):
    name = "Add"

    def compute(self):
        return self.left.compute() + self.right.compute()

class Pipe(Expression):
    name = "Pipe"

    def __str__(self):
        return "Pipe()"

class StartPipe(object):
    pass
class EndPipe(object):
    pass


class Minus(Expression):
    name = "Minus"

    def __str__(self):
        return "Minus()"

class Subtract(BinaryOperator):
    name = "Subtract"

    def compute(self):
        return self.left.compute() - self.right.compute()

class Multiply(BinaryOperator):
    name = "Multiply"

    def compute(self):
        return self.left.compute() * self.right.compute()

class Divide(BinaryOperator):
    name = "Divide"

    def compute(self):
        left_value = self.left.compute()
        right_value = self.right.compute()
        return float(left_value) / float(right_value)

class Mod(BinaryOperator):
    name = "Mod"

    def compute(self):
        return self.left.compute() % self.right.compute()

class Exponent(BinaryOperator):
    name = "Exponent"

    def compute(self):
        return self.left.compute() ** self.right.compute()


class UnaryOperator(Expression):
    name = "UnaryOperator"

    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return "%s(%s)" % (self.name, self.expr)

class Factorial(UnaryOperator):
    name = "Factorial"

    def compute(self):
        return math.factorial(self.expr.compute())

class Negate(UnaryOperator):
    name = "Negate"

    def compute(self):
        return -self.expr.compute()


# ---------------------------------------------------------------------------------------------
# Main Calculator class.

class Calculator(object):
    """Calculator evaluates expression strings and can test them against Python equivalents."""

    def evaluate(self, lines):
        """Given a list of expression strings, parse and compute each one and print the result."""

        for line in lines:
            if len(line.strip()) == 0:
                continue

            result = self.compute(line)
            if isinstance(result, float):
                print Util.format_float(result)
            else:
                print result

    def compute(self, line):
        """Takes a single line, parses, and computes it into a float value."""

        line = Util.sanitize_line(line)
        token = Parser.parse_string_to_tokens(line)
        expr = Expression.parse_token_to_expression(token)
        return expr.compute()

    def run_tests(self, test_cases):
        """Runs a series of expression strings against their Python equivalents."""

        for case in test_cases:
            self.test(case)

    def test(self, line):
        """Take a single expression string, compute it, and compare that result to an equivalent Python expression."""

        line = Util.sanitize_line(line)

        # Evaluate the given expression.
        token = Parser.parse_string_to_tokens(line)
        expr = Expression.parse_token_to_expression(token)
        result = expr.compute()

        # Convert the expression to Python and evaluate.
        py_line = self.line_to_python_expr(line)
        py = getattr(__builtins__, 'e' + 'v' + 'a' + 'l')
        try:
            py_result = py(py_line)
        except:
            print "Couldn't evaluate '%s' as a Python expression." % py_line
            return

        sys.stdout.write("Testing '%s' against python '%s' ... " % (line, py_line))

        assert result == py_result, "Expression '%s' = %s didn't equal python line '%s' = %s\n%s" % (line, result, py_line, py_result, expr)

        print "OK"


    def line_to_python_expr(self, line):
        """Convert the given expression string into a Python string."""

        line = self.convert_literal_replacements(line)
        line = self.convert_pipes_to_abs(line)
        line = self.convert_exclamation_to_factorial(line)

        return line

    def convert_literal_replacements(self, line):
        to_replace = {
                'lg': 'math.log10',
                'ln': 'math.log',
                '^' : '**',
                'mod': '%',
                'e': 'math.e',
                'Pi': 'math.pi',
                'sin': 'math.sin',
                'cos': 'math.cos',
                'tan': 'math.tan'
                }

        for expr, py_expr in to_replace.iteritems():
            line = line.replace(expr, py_expr)

        return line

    def convert_exclamation_to_factorial(self, line):
        bang = re.compile('[0-9]*!')
        for match in bang.finditer(line):
            s = match.start()
            e = match.end()
            expr = match.group()
            line = line[:s] + 'math.factorial(' + expr[:-1] + ')' + line[e:]
        return line

    def convert_pipes_to_abs(self, line):
        """An admittedly dumb method of replacing pipes with math.abs(...). Won't work for nested cases."""

        i = 0
        count = 0
        while i < len(line):
            char = line[i]
            if char == '|':
                even = count % 2 == 0
                if even:
                    line = line[:i] + 'abs(' + line[i+1:]
                else:
                    line = line[:i] + ')' + line[i+1:]
                count += 1
            i += 1
        return line


class Util(object):
    """Utility functions for formatting and parsing."""

    @classmethod
    def sanitize_line(cls, line):
        line = line.replace(" ", "")

        # Remove the trailing newline.
        if line[-1] == "\n":
            line = line[:-1]

        return line

    @classmethod
    def format_float(cls, value):
        num = "%.5f" % round(value, 5)
        i = len(num) - 1
        while i >= 0:
            digit = num[i]
            if digit != "0":
                num = num[0:i+1]
                break
            i -= 1

        if num[-1] == ".":
            num = num[:-1]

        return num


# ---------------------------------------------------------------------------------------------
# Functions for actually running the program.

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
        Calculator().run_tests(lines)
    else:
        Calculator().evaluate(lines)

if __name__ == "__main__":
    main()


