# Simple calculator
# Parses strings to tokens to a tree of expressions

class Expression
  def calculate
  end
end

# Represents constants, floats and integers.
class Constant < Expression
  def initialize(value)
    if value.include?(".")
      @value = value.to_f
    else
      @value = value.to_i
    end
  end
  
  def calculate
    @value
  end
  
  def to_s
    "Constant(#{@value})"
  end
end

class BinaryOperator < Expression
end

class Multiply < BinaryOperator
  def initialize(left, right)
    @left = left
    @right = right
  end
  
  def calculate
    @left.calculate() * @right.calculate()
  end
end

class Divide < BinaryOperator
  def initialize(left, right)
    @left = left
    @right = right
  end
  
  def calculate
    result = @left.calculate().to_f / @right.calculate().to_f
    if result.nan?
      result = @left.calculate() / @right.calculate()
    end
    result
  end
end

class Exponent < BinaryOperator
  def initialize(left, right)
    @left = left
    @right = right
  end
  
  def calculate
    @left.calculate() ** @right.calculate()
  end
end

class Add < BinaryOperator
  def initialize(left, right)
    @left = left
    @right = right
  end
  
  def calculate
    @left.calculate() + @right.calculate()
  end
end

class Subtract < BinaryOperator
  def initialize(left, right)
    @left = left
    @right = right
  end
 
  def calculate
    @left.calculate() - @right.calculate()
  end
end

# Unary operators work on just a single expression, like - or !.
class UnaryOperator < Expression
end

class Negate < UnaryOperator
  def initialize(target)
    @target = target
  end
  
  def calculate
    -@target.calculate()
  end
end

# Represents grouped expressions, like parens, brackets, braces, etc.
class Group < Expression
  def initialize(inner)
    @inner_expr = inner
  end
  
  def calculate
    @inner_expr.calculate()
  end
end


# ---------------------------------------------------------------
# Parsing

class Token
end

class Parenthesis < Token
  def initialize(paren)
    @paren = paren
  end
  
  def is_open?
    @paren == "("
  end
  
  def is_close?
    @paren == ")"
  end
  
  def to_s
    if is_open?
      "Token(OpenParen)"
    else
      "Token(CloseParen)"
    end
  end
end

class Number < Token
  attr_reader :number
  
  def initialize(number)
    @number = number
  end
  
  def to_s
    "Token(Number(#{@number}))"
  end
end

class Operator < Token
  attr_reader :symbol
  
  def initialize(symbol)
    @symbol = symbol
  end
  
  def to_s
    "Token(Operator(#{@symbol}))"
  end
end


# Has mechanisms to parse strings and series of tokens into expressions.
class Parser
  def parse(expression_string)
    tokens = parse_string_to_tokens(expression_string)
    parse_tokens_to_expression(tokens)
  end
  
  # Takes a raw expression string and returns a list of parse tokens.
  def parse_string_to_tokens(string)
    numeric_chars = "0123456789."
    operator_chars = "*/+-^"
    group_chars = "()"
    
    tokens = []
    i = 0
    while i < string.length
      char = string[i]
      
      if numeric_chars.include?(char)
        j = i
        number = ""
        while j < string.length
          number_char = string[j]
          if numeric_chars.include?(number_char)
            number += number_char
          else
            i -= 1
            break
          end
          i += 1
          j += 1
        end # end j
        
        token = Number.new(number)
        tokens.push(token)
      end # end parse number
      
      if operator_chars.include?(char)
        token = Operator.new(char)
        tokens.push(token)
      end
      
      if group_chars.include?(char)
        token = Parenthesis.new(char)
        tokens.push(token)
      end
      
      i += 1
    end # end i
    
    tokens
  end
  
  # Parses a given list of tokens (and expressions) into a list of a single expression.
  def parse_tokens_to_expression(tokens)
    with_numbers = parse_numbers(tokens)
    grouped = parse_groups(with_numbers)
    with_negations = parse_negate_operators(grouped)
    
    # Parse all the binary operators to make the tree.
    expressions = parse_operators(with_negations, ["^"])
    expressions = parse_operators(with_negations, ["*", "/"])
    expressions = parse_operators(expressions, ["+", "-"])
    
    expressions
  end
  
  # Parses all the binary operators, ^ * / + -.
  def parse_operators(expressions, operators_to_parse)

    i = 0
    while i < expressions.length
      expr = expressions[i]
      
      if expr.is_a?(Operator) and operators_to_parse.include?(expr.symbol)
        left = expressions[i - 1]
        right = expressions[i + 1]
        
        if expr.symbol == "^"
          expr = Exponent.new(left, right)
        elsif expr.symbol == "*"
          expr = Multiply.new(left, right)
        elsif expr.symbol == "/"
          expr = Divide.new(left, right)
        elsif expr.symbol == "+"
          expr = Add.new(left, right)
        elsif expr.symbol == "-"
          expr = Subtract.new(left, right)
        end
        
        expressions.slice!(i - 1, 3)
        expressions.insert(i - 1, expr)
        i -= 1
      end
      
      i += 1
    end  # end i
    
    expressions
  end
  
  # Turns all the numeric tokens into expression Constants.
  def parse_numbers(tokens)
    i = 0
    while i < tokens.length
      token = tokens[i]
      if token.is_a?(Number)
        tokens.slice!(i, 1)
        expr = Constant.new(token.number)
        tokens.insert(i, expr)
      end
      i += 1
    end
    tokens
  end
  
  # Parses all the parenthetical groups ().
  def parse_groups(tokens)
    tr = []
    
    inside = false
    count = 0
    
    start = 0
    stop = 0
    groups = []
    
    i = 0
    while i < tokens.length
      token = tokens[i]
      
      if token.is_a?(Parenthesis)
        if token.is_open? and not inside
          inside = true
          start = i
          count = 0
        end
        
        if token.is_open? and inside
          count += 1
        end
        if token.is_close? and inside
          count -= 1
        end
        
        if count == 0
          stop = i
          
          groups.push({:start => start, :stop => stop})
          
          start = 0
          stop = 0
          inside = false
        end
      end # end Parenthesis
      
      i += 1
    end  # end i
    
    offset = 0
    groups.each do |group|
      start = group[:start] - offset
      stop = group[:stop] - offset
      
      num_to_remove = stop - start + 1

      group_tokens = tokens.slice!(start, num_to_remove)
      inner_tokens = group_tokens[1...group_tokens.length-1]
      inner_expr = parse_tokens_to_expression(inner_tokens)[0]
      
      tokens.insert(start, Group.new(inner_expr))
      
      offset += num_to_remove - 1
    end
    
    tokens
  end
  
  # Parses all the '-' operators that appear to negate the next expression instead of 
  # perform subtraction.
  def parse_negate_operators(tokens)
    i = 0
    while i < tokens.length
      token = tokens[i]
      prev_token = i > 0 ? tokens[i - 1] : nil
      
      if token.is_a?(Operator)
        if token.symbol == "-"
          prev_is_operator = (not prev_token.nil? and prev_token.is_a?(Operator))
          
          if i == 0 or prev_is_operator
            elts = tokens.slice!(i, 2)
            target = parse_tokens_to_expression([elts[1]])[0]
            expr = Negate.new(target)
            tokens.insert(i, expr)
          end
          
        end
      end
      
      i += 1
    end
    
    tokens
  end
end

class Calculator
  def initialize()
  end
  
  def evaluate(expression_string)
    p = Parser.new()
    expr = p.parse(expression_string)
    expr[0].calculate()
  end
end



class TaskRunner
  def initialize()
  end
  
  def evaluate(line)
    line.gsub!(" ", "")
    line.strip!
    
    calc = Calculator.new()
    result = calc.evaluate(line)
    TaskRunner.format_result(result)
  end
  
  def self.remove_trailing_decimal(str)
    if str[-1] == "."
      str.slice(0, str.length - 1)
    else
      str
    end
  end

  def self.remove_trailing_zeros(str)
    if str[-1] == "0"
      remove_trailing_zeros str.slice(0, str.length-1)
    else
      str
    end
  end

  def self.format_result(result)
    if result.to_s.include?(".")
      str = "%.5f" % result
      str = remove_trailing_zeros(str)
      remove_trailing_decimal(str)
    else
      result.to_s
    end
  end
  
end

def convert_to_ruby(str)
  str.gsub("^", "**")
end

def main(args)
  runner = TaskRunner.new()
  
  filename = args[0]
  test_flag = false
  test_against_ruby = false
  
  if args.length == 2 and ['-t', '--test'].include?(args[1])
    test_flag = true
  elsif args.length == 2 and ['-r', '--ruby'].include?(args[1])
    test_against_ruby = true
  end
  
  f = File.open(filename)
  lines = f.readlines()
  
  if test_against_ruby
    method = ("e" + "v" + "a" + "l").to_sym
    
    evaluate = Proc.new {|str| Object.send(method, str)}
    
    lines.each do |line|
      answer = runner.evaluate(line).strip
      
      ruby = convert_to_ruby(line)
      answer_ruby = TaskRunner.format_result(evaluate.call(ruby))
      
      passes = answer_ruby == answer
      
      if passes
        puts "true"
      else
        puts "FAILED: #{line} expected #{answer_ruby} but got #{answer}"
      end
    end
  elsif test_flag
    lines.each do |line|
      if line.strip.length > 0
        test_case, expected = line.strip.split("=")
        expected.strip!
        test_case.strip!
        
        answer = runner.evaluate(test_case).strip
        passes = expected == answer
        
        if passes
          puts "true"
        else
          puts "FAILED: #{test_case} expected #{expected} but got #{answer}"
        end
        
      end
    end
  else
    lines.each do |line|
      if line.strip.length > 0
        puts runner.evaluate(line.strip)
      end
    end
  end
end

main(ARGV)

