import numpy as np
from scipy.linalg import qr

def compress_image(image_matrix, k):
    """
    Performs Pivoted QR decomposition (Rank-Revealing QR) on the image matrix 
    and reconstructs it using the top k components.
    
    Args:
        image_matrix (numpy.ndarray): The 2D array representing the grayscale image.
        k (int): The number of components to keep.
        
    Returns:
        reconstructed_image (numpy.ndarray): The compressed version of the image.
        original_size (int): Number of elements in original matrix.
        compressed_size (int): Number of elements stored in Q_k, R_k and P.
    """
    # Pivoted QR Decomposition
    # A[:, P] = Q @ R
    Q, R, P = qr(image_matrix, pivoting=True)
    
    # Truncate Q and R to keep only k columns/rows
    Q_k = Q[:, :k]
    R_k = R[:k, :]
    
    # Reconstruct the permuted image B = Q_k @ R_k
    B_approx = np.dot(Q_k, R_k)
    
    # Reverse the permutation to get the original image approximation
    # If B = A[:, P], then A[:, P[j]] = B[:, j] is not quite right.
    # Python slicing: B = A[:, P]. 
    # To inverse: create empty A_approx, then A_approx[:, P] = B
    
    reconstructed_image = np.zeros_like(image_matrix, dtype=float)
    reconstructed_image[:, P] = B_approx
    
    # Calculate sizes for metrics
    h, w = image_matrix.shape
    original_size = h * w
    # Sizes: Q_k is h*k, R_k is k*w, P is w (integers)
    compressed_size = (h * k) + (k * w) + w 
    
    return reconstructed_image, original_size, compressed_size
