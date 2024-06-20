
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def main():
    #init functions

    ax,colors,colors_blue=plot_setting( radius=3)

    '''
    # general parameter
    radius = 0.5
    # Create a 3D figure
    fig = plt.figure(figsize=(3,3))
    plt.tight_layout()

    ax = fig.add_subplot(111, projection='3d')
    #ax = p3.Axes3D(fig)
    ax.set_xlim3d([-radius / 2, radius / 2])
    ax.set_ylim3d([0, radius])
    ax.set_zlim3d([-radius / 3., radius * 2 / 3.])
    '''

    # Define the coordinates
    x = [0, -0.09078452, -0.18190606, -0.22566715, -0.314275]
    y = [1.2279323, 1.1182609, 0.6185465, 0.06494771, 0]
    z = [0, -0.02759667, -0.05151606, -0.06999476, 0.09107707]

    # Plot the 3D line
    ax.plot3D(x, y, z, 'r-', linewidth=2)

    # turn off grid and axis
    ax.grid(False)
    ax.set_axis_off()

    # Set labels and title
    '''
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Line Plot')
    '''
    # Adjust the view

    ax.view_init(elev=0, azim=-90)
    # Display the plot
    plt.show()

def plot_setting(figsize=(3,3), radius=1,vis_mode='default'):
    fig = plt.figure(figsize=figsize)
    plt.tight_layout()

    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim3d([-radius / 2, radius / 2])
    ax.set_ylim3d([0, radius])
    ax.set_zlim3d
    colors_blue = ["#4D84AA", "#5B9965", "#61CEB9", "#34C1E2", "#80B79A"]  # GT color
    colors_orange = ["#DD5A37", "#D69E00", "#B75A39", "#FF6D00", "#DDB50E"]  # Generation color
    colors = colors_orange
    if vis_mode == 'upper_body':  # lower body taken fixed to input motion
        colors[0] = colors_blue[0]
        colors[1] = colors_blue[1]
    elif vis_mode == 'gt':
        colors = colors_blue

    return ax,colors,colors_blue

def plot_background(minx, maxx, miny, minz, maxz):
        ## Plot a plane XZ
        verts = [
            [minx, miny, minz],
            [minx, miny, maxz],
            [maxx, miny, maxz],
            [maxx, miny, minz]
        ]
        xz_plane = Poly3DCollection([verts])
        xz_plane.set_facecolor((0.5, 0.5, 0.5, 0.5))

        plt.show()

        return xz_plane

def  data_processing(joints,dataset):
    # processing data
    # (seq_len, joints_num, 3)
    data = joints.copy().reshape(len(joints), -1, 3)

    # preparation related to specific datasets
    if dataset == 'kit':
        data *= 0.003  # scale for visualization
    elif dataset == 'humanml':
        data *= 1.3  # scale for visualization
    elif dataset in ['humanact12', 'uestc']:
        data *= -1.5  # reverse axes, scale for visualization
    MINS = data.min(axis=0).min(axis=0)


    height_offset = MINS[1]
    data[:, :, 1] -= height_offset  # subtract the y-values of all data by height_offset
    trajec = data[:, 0, [0, 2]]  # this is a 2d projection of 1st point trajectory(through all frames) to the xz plane

    data[..., 0] -= data[:, 0:1, 0]  # looks like it is doing some offseting from the 1st point
    data[..., 2] -= data[:, 0:1, 2]

    return data,trajec

#plot 3D data on renewed frame
def uodate_frame(ax,index,data,trajec,kinematic_tree,colors,colors_blue,gt_frames=[]):
    MINS = data.min(axis=0).min(axis=0)
    MAXS = data.max(axis=0).max(axis=0)
    plot_background(MINS[0] - trajec[index, 0], MAXS[0] - trajec[index, 0], 0, MINS[2] - trajec[index, 1],
                 MAXS[2] - trajec[index, 1])



    print(index)

    #remove all existing lines
    for line in ax.lines:
        line.remove()

    for object in ax.collections:
        object.remove()
        ax.dist=7.5

    used_colors = colors_blue if index in gt_frames else colors

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
    return



def animate(title,fps=120,gt_frames=[]):

    return

if __name__ == "__main__":
    main()