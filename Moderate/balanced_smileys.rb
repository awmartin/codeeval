

class TaskRunner
  def initialize()
    @integers = 26.times.map {|i| (i + 1).to_s }
  end
  
  def evaluate(line)
    indices = indices_of_potential_emoticons(line)
    indices_permutations = permutations(indices)
    
    to_test = indices_permutations.map do |perm|
      if perm.length == 0
        line.dup
      else
        chars = line.dup
        perm.each do |index|
          chars[index] = "|"
        end
        chars
      end
    end
    
    to_test.each do |string|
      if is_valid(string)
        return "YES"
      end
    end
    
    return "NO"
  end
  
  def permutations(values)
    if values.length == 0
      return []
    end
    if values.length == 1
      return [[], values]
    end
    
    first = values[0]
    rest = values.slice(1, values.length)
    rest_permutations = permutations(rest)
    tr = []
    rest_permutations.each do |perm|
      tr.push(perm)
      tr.push([first] + perm)
    end
    
    tr
  end
  
  def indices_of_potential_emoticons(chars)
    tr = []
    
    i = 0
    while i < chars.length
      char = chars[i]
      prev_char = i == 0 ? nil : chars[i - 1]
      
      if char == "("
        if prev_char == ":"
          tr.push(i)
        end
      elsif char == ")"
        if prev_char == ":"
          tr.push(i)
        end
      end
      
      i += 1
    end
    
    tr
  end
  
  def get_parity(chars)
    count = 0

    chars.each_char do |char|      
      if char == "("
        count += 1
      elsif char == ")"
        count -= 1
      end
    end
    
    count
  end
  
  def is_valid(chars)
    count = 0
    
    chars.each_char do |char|      
      if char == "("
        count += 1
      elsif char == ")"
        count -= 1
      end
      
      if count < 0
        return false
      end
    end
    
    if count == 0
      true
    else
      false
    end
  end
end


def main(args)
  runner = TaskRunner.new()
  
  filename = args[0]
  test_flag = false
  if args.length == 2 and ['-t', '--test'].include?(args[1])
    test_flag = true
  end
  
  f = File.open(filename)
  lines = f.readlines()
  
  if test_flag
    lines.each do |line|
      if line.strip.length > 0
        test_case, expected = line.strip.split(" ")
        answer = runner.evaluate(test_case)
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

