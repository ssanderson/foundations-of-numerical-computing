## Title/About Me (1 minute (1/180))
## Outline (2 minutes (3/180))
## Environment Setup (7 minutes (10/180))

My plan for providing an environment in this talk is to set up a
[JupyterHub](https://github.com/jupyterhub/jupyterhub) instance that provides a
Docker container for each student with an up-to-date scientific python
installation. This will hopefully avoid the often-painful process of setting up
a scientific python environment on users' laptops; each user will just need to
be able to access a public URL on the internet.

In the event that internet fails during the tutorial, my backup plan will be to
go through the exercises together on my presentation laptop, taking volunteers
from the audience to implement solutions.

## Section 1: Why Do We Need Numpy?

In this section we motivate the need for special-purpose data structures like
the `numpy.ndarray` in numerical computing.

The goal of this section is for students to develop an intuition for why
Python's built-in data structures are inefficient for large-scale numerical
computing.

### Review of Python Lists (4 minutes (14/180)

The goal of this section is to briefly review Python lists. This review will
serve as a point of comparison when we introduce numpy arrays in subsequent
sections. (Notes in parentheses indicate points of future comparison).

This section also serves to point out features of Python lists that we often
take for granted (e.g., the fact that we can put values of different types into
a list), which we'll give up with numpy in exchange for better performance.

- Indexing
  - Scalar access is 0-indexed. (Same as numpy)
  - Negative indexing counts from end of list. (Same as numpy)
  - Slicing allows us to copy at regular intervals from a region. (Syntax same
    as numpy; different copying semantics)
- Efficiently size-mutable (unlike numpy).
- Can hold objects of different types (unlike numpy).

### Profiling Numerical Algorithms with Python Lists (6 minutes (20/180))

The goal of this section is to show that numerical algorithms are unacceptably
slow when implemented using python's built-in lists and integers.

We demonstrate this implementing a matrix multiplication function using
matrices represented as lists-of-lists and showing how long it takes to
multiply matrices of various sizes. We compare this performance to an
alternative implementation in Fortran using f2py (via the Jupyter Notebook's
``%%fortran`` magic), and we learn that Python's performance for this task is
several orders of magnitude worse than the native fortran implementation.

### Why is the Python Version so Slow? (5 minutes (25/180))

In this section, we explain why the Python code we showed in the previous
section is so much slower than the native fortran code.

We highlight two important observations:

1. Numerical algorithms on lists of Python ints/floats are slow because we have
   to pay the overhead of dynamic dispatch on every data element in our lists.
2. Numerical algorithms on lists of Python ints/floats are slow because we have
   to pay the overhead of bytecode interpretation on every operation we perform.

We observe that, very often, both of these overheads are wasteful. If we know
we have a list containing only values of a single type, then we don't need
dynamic dispatch on each element. Similarly, if we want to perform the same
operation in every iteration of a loop, then bytecode interpretation is
unnecessary.

### How Numpy Makes Numerical Algorithms Fast (5 minutes (30/180))

In this section, we explain how numpy allows us to fix the performance problems
observed in the previous section by giving up some flexibility in how it allows
us to use its data structures.

Numpy solves the performance problems listed above by:

1. Providing containers that can only have one kind of element (which removes
   the cost of dynamic dispatch).

2. Providing "vectorized" functions that operate on entire arrays at once
   (which removes the cost of interpretation).

- Show an example of constructing a numpy array from a list/list of lists.
- Illustrate (1) by trying (and failing) to insert an object into an array of
  ints.
- Illustrate (2) by showing that `ndarray` overloads binary operators like `+`
  and `*` to perform element-wise operations.
- Show that matrix multiplication using numpy array is competitive with
  Fortran.

### Exercise: How Much Data Do You Need for Numpy Dot Product to Be Faster? (5 minutes (35/180))

Nothing in life is free. Numpy allows us to speed up computations on large
arrays by performing one moderately complex dispatch **per array** instead of a
cheap dispatch **per array element**. Since the single numpy dispatch is more
complex, we might expect that numpy is still slower for very small
arrays. Using the ``%%timeit`` builtin, can you figure out how many data points
you need to have for a numpy dot product to be faster than a pure-python
implementation.

Example Test:
```
In [9]: a = np.array([1, 2, 3]); b = np.array([2, 3, 4])
In [10]: %timeit (a * b).sum()
1000000 loops, best of 3: 1.33 µs per loop

In [11]: a = [1, 2, 3]; b = [2, 3, 4]
In [12]: %timeit sum(x * y for x, y in zip(a, b))
1000000 loops, best of 3: 531 ns per loop
```

## Section 2: Core Numpy Operations

In this section, we show core features and numpy idioms that should form users'
primary day-to-day toolbox. This section is the core content of the tutorial.

The main goals of this section are:

1. Provide an overview of important numpy features and concepts.
2. Provide a set of examples of solving problems by "thinking with arrays".

### Creating Arrays (5 minutes (40/180))

[Reference](https://docs.scipy.org/doc/numpy-1.13.0/reference/routines.array-creation.html)

We're going to see a bunch of different ways to create arrays in the upcoming
examples, so we start by showing various examples of ways to create arrays.

The important takeaway from this section is just that there are lots of useful
built-in ways to create arrays.

- `np.array`
- `np.arange`/`np.linspace`/`np.logspace`
- `np.full`/`np.empty`/`np.ones`/`np.zeros`
- `np.full_like`/`np.empty_like`/`np.ones_like`/`np.zeros_like`
- `np.eye`/`np.identity`/`np.diag`
- `np.RandomState`
- `np.load`/`np.save`
- `np.loadtxt`/`pandas.read_csv`

### Exercises: (5 minutes (45/180))

- Create 5 x 5 array containing only only the number zero. (`np.zeroes((5, 5))`)
- Create 3 x 3 x 3 array containing only only the number one.  (`np.ones((3, 3, 3))`)
- Create a 10 x 10 array containing values from 1 to 10 on the diagonal. (`np.diag(np.arange(1, 11))`)
- Save one of the above arrays to disk. Load it back from disk.
- Create a 100 x 100 array containing samples from a standard normal distribution. (`np.RandomState.normal`)

### UFuncs (10 minutes (55/180))

[Reference](https://docs.scipy.org/doc/numpy-1.13.0/reference/ufuncs.html)

Universal Functions (UFuncs) allow us to apply operations to every element of
an array (or on every pair of elements in multiple arrays).

UFuncs can be implemented either with functions (e.g. `np.sqrt`) or with
operators (e.g. `+`, `-`, `==`).  All of the binary operators have a corresponding
function as well, (e.g. `+` -> `np.add`).

Binary UFuncs all provide a suite of methods that implement reduction/traversal
algorithms in terms of their associated binary operator.

- `ufunc.reduce`: Folds the binary operator over a dimension. For example, `add.reduce` -> `sum`.
- `ufunc.accumulate`: Folds the binary operator over a dimension, keeping a
  running tally of results. For example `add.accumulate` -> `cumsum`.
- `ufunc.outer`: Applies binary operator to pairs of elements from two
  arrays.
- `ufunc.reduceat`: Applies `reduce` to successive slices of array. I've never
  seen this used in the wild. We're not going to spend time on it.
- `ufunc.at`: Also never seen this used.

### Exercises: (10 minutes (65/180))

- Write a function that takes an array of any shape and calculates
  `sin(x) ** 2 + cos(x) ** 2` for each element of the array.
- Write a function that takes a 2D array and returns a 1D array containing the
  sum of each column.
- Write a function that takes a 2D array and returns a 1D array containing the
  sum of each row.
- Implement `np.cumprod` in terms of `np.multiply`.

### Broadcasting (15 minutes (80/180))

[Reference](https://docs.scipy.org/doc/numpy-1.13.0/user/basics.broadcasting.html)

So far, we've only seen operations on arrays that have exactly the same shape,
but one of the most powerful tools in numpy is its ability to combine arrays of
different dimensions. This technique is called "broadcasting". Broadcasting
allows us to apply operations on two arrays of unequal shape as long as the
arrays' shapes are "compatible".

Examples:

- `array + scalar`
- `array2d - array2d.mean(axis=0)`
- `array2d - array2d.mean(axis=1)`
- `(n x 1)` + `(1 x m)` -> `n x m`
- `(n,)` + `(m x 1)` -> `n x m`

The general intuition for "compatible" is that two arrays are compatible if
they can be converted to the same shape by replicating themselves along missing
axes.

- Talk about the broadcasting algorithm.
- Show `np.newaxis` for adding "synthetic" dimensions to arrays.
- Show that all multi-input ufuncs broadcast their operands before running.

### Exercises (10 minutes (90/180)

- Write a function that computes the shape of the output of two arrays when
  broadcasted together.

- Write a function that takes an array of interval start dates, an equal-length
  array of interval stop dates, and an array of output dates, and return a
  2D-boolean array with a column for each start/stop pair and a row for each
  output date. Example:

```
In [86]: starts
Out[86]: array(['2015-01-02', '2015-01-05', '2015-01-06'], dtype='datetime64[D]')

In [87]: stops
Out[87]: array(['2015-01-04', '2015-01-06', '2015-01-09'], dtype='datetime64[D]')

In [88]: out_dates
Out[88]:
array(['2015-01-02', '2015-01-03', '2015-01-04', '2015-01-05',
       '2015-01-06', '2015-01-07', '2015-01-08', '2015-01-09'], dtype='datetime64[D]')

In [89]: my_func(starts, stops, out_dates)
Out[89]:
array([[ True, False, False],
       [ True, False, False],
       [ True, False, False],
       [False,  True, False],
       [False,  True,  True],
       [False, False,  True],
       [False, False,  True],
       [False, False,  True]], dtype=bool)
```

(this is an example of a real problem I've encountered for which broadcasting
enables an elegant 1-line solution.)

### Break (10 minutes (100/180)

### Slicing and Selection (15 minutes (115/180))

[Reference](https://docs.scipy.org/doc/numpy-1.13.0/user/basics.indexing.html#indexing)

Often we want to operate on just a part of an array. Numpy provides many ways
to select sub-sections out of an array.

All the intuitions we have from `list` carry over straightforwardly.

- `a[i]`
- `a[i:j]`
- `a[i:]`
- `a[:j]`
- `a[i:j:k]`

One important difference is that slicing from an array doesn't make a copy; the
underlying data is still shared. This can be a powerful tool for saving memory
and CPU, but it can also bite you if you're not careful.

Slicing also generalizes to multiple dimensions in the way you'd expect.

- `a[i, j]`
- `a[i:, j:]`
- ...

In addition to the usual list-like semantics for slicing, there are two other
important techniques for selecting subsets of an array: index arrays and masks.

Passing an array of indices selects the elements at each index we passed.
`a[[1, 3, 5]]` gets the elements at indices 1, 3, and 5. This is often useful
for permutations. For example, we can use `argsort` to build a permutation
array that, when used as an indexer, would sort another array.

"Masking" allows us to select elements from an array by indexing with a boolean
array. This selects (after broadcasting) all the elements from the first array
where the boolean array was True.

Masking is most often used for filtering expressions like `a[a > 5]` or
`a[(a > 3) & (a < 5)]` (note the parentheses here; they're necessary because of
the relative precedence of `&` and `<`).

### Exercises (15 minutes (130/180))

- Write a function that takes a 2d array and selects the 2x2 array from its top-left corner.
- Write the same function, but select the bottom-right corner.
- Write a function that takes an array and returns an array containing all the
  values less than 3.
- Write a function that takes a 2d array and selects all the columns for which
  the mean is less than the median.
- Write a function that takes a "table" as a dictionary of 1d arrays and sorts
  all of the columns of the table by a single column (Hint: Use argsort.)

### Reshaping (3 minutes (133/180))

- `np.reshape`
- `np.transpose`
- `np.ravel`

### Concatenation (3 minutes (136/180))

- `np.hstack`
- `np.vstack`
- `np.concatenate`

### Review (9 minutes (145/180))

The purpose of this section is to reinforce the material we covered in the
preceding sections and to emphasize the ways in which the different features of
numpy complement one another.

- Array Creation
- UFuncs
- Broadcasting
- Slicing and Selection

- Show 1-2 examples of real-world problems solved using a combination of numpy
  features.

## Section 3: Peeking Under the Hood

We've seen how we can use numpy's core features to solve problems, but we
haven't talked much about how those features work. In this section, we talk
about how Numpy arrays are represented in memory, and we discuss how that
representation enables some surprising optimizations (and occasionally some
unexpected behaviors).

The main benefit of understanding this material for a numpy user is that it
helps build intuition for reasoning about the efficiency of various
operations. In particular, seeing how arrays are implemented is important for
understanding what operations create copies vs. what operations just create
views.

### What's in an Array? (7 minutes (152/180))

An array consists of the following information:

- Data: Pointer to the start of a `char *` array in C that contains the actual
  data stored in the array.
- DType: Describes the data stored in element of the array. In particular, this
  encodes the size of each element, as well as information used to dispatch
  UFuncs to the appropriate low-level information.
- Shape: Tuple describing the number and length of the dimensions of the array.
- Strides: Tuple describing how to get to an element at a particular coordinate.

### Slice and Stride Tricks (13 minutes (165/180))

Of these attributes, `strides` is the most interesting. If the array has
strides `(x, y, z)`, then that means that the array element at index `(i, j,
k)` is stored at offset `(i * x, j * y, k * z)` from the start of the data
buffer. This representation enables lots of clever tricks for avoiding copies
and creating "virtual" copies of arrays.

**Example 1: Zero-Copy Slices**

We can implement `a[::2]` without copying the underlying data by cutting the
shape in half and multiplying the strides by 2:

```
In [128]: data = np.arange(10)

In [129]: data
Out[129]: array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

In [130]: data.strides, data.shape
Out[130]: ((8,), (10,))

In [131]: data2 = data[::2]

In [132]: data2
Out[132]: array([0, 2, 4, 6, 8])

In [133]: data2.strides, data2.shape
Out[133]: ((16,), (5,))
```

In general, we can implement any pure slicing operation without making a copy
of the underlying data:

- Slicing with a `start` just moves the `data` pointer forward in the new
  array.
- Slicing with a `stop` just shrinks the `shape` of the new array.
- Slicing with a `step` shrinks the shape and applies a multiplier to the strides.

**Example 2: Virtual Copies**

Sometimes we want the **semantics** of copying an array, but we don't actually
want to pay the memory and CPU cost of making the copy. We can play tricks with
array strides to create arrays that appear to make copies, but without actually
making the copies.

```
In [138]: data
Out[138]: array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

In [139]: from numpy.lib.stride_tricks import as_strided

In [140]: data
Out[140]: array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

In [141]: as_strided(data, shape=(3, 10), strides=(0, 8))
Out[141]:
array([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
       [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
       [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]])

In [142]: as_strided(data, shape=(10, 3), strides=(8, 0))
Out[142]:
array([[0, 0, 0],
       [1, 1, 1],
       [2, 2, 2],
       [3, 3, 3],
       [4, 4, 4],
       [5, 5, 5],
       [6, 6, 6],
       [7, 7, 7],
       [8, 8, 8],
       [9, 9, 9]])
```

Although the above operations **look** like they've created copies, the
underlying data is never duplicated. This can be a powerful tool, but can also
create nasty and confusing bugs, so be careful when playing these sorts of
games.

```
In [155]: x = as_strided(data, shape=(3, 10), strides=(0, 8))

In [156]: x
Out[156]:
array([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
       [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
       [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]])

In [157]: data
Out[157]: array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

In [158]: data[0] = 100

In [159]: data
Out[159]: array([100,   1,   2,   3,   4,   5,   6,   7,   8,   9])

In [160]: x
Out[160]:
array([[100,   1,   2,   3,   4,   5,   6,   7,   8,   9],
       [100,   1,   2,   3,   4,   5,   6,   7,   8,   9],
       [100,   1,   2,   3,   4,   5,   6,   7,   8,   9]])
```

### Exercise: (5 minutes (170/180))

- Use `as_strided` to write a function that takes a 1-d array and returns a 2-D
  array with three columns, where each row is a length-3 slice of the input
  array.

```
In [168]: data
Out[168]: array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

In [169]: as_strided(data, (8, 3), (8, 8))
Out[169]:
array([[0, 1, 2],
       [1, 2, 3],
       [2, 3, 4],
       [3, 4, 5],
       [4, 5, 6],
       [5, 6, 7],
       [6, 7, 8],
       [7, 8, 9]])
```

### Conclusion: Review and Next Steps (10 minutes (180/180))

**Key Takeaways:**

- Numerical algorithms are slow in pure Python because the overhead of dynamic
  dispatch and interpretation dominates our runtime.

- Numpy solves these problems by imposing additional restrictions on the
  contents of arrays and by moving the inner loops of our algorithms into
  compiled C code.

- Using Numpy effectively often requires reworking a algorithms to use
  vectorized operations instead of explicit loops, but the resulting operations
  are usually simpler, clearer, and (much) faster than the pure Python
  equivalents.

**Next Steps:**

- [`scipy`](https://docs.scipy.org/doc/scipy/reference/) implements many
  algorithms for optimization, signal processing, linear algebra, and other
  important scientific needs.

- [`pandas`](https://pandas.pydata.org/pandas-docs/stable/) adds labelled,
  heterogenous data structures on top of numpy. It also provides efficient I/O
  routines and implementations of rolling/grouped algorithms.

- [`matplotlib`](https://matplotlib.org/) provides high-quality plotting
  routines using numpy arrays as its primary data format.

- [`scikit-learn`](http://scikit-learn.org/stable/) provides machiner learning
  algorithms using numpy arrays as its primary data format.

- Too many other libraries to discuss.
