

class Point
  attr_reader :x, :y
  def initialize(x, y)
    @x = x.to_f
    @y = y.to_f
  end
  
  def slope_to(other)
    (other.y - @y).to_f / (other.x - @x)
  end
  
  def dist_to(other)
    dx = other.x - @x
    dy = other.y - @y
    
    Math.sqrt(dx*dx + dy*dy)
  end
  
  def to_s
    "Point(#{@x}, #{@y})"
  end
  
  def equals(other)
    other.x == @x and other.y == @y
  end
end

class Segment
  def initialize(pt1, pt2)
    @start = pt1
    @stop = pt2
  end
  
  def line_through(other_start, other_stop)
    intersection_segment(other_start, other_stop, @start, @stop)
  end
  
  # Computes line-line intersection.
  def intersection(pt1, pt2, pt3, pt4)
    denominator = ((pt1.x - pt2.x) * (pt3.y - pt4.y) - 
         (pt1.y - pt2.y) * (pt3.x - pt4.x))
    
    if denominator == 0
      # Parellel lines
      return nil
    end
    
    x = ((pt1.x * pt2.y - pt1.y * pt2.x) * (pt3.x - pt4.x) - 
         (pt1.x - pt2.x) * (pt3.x * pt4.y - pt3.y * pt4.x)) /
        denominator
    
    y = ((pt1.x * pt2.y - pt1.y * pt2.x) * (pt3.y - pt4.y) -
         (pt1.y - pt2.y) * (pt3.x * pt4.y - pt3.y * pt4.x)) /
        denominator
    
    Point.new(x, y)
  end
  
  # The segment is pt3 - pt4. The line intersection must be between pt3 and pt4.
  def intersection_segment(pt1, pt2, pt3, pt4)
    pt = intersection(pt1, pt2, pt3, pt4)
    
    segment_length = pt3.dist_to(pt4)
    
    dist3 = pt.dist_to(pt3)
    dist4 = pt.dist_to(pt4)
    
    if dist3 + dist4 == segment_length
      pt
    else
      nil
    end
    
    # slope = pt4.slope_to(pt3)
    # 
    # y1 = pt.x * slope + pt3.y
    # y2 = pt.x * slope + pt4.y
    # 
    # y1 == pt.y or y2 == pt.y
  end
  
  def to_s
    "Segment(#{@start}, #{@stop})"
  end
end

class Block
  def initialize(street1, street2, avenue1, avenue2)
    @left = street1
    @right = street2
    @bottom = avenue1
    @top = avenue2
    
    @bottom_left = Point.new(@left, @bottom)
    @top_right = Point.new(@right, @top)
    @bottom_right = Point.new(@right, @bottom)
    @top_left = Point.new(@left, @top)
  end
  
  def to_s
    "Block(l=#{@left}, r=#{@right}, t=#{@top}, b=#{@bottom})"
  end
  
  def contains(x, y)
    @left <= x and x <= @right and @bottom <= y and y <= @top
  end
  
  def line_through(pt1, pt2)
    segments = [
      Segment.new(@bottom_left, @top_left),
      Segment.new(@top_left, @top_right),
      Segment.new(@top_right, @bottom_right),
      Segment.new(@bottom_right, @bottom_left)
    ]
    
    pts = []
    segments.each do |segment|
      pt = segment.line_through(pt1, pt2)
      if not pt.nil?
        pts.push pt
      end
    end
    
    tr = false
    if pts.length == 2
      # Check to see if we just went through a corner.
      puts "#{pts[0]} #{pts[1]}"
      if pts[0].equals(pts[1])
        tr = false
      else
        tr = true
      end
    elsif [1,3,4].include?(pts.length)
      tr = true
    else
      tr = false
    end
    
    tr
  end

end

class TaskRunner
  def initialize()

  end
  
  def parse_line_to_blocks line
    streets, avenues = line.split(" ")
    streets = streets.gsub("(", "").gsub(")", "").strip
    avenues = avenues.gsub("(", "").gsub(")", "").strip
    
    streets = streets.split(",").map {|str| str.to_i}  # x
    avenues = avenues.split(",").map {|str| str.to_i}  # y

    blocks = []
    i = 0
    while i < streets.length - 1
      j = 0
      while j < avenues.length - 1
        block = Block.new(
          streets[i], streets[i+1],
          avenues[j], avenues[j+1]
          )
        blocks.push(block)
        j += 1
      end
      i += 1
    end
    
    start = Point.new(streets[0], avenues[0])
    stop = Point.new(streets[-1], avenues[-1])
    
    [blocks, start, stop]
  end
  
  def evaluate(line)
    blocks, start, stop = parse_line_to_blocks line

    method1(blocks, start, stop)
  end
  
  def test
    # blocks = []
    # blocks.push(Block.new(0, 2, 0, 2))
    # blocks.push(Block.new(0, 2, 2, 4))
    # blocks.push(Block.new(2, 4, 2, 4))
    # blocks.push(Block.new(2, 4, 0, 2))
    #
    # start = Point.new(0, 0)
    # stop = Point.new(4, 4)
    #
    # puts method1(blocks, start, stop)
    #
    # # ----------------------------------
    #
    # blocks = []
    # blocks.push(Block.new(0, 2, 0, 2))
    # blocks.push(Block.new(0, 2, 2, 4))
    # blocks.push(Block.new(2, 4, 2, 4))
    # blocks.push(Block.new(2, 4, 0, 2))
    # blocks.push(Block.new(0, 2, 4, 6))
    #
    # start = Point.new(0, 0)
    # stop = Point.new(6, 4)
    #
    # puts method1(blocks, start, stop)

    # ----------------------------------
    
    blocks = []
    blocks.push(Block.new(1, 2, 0, 1))
    
    start = Point.new(0, 0)
    stop = Point.new(4, 5)
    
    puts method1(blocks, start, stop)
  end
  

  def method1 blocks, start, stop
    count = 0
    blocks.each do |block|
      if block.line_through(start, stop)
        count += 1
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
    runner.test()
    # lines.each do |line|
    #   if line.strip.length > 0
    #     test_case, expected = line.strip.split(" ")
    #     answer = runner.evaluate(test_case)
    #     passes = expected == answer
    #     if passes
    #       puts "true"
    #     else
    #       puts "FAILED: #{test_case} expected #{expected} but got #{answer}"
    #     end
    #   end
    # end
  else
    lines.each do |line|
      if line.strip.length > 0
        puts runner.evaluate(line.strip)
      end
    end
  end
end

main(ARGV)

