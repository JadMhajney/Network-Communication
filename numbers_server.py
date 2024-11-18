import socket
import select
import sys



def calculate(x,y,z):
    INT32_MIN = -2_147_483_648
    INT32_MAX = 2_147_483_647
    x = int(x)
    y = int(y)
    match z:
        case "+":
            res = (x+y)
        case "-":
            res = (x-y)
        case "*":
            res = (x*y)
        case "/":
            res = round(x / y, 2)
        case "^":
            res = (x^y)

    if res < INT32_MIN or res > INT32_MAX:
        return "Result exceeds signed 32-bit integer range"
    
def find_max(numbers):
    #the num is array of str
    for i in range (len(numbers)):
        numbers[i] = int(numbers[i])
    return max(numbers)
    
def find_max(numbers):
    #the num is array of str
    for i in range (len(numbers)):
        numbers[i] = int(numbers[i])
    return max(numbers)

def find_prime_factors(n):
    #returns array 
    factors = []    
    # Divide by 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2    
    # Check odd divisors
    divisor = 3
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 2
    # If n > 2, it's a prime factor
    if n > 2:
        factors.append(n)
    return factors


