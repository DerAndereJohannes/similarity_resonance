import numpy as np
from numpy import ndarray, array
from typing import Tuple


def algorithm(siml: dict, krg: list, a: float) -> dict:

    s, A = prepare_pow_iteration_params(krg, a, siml)
    new_siml = converge(s, A)

    final_siml = {}
    new_suml_max = new_siml.max()

    for index, node in enumerate(krg):
        final_siml[node.activity_set] = new_siml[index] / new_suml_max

    return final_siml


def converge(vector: array, mat: ndarray) -> array:
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

    matrix_shape = (len(krg), len(krg))
    matrix_a = np.zeros(matrix_shape)
    sim_vector = np.array([])
    sim_v = manhattan_norm_dict(sim_v)

    for i in range(matrix_shape[0]):
        sim_vector = np.append(sim_vector, sim_v[krg[i].activity_set])
        for j in range(matrix_shape[1]):
            if i == j and not krg[i].pre_set:
                matrix_a[i, j] = a + ((1.0 - a) * sim_vector[-1])
            elif krg[i].activity_set in krg[j].post_set:
                matrix_a[i, j] = (a * krg[j].post_set[krg[i].activity_set]) + \
                    ((1.0 - a) * sim_vector[-1])
            else:
                matrix_a[i, j] = (1.0 - a) * sim_vector[-1]

    return sim_vector, matrix_a


def manhattan_norm_dict(input_dict: dict) -> dict:
    denominator = sum(input_dict.values())
    return {k: v/denominator for k, v in input_dict.items()}


def manhattan_norm_ndarray(input_A: ndarray) -> ndarray:
    denominator = input_A.sum()
    return input_A/denominator


def eigenvalue(A: ndarray, v: array) -> float:
    Av = A.dot(v)
    return v.dot(Av)
