.. _linalg:

Linear Algebra
==============

.. module: best.linalg
    :synopsis: Some linear algebra routines.

The linear algebra module (:mod:`best.linalg`)
defines several functions that cannot be found in numpy or
scipy but are extremely useful in various Bayesian problems.


.. _linalg-kron:

Manipulating Kronecker Products
-------------------------------

Being able to avoid forming the Kronecker products in linear algebra
can save lots of memory and time. Here are a few functions that we have
put together. They should be slef-explanatory.

.. function:: best.linalg.kron_prod(A, x)

    Multiply a Kronecker product of matrices with a vector.

    The function computes the product:
        .. math::
            \mathbf{y} = (\otimes_{i=1}^s \mathbf{A}_i) \mathbf{x},

    where :math:`\mathbf{A}_i` are suitable matrices.
    The characteristic of the routine is that it does not form the
    Kronecker product explicitly. Also, :math:`\mathbf{x}` can be a
    matrix of appropriate dimensions. Of course, it will throw an
    exception if you don't have the dimensions right.

    :param A: Represents the Kronecker product of matrices.
    :type A: a matrix or a collection -list or tuple- of 2D numpy arrays.
    :param x: The vector you want to multiply the matrix with.
    :type x: numpy 1D or 2D array.
    :return: The product.
    :rtype: A 2D numpy array. If x was 1D, then it represents a columnt\
            matrix (i.e., a vector).

    Here is an example:

    >>> import numpy as np
    >>> import best.linalg
    >>> A1 = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
    >>> A2 = A1
    >>> A = (A1, A2)
    >>> x = np.random.randn(A1.shape[1] * A2.shape[1])
    >>> y = best.linalg.kron_prod(A, x)

    You should compare the result with:

    >>> ...
    >>> z = np.dot(np.kron(A1, A2), x)

    The last ones forms the Kronecker product explicitly and uses much more
    memory.


.. function:: best.linalg.kron_solve(A, y)

    Solve a linear system involving Kronecker products.

    The function solves the following linear system:
        .. math::
            (\otimes_{i=1}^s\mathbf{A}_i)\mathbf{x} = \mathbf{y},

    where :math:`\mathbf{A}_i` are suitable matrices and
    :math:`\mathbf{y}` is a vector or a matrix.

    :param A: Represents a Kronecker product of matrices.
    :type A: a matrix or a collection -list or tuple- of 2D numpy arrays.
    :param y: The right hand side of the equation.
    :type y: a 1D or 2D numpy array
    :returns: The solution of the linear system.
    :rtype: A numpy array of the same type as y.

    Here is an example:

    >>> import numpy as np
    >>> import best.linalg
    >>> A1 = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
    >>> A2 = A1
    >>> A = (A1, A2)
    >>> y = np.random.randn(A1.shape[1] * A2.shape[1])
    >>> x = best.linalg.kron_solve(A, y)

    Compare this with:

    >>> z = np.linalg.solve(np.kron(A1, A2), y)

    which actually builds the Kronecker product.


.. function:: best.linalg.update_cholesky(L, B, C)

    Updates the Cholesky decomposition of a matrix.

    We assume that :math:`\mathbf{L}` is the lower Cholesky decomposition
    of an :math:`n\times n` matrix :math:`\mathbf{A}`, and we want to
    calculate the Cholesky decomposition of the :math:`(n+m)\times (n+m)`
    matrix:

    .. math::
        \mathbf{A}' = \left(\begin{array}{cc}\mathbf{A}& \mathbf{B}\\
        \mathbf{B}^T & \mathbf{C} \end{array}\right)

    It can be easily shown that the Cholesky decomposition of
    :math:`\mathbf{A}'` is given by:

    .. math::
        \mathbf{L}' = \left(\begin{array}{cc}\mathbf{L}& \mathbf{0}\\
        \mathbf{D}_{21} & \mathbf{D}_{22}\end{array}\right)

    where

    .. math::
        \mathbf{B} = \mathbf{L} \mathbf{D}_{21}^T

    and

    .. math::
        \mathbf{D}_{22} \mathbf{D}_{22} = \mathbf{C}
        - \mathbf{D}_{21}\mathbf{D}_{21}^T.

    :param L: The Cholesky decomposition of the original matrix.
    :type L: 2D numpy array
    :param B: The :math:`n\times m` upper right part of the new matrix.
    :type B: 2D numpy array
    :param C: The :math:`m\times m` bottom diagonal part of the new matrix.
    :type C: 2D numpy array
    :returns: The lower Cholesky decomposition of the new matrix.
    :rtype: 2D numpy array

    Here is an example:

    >>> import numpy as np
    >>> import best.linalg
    >>> A = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
    >>> A_new = np.array([[2, -1, 0, 0], [-1, 2, -1, 0], [0, -1, 2, -1],\
    ...                   [0, 0, -1, 2]])
    >>> L = np.linalg.cholesky(A)
    >>> B = A_new[:3, 3:]
    >>> C = A_new[3:, 3:]
    >>> L_new = best.linalg.update_cholesky(L, B, C)

    to be compared with:

    >>> L_new = np.linalg.cholesky(A_new)


.. function:: best.linalg.update_cholesky_linear_system(x, L_new, z)

    Update the solution of Cholesky-solved linear system.

    Assume that originally we had an :math:`n\times n` lower triangular
    matrix :math:`\mathbf{L}` and that we have already solved the linear
    system:

    .. math::
        \mathbf{L} \mathbf{x} = \mathbf{y},

    Now, we wish to solve the linear system:

    .. math::
        \mathbf{L}'\mathbf{x}' = \mathbf{y}',

    where :math:`\mathbf{L}` is again lower triangular matrix whose
    top :math:`n \times n` component is identical to :math:`\mathbf{L}`
    and :math:`\mathbf{y}'` is :math:`(\mathbf{y}, \mathbf{z})`. The
    solution is:

    .. math::
        \mathbf{x}' = (\mathbf{x}, \mathbf{x}_u),

    where :math:`\mathbf{x}_u` is the solution of the triangular system:

    .. math::
        \mathbf{L}_{22}' * \mathbf{x}_u = \mathbf{z} - \mathbf{L}_{21}' \mathbf{x},

    where :math:`\mathbf{L}_{22}'` is the lower :math:`m\times m`
    component of :math:`\mathbf{L}'` and :math:`\mathbf{L}_{21}'` is the
    :math:`m\times n` bottom left component of :math:`\mathbf{L}'`.

    :param x: The solution of the first Cholesky system.
    :type x: 1D or 2D numpy array
    :param L_new: The new Cholesky factor (see :func:`best.linalg.update_cholesky`)
    :type L_new: 2D numpy array
    :param z: The new part of :math:`\mathbf{y}`.
    :type z: numpy array of the same type as x
    :returns: The solution of the linear system.
    :rtype: numpy array of the same type as x

    Here is an example:

    >>> A = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
    >>> A_new = np.array([[2, -1, 0, 0], [-1, 2, -1, 0], [0, -1, 2, -1],
    ...                  [0, 0, -1, 2]])
    >>> L = np.linalg.cholesky(A)
    >>> B = A_new[:3, 3:]
    >>> C = A_new[3:, 3:]
    >>> L_new = best.linalg.update_cholesky(L, B, C)
    >>> L_new_real = np.linalg.cholesky(A_new)
    >>> y = np.random.randn(3)
    >>> x = np.linalg.solve(L, y)
    >>> z = np.random.randn(1)
    >>> x_new = best.linalg.update_cholesky_linear_system(x, L_new, z)

    and compare it with:

    >>> x_new_real = np.linalg.solve(L_new_real, np.hstack([y, z]))


.. _linalg-gsvd:

Generalized Singular Value Decomposition
----------------------------------------

Let :math:`A\in\mathbb{R}^{m\times n}` and :math:`B\in\mathbb{R}^{p\times n}`.
The `Generalized Singular Value Decomposition \
<http://en.wikipedia.org/wiki/Generalized_singular_value_decomposition>`_
of :math:`[A B]` is such that

    .. math::

            U^T A Q = D_1 [0 R],\;\;V' B Q = D_2 [0 R],

where :math:`U, V` and :math:`Q` are orthogonal matrices and
:math:`Z^T` is the transpose of :math:`Z`.
Let :math:`k + l` be the effective numerical rank of the matrix
:math:`\left[A^T B^T\right]^T`, then :math:`R` is a
:math:`(k + l)\times(k + l)` non-singular upper triangular matrix,
:math:`D_1` and :math:`D_2` are :math:`m\times(k+l)`
and :math:`p\times(k+l)` "diagonal" matrices.
The particular structures of :math:`D_1` and :math:`D_2` depend
on the sign of :math:`m - k - l`. Consult the theory for more details.
This decomposition is extremely useful in computing the statistics
required for :class:`best.rvm.RelevantVectorMachine`.
Here is a class that interfaces LAPACK's
`dggsvd <http://www.netlib.no/netlib/lapack/double/dggsvd.f>`_:

.. class:: best.linalg.GeneralizedSVD

    :inherits: :class:`best.Object`

    A class that represents the generalized svd decomposition of A and B.

    .. method:: __init__(A, B[, do_U=True[, do_V=True[, do_Q=True]]])

        Initialize the object and perform the decomposition.

        A copy of ``A`` and ``B`` will be made.

        :param A: A :math:`m\times n` matrix.
        :type A: 2D numpy array
        :param B: A :math:`p\times n` matrix.
        :type B: 2D numpy array
        :param do_U: Compute ``U`` if ``True``.
        :type do_U: bool
        :param do_V: Compute ``U`` if ``True``.
        :type do_V: bool
        :param do_Q: Compute ``U`` if ``True``.
        :type do_Q: bool

        .. warning::
            Do not use the functionality that skips the computation
            of ``U, V`` or ``Q``. It does not work at the moment.

    .. attribute:: A

        Get the final form of the copy of ``A``.

    .. attribute:: B

        Get the final form of the copy of ``B``.

    .. attribute:: alpha

        Get the vector of singular values of ``A``.

    .. attribute:: beta

        Get the vector of singular values of ``B``.

    .. attribute:: U

        Get the orthogonal matrix :math:`U`.

    .. attribute:: V

        Get the orthogonal matrix :math:`V`.

    .. attribute:: Q

        Get the orthogonal matrix :math:`Q`.

    .. attribute:: m

        Get the number of rows of :math:`A`.

    .. attribute:: n

        Get the number of columns of :math:`A`.

    .. attribute:: p

        Get the number of rows of :math:`B`.

    .. attribute:: k

        Get :math:`k`.

    .. attribute:: l

        Get :math:`l`.

    .. attribute:: R

        Get the non-singular, upper triangular matrix :math:`R`.

    .. attribute:: C

        Get the diagonal :math:`C` matrix. See doc of ``dggsvd``.

    .. attribute:: S

        Get the diagonal :math:`S` matrix. See doc of ``ggsvd``.

    .. attribute:: D1

        Get the "diagonal" :math:`D_1` matrix.

    .. attribute:: D2

        Get the "diagonal" :math:`D_2` matrix.


.. _linalg-ic:

Incomplete Cholesky Decomposition
---------------------------------

Let :math:`A\in\mathbb{R}^{n\times n}` be a positive semi-definite
matrix. The class :class:`best.linalg.IncompleteCholesky` computes
the Cholesky factorization with complete pivoting of :math:`A`.

The factorization has the form:

    .. math::
        P^T A P = U^T U,
        :label: ic-upper

or

    .. math::
        P^T A P = L L^T,
        :label: ic-lower

where :math:`U\in\mathbb{R}^{k\times n}` is an upper triangular matrix,
:math:`L\in\mathbb{R}^{n\times k}` is a lower triangular matrix,
:math:`P\in\mathbb{R}^{n\times n}` is a permutation matrix and
:math:`k` is the (numerical) rank of matrix :math:`A`.

.. class:: best.linalg.IncompleteCholesky

    :inherits: :class:`best.Object`

    An interface to the LAPACK Fortran routine
    `?pstrf <http://www.netlib.org/lapack/explore-html/dd/dad/dpstrf_8f.html>`_
    which performs
    an Cholesky factorization with complete
    pivoting of a real symmetric positive semidefinite matrix A.

    .. method:: __init__(A[, lower=True[, tol=-1.[, \
                         name='Incomplete Cholesky']]])

        Initialize the object.

        :param A: The matrix whose decomposition you seek. It will
                be copied internally.
        :type A: 2D numpy array
        :param lower: If ``True``, then compute the lower incomplete
                      Cholesky. Otherwise compute the upper
                      incomplete Cholesky.
        :type lower: ``bool``
        :param tol: The desired tolerance (``float``). If a negative
                    tolerance is specified, then
                    :math:`n U \max\{A_{kk}\}` will be used.
        :type tol: ``float``
        :param name: A name for the object.
        :type name: `str`

    .. attribute:: A

        Get the matrix ``A``.

    .. attribute:: L

        Get the lower Cholesky factor (Returns ``None`` if not computed).

    .. attribute:: U

        Get the upper Cholesky factor (Returns ``None`` if not computed).

    .. attribute:: rank

        Get the numerical rank of ``A``.

    .. attribute:: piv

        Get a vector representing the permutation matrix ``P``.

    .. attribute:: P

        Get the permutation matrix ``P``.


Here is an example of how the class can be used::

    import numpy as np
    from best.maps import CovarianceFunctionSE
    from best.linalg import IncompleteCholesky
    x = np.linspace(-5, 5, 10)
    f = CovarianceFunctionSE(1)
    A = f(x, x, hyp=10.)
    #np.linalg.cholesky # This will fail to compute the normal
                        # Cholesky decomposition.
    ic = IncompleteCholesky(A)
    print 'rank: ', ic.rank
    print 'piv: ', ic.piv
    LL = np.dot(ic.L, ic.L.T)
    print np.linalg.norm((LL - np.dot(ic.P.T, np.dot(A, ic.P))))

This should produce the following text::

    rank:  9
    piv:  [0 9 4 7 2 8 1 5 6 3]
    3.33066907388e-16