# Interpolation Algorithms

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Supported Algorithms](#supported-algorithms)
6. [Contribution](#contribution)
7. [License](#license)

## Introduction

The Interpolation Algorithms GUI is a Python application built with Tkinter and Matplotlib. It provides an intuitive graphical interface to experiment with various interpolation algorithms. Users can add, remove, and drag points on a graph to see real-time updates of the interpolated curve, represented by different algorithms.

## Features

1. **Interactive Graphing**: Add and move points directly on the graph.
2. **Live Update**: Watch the curve change in real-time as you edit points.
3. **Multiple Algorithms**: Choose from Lagrange, Cubic Spline, Linear, Rational, and Hermite interpolation methods.
4. **Copy to Clipboard**: Easily copy the resulting equations or spline coefficients.
5. **Export Graph**: Save your graph as a PNG image.
6. **FAQ Section**: Learn about each algorithm and how to use them effectively.

## Installation

1. Clone the GitHub repository:
   ```
   git clone https://github.com/trevor050/Interpolation-Algorithms.git
   ```
2. Navigate to the project directory and install the required packages:
   ```
   cd Interpolation-Algorithms
   pip install -r requirements.txt
   ```
3. Run `main.py` to start the app:
   ```
   python main.py
   ```

## Usage

1. **Add Points**: Click the "Add Point" button and then click on the graph where you'd like to add a point.
2. **Remove Points**: Click the "Remove Point" button and then click on a point on the graph to remove it.
3. **Change Algorithm**: Use the dropdown menu to select the interpolation algorithm you'd like to use.
4. **Live Update**: Check or uncheck this box to enable or disable real-time updates as you edit points.
5. **Export Graph**: Click this button to save the current graph as a PNG image.

## Supported Algorithms

- **Lagrange**: This method uses the Lagrange form of the polynomial. It's simple but can oscillate wildly between points.
- **Cubic Spline**: This method fits a different cubic polynomial between each pair of data points.
- **Linear**: A simple method that connects each pair of consecutive points with a straight line.
- **Rational**: This method uses rational functions and is particularly useful when the function has poles.
- **Hermite**: This method also uses cubic polynomials but takes both function and derivative values at each point.



## Contribution

Feel free to fork the repository and submit pull requests. For major changes, open an issue first to discuss what you'd like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
