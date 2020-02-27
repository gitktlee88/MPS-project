# A prime number is a whole number greater than 1 whose only factors are 1 and itself.
# A factor is a whole number that can be divided evenly into another number.
import math


def is_prime(num):
    # Prime numbers must be greater than 1
    if num < 2:
        return False
    # The floor() method rounds a number DOWNWARDS to the nearest integer, and returns the result.
    # The sqrt() method returns the square root of a number.
    for n in range(2, math.floor(math.sqrt(num) + 1)):
        # print(n)
        if num % n == 0:
            return False
    return True


def sum_of_primes(nums):
    # sum_of_prime_nums = 0
    # for i in nums:
    #     if is_prime(i):
    #         sum_of_prime_nums += i
    # return sum_of_prime_nums
    return sum([x for x in nums if is_prime(x)])
