import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import numpy as np
from scipy.interpolate import lagrange
from scipy.interpolate import CubicSpline
import pyperclip
from scipy.interpolate import interp1d, BarycentricInterpolator, PchipInterpolator, Rbf
from tkinter import messagebox

# Global list to store points and the currently selected point
points = []
selected_point = None

# Axis limits, to avoid the plot from getting too big
AXIS_LIMIT = 1000
live_update = None

def on_pick(event):
    global selected_point
    ind = event.ind[0]
    selected_point = ind

def on_drag(event):
    global selected_point
    if selected_point is not None and event.xdata is not None and event.ydata is not None:
        new_point = (max(min(event.xdata, AXIS_LIMIT), -AXIS_LIMIT), max(min(event.ydata, AXIS_LIMIT), -AXIS_LIMIT))
        points[selected_point] = new_point
        ax.clear()
        ax.scatter(*zip(*points), color='red', picker=True)
        canvas.draw()
        if live_update.get():
            update_plot()
        else:
            plot_lagrange()

def on_release(event):
    global selected_point
    selected_point = None
    if not live_update.get():
        update_plot()


    

def update_plot():
    ax.clear()
    ax.grid(True)  # Enable grid lines
    ax.set_xlabel('X-Axis')  # Label for X-Axis
    ax.set_ylabel('Y-Axis')  # Label for Y-Axis
    
    if points:
        ax.scatter(*zip(*points), color='red', picker=True)
        
        if interpolation_method.get() == 'Lagrange':
            y_range = plot_lagrange()
        elif interpolation_method.get() == 'Cubic Spline':
            y_range = plot_cubic_spline()
        elif interpolation_method.get() == 'Newton':
            y_range = plot_newton()
        elif interpolation_method.get() == 'Linear':
            y_range = plot_linear()
        elif interpolation_method.get() == 'Rational':
            y_range = plot_rational()
        elif interpolation_method.get() == 'Hermite':
            y_range = plot_hermite()
        else:
            print("Invalid interpolation method specified")
            y_range = plot_lagrange()
            return

        if update_options.get() == "Best Fit":
            if y_range.size:
                min_y = min(min(y for _, y in points), np.nanmin(y_range))
                max_y = max(max(y for _, y in points), np.nanmax(y_range))
                buffer = 0.1 * (max_y - min_y)
                ax.set_ylim(min_y - buffer, max_y + buffer)
                ax.set_xlim(-15, 15)
        elif update_options.get() == 'Fit to Points':
            if points:
                min_x, max_x = min(x for x, y in points), max(x for x, y in points)
                min_y, max_y = min(y for x, y in points), max(y for x, y in points)
                ax.set_xlim(min_x - 0.1 * (max_x - min_x), max_x + 0.1 * (max_x - min_x))
                ax.set_ylim(min_y - 0.1 * (max_y - min_y), max_y + 0.1 * (max_y - min_y))
        elif update_options.get() == "Fixed 100x100":
            ax.set_xlim(-15, 15)
            ax.set_ylim(-100, 100)
    else:
        ax.set_xlim(-15, 15)
        ax.set_ylim(-100, 100)
        
    canvas.draw()





def add_point():
    new_point = (random.uniform(0, 10), random.uniform(0, 10))
    points.append(new_point)
    update_plot()

def remove_point():
    if points:
        points.pop()
        update_plot()

def plot_cubic_spline():
    x, y = zip(*sorted(points))  # Sort points by x-values
    x = np.array(x)
    y = np.array(y)
    cs = CubicSpline(x, y)
    x_range = np.linspace(min(x), max(x), 100)
    y_range = cs(x_range)
    ax.plot(x_range, y_range, color='green', label='Cubic Spline')
    
    equation_list = []
    for i in range(len(x) - 1):
        a, b, c, d = cs.c[:, i]
        equation = f"{a:.5f}x³ + {b:.5f}x² + {c:.5f}x + {d:.5f} for {x[i]} ≤ x < {x[i+1]}"
        equation_list.append(equation)
    
    formatted_equation = " ; ".join(equation_list)
    equation_label.config(text=f"Equation: {formatted_equation[:50]}...")  # Truncate for display
    return y_range



def plot_lagrange():
    if len(points) >= 2:
        x, y = zip(*points)
        x = np.array(x)
        y = np.array(y)
        poly = lagrange(x, y)
        x_range = np.linspace(min(x), max(x), 100)
        y_range = poly(x_range)
        ax.plot(x_range, y_range, color='blue', label='Lagrange Polynomial')
        formatted_equation = format_equation(np.poly1d(poly))
        equation_label.config(text=f"Equation: {formatted_equation}")
        return y_range  # Removed the tuple, now only returning y_range
    return np.array([])  # Returning an empty numpy array if there are no points

def plot_newton():
    x, y = zip(*points)
    newton_poly = BarycentricInterpolator(x, y)
    x_range = np.linspace(min(x), max(x), 100)
    y_range = newton_poly(x_range)
    ax.plot(x_range, y_range, label='Newton Polynomial')
    formatted_equation = "Newton's method (no simple equation)"
    equation_label.config(text=f"Equation: {formatted_equation}")
    return y_range



# Linear Interpolation
def plot_linear():
    x, y = zip(*sorted(points))  # Sort points by x-values
    x = np.array(x)
    y = np.array(y)
    lin_interp = interp1d(x, y)
    x_range = np.linspace(min(x), max(x), 100)
    y_range = lin_interp(x_range)
    ax.plot(x_range, y_range, color='purple', label='Linear Interpolation')
    formatted_equation = "Linear segments between points"
    equation_label.config(text=f"Equation: {formatted_equation}")
    return y_range

# Rational Interpolation (using Radial Basis Function with thin_plate as basis function)
def plot_rational():
    x, y = zip(*points)
    x = np.array(x)
    y = np.array(y)
    rbf = Rbf(x, y, function='thin_plate')
    x_range = np.linspace(min(x), max(x), 100)
    y_range = rbf(x_range)
    ax.plot(x_range, y_range, color='orange', label='Rational Interpolation')
    formatted_equation = "Rational Interpolation (no simple equation)"
    equation_label.config(text=f"Equation: {formatted_equation}")
    return y_range

# Hermite Interpolation (using Piecewise Cubic Hermite Interpolating Polynomial)
def plot_hermite():
    x, y = zip(*sorted(points))  # Sort points by x-values
    x = np.array(x)
    y = np.array(y)
    dy = np.gradient(y, x)  # Compute a simple gradient for derivative values
    hermite_interp = PchipInterpolator(x, y)
    x_range = np.linspace(min(x), max(x), 100)
    y_range = hermite_interp(x_range)
    ax.plot(x_range, y_range, color='brown', label='Hermite Interpolation')
    formatted_equation = "Hermite Interpolation (no simple equation)"
    equation_label.config(text=f"Equation: {formatted_equation}")
    return y_range

# Add these functions to your existing code and integrate them into your GUI the same way you did for Lagrange and Cubic Spline.



def format_equation(poly):
    terms = []
    coeffs = poly.coefficients
    for i, coef in enumerate(coeffs):
        if coef == 0:
            continue
        term = f"{coef:.5f}"
        if i < len(coeffs) - 1:
            term += "x"
            if i < len(coeffs) - 2:
                term += f"⁰¹²³⁴⁵⁶⁷⁸⁹"[len(coeffs) - i - 1]
        terms.append(term)
    return " + ".join(terms)

def copy_to_clipboard():
    if interpolation_method.get() == 'Lagrange':
        y_range = plot_lagrange()
        if y_range.size:  # Checking if the array is not empty
            x, y = zip(*points)
            x = np.array(x)
            y = np.array(y)
            poly = lagrange(x, y)
            formatted_equation = format_equation(np.poly1d(poly)).replace(' x ', 'x + ').replace('  +', ' +')
            pyperclip.copy(f"y = {formatted_equation}")
    elif interpolation_method.get() == 'Cubic Spline':
        x, y = zip(*sorted(points))
        x = np.array(x)
        y = np.array(y)
        cs = CubicSpline(x, y)
        
        equation_list = []
        for i in range(len(x) - 1):
            a, b, c, d = cs.c[:, i]
            equation = f"({a:.5f}x^3 + {b:.5f}x^2 + {c:.5f}x + {d:.5f}){{x>={x[i]} and x<{x[i+1]}}}"
            equation_list.append(equation)
        
        formatted_equation = " + ".join(equation_list)
        pyperclip.copy(formatted_equation)
    elif interpolation_method.get() == 'Newton':
        x, y = zip(*points)
        points_str = ', '.join([f"({x}, {y})" for x, y in points])
        pyperclip.copy(f"Newton's Method Points: {points_str}")
    elif interpolation_method.get() == 'Linear':
        x, y = zip(*sorted(points))
        x = np.array(x)
        y = np.array(y)
        lin_interp = interp1d(x, y)
        x_range = np.linspace(min(x), max(x), 100)
        y_range = lin_interp(x_range)
        equation_list = []
        for i in range(len(x) - 1):
            slope = (y[i+1] - y[i]) / (x[i+1] - x[i])
            intercept = y[i] - slope * x[i]
            equation = f"({slope:.5f}x + {intercept:.5f}){{x>={x[i]} and x<{x[i+1]}}}"
            equation_list.append(equation)
        
        formatted_equation = " + ".join(equation_list)
        pyperclip.copy(formatted_equation)
    elif interpolation_method.get() == 'Rational':
        x, y = zip(*points)
        x = np.array(x)
        y = np.array(y)
        rbf = Rbf(x, y, function='thin_plate')
        x_range = np.linspace(min(x), max(x), 100)
        y_range = rbf(x_range)
        equation_list = []
        for i in range(len(x) - 1):
            equation = f"({y_range[i]:.5f}){{x>={x[i]} and x<{x[i+1]}}}"
            equation_list.append(equation)
        
        formatted_equation = " + ".join(equation_list)
        pyperclip.copy(formatted_equation)
    elif interpolation_method.get() == 'Hermite':
        x, y = zip(*sorted(points))
        x = np.array(x)
        y = np.array(y)
        dy = np.gradient(y, x)
        hermite_interp = PchipInterpolator(x, y)
        x_range = np.linspace(min(x), max(x), 100)
        y_range = hermite_interp(x_range)
        equation_list = []
        for i in range(len(x) - 1):
            equation = f"({y_range[i]:.5f}){{x>={x[i]} and x<{x[i+1]}}}"
            equation_list.append(equation)
        formatted_equation = " + ".join(equation_list)
        pyperclip.copy(formatted_equation)
    else:
        print("Invalid interpolation method specified")
        return
        
def show_faq():
    faq_window = tk.Toplevel(root)
    faq_window.title("FAQ")

    tk.Label(faq_window, text="FAQ - Interpolation Algorithms and Features", font=("Arial", 16)).pack()

    tk.Label(faq_window, text="1. Lagrange Interpolation:", font=("Arial", 14, "bold")).pack(anchor="w")
    tk.Label(faq_window, text="Method: Uses polynomial bases to fit the curve.").pack(anchor="w")
    tk.Label(faq_window, text="Equation: Polynomial equations based on basis polynomials.").pack(anchor="w")
    tk.Label(faq_window, text="Pros: Simple and easy to understand.").pack(anchor="w")
    tk.Label(faq_window, text="Cons: Not efficient for large sets of points.").pack(anchor="w")
    tk.Label(faq_window, text="Copy to Clipboard: Gives a polynomial equation that represents the curve.").pack(anchor="w")

    tk.Label(faq_window, text="2. Cubic Spline:", font=("Arial", 14, "bold")).pack(anchor="w")
    tk.Label(faq_window, text="Method: Uses piecewise cubic polynomials.").pack(anchor="w")
    tk.Label(faq_window, text="Equation: Different polynomials for each sub-interval.").pack(anchor="w")
    tk.Label(faq_window, text="Pros: Smoother curves, better for larger sets.").pack(anchor="w")
    tk.Label(faq_window, text="Cons: More complex to understand.").pack(anchor="w")
    tk.Label(faq_window, text="Copy to Clipboard: Gives piecewise equations for each sub-interval.").pack(anchor="w")

    tk.Label(faq_window, text="3. Linear Interpolation:", font=("Arial", 14, "bold")).pack(anchor="w")
    tk.Label(faq_window, text="Method: Simplest form of interpolation.").pack(anchor="w")
    tk.Label(faq_window, text="Equation: Straight lines between points.").pack(anchor="w")
    tk.Label(faq_window, text="Pros: Simple, fast, and easy to compute.").pack(anchor="w")
    tk.Label(faq_window, text="Cons: Not smooth, only useful for very simple cases.").pack(anchor="w")
    tk.Label(faq_window, text="Copy to Clipboard: Gives linear equations for each sub-interval.").pack(anchor="w")

    tk.Label(faq_window, text="4. Rational Interpolation:", font=("Arial", 14, "bold")).pack(anchor="w")
    tk.Label(faq_window, text="Method: Uses ratios of polynomials.").pack(anchor="w")
    tk.Label(faq_window, text="Equation: Rational function.").pack(anchor="w")
    tk.Label(faq_window, text="Pros: Can represent more complex functions.").pack(anchor="w")
    tk.Label(faq_window, text="Cons: Can be unstable or have poles.").pack(anchor="w")
    tk.Label(faq_window, text="Copy to Clipboard: Gives a rational equation that represents the curve.").pack(anchor="w")

    tk.Label(faq_window, text="5. Hermite Interpolation:", font=("Arial", 14, "bold")).pack(anchor="w")
    tk.Label(faq_window, text="Method: Uses both function values and derivatives.").pack(anchor="w")
    tk.Label(faq_window, text="Equation: Polynomial equations with derivatives.").pack(anchor="w")
    tk.Label(faq_window, text="Pros: Can consider slope at data points for better fitting.").pack(anchor="w")
    tk.Label(faq_window, text="Cons: Requires derivative information.").pack(anchor="w")
    tk.Label(faq_window, text="Copy to Clipboard: Gives a polynomial equation with derivative terms.").pack(anchor="w")

    tk.Label(faq_window, text="7. Copying to Clipboard:", font=("Arial", 14, "bold")).pack(anchor="w")
    tk.Label(faq_window, text="For Lagrange, you get a single polynomial.").pack(anchor="w")
    tk.Label(faq_window, text="For Cubic Spline, you get piecewise equations for each sub-interval.").pack(anchor="w")
    tk.Label(faq_window, text="For others, the format may vary but is designed to be as usable as possible.").pack(anchor="w")

    tk.Button(faq_window, text="Close", command=faq_window.destroy).pack(pady=10)

def export_graph():
    fig.savefig("interpolation_graph.png")
    messagebox.showinfo("Export Successful", "Your graph has been exported as exported_graph.png.")
def main():
    global ax, canvas, update_options, live_update, equation_label, interpolation_method, root, fig

    root = tk.Tk()
    root.title("Interpolation Algorithms")

    button_frame = ttk.Frame(root)
    button_frame.pack(side=tk.TOP, fill=tk.X)

    add_button = ttk.Button(button_frame, text="Add Point", command=add_point)
    add_button.pack(side=tk.LEFT)

    remove_button = ttk.Button(button_frame, text="Remove Point", command=remove_point)
    remove_button.pack(side=tk.LEFT)

    copy_button = ttk.Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard)
    copy_button.pack(side=tk.RIGHT)

    live_update = tk.BooleanVar(value=True)
    live_update_checkbox = ttk.Checkbutton(button_frame, text="Live Update", variable=live_update)
    live_update_checkbox.pack(side=tk.RIGHT)

    update_options = tk.StringVar(value='Best Fit')
    update_menu = tk.OptionMenu(button_frame, update_options, 'Fixed 100x100', 'Fit to Points', 'Best Fit')
    update_menu.pack(side=tk.RIGHT)

    equation_frame = ttk.Frame(root)
    equation_frame.pack(side=tk.BOTTOM, fill=tk.X)
    equation_label = ttk.Label(equation_frame, text="Equation: ", font=("Arial", 16))
    equation_label.pack(side=tk.LEFT)
    fig, ax = plt.subplots()
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)

    interpolation_method = tk.StringVar(value='Lagrange')  # You might already have this line
    interpolation_menu = tk.OptionMenu(button_frame, interpolation_method, 'Lagrange', 'Cubic Spline', 'Newton', 'Linear', 'Rational', 'Hermite')
    interpolation_menu.pack(side=tk.RIGHT)
    interpolation_method.trace_add("write", lambda *args: update_plot())

    update_options.trace_add("write", lambda *args: update_plot())
    live_update.trace_add("write", lambda *args: update_plot())

    export_button = ttk.Button(button_frame, text="Export Graph", command=export_graph)
    export_button.pack(side=tk.LEFT)

    # Inside your main() function, where you set up your Tkinter widgets
    faq_button = ttk.Button(button_frame, text="?", width=2.5, command=show_faq)  # ASCII art or image can be used here
    faq_button.pack(side=tk.LEFT)
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    fig.canvas.mpl_connect('pick_event', on_pick)
    fig.canvas.mpl_connect('motion_notify_event', on_drag)
    fig.canvas.mpl_connect('button_release_event', on_release)

    # Inside your main() function, where you set up your Tkinter widgets
    

    

    root.mainloop()

if __name__ == "__main__":
    main()
