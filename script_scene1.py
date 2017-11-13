#!/usr/bin/env python3.6

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from script_queries import run_queries

BUSINESS_IDS = [
    # SELECT * FROM tmp2 WHERE businessID IN(SELECT businessID FROM tmp2 GROUP BY businessId HAVING MIN(avg_stars)<3 AND MAX(avg_stars)>4);
    "LNOnYo13ggdoEGD-syYHIA",  # "YQFcxE9UXrKc-QuTUu7twQ",
    # SELECT * FROM tmp2 WHERE businessID IN (SELECT businessID FROM tmp2 GROUP BY businessId HAVING MAX(avg_stars)-MIN(avg_stars)>2);
    "3Qi7NwTpAc3Oh1-wMb546w",  # "sQV-yfhFjeRWnHw66n8qrQ",
    # SELECT * FROM tmp2 WHERE businessID IN (SELECT businessID FROM tmp2 GROUP BY businessId HAVING AVG(avg_stars)<3 AND SUM(reviewYear)=12081);
    "DPZBuTuL7w5MVxsCEyQudQ",  # "n0SSApg8pIMu9uWr7IvxcQ",
    # SELECT * FROM tmp2 WHERE businessID IN (SELECT businessID FROM tmp2 GROUP BY businessId HAVING MAX(count_stars)-MIN(count_stars)>60);
    "PycR_Mr5jA9jB4Xg3nX0Yw",  # "S1N5-ZXwR4fUIPs6dLnBYQ",
    # SELECT * FROM tmp2 WHERE businessID IN (SELECT businessID FROM tmp2 GROUP BY businessId HAVING MAX(sum_stars)-MIN(sum_stars)>400);
    "-9eNGMp8XiygI8t8QFuFWw",  # "xpocpPlEWaQygGMLSvjelQ",#"wHq1efQVz17338k_aUOX3w",
    ]
LARGENUM = 9999999999


def draw_scene_1(data):
    print("Drawing plots...")
    for i, plot in enumerate(["Test Set", "Validation Set"]):
        xs = np.arange(2010, 2018)
        fig = plt.figure(i)
        ax = fig.add_subplot(111, projection="3d")
        for color, idx in zip(["violet","y","b","g","r"], [4,3,2,1,0]):
            avg_rating, count_ratings = 0. * xs, 0 * xs
            for j, row in enumerate(data[idx]):
                if j%2==i and row[0] == BUSINESS_IDS[idx]:
                    avg_rating[row[1] - 2010] += row[2]
                    count_ratings[row[1] - 2010] += 1
            avg_rating = np.divide(avg_rating,
                [LARGENUM if k <= 10 else k for k in count_ratings])
            ax.bar(xs[:-1], avg_rating[:-1], zs=idx,
                zdir="y", color=color)
        ax.set_title(plot)
        ax.set_xlabel("year")
        ax.set_ylabel("business ID")
        ax.set_zlabel("rating")
        ax.set_xlim3d(2010, 2017)
        ax.set_zlim3d(0, 4.5)
        ax.set_yticks([])
    plt.show()


def main():
    # run DB queries
    _, result = run_queries([
        "SELECT businessID,reviewYear,stars FROM Reviews WHERE businessID='{}'"
        .format(i) for i in BUSINESS_IDS])

    # draw plots
    draw_scene_1(result)

if __name__ == "__main__":
    main()

# QUERY0 = ["DROP VIEW IF EXISTS tmp, tmp2"]
# QUERY1 = ["CREATE VIEW tmp AS SELECT l.businessID,l.reviewYear,l.stars " +
#    "FROM Reviews l WHERE l.businessID IN (SELECT r.businessID FROM "+
#    "Reviews r GROUP BY r.businessID HAVING min(r.reviewYear)<2012) " +
#    "ORDER BY l.businessID,l.reviewYear"]
# QUERY2 = ["CREATE VIEW tmp2 AS SELECT businessID,reviewYear,COUNT(stars)," +
#    "SUM(stars) FROM tmp GROUP BY businessID,reviewYear " +
#    "HAVING COUNT(stars)>20"]
# QUERY3_8 = ["SELECT businessID,reviewYear,stars FROM Reviews WHERE businessID = '{}'"
#    .format(i) for i in BUSINESS_IDS]
# QUERY0 + QUERY1 + QUERY3_8 + QUERY0
