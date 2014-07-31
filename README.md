 # Markdown Math

A simple utility to convert Markdown flavored with LaTeX $$ into image equations.
Note that this overwrites the original file.
Only equations on their own line will work for now.

As an example, consider the following line in your `README.md` file:

``` latex
 $i\hbar\frac{\partial}{\partial t} \Psi(\mathbf{r},t) = \left [ \frac{-\hbar^2}{2m}\nabla^2 + V(\mathbf{r},t)\right ] \Psi(\mathbf{r},t)$
```

Running the command

``` bash
python mdmath.py README.md
```

would be rendered like this:

<p align="center" class="mdequation"><img src=".equations/49c77b1aa2b0da39771a9acdeffc3b9749f8c88e26bebd731173583d8b04beaa.png" alt="$i\hbar\frac{\partial}{\partial t} \Psi(\mathbf{r},t) = \left [ \frac{-\hbar^2}{2m}\nabla^2 + V(\mathbf{r},t)\right ] \Psi(\mathbf{r},t)$" /></p>


## Testing obsolete?

$$
\Psi(\mathbf{r},t) 
$$

This works $$\int x dx$$?

$$
\begin{align*}
  & \phi(x,y) = \phi \left(\sum_{i=1}^n x_ie_i, \sum_{j=1}^n y_je_j \right)
  = \sum_{i=1}^n \sum_{j=1}^n x_i y_j \phi(e_i, e_j) = \\
  & (x_1, \ldots, x_n) \left( \begin{array}{ccc}
      \phi(e_1, e_1) & \cdots & \phi(e_1, e_n) \\
      \vdots & \ddots & \vdots \\
      \phi(e_n, e_1) & \cdots & \phi(e_n, e_n)
    \end{array} \right)
  \left( \begin{array}{c}
      y_1 \\
      \vdots \\
      y_n
    \end{array} \right)
\end{align*}
$$
The following is a math block:

$$ 5 + 5 $$

But next comes a paragraph with an inline math statement:

\$$ 5 + 5 $$
