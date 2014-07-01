
(function Solution(){
  function is_palindrome(number) {
    var word = number.toString();
    if (word.length === 1) {
      return true;
    }
    if (word.length === 2 && word[0] === word[1]) {
      return true;
    }
    
    if (word[0] == word[word.length-1]) {
      return is_palindrome(word.substr(1, word.length-2));
    } else {
      return false;
    }
  }
  
  // A dumb algorithm to determine whether n is prime.
  function is_prime(n) {
    if (n < 2) {
      return false;
    }
    if (n % 2 === 0) {
      return true;
    }
    
    var i = 3;
    while (i * i <= n) {
      if (n % i === 0) {
        return false;
      }
      i += 2;
    }
    
    return true;
  }
  
  function main() {
    var i;
    
    for (i = 999; i >= 0; i --) {
      if (is_prime(i) && is_palindrome(i)) {
        console.log(i);
        break;
      }
    }
    
  }
  
  main()
})();