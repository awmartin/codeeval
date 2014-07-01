
class Point
  attr_reader :x, :y
  
  def initialize(x, y)
    @x = x.to_i
    @y = y.to_i
  end
  
  def slope_to(other)
    if @x == other.x
      return nil
    end
    
    (other.y - @y).to_f / (other.x - @x)
  end
  
  def dist_to(other)
    dy = other.y - @y
    dx = other.x - @x
    
    Math.sqrt(dy*dy + dx*dx)
  end
  
  def equals(other)
    @x == other.x and @y == other.y
  end
end

class TaskRunner
  def initialize()
    @links = []
  end
  
  def evaluate(line)
    line.gsub!(" ", "")
    line.gsub!("(", "")
    line.gsub!(")", "")
    
    coords = line.split(",")
    
    # If there are duplicate points, this can't be a square.
    pts = pts_from_coords coords
    if duplicates(pts)
      return "false"
    end
    
    if method3(coords) #or method2(coords) or method1(coords)
      "true"
    else
      "false"
    end
  end
  
  def pts_from_coords coords
    pts = []
    i = 0
    while i < coords.length
      x = coords[i]
      y = coords[i + 1]
      pts.push(Point.new(x, y))
      i += 2
    end
    pts
  end

  def duplicates pts
    i = 0
    while i < pts.length - 1
      j = i + 1
      while j < pts.length
        pt1 = pts[i]
        pt2 = pts[j]
        
        if pt1.equals(pt2)
          return true
        end
        
        j += 1
      end
      i += 1
    end
    
    false
  end
  
  def sanitize_floats values
    values.map {|val| val.round(5)}
  end
  
  def find_other(value, list)
    i = 0
    while i < list.length
      if value != list[i]
        return list[i]
      end
      i += 1
    end
    nil
  end
  
  def method3 coords
    # Parse to Points
    pts = pts_from_coords coords
    
    # From any given point to all the others, we are grabbing 2 sides and 1 diagonal.
    # Use this fact to find the lengths of sides and diagonals.
    lengths = pts.slice(1, pts.length).map {|pt| pts[0].dist_to(pt)}
    lengths = sanitize_floats(lengths)
    
    first_count = lengths.count(lengths[0])
    second_count = lengths.count(lengths[1])
    third_count = lengths.count(lengths[2])
    
    # Of these 3 distances, we can tell which are side and diagonal lengths.
    if first_count == 2
      side_length = lengths[0]
      diagonal_length= find_other(side_length, lengths)
    elsif second_count == 2
      side_length = lengths[1]
      diagonal_length= find_other(side_length, lengths)
    elsif third_count == 2
      side_length = lengths[2]
      diagonal_length= find_other(side_length, lengths)
    else
      return false
    end
    
    # Of all the 6 lengths, count how many sides and diagonals there are.
    lengths = []
    i = 0
    while i < pts.length - 1
      j = i + 1
      while j < pts.length
        pt1 = pts[i]
        pt2 = pts[j]
        
        lengths.push(pt1.dist_to(pt2))
        j += 1
      end
      i += 1
    end
    
    lengths.each do |len|
      if len == 0.0
        return false
      end
    end
    
    lengths = sanitize_floats(lengths)
    
    # puts "#{lengths.join(',')} #{diagonal_length} #{side_length}"
    
    if lengths.count(diagonal_length) == 2 and lengths.count(side_length) == 4
      true
    else
      false
    end
  end
  
  def method2 coords
    xs = []
    i = 0
    while i < coords.length
      xs.push(coords[i])
      i += 2
    end
    
    ys = []
    i = 1
    while i < coords.length
      ys.push(coords[i])
      i += 2
    end
    
    if check_for_dups(xs) and check_for_dups(ys)
      true
    else
      false
    end
  end
  
  def check_for_dups list
    first = list[0]
    list = list.slice(1, list.length)
    has_first_again = list.index(first)
    if has_first_again.nil?
      return false
    end
    
    list = list.reject {|el| el == first}
    if list[0] != list[1]
      false
    else
      true
    end
  end
  
  def method1 coords
    pts = pts_from_coords coords
    
    slopes = []
    i = 0
    while i < pts.length - 1
      j = i + 1
      while j < pts.length
        pt1 = pts[i]
        pt2 = pts[j]
        slopes.push(pt1.slope_to(pt2))
        slopes = slopes.map {|val| val.nil? ? nil : val.abs}
        j += 1
      end
      i += 1
    end
    
    nil_count = slopes.count(nil)
    one_count = slopes.count(1)
    zero_count = slopes.count(0)
    
    if nil_count == 2 and one_count == 2 and zero_count == 2
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

