

import matplotlib.pyplot as plt
import numpy as np
import space, draw

class AngleDistribution(object):

    def __init__(self, dir, lines, angleWidth):
        # 0.01 approx 6 degrees
        self.dirs = map(draw.Line.getGradient, lines)
        self.angles = np.array(list(map(space.angle, self.dirs))) - space.angle(dir)

        self.angleWidth = angleWidth
        self.numAngles = int(2 * np.pi / angleWidth)

        self.n, self.bin, self.patches = [], [], []

    def getTotal(self):
        return sum(self.n)

    def draw(self):
        plt.ion()
        plt.clf()
        # plt.plot(self.wells * 180 / np.pi, self.angleDist)
        self.n, self.bins, self.patches = plt.hist(self.angles, self.numAngles, facecolor='blue', alpha=0.5)
        plt.title("Angle distribution")
        plt.xlabel("Angle [radians]")
        plt.ylabel("Count")
        plt.show(block=False)



class TimeHandler(object):

    def __init__(self, start, end, *args):
        self.start = start
        self.end = end
        self.intermediate = args

        self.diffs = None
        self.avg_diffs = None

    def total_elapsed(self):
        return self.end - self.start

    def calculate_time_differences(self):
        self.diffs = [[self.intermediate[i+1][j] - self.intermediate[i][j]
            for j in range(len(self.intermediate[i]))]
            for i in range(len(self.intermediate) - 1)]

        self.avg_diffs = [sum(self.diffs[i]) / len(self.diffs[i]) for i in range(len(self.diffs))]

    def print_time_diffs(self):
        if self.diffs is not None:
            for i in range(len(self.avg_diffs)):
                print("Process #%i: %f s" % (i, self.avg_diffs[i]))
        else:
            self.calculate_time_differences()
            self.print_time_diffs()
