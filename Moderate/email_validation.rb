
class TaskRunner
  def initialize()
    @links = []
  end
  
  def evaluate(line)
    email_regex = /^([a-zA-Z0-9\.\-\+]*?|\"[a-zA-Z0-9\.\-\+\@]*?\")[@]{1}[a-zA-Z0-9\.\-]*?\.[a-zA-Z]{2,3}/
    email_regex.match(line).nil? ? 'false' : 'true'
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

