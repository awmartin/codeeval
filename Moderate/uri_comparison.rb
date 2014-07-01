require 'uri'

class TaskRunner
  def initialize()
    @links = []
  end
  
  def evaluate(line)
    uri1, uri2 = line.split(";")

    decode(uri1) == decode(uri2) ? "True" : "False"
  end
  
  def decode url
    url = URI.unescape(url).gsub(":80", "")
    colon = url.index(":")  # first colon, after http
    domain_name = colon + 3
    
    last = url.length
    i = domain_name
    while i < url.length
      char = url[i]
      if char == "/"
        last = i
        break
      end
      i += 1
    end

    url = url.slice(0, last).downcase + url.slice(last, url.length)
    url
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

