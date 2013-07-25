"""Updates the solution of a linear system involving a Cholesky factor.

Author:
    Ilias Bilionis

Date:
    2/1/2013

"""

import scipy.linalg
import numpy as np


def update_cholesky_linear_system(x, L_new, z):
    """Updates the solution of a linear system involving a Cholesky factor.

    Assume that originally we had an n x n matrix lower triangular matrix L
    and that we have already solved the linear system:
        L * x = y.
    We wish now to solve the linear system:
        L_new * x_new = y_new,
    where L_new is again lower triangular but the fist n x n component is
    identical to L and y_new is (y, z). The solution is:
        x_new = (x, x_u),
    where x_u is the solution of the triangular system:
        D22 * x_u = z - D21 * x,
    where D22 is the lower m x m component of L_new and D21 is the m x n
    bottom left component of L_new.

    Arguments:
        x       ---     The original solution. It can be either a vector or a
                        matrix.
        L_new   ---     The new lower Cholesky factor.
        z       ---     The new right hand side as described above.
    """
    assert isinstance(x, np.ndarray)
    assert x.ndim <= 2
    regularized_x = False
    if x.ndim == 1:
        regularized_x = True
        x = x.reshape((x.shape[0], 1))
    assert isinstance(L_new, np.ndarray)
    assert L_new.shape[0] == L_new.shape[1]
    assert isinstance(z, np.ndarray)
    assert z.ndim <= 2
    regularized_z = False
    if z.ndim == 1:
        regularized_z = True
        z = z.reshape((z.shape[0], 1))
    assert x.shape[1] == z.shape[1]
    assert L_new.shape[0] == x.shape[0] + z.shape[0]
    n = x.shape[0]
    D22 = L_new[n:, n:]
    D21 = L_new[n:, :n]
    x_u = scipy.linalg.solve_triangular(D22, z - np.dot(D21, x), lower=True)
    y = np.vstack([x, x_u])
    if regularized_x or regularized_z:
        y = y.reshape((y.shape[0],))
    return y
