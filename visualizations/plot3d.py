import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import mpl_toolkits.mplot3d.axes3d as p3
# import cv2
from textwrap import wrap


def plot_3d_motion(save_path, parents, joints_positions, title, scale_factor=1.3, figsize=(10, 10), fps=120, radius=10):
    matplotlib.use('Agg')

    title = '\n'.join(wrap(title, 20))

    def init():
        ax.set_xlim3d([-radius / 2, radius / 2])
        ax.set_ylim3d([0, radius])
        ax.set_zlim3d([-radius / 3., radius * 2 / 3.])
        fig.suptitle(title, fontsize=10)
        ax.grid(b=False)

    def plot_xzPlane(minx, maxx, miny, minz, maxz):
        verts = [
            [minx, miny, minz],
            [minx, miny, maxz],
            [maxx, miny, maxz],
            [maxx, miny, minz]
        ]
        xz_plane = Poly3DCollection([verts])
        xz_plane.set_facecolor((0.5, 0.5, 0.5, 0.5))
        ax.add_collection3d(xz_plane)

    data = joints_positions.copy().reshape(len(joints_positions), -1, 3)

    # preparation related to specific datasets
    data *= scale_factor # scale for visualization

    fig = plt.figure(figsize=figsize)
    plt.tight_layout()
    ax = p3.Axes3D(fig)
    init()
    MINS = data.min(axis=0).min(axis=0)
    MAXS = data.max(axis=0).max(axis=0)
    ax.set_xlim(MINS[0], MAXS[0])
    ax.set_ylim(MINS[1], MAXS[1])
    ax.set_zlim(MINS[2], MAXS[2])

    frame_number = data.shape[0]
    # height_offset = MINS[1]
    # data[:, :, 1] -= height_offset
    # trajec = data[:, 0, [0, 2]]
    # data[..., 0] -= data[:, 0:1, 0]
    # data[..., 2] -= data[:, 0:1, 2]

    def update(index):
        ax.lines = []
        ax.collections = []
        ax.view_init(elev=120, azim=-90)
        ax.dist = 7.5
        # plot_xzPlane(MINS[0] - trajec[index, 0], MAXS[0] - trajec[index, 0], 0, MINS[2] - trajec[index, 1],
        #             MAXS[2] - trajec[index, 1])
        for joint in range(1, len(parents)):
            ax.plot3D(data[index, [joint, parents[joint]], 0], data[index, [joint, parents[joint]], 1], data[index, [joint, parents[joint]], 2],
                      color="green", linewidth=2, linestyle='-',  marker='o')

        plt.axis('off')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])

    ani = FuncAnimation(fig, update, frames=frame_number, interval=1000 / fps, repeat=False)

    ani.save(save_path, fps=fps)
    plt.close()

