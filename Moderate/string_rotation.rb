

class TaskRunner
  def initialize()
  end
  
  def rotate(word)
    word.slice(1, word.length) + word[0]
  end
  
  def evaluate(line)
    word, to_test = line.split(",")
    
    i = 0
    while i < word.length
      if to_test == word
        return "True"
      end
      to_test = rotate(to_test)
      i += 1
    end
    
    return "False"
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

