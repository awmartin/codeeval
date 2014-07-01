


class TaskRunner
  def initialize
  end
  
  def evaluate(line)
    num_people, m = line.split(",")
    num_people = num_people.to_i
    m = m.to_i
    
    people = num_people.times.map {|i| i}
    method2(people, m)
  end
  
  def method2(people, m)
    still_alive = people.map {|i| true}
    to_kill = []
    
    count = 0
    index = 0
    
    while num_still_alive(still_alive) > 0
      if still_alive[index]
        count += 1
      end
      
      if count == m
        to_kill.push(index)
        still_alive[index] = false
        count = 0
      end
      
      index += 1
      if index == people.length
        index = 0
      end
    end
    
    to_kill.join(" ")
  end
  
  def num_still_alive(still_alive)
    still_alive.select {|x| x}.length
  end
  
  def method1(people, m)
    to_kill = []
    
    pos = m
    while people.length > 0
      next_person = people.slice!(pos - 1, 1)
      to_kill.push(next_person)
      
      if people.length == 0
        break
      end
      
      pos += m - 1
      while pos >= people.length
        pos -= people.length
      end
    end
    
    to_kill.join(" ")
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

