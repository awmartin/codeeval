
class Hole
  def initialize(string)
    @width, @height = parse(string)
  end
  
  def parse(string)
    corner1, corner2 = string.split(" ")
    x1, y1 = parse_corner(corner1)
    x2, y2 = parse_corner(corner2)
    [(x2 - x1).abs, (y2 - y1).abs]
  end
  
  def parse_corner(corner)
    corner.slice(1, corner.length-2).split(",").map {|x| x.to_i}
  end
  
  def can_fit_brick(brick)
    can_fit(brick.width, brick.height) or 
    can_fit(brick.width, brick.depth) or
    can_fit(brick.height, brick.depth)
  end
  
  def can_fit(width, height)
    (width <= @width and height <= @height) or (height <= @width and width <= @height)
  end
end

class Brick
  attr_reader :id, :width, :height, :depth
  
  def initialize(string)
    @id, @width, @height, @depth = parse(string)
  end
  
  def parse(string)
    id, corner1, corner2 = string.slice(1, string.length-2).split(" ")
    x1, y1, z1 = parse_corner(corner1)
    x2, y2, z2 = parse_corner(corner2)
    [id, (x2 - x1).abs, (y2 - y1).abs, (z2 - z1).abs]
  end
  
  def parse_corner(corner)
    corner.slice(1, corner.length-2).split(",").map {|x| x.to_i}
  end
end


class TaskRunner
  def initialize()
  end
  
  def evaluate(line)
    hole_str, brick_str = line.split("|")
    brick_strs = brick_str.split(";")
    hole = Hole.new(hole_str)
    bricks = brick_strs.map {|str| Brick.new(str)}
    
    bricks_that_fit = []
    bricks.each do |brick|
      if hole.can_fit_brick(brick)
        bricks_that_fit.push(brick.id)
      end
    end
    
    if bricks_that_fit.length == 0
      "-"
    else
      bricks_that_fit.join(",")
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

