
class Link
  attr_reader :left, :right, :consumed
  
  def initialize(link_str)
    left, right = link_str.split("-")
    @left = left
    @right = right
    
    @consumed = false
  end
  
  def consume!
    @consumed = true
  end
end

class Chain
  attr_reader :links
  
  def initialize(links)
    @links = links
  end
  
  def push_front(link)
    @links = [link] + @links
  end
  
  def evaluate(num_expected_links)
    if @links.length == 0
      return "BAD"
    end

    if @links[0].left != "BEGIN" or 
        @links[-1].right != "END" or 
        @links.length != num_expected_links
      return "BAD"
    end
    
    i = 1
    while i < @links.length
      prev = @links[i - 1]
      this = @links[i]
      
      if prev.right != this.left
        return "BAD"
      end
      
      i += 1
    end
    
    "GOOD"
  end
end

class TaskRunner
  def initialize()
    @links = []
  end
  
  def evaluate(line)
    link_strs = line.split(";")
    @links = link_strs.map {|str| Link.new(str)}
    
    start = find_links("BEGIN", @links)
    if start.length > 1
      return "BAD"
    end
    
    possible_chains = get_chains("BEGIN", @links)
    
    any_good = possible_chains.map {|chain| chain.evaluate(@links.length)}
    if not any_good.index("GOOD").nil?
      "GOOD"
    else
      "BAD"
    end
  end
  
  # Returns all the possible chains given the links that haven't been consumed yet.
  # Returns an array of arrays.
  def get_chains(start_value, links_to_pick_from)
    # Handle the base case here. If we're just given a list with one element, just return it.
    if links_to_pick_from.length == 1
      first = links_to_pick_from[0]
      
      if first.left == start_value
        return [Chain.new(links_to_pick_from.dup)]
      else
        # This will cause a BAD chain.
        return []
      end
    end
    
    possible_chains = []
    
    # Possible first links.
    first_links = find_links(start_value, links_to_pick_from)
    
    first_links.each do |first|
      links = remove_link(first, links_to_pick_from)
      
      # Get a list of Chain objects that start with the right-hand value of 'link'
      chains = get_chains(first.right, links)
      
      # Add the first element to all the subchains.
      chains.each do |chain|
        chain.push_front(first)
        possible_chains.push(chain)
      end
    end
    
    possible_chains
  end
  
  def remove_link(link_to_remove, links)
    links = links.dup
    if not links.include?(link_to_remove)
      return links
    end
    links.reject {|link| link == link_to_remove}
  end
  
  def find_links(key, links)
    links.select {|link| link.left == key}
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

