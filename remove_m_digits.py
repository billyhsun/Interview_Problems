# Find length of n, and get all digits of n
def remove_m_digits(n: 'int', m: 'int') -> 'int':
    digits = []
    n = str(n)
    for digit in n:
        digits.append(int(digit))
    if len(digits) > 10000 or int(n) < 0:
        return -1   # Error

    # res = find_min_orig(digits, m)
    res = find_min_greedy(digits, m)
    return res


# Convert list of digits to number
def list_to_num(digits: 'list') -> 'int':
    n = 0
    k = 1
    for i in reversed(digits):
        n += i * k
        k *= 10
    return n


# Original solution, time complexity: O(m*n)
def find_min_orig(digits: 'list', m: 'int') -> 'int':
    if m >= len(digits) or len(digits) == 0:
        return 0
    elif m == 0:
        return list_to_num(digits)
    else:
        # Go through all possible remaining numbers by removing one digit
        nums = {}
        for i in range(len(digits)):
            temp = digits[:i] + digits[(i+1):]
            nums[i] = list_to_num(temp)
        min_ind = min(nums, key=nums.get)
        digits = digits[:min_ind] + digits[min_ind+1:]

        return find_min_orig(digits, m-1)


# Greedy solution using a stack, time complexity: O(n)
def find_min_greedy(digits: 'list', m: 'int') -> 'int':
    stack = []
    counter = 0
    for digit in digits:
        while len(stack) > 0 and stack[-1] > digit and counter < m:
            stack.pop()
            counter += 1
        stack.append(digit)

    while counter < m:
        stack.pop()
        counter += 1

    res = list_to_num(stack)
    return res


if __name__ == "__main__":
    m = 3
    num = 3423423
    print(remove_m_digits(num, m))
