

class TaskRunner
  def initialize()
  end
  
  def evaluate(line)
    if is_hsl(line)
      convert_hsl_to_rgb(line)
    elsif is_hsv(line)
      convert_hsv_to_rgb(line)
    elsif is_cmyk(line)
      convert_cmyk_to_rgb(line)
    elsif is_hex(line)
      convert_hex_to_rgb(line)
    end
  end
  
  def is_hsl(color)
    color[0..2] == "HSL"
  end
  
  def is_hsv(color)
    color[0..2] == "HSV"
  end
  
  def is_cmyk(color)
    color[0...1] == "("
  end
  
  def is_hex(color)
    color[0...1] == "#"
  end
  
  def convert_hsl_to_rgb(color)
    h, s, l = parse_hsl(color)
    s /= 100.0
    l /= 100.0
    
    c = (1.0 - (2.0*l - 1.0).abs) * s
    x = c * (1.0 - ((h / 60.0) % 2 - 1.0).abs)
    m = l - c / 2.0
    
    if 0 <= h and h < 60
      r, g, b = c, x, 0
    elsif 60 <= h and h < 120
      r, g, b = x, c, 0
    elsif 120 <= h and h < 180
      r, g, b, = 0, c, x
    elsif 180 <= h and h < 240
      r, g, b = 0, x, c
    elsif 240 <= h and h < 300
      r, g, b, = x, 0, c
    elsif 300 <= h and h < 360
      r, g, b = c, 0, x
    end
    
    format_rgb((255 * (r + m)).round, (255*(g + m)).round, (255*(b + m)).round)
  end
  
  def convert_hsv_to_rgb(color)
    h, s, v = parse_hsv(color)
    s /= 100.0
    v /= 100.0
    
    c = v * s
    x = c * (1.0 - ((h / 60.0) % 2 - 1.0).abs)
    m = v - c
    
    if 0 <= h and h < 60
      r, g, b = c, x, 0
    elsif 60 <= h and h < 120
      r, g, b = x, c, 0
    elsif 120 <= h and h < 180
      r, g, b, = 0, c, x
    elsif 180 <= h and h < 240
      r, g, b = 0, x, c
    elsif 240 <= h and h < 300
      r, g, b, = x, 0, c
    elsif 300 <= h and h < 360
      r, g, b = c, 0, x
    end

    format_rgb((255 * (r + m)).round, (255*(g + m)).round, (255*(b + m)).round)
  end
  
  def convert_cmyk_to_rgb(color)
    c, m, y, k = parse_cmyk(color)
    r = 255 * (1.0 - c) * (1.0 - k)
    g = 255 * (1.0 - m) * (1.0 - k)
    b = 255 * (1.0 - y) * (1.0 - k)
    format_rgb(r.round, g.round, b.round)
  end
  
  def convert_hex_to_rgb(color)
    r, g, b = parse_hex(color)
    format_rgb(r.hex, g.hex, b.hex)
  end
  
  def format_rgb(r, g, b)
    "RGB(#{r},#{g},#{b})"
  end
  
  def parse_hsl(color)
    in_parens = color[4...(color.length-1)]
    values = in_parens.split(",")
    values.map {|value| value.to_i}
  end
  
  def parse_hsv(color)
    in_parens = color[4...(color.length-1)]
    values = in_parens.split(",")
    values.map {|value| value.to_i}
  end
  
  def parse_cmyk(color)
    in_parens = color[1...(color.length-1)]
    values = in_parens.split(",")
    values.map {|value| value.to_f}
  end
  
  def parse_hex(color)
    without_hash = color[1..color.length]
    r = without_hash[0...2]
    g = without_hash[2...4]
    b = without_hash[4...6]
    [r, g, b]
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

