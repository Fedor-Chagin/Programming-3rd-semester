import timeit
import matplotlib.pyplot as plt
from factorial import *

nums = list(range(1, 101, 10))

funcs = [
    ("fact_recursive", fact_recursive),
    ("fact_iterative", fact_iterative), 
    ("fact_recursive_memo", fact_recursive_memo),
    ("fact_iterative_memo", fact_iterative_memo)
]


results = {}
for name, func in funcs:
    times = []
    for n in nums:
        t = timeit.timeit(lambda: func(n), number=100) / 100
        times.append(t)
    results[name] = times

plt.figure(figsize=(10,6))
for name, times in results.items():
    plt.plot(nums, times, marker='o', label=name)

plt.xlabel('n')
plt.ylabel('Время (сек)')
plt.legend()
plt.grid(True)
plt.savefig('benchmark.png')
plt.show()

print("Чистый бенчмарк (n=50, один вызов):")
for name, func in funcs:
    start = timeit.default_timer()
    func(50)
    end = timeit.default_timer()
    print(f"{name}: {end-start:.6f} сек")