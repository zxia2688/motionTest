import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, FFMpegFileWriter
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import mpl_toolkits.mplot3d.axes3d as p3
# import cv2
from textwrap import wrap


def list_cut_average(ll, intervals):
    if intervals == 1:
        return ll

    bins = math.ceil(len(ll) * 1.0 / intervals)
    ll_new = []
    for i in range(bins):
        l_low = intervals * i
        l_high = l_low + intervals
        l_high = l_high if l_high < len(ll) else len(ll)
        ll_new.append(np.mean(ll[l_low:l_high]))
    return ll_new


def plot_3d_motion(save_path, kinematic_tree, joints, title, dataset, figsize=(3, 3), fps=120, radius=1,
                   vis_mode='default', gt_frames=[]):
    #matplotlib.use('Agg')

    title = '\n'.join(wrap(title, 20))

    def init():

        ax.set_xlim3d([-radius / 2, radius / 2])
        ax.set_ylim3d([0, radius])
        ax.set_zlim3d([-radius / 3., radius * 2 / 3.])
        # Set labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D Plot')
        # print(title)
        fig.suptitle(title, fontsize=10)
        ax.grid(b=False)

        """
        # Get the minimum and maximum values

        x_min, y_min, z_min = -0.29998797, 0.00166055, -0.09749115
        x_max, y_max, z_max = 0.37909693, 1.5627236, 0.47897243

        # Create a 3D figure
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')



       

        # Set the axis limits
        ax.set_xlim3d(x_min, x_max)
        ax.set_ylim3d(y_min, y_max)
        ax.set_zlim3d(z_min, z_max)
        # print(title)
        fig.suptitle(title, fontsize=10)
        ax.grid(b=False)
        """


    def plot_xzPlane(minx, maxx, miny, minz, maxz):
        ## Plot a plane XZ
        verts = [
            [minx, miny, minz],
            [minx, miny, maxz],
            [maxx, miny, maxz],
            [maxx, miny, minz]
        ]
        xz_plane = Poly3DCollection([verts])
        xz_plane.set_facecolor((0.5, 0.5, 0.5, 0.5))
        ax.add_collection3d(xz_plane)

        # Set the camera view to focus on the XZ plane
        ax.view_init(elev=0, azim=-90)

        plt.show()
    #         return ax

    #processing data
    # (seq_len, joints_num, 3)
    data = joints.copy().reshape(len(joints), -1, 3)

    # Print the shape of the data variable (display the data)
    print("Shape of data:", data.shape)

    # Print the minimum and maximum values of the data
    print("Minimum values of data:", data.min(axis=0).min(axis=0))
    print("Maximum values of data:", data.max(axis=0).max(axis=0))


    # Get the current limits of the x-axis
    x_min, x_max = plt.xlim()
    print("X-axis range:", x_min, "-", x_max)

    # Get the current limits of the y-axis
    y_min, y_max = plt.ylim()
    print("Y-axis range:", y_min, "-", y_max)


    # preparation related to specific datasets
    if dataset == 'kit':
        data *= 0.003  # scale for visualization
    elif dataset == 'humanml':
        data *= 1.3  # scale for visualization
    elif dataset in ['humanact12', 'uestc']:
        data *= -1.5 # reverse axes, scale for visualization

    #set up the plot
    fig = plt.figure(figsize=figsize)
    plt.tight_layout()
    ax = fig.add_subplot(111, projection='3d')
    #ax = p3.Axes3D(fig)
    init()
    MINS = data.min(axis=0).min(axis=0)
    MAXS = data.max(axis=0).max(axis=0)

    print("Minimum values of joint positions:", MINS)
    print("Maximum values of joint positions:", MAXS)
    plt.show()

    colors_blue = ["#4D84AA", "#5B9965", "#61CEB9", "#34C1E2", "#80B79A"]  # GT color
    colors_orange = ["#DD5A37", "#D69E00", "#B75A39", "#FF6D00", "#DDB50E"]  # Generation color
    colors = colors_orange
    if vis_mode == 'upper_body':  # lower body taken fixed to input motion
        colors[0] = colors_blue[0]
        colors[1] = colors_blue[1]
    elif vis_mode == 'gt':
        colors = colors_blue

    frame_number = data.shape[0]
    #     print(dataset.shape)

    height_offset = MINS[1]
    data[:, :, 1] -= height_offset # subtract the y-values of all data by height_offset
    trajec = data[:, 0, [0, 2]] # this is a 2d projection of 1st point trajectory(through all frames) to the xz plane

    data[..., 0] -= data[:, 0:1, 0] # looks like it is doing some offseting from the 1st point
    data[..., 2] -= data[:, 0:1, 2]

    plt.show()
    #     print(trajec.shape)

    def update(index):
        #         print(index)
        #ax.lines = []
        for line in ax.lines:
            line.remove()
        #ax.collections = []

        for line in ax.collections:
            line.remove()
        ax.view_init(elev=120, azim=-90)
        ax.dist = 7.5
        #         ax =




        plot_xzPlane(MINS[0] - trajec[index, 0], MAXS[0] - trajec[index, 0], 0, MINS[2] - trajec[index, 1],
                     MAXS[2] - trajec[index, 1])
        #         ax.scatter(dataset[index, :22, 0], dataset[index, :22, 1], dataset[index, :22, 2], color='black', s=3)


        # if index > 1:
        #     ax.plot3D(trajec[:index, 0] - trajec[index, 0], np.zeros_like(trajec[:index, 0]),
        #               trajec[:index, 1] - trajec[index, 1], linewidth=1.0,
        #               color='blue')
        # #             ax = plot_xzPlane(ax, MINS[0], MAXS[0], 0, MINS[2], MAXS[2])


        used_colors = colors_blue if index in gt_frames else colors
        for i, (chain, color) in enumerate(zip(kinematic_tree, used_colors)):
            if i < 5:
                linewidth = 4.0
            else:
                linewidth = 2.0

            x = data[index, chain, 0]
            y = data[index, chain, 1]
            z = data[index, chain, 2]

            ax.plot3D(data[index, chain, 0], data[index, chain, 1], data[index, chain, 2], linewidth=linewidth,
                      color=color)
            plt.show()

        #         print(trajec[:index, 0].shape)

        ax.autoscale()

        plt.savefig(r'C:\Users\Test\myproject\motionTest\motion-diffusion-model\save\plot_test_{:d}.png'.format(index))

        plt.axis('off')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])

    ani = FuncAnimation(fig, update, frames=frame_number, interval=1000 / fps, repeat=False)

    # writer = FFMpegFileWriter(fps=fps)
    ani.save(save_path, fps=fps)
    # ani = FuncAnimation(fig, update, frames=frame_number, interval=1000 / fps, repeat=False, init_func=init)
    # ani.save(save_path, writer='pillow', fps=1000 / fps)

    plt.close()
