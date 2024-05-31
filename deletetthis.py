import numpy as np


def solve_riccati(A, B, Q, R, tol=1e-9, max_iter=1000):
    """
    Solve the continuous-time algebraic Riccati equation (CARE) using an iterative approach.

    A^T P + P A - P B R^{-1} B^T P + Q = 0

    Parameters:
    A : numpy.ndarray
        The state matrix.
    B : numpy.ndarray
        The input matrix.
    Q : numpy.ndarray
        The state weighting matrix.
    R : numpy.ndarray
        The input weighting matrix.
    tol : float
        The tolerance for convergence.
    max_iter : int
        The maximum number of iterations.

    Returns:
    P : numpy.ndarray
        The solution matrix.
    """
    # Initialize P with the solution to the Lyapunov equation (A^T P + P A + Q = 0)
    P = np.copy(Q)
    
    # Inverse of R
    R_inv = np.linalg.inv(R)

    for i in range(max_iter):
        P_next = Q + A.T @ P + P @ A - P @ B @ R_inv @ B.T @ P
        if np.linalg.norm(P_next - P, ord='fro') < tol:
            P = P_next
            break
        P = P_next
    
    return P

# Example usage
A = np.array([[0, 1], [-2, -3]])
B = np.array([[0], [1]])
Q = np.array([[1, 0], [0, 1]])
R = np.array([[1]])

P = solve_riccati(A, B, Q, R)
print("Solution P:")
print(P)