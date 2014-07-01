
(function Solution(){
  
  // A dumb algorithm to determine whether n is prime.
  function is_prime(n) {
    if (n < 2) {
      return false;
    }
    if (n == 2) {
      return true;
    }
    if (n % 2 === 0) {
      return false;
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
    var num_primes = 0;
    var i = 2;
    var sum = 0;
    
    while (num_primes < 1000) {
      if (is_prime(i)) {
        sum += i;
        num_primes ++;
      }
      i += 1;
    }

    console.log(sum);
  }
  
  main();
})();