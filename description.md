Description
-----------

Python is one of the world's most popular programming languages for numerical
computing. In areas of application like physical simulation, signal processing,
predictive analytics, and more, engineers and data scientists increasingly use
Python as their primary tool for working with numerical large-scale data.

Despite this diversity of application domains, almost all numerical programming
in Python builds upon a small foundation of libraries. In particular, the
`numpy.ndarray` is the core data structure for the entire PyData ecosystem, and
the `numpy` library provides many of the foundational algorithms used to power
more domain-specific libraries.

The goal of this tutorial is to provide an introduction to numpy -- how it
works, how it's used, and what problems it aims to solve. In particular, we
will focus on building up students' mental model of how numpy works and how
**idiomatic** usage of numpy allows us to implement algorithms much more
efficiently than is possible in pure Python.

Audience
--------

This tutorial is intended for programmers with intermediate python skills who want to improve their ability to use Python for numerical computing. Example audience members might include:

- Software engineers who work with Python but have had limited exposure to Python's numerical computing stack.
- Data scientists who have used numpy and pandas and want to develop a deeper understanding of how those libraries work.

By the end of this tutorial, students will learn the following skills:

- Students will develop a mental model of how numpy arrays work, and why they're faster than "vanilla" python when used properly.
- Students will learn to apply techniques like vectorization, broadcasting, and fancy indexing to write fast, clear, and idiomatic numpy code.
- Students will be able to recognize common pathological uses of numpy (e.g., looping over the elements of an array to calculate a sum) and will be able to replace these pathological uses with efficient alternatives.

Additional Notes
----------------

**Prior Experience With This Tutorial:**

I've given a shorter version of this tutorial as a non-interactive
presentation, which can be found on YouTube at
https://www.youtube.com/watch?v=YAHZa8xZWBU. Talk materials can be found at
https://github.com/ssanderson/pydata-toolbox.

**Speaking/Teaching Experience:**

I've spoken at several other Python conferences on topics in numerical
programming and metaprogramming:

- [PyCon 2015 - Playing with Python Bytecode (with Joe Jevnik)](https://www.youtube.com/watch?v=mxjv9KqzwjI)
- [PyBay 2016 - Unspeakably Evil Hacks in Service of Marginally Improved Syntax](https://www.youtube.com/watch?v=CcfZeZNJC4E)
- [PyData 2015 - Developing an Expression Language for Quantitative Financial Modeling](https://www.youtube.com/watch?v=8XlDvGYhlr8j)

**Experience with the Subject Matter:**

I work regularly with numpy, pandas, and other numerical Python libraries as an
engineer at [Quantopian](https://www.quantopian.com/), where I help maintain
[Zipline](https://github.com/quantopian/zipline), a financial algorithm
simulator that uses numpy extensively.
