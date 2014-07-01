
import sys

class PokerHands(object):

    def evaluate(self, lines):
        for line in lines:
            line = Util.sanitize_line(line)
            print self.compute(line)
        
    def run_tests(self, test_cases):
        for input, expected in test_cases:
            result = self.compute(input)
            if str(expected) == str(result):
                print "Test passed: %s" % input
            else:
                print "Test failed: Expected %s and got %s" % (expected, result)
        
    def compute(self, hands):
        cards = hands.split(" ")
        
        hand_left = Hand.parse(cards[:5])
        hand_right = Hand.parse(cards[5:])

        if hand_left.hand is None and \
                hand_right.hand is not None:
            return 'right'
        
        if hand_left.hand is not None and \
                hand_right.hand is None:
            return 'left'

        def compare(left, right):
            if left < right:
                return 'right'
            if left > right:
                return 'left'
            return 'none'
        
        def compare_high_card():
            # Distinguish by high card.
            i = 0
            left_cards = sorted(hand_left.cards, key=lambda card:card.value)
            right_cards = sorted(hand_right.cards, key=lambda card:card.value)
            while i < 5:
                left_card = left_cards[i]
                right_card = right_cards[i]
                comparison = compare(left_card, right_card)
                if comparison is not 'none':
                    return comparison
                i += 1
            return 'none'
        
        
        if hand_left.hand is None and \
                hand_right.hand is None:
            return compare_high_card()
        
        if hand_left.hand.value == hand_right.hand.value:
            # Distinguish by the value of the cards held in the hand.
            cards_left = hand_left.hand.cards
            cards_right = hand_right.hand.cards
            
            if len(cards_left) == 1:
                comparison = compare(cards_left[0], cards_right[0])
                if comparison is not 'none':
                    return comparison
                return compare_high_card()
            
            if len(cards_left) == 2:
                first = compare(cards_left[0], cards_right[0])
                if first is not 'none':
                    return first
                second = compare(cards_left[1], cards_right[1])
                if second is not 'none':
                    return second
                return compare_high_card()
        
        return compare(hand_left.hand.value, hand_right.hand.value)
        
card_values = {
    '2':2,
    '3':3,
    '4':4,
    '5':5,
    '6':6,
    '7':7,
    '8':8,
    '9':9,
    'T':10,
    'J':11,
    'Q':12,
    'K':13,
    'A':14
    }
card_names = {
    2:'2',
    3:'3',
    4:'4',
    5:'5',
    6:'6',
    7:'7',
    8:'8',
    9:'9',
    10:'Ten',
    11:'Jack',
    12:'Queen',
    13:'King',
    14:'Ace'
    }
suits = {
    'S':'Spades',
    'C':'Clubs',
    'D':'Diamonds',
    'H':"Hearts"
    }

class OnePair(object):
    value = 1
    
    def __init__(self, *cards):
        self.cards = cards
    
    def __str__(self):
        return "OnePair(%s)" % str([str(c) for c in self.cards])
    
    @classmethod
    def check(cls, cards):
        i = 0
        num_duplicates = 0
        pair = None
        
        while i < len(cards) - 1:
            card = cards[i]
            others = cards[i+1:]
            
            other_values = [c.value for c in others]
            num_in_others = other_values.count(card.value)
            
            if num_in_others > 1:
                # This was more than one pair... Three-of-a-kind?
                return None
            if num_in_others == 1:
                num_duplicates += 1
                other_index = other_values.index(card.value)
                other_card = others[other_index]
                pair = [card, other_card]
            if num_duplicates > 1:
                # Was more than one pair, perhaps two pair?
                return None
            
            i += 1
        
        if pair is not None:
            return cls(pair[0])
        else:
            return None

class TwoPair(object):
    value = 2
    
    def __init__(self, *cards):
        self.cards = cards
    
    def __str__(self):
        return "TwoPair(%s)" % str([str(c) for c in self.cards])
    
    @classmethod
    def check(cls, cards):
        i = 0
        num_pairs = 0
        first_pair = None
        second_pair = None
        
        while i < len(cards) - 1:
            card = cards[i]
            others = cards[i+1:]
            
            other_values = [c.value for c in others]
            num_in_others = other_values.count(card.value)
            
            if num_in_others > 1:
                # This was more than one pair... Three-of-a-kind?
                return None
            
            if num_in_others == 1:
                other_index = other_values.index(card.value)
                other_card = others[other_index]

                if num_pairs == 0:
                    first_pair = (card, other_card)
                if num_pairs == 1:
                    second_pair = (card, other_card)
                num_pairs += 1
                
            i += 1
        
        if first_pair is not None and \
                second_pair is not None:
            return cls(first_pair[0], second_pair[0])
        else:
            return None

class ThreeOfAKind(object):
    value = 3
    
    def __init__(self, *cards):
        self.cards = cards
    
    def __str__(self):
        return "ThreeOfAKind(%s)" % str([str(c) for c in self.cards])
    
    @classmethod
    def check(cls, cards):
        i = 0
        triplet = None
        
        while i < len(cards) - 2:
            card = cards[i]
            others = cards[i+1:]
            
            other_values = [c.value for c in others]
            num_in_others = other_values.count(card.value)
            
            if num_in_others > 2:
                # This was more than one pair... Four-of-a-kind?
                return None
            
            if num_in_others == 2:
                second_offset = i + 1
                second_card_index = other_values.index(card.value) + second_offset
                second_card = cards[second_card_index]
                
                third_card_index = cards[second_card_index+1:].index(card.value) + second_card_index+1
                third_card = cards[third_card_index]
                
                indices = [0,1,2,3,4]
                indices.remove(i)
                indices.remove(second_card_index)
                indices.remove(third_card_index)
                
                unused_card_1 = cards[indices[0]]
                unused_card_2 = cards[indices[1]]
                if unused_card_1 == unused_card_2:
                    # Full house.
                    return None
                triplet = (card, second_card, third_card)
                break
                
            i += 1
        
        if triplet is not None:
            return cls(triplet[0])
        else:
            return None


class Straight(object):
    value = 4
    def __init__(self, *cards):
        self.cards = cards
    
    def __str__(self):
        return "Straight(high=%s)" % str(self.cards[0])
    
    @classmethod
    def check(cls, cards, check_flush=True):
        cards = sorted(cards, key=lambda a: a.value)
        
        i = 0
        while i < len(cards) - 1:
            left_card = cards[i]
            right_card = cards[i + 1]
            if left_card.value != right_card.value - 1:
                return None
            i += 1
        
        if check_flush:
            flush = Flush.check(cards, check_straight=False)
            if flush is not None:
                # Straight flush.
                return None
        
        return cls(cards[-1])
            

class Flush(object):
    value = 5
    def __init__(self, *cards):
        self.cards = cards
    
    def __str__(self):
        return "Flush(%s)" % self.cards[0].suit
    
    @classmethod
    def check(cls, cards, check_straight=True):
        suit = cards[0].suit
        i = 1
        while i < len(cards):
            card = cards[i]
            if card.suit != suit:
                return None
            i += 1
        
        if check_straight:
            straight = Straight.check(cards)
            if straight is not None:
                # Straight flush.
                return None
        
        return cls(cards[0])
        
class FullHouse(object):
    value = 6
    
    def __init__(self, *cards):
        self.cards = cards
    
    def __str__(self):
        return "FullHouse(3x=%s, 2x=%s)" % self.cards
    
    @classmethod
    def check(cls, cards):
        i = 0

        two_set = None
        three_set = None
        
        while i < len(cards) - 1:
            card = cards[i]
            others = cards[i+1:]
            
            other_values = [c.value for c in others]
            num_in_others = other_values.count(card.value)
            
            if num_in_others == 1:
                other_index = other_values.index(card.value)
                other_card = others[other_index]
                
                if three_set is not None:
                    if card in three_set or other_card in three_set:
                        # If cards are J,J,J,Q,Q, we can register a three set for Jacks and 
                        # potentially a two set of Jacks by mistake on the next iteration.
                        i += 1
                        continue
                
                two_set = (card, other_card)

                if two_set is not None and \
                        three_set is not None:
                    return cls(three_set[0], two_set[0])
            
            if num_in_others == 2:
                second_offset = i + 1
                second_card_index = other_values.index(card.value) + second_offset
                second_card = cards[second_card_index]
                
                third_card_index = cards[second_card_index+1:].index(card.value) + second_card_index+1
                third_card = cards[third_card_index]
                
                three_set = (card, second_card, third_card)

                if two_set is not None and \
                        three_set is not None:
                    return cls(three_set[0], two_set[0])
                
            i += 1

        return None

class FourOfAKind(object):
    value = 7
    
    def __init__(self, *cards):
        self.cards = cards
        
    def __str__(self):
        return "FourOfAKind(%s)" % (self.cards[0])
    
    @classmethod
    def check(cls, cards):
        card = cards[0]
        second_card = cards[1]
        
        values = [c.value for c in cards]
        if values.count(card.value) == 4:
            return cls(card)
        if values.count(second_card.value) == 4:
            return cls(second_card)
        
        return None

class StraightFlush(object):
    value = 8
    
    def __init__(self, *cards):
        self.cards = cards
        
    def __str__(self):
        return "StraightFlush(%s)" % (self.cards[0])
    
    @classmethod
    def check(cls, cards):
        cards = sorted(cards)
        
        straight = Straight.check(cards, check_flush=False)
        if straight is None:
            return None
        flush = Flush.check(cards, check_straight=False)
        if flush is None:
            return None
        if cards[-1].value == 14:
            # Royal flush
            return None
        return cls(cards[-1])

class RoyalFlush(object):
    value = 9
    
    def __init__(self, *cards):
        self.cards = cards
        
    def __str__(self):
        return "StraightFlush(%s)" % (self.cards[0])
    
    @classmethod
    def check(cls, cards):
        cards = sorted(cards)
        
        straight = Straight.check(cards, check_flush=False)
        if straight is None:
            return None
        flush = Flush.check(cards, check_straight=False)
        if flush is None:
            return None
        if cards[-1].value != 14:
            # Top card not an ace
            return None
        return cls(cards[-1])

hand_types = [
    RoyalFlush,
    StraightFlush,
    FourOfAKind,
    FullHouse,
    Flush,
    Straight,
    ThreeOfAKind,
    TwoPair,
    OnePair,
    ]

class Hand(object):
    def __init__(self, cards):
        self.cards = cards

        self.hand = None
        self.high_card = None
        
        self.get_high_card()
        self.get_hand_type()
    
    def get_high_card(self):
        self.high_card = max(self.cards)
    
    def get_hand_type(self):
        for hand_type in hand_types:
            hand = hand_type.check(self.cards)
            if hand is not None:
                self.hand = hand
                break
        
    @classmethod
    def parse(cls, card_strings):
        cards = []
        for card_string in card_strings:
            cards.append(Card.parse(card_string))
        return cls(cards)


class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def __str__(self):
        name = card_names[self.value]
        return "%s of %s" % (name, self.suit)
    
    @classmethod
    def parse(cls, card_string):
        value_str = card_string[0]
        suit_str = card_string[1]
        return cls(card_values[value_str], suits[suit_str])
    
    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        return self.value == other.value
    def __ne__(self, other):
        if isinstance(other, int):
            return self.value != other
        return self.value != other.value
    def __lt__(self, other):
        if isinstance(other, int):
            return self.value < other
        return self.value < other.value
    def __gt__(self, other):
        if isinstance(other, int):
            return self.value > other
        return self.value > other.value
    def __le__(self, other):
        if isinstance(other, int):
            return self.value <= other
        return self.value <= other.value
    def __ge__(self, other):
        if isinstance(other, int):
            return self.value >= other
        return self.value >= other.value



class Util(object):
    """Utility functions for formatting and parsing."""

    @classmethod
    def sanitize_line(cls, line):
        # Remove the trailing newline.
        if line[-1] == "\n":
            line = line[:-1]
        return line

def open_input_file(filename):
    lines = None
    with open(filename) as f:
        lines = f.readlines()
    assert lines is not None and isinstance(lines, list), "File wasn't read properly."
    return lines

def parse_args():
    args = sys.argv
    assert len(args) in (2, 3), "Provide a filename or filename plus the --test flag."

    filename = args[1]

    test_flag = False
    if len(args) == 3:
        if args[2] in ('--test', '-t'):
            test_flag = True
        else:
            assert False, "First argument should be a filename and the second either --test or -t."

    return filename, test_flag

def main():
    filename, test_flag = parse_args()
    lines = open_input_file(filename)
    
    #test_flag = True
    if test_flag:
        test_file = """6D 7H AH 7S QC 6H 2D TD JD AS
JH 5D 7H TC JS JD JC TS 5S 7S
2H 8C AD TH 6H QD KD 9H 6S 6C
JS JH 4H 2C 9H QH KC 9D 4D 3S
TC 7H KH 4H JC 7D 9S 3H QS 7S
TC 7H KH 4H JC 3D 3H 2C 2H 2D
TC 7H KH 4H JC 6D 3H 3C 3D 2D"""

        test_answers = """left
none
right
left
right
right"""

        test_cases = zip(test_file.split("\n"), test_answers.split("\n"))
        
        PokerHands().run_tests(test_cases)
    else:
        PokerHands().evaluate(lines)
        
if __name__ == "__main__":
    main()