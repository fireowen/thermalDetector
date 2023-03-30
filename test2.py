import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initial value of j
j_initial = 30

# Define the slider
slider_ax = fig.add_axes([0.2, 0.05, 0.6, 0.05])
slider = Slider(slider_ax, 'j', 5, 100, valinit=j_initial, valstep=1)

# Define the plot function
def plot_sphere(j):
    u, v = np.mgrid[0:2*np.pi:j, 0:np.pi:20j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.clear()
    ax.plot_wireframe(x, y, z, color="red")
    ax.set_title("Sphere (j={})".format(j))
    fig.canvas.draw_idle()

# Update the plot when the slider is changed
slider.on_changed(plot_sphere)

# Plot the initial sphere
plot_sphere(j_initial)

# Show the plot
plt.show()
