from typing import Literal
import numpy as np
from scipy.linalg import solve, solve_banded
from . import PPoly
from ._polyint import _isscalar

__all__ = ["base_alg", "alg2", "apply_alg2", "alg1"]

def prep_data(x, y, axis, dydx=None):
    x, y = map(np.asarray, (x, y))
    if np.issubdtype(x.dtype, np.complexfloating):
        raise ValueError("`x` must contain real values.")
    x = x.astype(float)
    if np.issubdtype(y.dtype, np.complexfloating):
        dtype = complex
    else:
        dtype = float
    if dydx is not None:
        dydx = np.asarray(dydx)
        if y.shape != dydx.shape:
            raise ValueError("The shapes of `y` and `dydx` must be identical.")
        if np.issubdtype(dydx.dtype, np.complexfloating):
            dtype = complex
        dydx = dydx.astype(dtype, copy=False)
    y = y.astype(dtype, copy=False)
    axis = axis % y.ndim
    if x.ndim != 1:
        raise ValueError("`x` must be 1-dimensional.")
    if x.shape[0] < 2:
        raise ValueError("`x` must contain at least 2 elements.")
    if x.shape[0] != y.shape[axis]:
        raise ValueError(f"The length of `y` along `axis`={axis} doesn't "
                         "match the length of `x`")
    if not np.all(np.isfinite(x)):
        raise ValueError("`x` must contain only finite values.")
    if not np.all(np.isfinite(y)):
        raise ValueError("`y` must contain only finite values.")
    if dydx is not None and not np.all(np.isfinite(dydx)):
        raise ValueError("`dydx` must contain only finite values.")
    dx = np.diff(x)
    if np.any(dx <= 0):
        raise ValueError("`x` must be strictly increasing sequence.")
    y = np.moveaxis(y, axis, 0)
    if dydx is not None:
        dydx = np.moveaxis(dydx, axis, 0)
    return x, dx, y, axis, dydx

class base_alg(PPoly):
    def __init__(self, x, y, dydx, axis=0, extrapolate=None):
        if extrapolate is None:
            extrapolate = True
        x, dx, y, axis, dydx = prep_data(x, y, axis, dydx)
        dxr = dx.reshape([dx.shape[0]] + [1] * (y.ndim - 1))
        slope = np.diff(y, axis=0) / dxr
        t = (dydx[:-1] + dydx[1:] - 2 * slope) / dxr
        c = np.empty((4, len(x) - 1) + y.shape[1:], dtype=t.dtype)
        c[0] = t / dxr
        c[1] = (slope - dydx[:-1]) / dxr - t
        c[2] = dydx[:-1]
        c[3] = y[:-1]
        super().__init__(c, x, extrapolate=extrapolate)
        self.axis = axis

class alg2(base_alg):
    def __init__(self, x, y, axis=0, extrapolate=None):
        x, _, y, axis, _ = prep_data(x, y, axis)
        if np.iscomplexobj(y):
            msg = ("`alg2` only works with real values for `y`. "
                   "If you are trying to use the real components of the passed array, "
                   "use `np.real` on the array before passing to `alg2`.")
            raise ValueError(msg)
        xp = x.reshape((x.shape[0],) + (1,)*(y.ndim-1))
        dk = self._find_derivatives(xp, y)
        super().__init__(x, y, dk, axis=0, extrapolate=extrapolate)
        self.axis = axis

    @staticmethod
    def _edge_case(h0, h1, m0, m1):
        d = ((2*h0 + h1)*m0 - h0*m1) / (h0 + h1)
        mask = np.sign(d) != np.sign(m0)
        mask2 = (np.sign(m0) != np.sign(m1)) & (np.abs(d) > 3.*np.abs(m0))
        mmm = (~mask) & mask2
        d[mask] = 0.
        d[mmm] = 3.*m0[mmm]
        return d

    @staticmethod
    def _find_derivatives(x, y):
        y_shape = y.shape
        if y.ndim == 1:
            x = x[:, None]
            y = y[:, None]
        hk = x[1:] - x[:-1]
        mk = (y[1:] - y[:-1]) / hk
        if y.shape[0] == 2:
            dk = np.zeros_like(y)
            dk[0] = mk
            dk[1] = mk
            return dk.reshape(y_shape)
        smk = np.sign(mk)
        condition = (smk[1:] != smk[:-1]) | (mk[1:] == 0) | (mk[:-1] == 0)
        w1 = 2*hk[1:] + hk[:-1]
        w2 = hk[1:] + 2*hk[:-1]
        with np.errstate(divide='ignore', invalid='ignore'):
            whmean = (w1/mk[:-1] + w2/mk[1:]) / (w1 + w2)
        dk = np.zeros_like(y)
        dk[1:-1][condition] = 0.0
        dk[1:-1][~condition] = 1.0 / whmean[~condition]
        dk[0] = alg2._edge_case(hk[0], hk[1], mk[0], mk[1])
        dk[-1] = alg2._edge_case(hk[-1], hk[-2], mk[-1], mk[-2])
        return dk.reshape(y_shape)

def apply_alg2(xi, yi, x, der=0, axis=0):
    P = alg2(xi, yi, axis=axis)
    if der == 0:
        return P(x)
    elif _isscalar(der):
        return P.derivative(der)(x)
    else:
        return [P.derivative(nu)(x) for nu in der]

class alg1(base_alg):
    def __init__(self, x, y, axis=0, bc_type='not-a-knot', extrapolate=None):
        x, dx, y, axis, _ = prep_data(x, y, axis)
        n = len(x)
        bc, y = self._validate_bc(bc_type, y, y.shape[1:], axis)
        if extrapolate is None:
            if bc[0] == 'periodic':
                extrapolate = 'periodic'
            else:
                extrapolate = True
        if y.size == 0:
            s = np.zeros_like(y)
        else:
            dxr = dx.reshape([dx.shape[0]] + [1] * (y.ndim - 1))
            slope = np.diff(y, axis=0) / dxr
            if n == 2:
                if bc[0] in ['not-a-knot', 'periodic']:
                    bc[0] = (1, slope[0])
                if bc[1] in ['not-a-knot', 'periodic']:
                    bc[1] = (1, slope[0])
            if n == 3 and bc[0] == 'not-a-knot' and bc[1] == 'not-a-knot':
                A = np.zeros((3, 3))
                b = np.empty((3,) + y.shape[1:], dtype=y.dtype)
                A[0, 0] = 1
                A[0, 1] = 1
                A[1, 0] = dx[1]
                A[1, 1] = 2 * (dx[0] + dx[1])
                A[1, 2] = dx[0]
                A[2, 1] = 1
                A[2, 2] = 1
                b[0] = 2 * slope[0]
                b[1] = 3 * (dxr[0] * slope[1] + dxr[1] * slope[0])
                b[2] = 2 * slope[1]
                m = b.shape[0]
                s = solve(A, b.reshape(m, -1), overwrite_a=True, overwrite_b=True,
                          check_finite=False).reshape(b.shape)
            elif n == 3 and bc[0] == 'periodic':
                t = (slope / dxr).sum(0) / (1. / dxr).sum(0)
                s = np.broadcast_to(t, (n,) + y.shape[1:])
            else:
                A = np.zeros((3, n))
                b = np.empty((n,) + y.shape[1:], dtype=y.dtype)
                A[1, 1:-1] = 2 * (dx[:-1] + dx[1:])
                A[0, 2:] = dx[:-1]
                A[-1, :-2] = dx[1:]
                b[1:-1] = 3 * (dxr[1:] * slope[:-1] + dxr[:-1] * slope[1:])
                bc_start, bc_end = bc
                if bc_start == 'periodic':
                    A = A[:, 0:-1]
                    A[1, 0] = 2 * (dx[-1] + dx[0])
                    A[0, 1] = dx[-1]
                    b = b[:-1]
                    a_m1_0 = dx[-2]
                    a_m1_m2 = dx[-1]
                    a_m1_m1 = 2 * (dx[-1] + dx[-2])
                    a_m2_m1 = dx[-3]
                    a_0_m1 = dx[0]
                    b[0] = 3 * (dxr[0] * slope[-1] + dxr[-1] * slope[0])
                    b[-1] = 3 * (dxr[-1] * slope[-2] + dxr[-2] * slope[-1])
                    Ac = A[:, :-1]
                    b1 = b[:-1]
                    b2 = np.zeros_like(b1)
                    b2[0] = -a_0_m1
                    b2[-1] = -a_m2_m1
                    m = b1.shape[0]
                    s1 = solve_banded((1, 1), Ac, b1.reshape(m, -1), overwrite_ab=False,
                                      overwrite_b=False, check_finite=False)
                    s1 = s1.reshape(b1.shape)
                    m = b2.shape[0]
                    s2 = solve_banded((1, 1), Ac, b2.reshape(m, -1), overwrite_ab=False,
                                      overwrite_b=False, check_finite=False)
                    s2 = s2.reshape(b2.shape)
                    s_m1 = ((b[-1] - a_m1_0 * s1[0] - a_m1_m2 * s1[-1]) /
                            (a_m1_m1 + a_m1_0 * s2[0] + a_m1_m2 * s2[-1]))
                    s = np.empty((n,) + y.shape[1:], dtype=y.dtype)
                    s[:-2] = s1 + s_m1 * s2
                    s[-2] = s_m1
                    s[-1] = s[0]
                else:
                    if bc_start == 'not-a-knot':
                        A[1, 0] = dx[1]
                        A[0, 1] = x[2] - x[0]
                        d = x[2] - x[0]
                        b[0] = ((dxr[0] + 2*d) * dxr[1] * slope[0] +
                                dxr[0]**2 * slope[1]) / d
                    elif bc_start[0] == 1:
                        A[1, 0] = 1
                        A[0, 1] = 0
                        b[0] = bc_start[1]
                    elif bc_start[0] == 2:
                        A[1, 0] = 2 * dx[0]
                        A[0, 1] = dx[0]
                        b[0] = -0.5 * bc_start[1] * dx[0]**2 + 3 * (y[1] - y[0])
                    if bc_end == 'not-a-knot':
                        A[1, -1] = dx[-2]
                        A[-1, -2] = x[-1] - x[-3]
                        d = x[-1] - x[-3]
                        b[-1] = ((dxr[-1]**2*slope[-2] +
                                 (2*d + dxr[-1])*dxr[-2]*slope[-1]) / d)
                    elif bc_end[0] == 1:
                        A[1, -1] = 1
                        A[-1, -2] = 0
                        b[-1] = bc_end[1]
                    elif bc_end[0] == 2:
                        A[1, -1] = 2 * dx[-1]
                        A[-1, -2] = dx[-1]
                        b[-1] = 0.5 * bc_end[1] * dx[-1]**2 + 3 * (y[-1] - y[-2])
                    m = b.shape[0]
                    s = solve_banded((1, 1), A, b.reshape(m, -1), overwrite_ab=True,
                                     overwrite_b=True, check_finite=False)
                    s = s.reshape(b.shape)
        super().__init__(x, y, s, axis=0, extrapolate=extrapolate)
        self.axis = axis

    @staticmethod
    def _validate_bc(bc_type, y, expected_deriv_shape, axis):
        if isinstance(bc_type, str):
            if bc_type == 'periodic':
                if not np.allclose(y[0], y[-1], rtol=1e-15, atol=1e-15):
                    raise ValueError(
                        f"The first and last `y` point along axis {axis} must "
                        "be identical (within machine precision) when "
                        "bc_type='periodic'.")
            bc_type = (bc_type, bc_type)
        else:
            if len(bc_type) != 2:
                raise ValueError("`bc_type` must contain 2 elements to "
                                 "specify start and end conditions.")
            if 'periodic' in bc_type:
                raise ValueError("'periodic' `bc_type` is defined for both "
                                 "curve ends and cannot be used with other "
                                 "boundary conditions.")
        validated_bc = []
        for bc in bc_type:
            if isinstance(bc, str):
                if bc == 'clamped':
                    validated_bc.append((1, np.zeros(expected_deriv_shape)))
                elif bc == 'natural':
                    validated_bc.append((2, np.zeros(expected_deriv_shape)))
                elif bc in ['not-a-knot', 'periodic']:
                    validated_bc.append(bc)
                else:
                    raise ValueError(f"bc_type={bc} is not allowed.")
            else:
                try:
                    deriv_order, deriv_value = bc
                except Exception as e:
                    raise ValueError(
                        "A specified derivative value must be "
                        "given in the form (order, value)."
                    ) from e
                if deriv_order not in [1, 2]:
                    raise ValueError("The specified derivative order must "
                                     "be 1 or 2.")
                deriv_value = np.asarray(deriv_value)
                if deriv_value.shape != expected_deriv_shape:
                    raise ValueError(
                        f"`deriv_value` shape {deriv_value.shape} is not "
                        f"the expected one {expected_deriv_shape}."
                    )
                if np.issubdtype(deriv_value.dtype, np.complexfloating):
                    y = y.astype(complex, copy=False)
                validated_bc.append((deriv_order, deriv_value))
        return validated_bc, y
