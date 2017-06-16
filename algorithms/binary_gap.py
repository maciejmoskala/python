"""
Codility task: BinaryGap
Score: 100%
"""

def solution(N):
    count = 0
    solution = 0
    binary_string = str(bin(N)).strip('0b')

    for binary_byte in binary_string:
        if binary_byte == '0':
            count += 1
        else:
            solution = count if count > solution else solution
            count = 0

    return solution
