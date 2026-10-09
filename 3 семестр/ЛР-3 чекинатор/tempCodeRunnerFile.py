def factorial_dict(n: int, res = 1) -> dict:
    print(res)
    if n == 1:
        return {
            '1!': res
        }
    return factorial_dict(n - 1, res * n)

print(factorial_dict(3))