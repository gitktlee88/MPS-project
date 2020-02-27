# Writing a Python program that returns the sum of all numbers
# in a sequence that are prime numbers.

# We'll create two functions to do this,
# one that determines if a number is prime or not and
# another that adds the prime numbers from a given sequence of numbers.

# Create a directory called primes in a workspace of your choosing.

import pytest
from primes import is_prime, sum_of_primes


def test_prime_low_number():
    assert is_prime(1) == False


def test_prime_prime_number():
    assert is_prime(29)


def test_prime_composite_number():
    assert is_prime(15) == False


def test_sum_of_primes_empty_list():
    assert sum_of_primes([]) == 0


def test_sum_of_primes_mixed_list():
    assert sum_of_primes([11, 15, 17, 18, 20, 100]) == 28
