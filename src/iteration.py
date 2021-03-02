import numpy as np
from numpy import ndarray, array
from typing import Tuple


def algorithm(siml: dict, krg: list, a: float) -> dict:
    """Power iteration algorithm to solve for stable max eigenvector and value.
    Method includes the setting up of the matrix/vector and then doing the
    iteration process.

    Args:
        siml (dict): Label similarity initial values.
        krg (list): List containing all of the KRG nodes with outgoing arcs.
        a (float): Parameter which defines what ratio of the end result should
            be influenced by similarity resonance.

    Returns:
        dict(Tuple[str, str] -> float): Final similarity values.
    """

    s, A = prepare_pow_iteration_params(krg, a, siml)
    new_siml = converge(s, A)

    final_siml = {}
    new_suml_max = new_siml.max()

    for index, node in enumerate(krg):
        final_siml[node.activity_set] = new_siml[index] / new_suml_max

    return final_siml


def converge(vector: array, mat: ndarray) -> array:
    """Power iteration method. Stops when change in eigenvalue is less than
    0.000000001.

    Args:
        vector (array): Power iteration vector.
        mat (ndarray): Power iteration matrix.

    Returns:
        array: Final stable power iteration vector.
    """
    stable_vector = vector
    ev = eigenvalue(mat, stable_vector)

    while True:
        stable_vector = mat.dot(stable_vector)
        stable_vector = manhattan_norm_ndarray(stable_vector)

        ev_new = eigenvalue(mat, stable_vector)
        if np.abs(ev - ev_new) < 0.000000001:
            break

        ev = ev_new

    return stable_vector


def prepare_pow_iteration_params(krg: list, a: float,
                                 sim_v: dict) -> Tuple[array, ndarray]:
    """Preparation of the vector and matrix for the power iteration problem.

    Args:
        krg (list): List containing all of the KRG nodes with outgoing arcs.
        a (float): Parameter which defines what ratio of the end result should
            be influenced by similarity resonance.
        sim_v (dict): Label similarity initial values.

    Returns:
        Tuple[array, ndarray]: vector and matrix to be used for
            power iteration.
    """

    matrix_shape = (len(krg), len(krg))
    matrix_a = np.zeros(matrix_shape)
    sim_vector = np.array([])
    sim_v = manhattan_norm_dict(sim_v)

    for i in range(matrix_shape[0]):
        sim_vector = np.append(sim_vector, sim_v[krg[i].activity_set])
        for j in range(matrix_shape[1]):
            if i == j and not krg[i].pre_set and not krg[i].post_set:
                matrix_a[i, j] = a + ((1.0 - a) * sim_vector[-1])
            elif krg[i].activity_set in krg[j].pre_set:
                matrix_a[i, j] = (a * krg[j].pre_set[krg[i].activity_set]) + \
                    ((1.0 - a) * sim_vector[-1])
            elif krg[i].activity_set in krg[j].post_set:
                matrix_a[i, j] = (a * krg[j].post_set[krg[i].activity_set]) + \
                    ((1.0 - a) * sim_vector[-1])
            else:
                matrix_a[i, j] = (1.0 - a) * sim_vector[-1]

    return sim_vector, matrix_a


def manhattan_norm_dict(input_dict: dict) -> dict:
    """Manhattan norm on values of a dictionary (used for sim vector).

    Args:
        input_dict (dict): Dictionary where the values are to be normalized.

    Returns:
        dict: Dictionary with normalized values.
    """
    denominator = sum(input_dict.values())
    return {k: v/denominator for k, v in input_dict.items()}


def manhattan_norm_ndarray(input_A: ndarray) -> ndarray:
    """Manhattan norm on an ndarray (used for matrix).

    Args:
        input_A (ndarray): ndarray to be normalized.

    Returns:
        ndarray: Normalized ndarray.
    """
    denominator = input_A.sum()
    return input_A/denominator


def eigenvalue(A: ndarray, v: array) -> float:
    """calculate the eigenvalue of the vector to the matrix.

    Args:
        A (ndarray): Input matrix.
        v (array): Input vector.

    Returns:
        float: Eigenvalue of vector to matrix.
    """
    Av = A.dot(v)
    return v.dot(Av)
