import numpy as np
from numpy.lib.function_base import quantile


def compute_distances(data, query, dist):
    """ Compute distances.
    Computes the distances between the vectors (rows) of a dataset and a
    single query). Three distances are supported:
    * Manhattan distance ("L1");
    * squared Euclidean distance ("L2");
    * Chebyshev distance ("inf").
    """
    distances = np.zeros((len(data),), dtype=np.float32)
    if dist == "L1":
        distances = np.sum(np.abs(data - query), axis=1)
    elif dist == "L2":
        distances = np.sqrt(np.sum((data - query) ** 2, axis=1))
    elif dist == "inf":
        distances = np.max(np.abs(data - query), axis=1)
    elif dist == "inter":
        distances = np.sum(np.minimum(data, query), axis=1)
    elif dist == "chi2":
        distances = np.sum((data - query) ** 2 / (data + query), axis=1)
    return distances


def knn_search(data, query, k=1, dist="L2"):
    """Brute force version of knn"""
    distances = compute_distances(data, query, dist)
    if k == 1:
        min_idx = np.argmin(distances)
        return [min_idx], [distances[min_idx]]
    else:
        min_idx = np.argpartition(distances, k)[:k]
        return min_idx, distances[min_idx]


def radius_search(data, query, r=1.0, norm="L2"):
    """ Brute-force radius search"""

    distances = compute_distances(data, query, norm)
    indices = np.where(distances <= r)[0]

    return indices, distances[indices]
