

class TaskRunner
  def initialize()
  end
  
  def evaluate(number)
    count = 0
    
    while not is_palindrome(number)
      number = (number.reverse.to_i + number.to_i).to_s
      count += 1
      if count > 100
        break
      end
    end

    "#{count} #{number}"
  end
  
  def is_palindrome num
    str = num.to_s
    
    while str.length > 0
      if str.length == 1
        return true
      end
      if str.length == 2 and str[0] == str[1]
        return true
      end
      if str[0] != str[-1]
        return false
      end
      
      str = str.slice(1, str.length-2)
    end
    
    true
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

