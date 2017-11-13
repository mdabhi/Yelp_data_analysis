#!/usr/bin/env python3.6

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from script_queries import run_queries

def draw_scene_2(data):
    print("Drawing plots...")
    for i, plot in enumerate([["Test Set", None], ["Validation Set", "g"]]):
        data_plot = []
        for idx, j in enumerate(data[0]):
            if idx%2 == i:
                coords = [0, j[1]]
                for k in [l for l in j[-7:] if l]:
                    start, end = [int(l) for l in k.split("-")]
                    coords[0] += end - start + (0 if end > start else 24)
                data_plot.append(coords)
        data_plot = np.array(data_plot)

        fig = plt.figure(i)
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(data_plot[:,0], data_plot[:,1], zs=range(len(data_plot)),
            zdir="y", s=100, color=plot[1])
        ax.set_title(plot[0])
        ax.set_xlabel("total hours")
        ax.set_ylabel("businesses")
        ax.set_zlabel("rating")
        ax.set_xlim3d(0, 200)
        ax.set_ylim3d(0, len(data_plot))
        ax.set_zlim3d(1.5, 5)
        ax.set_yticks([])
    plt.show()

def main():
    # run DB queries
    _, result = run_queries(["SELECT businessID,stars,{} FROM Businesses"
        .format(",".join(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]))])

    # draw plots
    draw_scene_2(result)

if __name__ == "__main__":
    main()

