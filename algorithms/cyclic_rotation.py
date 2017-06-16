"""
Codility task: CyclicRotation
Score: 100%
"""

def solution(A, K):
    A_size = len(A)
    if A_size == 0:
        return A
    
    K = K % A_size
    return A[-K:] + A[:-K]
