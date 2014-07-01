
COIN_DESCRIPTIONS = [
  ['PENNY', 1],
  ['PENCE', 3],
  ['NICKEL', 5]
]


class Coin
  attr_reader :name, :value
  
  def initialize(name, value)
    @name = name
    @value = value
  end
end

class Collection
  def initialize
    @coins = []
  end
  
  def add_coin(coin)
    @coins.push(coin)
  end
  
  def sum
    amt = 0
    @coins.each do |coin|
      amt += coin.value
    end
    amt
  end
  
  def num_coins
    @coins.length
  end
end


class TaskRunner
  def initialize()
    @available_coins = COIN_DESCRIPTIONS.map {|desc| Coin.new(desc[0], desc[1])}
  end
  
  def evaluate(line)
    amt = line.to_i

    get_coins(amt).num_coins
  end

  def get_coins(amt)
    collection = Collection.new
    
    i = @available_coins.length - 1

    while i >= 0
      coin = @available_coins[i]
      
      if coin.value <= amt
        collection.add_coin(coin)
        amt -= coin.value
      else
        # Coin didn't help us. Advance to the next one.
        i -= 1
      end
      
      if amt == 0
        break
      end
    end
    
    collection
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

