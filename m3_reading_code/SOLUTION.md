I got these answers by having the LLM analyze the original file. See how close your answers come to these answers. 

The original file can be found here: https://github.com/scipy/scipy/blob/v1.16.0/scipy/interpolate/_cubic.py#L569-L973


## Question 1: 
The file `original.py` implements several piecewise cubic spline interpolation algorithms. The two main, distinct algorithms referenced by the task are:

- __PCHIP (Piecewise Cubic Hermite Interpolating Polynomial)__: Implemented in the `PchipInterpolator` class. This method creates a C1-smooth (continuous first derivative) spline that preserves the shape of the data. It determines the derivative at each data point locally, using formulas designed to prevent overshoots and maintain the monotonicity of the original data. This makes it suitable for data that is not smooth.

- __Cubic Spline Interpolation__: Implemented in the `CubicSpline` class. This method creates a C2-smooth (continuous second derivative) spline. To achieve this higher level of smoothness, it constructs and solves a global system of linear equations to find the derivatives at each point simultaneously. This results in a smoother curve but may not preserve the local shape (e.g., monotonicity) of the data as strictly as PCHIP.

## Question 2: 
The `_edge_case` static method is responsible for calculating the derivatives at the two endpoints of the dataset.

The standard PCHIP algorithm calculates the derivative at a point by considering the slopes of the line segments on both its left and right sides. However, this is not possible for the very first point (which has no left segment) or the very last point (which has no right segment).

The `_edge_case` method handles this by using a __one-sided, three-point formula__ to estimate the derivative. It also contains logic to ensure the result remains "shape-preserving" by checking if the calculated derivative has the same sign as the slope of the end segment and capping its magnitude to avoid introducing artificial oscillations. It is necessary because without it, the derivatives at the boundaries would be undefined, and the spline could not be constructed.

## Question 3: 

The system of linear equations in the `CubicSpline` class represents the set of conditions required to enforce __C2 continuity__ across the interior data points.

For a cubic spline to be C2-smooth, the second derivative of the cubic polynomial on the left of an interior point must equal the second derivative of the cubic polynomial on the right of that point. When this condition is applied to all interior points, it generates a system of linear equations.

- __The unknowns__ in the system are the first derivatives at each data point.
- __The equations__ link the unknown derivatives at adjacent points (`s[i-1]`, `s[i]`, `s[i+1]`) based on the data (`x` and `y` values).

By solving this system (which is efficiently done because it is tridiagonal), the algorithm finds the unique set of derivative values that ensures the entire spline is twice continuously differentiable, resulting in a visually smooth curve.
