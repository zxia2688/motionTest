import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, FFMpegFileWriter
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import mpl_toolkits.mplot3d.axes3d as p3

def main():

    radius = 3

    # Create a 3D figure
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim3d([-radius / 2, radius / 2])
    ax.set_ylim3d([0, radius])
    ax.set_zlim3d([-radius / 3., radius * 2 / 3.])
    ax.view_init(elev=30, azim=-45)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Plot')
    ax.grid(b=False)



    minx = -0.38998434
    maxx = 0.49282598
    miny = 0
    minz = -0.12673849
    maxz = 0.62266415

    plot_xzPlane(ax, minx, maxx, miny, minz, maxz)

    x = [0, -0.09078452, -0.18190606, -0.22566715, -0.314275]
    y = [1.2279323, 1.1182609, 0.6185465, 0.06494771, 0]
    z = [0, -0.02759667, -0.05151606, -0.06999476, 0.09107707]

    ax.plot3D(x, y, z, color='r', linewidth=4)

    plt.show()
    plt.pause(5)  # Pause for 5 seconds to display the plot window

def plot_xzPlane(ax, minx, maxx, miny, minz, maxz):
    # Plot a plane XZ
    verts = [
        [minx, miny, minz],
        [minx, miny, maxz],
        [maxx, miny, maxz],
        [maxx, miny, minz]
    ]
    xz_plane = Poly3DCollection([verts])
    xz_plane.set_facecolor((0.5, 0.5, 0.5, 0.5))
    ax.add_collection3d(xz_plane)

if __name__ == "__main__":
    main()
