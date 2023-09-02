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

This is a fun little app that teaches you about different Interpolation Algorithms. If you need to learn about them for any reason then this is a fun and interactive app to do it. Want me too add something more? Create a feature request in issues

## Features

1. **Interactive Graphing**: Add and move points directly on the graph.
2. **Live Update**: Watch the curve change in real-time as you edit points.
3. **Multiple Algorithms**: Choose from Lagrange, Cubic Spline, Linear, Rational, and Hermite interpolation methods.
4. **Copy to Clipboard**: Easily copy the resulting equations or spline coefficients.
5. **Export Graph**: Save your graph as a PNG image.
6. **FAQ Section**: Learn about each algorithm and how to use them effectively.


## Installation

### Prerequisites

This project requires Tkinter, which comes pre-installed with Python for Windows and macOS. However, if you're running a custom or minimal Python installation, you may need to install it manually.


#### Install it on Ubuntu:

```bash
sudo apt-get install python-tk
```



### Steps

1. Clone the GitHub repository:
   ```bash
   git clone https://github.com/Trevor050/Interpolation-Algorithms.git
   ```
2. Navigate to the project directory and install the required packages:
   ```bash
   cd InterpolationAlgorithmsGUI
   pip install -r requirements.txt
   ```
3. Run `main.py` to start the application:
   ```bash
   python main.py
   ```


## Usage

1. **Add Points**: Click the "Add Point" button and then click on the graph where you'd like to add a point.
2. **Remove Points**: Click the "Remove Point" button and then click on a point on the graph to remove it.
3. **Change Algorithm**: Use the dropdown menu to select the interpolation algorithm you'd like to use.
4. **Live Update**: Check or uncheck this box to enable or disable real-time updates as you edit points.
5. **Export Graph**: Click this button to save the current graph as a PNG image.

## Screenshots

These are three different screenshots using three different interpolation methods on the same graph! (They use different graphing styles too)

### Lagrange Interpolation
![Lagrange Interpolation](https://github.com/trevor050/Interpolation-Algorithms/blob/main/screenshots/Screenshot%202023-09-02%20at%204.24.40%20PM.png)

### Rational
![Cubic Spline](https://github.com/trevor050/Interpolation-Algorithms/blob/main/screenshots/Screenshot%202023-09-02%20at%204.25.10%20PM.png)

### Cublic Spline
![Newton's Method](https://github.com/trevor050/Interpolation-Algorithms/blob/main/screenshots/Screenshot%202023-09-02%20at%204.25.21%20PM.png)


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
