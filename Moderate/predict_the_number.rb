

class TaskRunner
  def initialize()
  end
  
  def rotate(word)
    word.slice(1, word.length) + word[0]
  end
  
  def evaluate(line)
    n = line.to_i
    values = "01121220122020011220200120010112"
    get_value(n, values)
  end
  
  def cycle(values)
    values.gsub!("2", "3")
    values.gsub!("1", "2")
    values.gsub!("0", "1")
    values.gsub!("3", "0")
    values
  end
  
  def get_value(n, values)
    if n < 32
      values[n]
    else
      
      mag = Math.log(n, 2).floor
      n -= 2 ** mag
      
      get_value(n, cycle(values))
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

