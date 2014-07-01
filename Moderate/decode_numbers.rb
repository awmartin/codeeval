
class TaskRunner
  def initialize()
    @integers = 26.times.map {|i| (i + 1).to_s }
  end
  
  def evaluate(line)
    decode(line).to_s
  end
  
  def decode(string)
    if string.length == 1
      return 1
    end
    
    count = 0
    @integers.each do |integer|
      if string.slice(0,1) == integer
        count += decode string.slice(1,string.length)
      elsif string.slice(0,2) == integer
        remainder = string.slice(2,string.length)
        if remainder.length == 0
          count += 1
        else
          count += decode remainder
        end
      end
    end
    
    count
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

