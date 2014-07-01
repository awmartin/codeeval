

class TaskRunner
  def initialize()
  end
  
  def evaluate(line)
    margin = 6    # distance btw first/last bat and buildings
    
    input = line.split(" ")
    
    wire_length = input[0].to_i
    interval_btw_bats = input[1].to_i
    num_bats = input[2].to_i
    if input.length > 3
      known_bats = input[3..input.length].map {|pos| pos.to_i - margin}
    else
      known_bats = []
    end
    
    allowed_length = wire_length - margin * 2
    
    max_count = 0
    offset = 0
    
    # Brute force check.
    while offset <= interval_btw_bats
      x = offset
      bats = []  # The array of bats so far.
      
      while x <= allowed_length
        close_to_bat = false
        
        (bats + known_bats).each do |pos|
          if (x - pos).abs < interval_btw_bats
            close_to_bat = true
            if not bats.include?(pos)
              bats.push(pos)
              x = pos - interval_btw_bats
            end
            break
          end
        end
      
        if not close_to_bat
          bats.push(x)
        end
        x += interval_btw_bats
      end
      
      max_count = bats.length > max_count ? bats.length : max_count
      offset += 1
    end

    return max_count - known_bats.length
  end
end

def main(args)
  runner = TaskRunner.new()
  
  filename = args[0]
  f = File.open(filename)
  lines = f.readlines()
  
  lines.each do |line|
    if line.strip.length > 0
      puts runner.evaluate(line)
    end
  end
end

main(ARGV)

