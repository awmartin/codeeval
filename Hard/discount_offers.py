import sys
import re
import math

vowels = ['a', 'e', 'i', 'o', 'u', 'y']

num_letters = len

def num_vowels(string):
    count = 0
    for letter in string.lower():
        if letter in vowels:
            count += 1
    return count

def num_consonants(string):
    # All strings are preprocessed to exclude non-letters.
    return num_letters(string) - num_vowels(string)

def factors(n):
    if n <= 0:
        return set()
    factors = set(reduce(list.__add__, 
        [[i, n/i] for i in range(1, int(math.sqrt(n)) + 1) if n % i == 0]
        ))
    factors.remove(1)
    return factors
# Test
assert 1 not in factors(10), "1 was found in the factors list"
assert 2 in factors(10)
assert 5 in factors(10)


def share_factors(x, y):
    common_factors = factors(x).intersection(factors(y))
    return len(common_factors) > 0
# Test
assert share_factors(10, 12), "10 and 12 didn't share factors, but should have."
assert not share_factors(14, 15), "14 and 15 shared factors, but shouldn't have."

def is_even(n):
    return n % 2 == 0
assert is_even(4), "4 wasn't detected as even."


def calculate_ss(customer_info, product_info):
    # 0 = num_letters, 1 = num_vowels, 2 = num_consonants
    score = None
    if is_even(product_info[0]):
        score = customer_info[1] * 1.5
    else:
        score = customer_info[2]
    
    if share_factors(customer_info[0], product_info[0]):
        score *= 1.5
    
    return score


def get_customers_and_products(line):
    """Returns a tuple of a list of customers and products as strings."""
    customers, products = line.split(";")
    return (customers.split(","), products.split(","))
assert get_customers_and_products("a,b,c;d,e,f") == (['a','b','c'], ['d','e','f'])


def build_customer_product_matrix(customers, products):
    """Produces a matrix of customer vs product containing the SS."""
    
    size = max(len(customers), len(products))
    
    customer_lut = []
    for customer in customers:
        customer_lut.append((
            num_letters(customer),
            num_vowels(customer),
            num_consonants(customer),
            ))
    
    product_lut = []
    for product in products:
        product_lut.append((num_letters(product),))
    
    matrix = []
    for i in range(0, size):
        matrix.append([0 for j in range(0, size)])
    
    for c, customer in enumerate(customers):
        for p, product in enumerate(products):
            matrix[c][p] = calculate_ss(customer_lut[c], product_lut[p])
    
    return matrix


def is_assignable(matrix):
    """Determine whether an assignment is possible with the given matrix."""
    return get_assignment(matrix) is not None

def has_duplicates(permutation):
    return len(set(permutation)) != len(permutation)

def get_permutations(assignments):
    """Given a list of lists, return the possible permutations."""
    
    if len(assignments) == 1:
        return [[x] for x in assignments[0]]
    
    permutations = []
    for index in assignments[0]:
        perms = get_permutations(assignments[1:])
        for remainder in perms:
            perm = [index]
            perm.extend(remainder)
            permutations.append(perm)
    
    return permutations
assert get_permutations([[1,2],[3]]) == [[1,3], [2,3]]

def get_assignment(matrix):
    size = len(matrix)
    assignments = [None for i in range(size)]
    
    for r, row in enumerate(matrix):
        found = []
        for c, el in enumerate(row):
            if el == 0:
                found.append(c)
        if len(found) > 0:
            assignments[r] = found
        else:
            assert False, "Should be at least one zero"
    print assignments
    
    permutations = get_permutations(assignments)
    for permutation in permutations:
        if not has_duplicates(permutation):
            return permutation
    
    return None

def subtract_elements_from_max(matrix):
    m = 0
    for row in matrix:
        m = max(max(row), m)
    size = len(matrix)
    for r in range(size):
        for c in range(size):
            matrix[r][c] = m - matrix[r][c]

def subtract_min_from_each_row(matrix):
    for i,row in enumerate(matrix):
        m = min(row)
        for j,val in enumerate(row):
            matrix[i][j] = val - m
    
def subtract_min_from_each_column(matrix):
    size = len(matrix)
    for c in range(size):
        m = 10000000
        for r in range(size):
            val = matrix[r][c]
            m = min(m, val)
        for r in range(size):
            matrix[r][c] -= m

def score_assignment(matrix, assignment):
    s = 0
    for c, p in enumerate(assignment):
        s += matrix[c][p]
    return s

def get_total_score_for_line(line):
    customers, products = get_customers_and_products(line)
    matrix = build_customer_product_matrix(customers, products)
    
    subtract_elements_from_max(matrix)
    
    # Subtract min 
    subtract_min_from_each_row(matrix)
    if is_assignable(matrix):
        assignment = get_assignment(matrix)
        return score_assignment(matrix, assignment)
    
    subtract_min_from_each_column(matrix)
    if is_assignable(matrix):
        assignment = get_assignment(matrix)
        return score_assignment(matrix, assignment)

    return 0
    

strip_regex = re.compile("[^a-z;,]")
def sanitize_line(line):
    return re.sub(strip_regex, "", line.lower())

def main():
    args = sys.argv
    # assert len(args) == 2, "Please specify one file as an argument."
    filename = args[1]
    
    lines = None
    with open(filename) as f:
        lines = f.readlines()
    # assert lines is not None and isinstance(lines, list), "File wasn't read properly."
    
    for line in lines:
        if len(line.strip()) == 0:
            continue
        stripped_line = sanitize_line(line)
        
        score = get_total_score_for_line(stripped_line)
        print "%.2f" % score
    
if __name__ == "__main__":
    main()

