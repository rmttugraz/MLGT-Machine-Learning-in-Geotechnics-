# -*- coding: utf-8 -*-
'''
This script generates the logo of the MLGT (Machine Learning in Geotechnics)
research group of the Graz Univeristy of Technology. Current members of MLGT
are the "Institute of Rock Mechanics and Tunnelling"
and the "Institute of Soil Mechanics, Foundation Engineering and Computational
Geotechnics"
- https://www.tugraz.at/institute/fmt/home/
- https://www.tugraz.at/en/institutes/ibg/home/

For further information contact Georg H. Erharter MSc (erharter@tugraz.at)
'''

import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import matplotlib.tri as tri
import numpy as np


class coordinates():

    def __init__(self):
        pass

    def x_y(self, r, angle):
        # function computes cartesian coordinates of points on a circle based
        # on the angle and radius
        x = np.sin(np.radians(angle)) * r
        y = np.cos(np.radians(angle)) * r
        return x, y

    def compute_circle(self):
        # function computes the position of the circle in the upper right
        # corner of the MLGT logo
        r = 2  # radius of circle
        shift = 4  # distance to center of plot

        circle_xs = []
        circle_ys = []

        for i in np.arange(370, step=45):
            x, y = self.x_y(r, i)
            circle_xs.append(x)
            circle_ys.append(y)

        circle_xs = np.array(circle_xs) + shift
        circle_ys = np.array(circle_ys) + shift

        return circle_xs, circle_ys

    def random_points(self):
        # function generates random points outside of the circle
        num = 13  # total number of random points
        spread = 3  # controlls scattering of random points
        rand_xs = np.array([np.random.randn() for i in range(num)]) * spread
        rand_ys = np.array([np.random.randn() for i in range(num)]) * spread
        # delete unwanted points within circle
        indices = np.where(np.logical_or(rand_ys > 6, rand_ys < -4.5))[0]
        rand_xs = np.delete(rand_xs, indices)
        rand_ys = np.delete(rand_ys, indices)

        return rand_xs, rand_ys

    def all_points(self):
        # concatenate the x- & y- points of the circle and the random points
        circle_xs, circle_ys = self.compute_circle()
        rand_xs, rand_ys = self.random_points()
        xs = np.concatenate((circle_xs, rand_xs))
        ys = np.concatenate((circle_ys, rand_ys))
        return xs, ys


class plotter():

    def __init__(self):
        pass

    def plot(self, all_xs, all_ys, circle_xs, circle_ys, mode='subtitle'):
        # function creates the final plot of the MLGT Logo
        fig, ax = plt.subplots(figsize=(10, 10))

        linewidth = 6
        c = 0.65
        c = np.full(3, c)

        triang = tri.Triangulation(all_xs, all_ys)
        mask = np.zeros(len(triang.neighbors))

        # mask off unwanted triangles
        for i in np.flip(np.arange(-6, 0)):
            mask[i] = 1
        triang.set_mask(mask)

        # plot grid
        ax.triplot(triang, 'bo-', color=c, linewidth=linewidth)
        ax.plot(circle_xs, circle_ys, color=c, zorder=6,
                linewidth=linewidth)

        # scatter points in front of grid
        ax.scatter(all_xs, all_ys, color='black', linewidth=0.5,
                   edgecolor=c, s=150, zorder=7)

        # write MLGT text
        text = ax.text(-7, -1.2, 'MLGT', zorder=9,
                       horizontalalignment='left',
                       verticalalignment='center',
                       fontdict=dict(fontsize=150, fontname='Consolas',
                                     fontweight='normal'))
        text.set_path_effects([path_effects.Stroke(linewidth=7,
                                                   foreground='white'),
                               path_effects.Normal()])
        if mode == 'subtitle':
            text = ax.text(-7, -3.2, 'Machine Learning in Geotechnics',
                           zorder=9,
                           horizontalalignment='left',
                           verticalalignment='center',
                           fontdict=dict(fontsize=25, fontname='Consolas',
                                         fontweight='bold'))
            text.set_path_effects([path_effects.Stroke(linewidth=6,
                                                       foreground='white'),
                                   path_effects.Normal()])

        # set limits of plot
        dim = 10
        ax.set_aspect('equal')
        ax.set_xlim(left=-dim, right=dim)
        ax.set_ylim(top=8, bottom=-8)
        ax.set_axis_off()


if __name__ == '__main__':
    # instantiate classes
    coords = coordinates()
    pltr = plotter()

    # fix random seed for reproducibility
    np.random.seed(2)

    # all:
    all_xs, all_ys = coords.all_points()
    circle_xs, circle_ys = coords.compute_circle()

    # plot logo
    pltr.plot(all_xs, all_ys, circle_xs, circle_ys, mode='subtitle')

    # save logo
    #plt.savefig('MLGT_logo.jpg', dpi=1200, bbox_inches='tight', pad_inches=0)
