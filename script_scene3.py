#!/usr/bin/env python3.5
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from script_queries import run_queries

def draw_scene_3(data):
    print("Drawing plots...")
    for i, plot in enumerate([["Test Set", None], ["Validation Set", "g"]]):
        data_plot = np.array([r for k, r in enumerate(data[0]) if k%2==i])

        fig = plt.figure(i)
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(data_plot[:,0], data_plot[:,1], zs=range(len(data_plot)),
            zdir="y", color=plot[1])
        ax.set_title(plot[0])
        ax.set_xlabel("review length")
        ax.set_ylabel("review index")
        ax.set_zlabel("likes")
        ax.set_xlim3d(0, 5000)
        ax.set_ylim3d(0, len(data_plot))
        ax.set_zlim3d(0, 200)
        ax.set_yticks([])
    plt.show()

def main():
    # run DB queries
    _, result = run_queries(["SELECT CHAR_LENGTH(reviewText) l, "
        "useful+funny+cool FROM Reviews GROUP BY l"])

    # draw plots
    draw_scene_3(result)

if __name__ == "__main__":
    main()

