"""
Codility task: OddOccurrencesInArray
Score: 100%
"""

def solution(A):
    solution = 0
    for element in A:
        solution ^= element

    return solution
