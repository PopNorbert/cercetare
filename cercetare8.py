import time
import random
import math
import matplotlib.pyplot as plt
import pandas as pd


def square_and_multiply(base, exponent, modulus):
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent % 2 == 1:  
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result


def precomputed_exponentiation(base, exponent, modulus, max_exponent):
    
    table = {}
    current = base % modulus
    for i in range(max_exponent + 1):
        table[2**i] = current
        current = (current * current) % modulus

    
    result = 1
    while exponent > 0:
        largest_power_of_2 = 2 ** (int(math.log2(exponent)))
        result = (result * table[largest_power_of_2]) % modulus
        exponent -= largest_power_of_2

    return result


def generate_large_prime(bits):
    while True:
        candidate = random.getrandbits(bits)
        if candidate % 2 != 0 and all(candidate % i != 0 for i in range(3, int(candidate**0.5) + 1, 2)):
            return candidate


bases = [2, 3, 7, 13, 17]
exponents = [2**16, 2**64, 2**512, 2**1024]  
modulus_sizes = [16,32]  


small_primes = {size: generate_large_prime(size) for size in modulus_sizes}

results = []

for base in bases:
    for exponent in exponents:
        for modulus_bits in modulus_sizes:
            modulus = small_primes[modulus_bits]

            
            start_time = time.perf_counter_ns()
            baseline_result = square_and_multiply(base, exponent, modulus)
            baseline_time = time.perf_counter_ns() - start_time

            
            max_exponent = int(math.log2(exponent))  
            start_time = time.perf_counter_ns()
            optimized_result = precomputed_exponentiation(base, exponent, modulus, max_exponent)
            optimized_time = time.perf_counter_ns() - start_time

            
            assert baseline_result == optimized_result, "Mismatch in results!"

            
            results.append({
                "Base": base,
                "Exponent": f"2^{int(math.log2(exponent))}",
                "Modulus Size (bits)": modulus_bits,
                "Baseline Time (ns)": baseline_time,
                "Optimized Time (ns)": optimized_time,
                "Speedup": baseline_time / optimized_time
            })


baseline_times = [result["Baseline Time (ns)"] for result in results]
optimized_times = [result["Optimized Time (ns)"] for result in results]
speedups = [result["Speedup"] for result in results]
modulus_sizes = [result["Modulus Size (bits)"] for result in results]


plt.figure(figsize=(12, 6))
plt.plot(modulus_sizes, baseline_times, label="Baseline Times", marker='o')
plt.plot(modulus_sizes, optimized_times, label="Optimized Times", marker='s')
plt.xlabel("Modulus Size (bits)")
plt.ylabel("Execution Time (ns)")
plt.title("Execution Time Comparison")
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(modulus_sizes, speedups, label="Speedup", marker='^', color='green')
plt.xlabel("Modulus Size (bits)")
plt.ylabel("Speedup Factor")
plt.title("Speedup of Optimized Method")
plt.legend()
plt.grid()
plt.show()

pd.set_option('display.max_rows', None)


pd.set_option('display.max_columns', None)


pd.set_option('display.max_colwidth', None)

df = pd.DataFrame(results)
print(df)
