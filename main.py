import matplotlib.pyplot as plt
import numpy as np
from random import uniform
from matplotlib.widgets import Slider
from copy import deepcopy

class Vertex():
    def __init__(self, x, y, z):
        self.update(x, y, z)

    def update(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def copy(self):
        return Vertex(self.x, self.y, self.z)

    def get(self):
        return (self.x, self.y, self.z)

class Edge():
    def __init__(self, vertex1, vertex2):
        self.vertex1 = vertex1
        self.vertex2 = vertex2

    def get(self):
        return self.vertex1, self.vertex2

class Plane():
    def __init__(self):
        self.vertexes: list[Vertex] = []
        while True:
            self.vertexes.clear()
            self.create_random_vertex(1, 1, None)
            self.create_random_vertex(None, 1, 1)
            self.create_random_vertex(-1, None, 1)
            self.calculate_plane_equation()
            if 0 in [self.A, self.B, self.C]: continue
            self.vertexes.append(self.calculate_vertex(-1, -1, None))
            self.vertexes.append(self.calculate_vertex(1, -1, None))
            if -3/4 <= self.vertexes[3].z <= 3/4 and -3/4 <= self.vertexes[4].z <= 3/4: break
        self.edges: list[Edge] = []
        for ID, V1 in enumerate(self.vertexes):
            self.edges.append(Edge(V1, self.vertexes[ID+1] if ID < 4 else self.vertexes[0]))

    def create_random_vertex(self, x, y, z):
        random_coordinate = uniform(-3/4, 3/4)
        if x is None: x = random_coordinate
        if y is None: y = random_coordinate
        if z is None: z = random_coordinate
        self.vertexes.append(Vertex(x, y, z))

    def calculate_plane_equation(self):
        x1, y1, z1 = self.vertexes[0].get()
        x2, y2, z2 = self.vertexes[1].get()
        x3, y3, z3 = self.vertexes[2].get()
        abx = x2 - x1
        aby = y2 - y1
        abz = z2 - z1
        acx = x3 - x1
        acy = y3 - y1
        acz = z3 - z1
        self.A = aby * acz - abz * acy
        self.B = abz * acx - abx * acz
        self.C = abx * acy - aby * acx
        self.D = -(self.A*x1+self.B*y1+self.C*z1)

    def calculate_vertex(self, x, y, z):
        x0 = x
        y0 = y
        z0 = z
        if x is None: x0 = -(self.D+self.C*z0+self.B*y0)/self.A
        if y is None: y0 = -(self.D+self.C*z0+self.A*x0)/self.B
        if z is None: z0 = -(self.D+self.B*y0+self.A*x0)/self.C
        return Vertex(x0, y0, z0)

    def get_edges(self):
        return [edge.get() for edge in self.edges]

class Cube():
    def __init__(self):
        self.frame = MAIN_FIG.add_subplot([0,0.3,1,0.7])
        self.frame.set_facecolor("black")
        self.angles = [45, 45, 90]
        self.plane_original = Plane()
        self.plane = deepcopy(self.plane_original)
        self.vertexes_original: list[Vertex] = np.array([
            Vertex(1, 1, 1),
            Vertex(1, -1, 1),
            Vertex(-1, -1, 1),
            Vertex(-1, 1, 1),
            Vertex(1, 1, -1),
            Vertex(1, -1, -1),
            Vertex(-1, -1, -1),
            Vertex(-1, 1, -1)])
        self.vertexes: list[Vertex] = deepcopy(self.vertexes_original)
        self.edges: list[Edge] = np.array([
            Edge(self.vertexes[0], self.vertexes[1]),
            Edge(self.vertexes[1], self.vertexes[2]),
            Edge(self.vertexes[2], self.vertexes[3]),
            Edge(self.vertexes[3], self.vertexes[0]),
            Edge(self.vertexes[4], self.vertexes[5]),
            Edge(self.vertexes[5], self.vertexes[6]),
            Edge(self.vertexes[6], self.vertexes[7]),
            Edge(self.vertexes[7], self.vertexes[4]),
            Edge(self.vertexes[0], self.vertexes[4]),
            Edge(self.vertexes[1], self.vertexes[5]),
            Edge(self.vertexes[2], self.vertexes[6]),
            Edge(self.vertexes[3], self.vertexes[7])])
        self.rotate()
        self.draw()

    def get_edges(self):
        return [edge.get() for edge in self.edges]
    
    def get_vertexes(self):
        return [vertex.get() for vertex in self.vertexes]

    def rotate_vertex(self, vertex, axis, angle=45):
        radian_angle = angle * np.pi / 180
        vertex = np.array(vertex.get())
        S = np.sin(radian_angle)
        C = np.cos(radian_angle)
        if axis == 0: mat = np.array([[1, 0, 0], [0, C, S], [0, -S, C]])
        if axis == 1: mat = np.array([[C, 0, S], [0, 1, 0], [-S, 0, C]])
        if axis == 2: mat = np.array([[C, S, 0], [-S, C, 0], [0, 0, 1]])
        return vertex.dot(mat)

    def rotate(self):
        for ID in range(len(self.vertexes)):
            self.vertexes[ID].update(*self.vertexes_original[ID].get())
            for axis, angle in enumerate(self.angles):
                self.vertexes[ID].update(*self.rotate_vertex(self.vertexes[ID], axis, angle))
        for ID in range(len(self.plane.vertexes)):
            self.plane.vertexes[ID].update(*self.plane_original.vertexes[ID].get())
            for axis, angle in enumerate(self.angles):
                self.plane.vertexes[ID].update(*self.rotate_vertex(self.plane.vertexes[ID], axis, angle))

    def change_angle(self, axis, val):
        self.angles[axis] = val
        self.rotate()
        self.draw()

    def draw(self):
        self.frame.cla()
        self.frame.set_xlim([-2,2])
        self.frame.set_ylim([-2,2])
        minZ = min([vertex.z for vertex in self.vertexes])
        for edge in self.get_edges():
            v1, v2 = edge
            Xs, Ys, Zs = zip(v1.get(), v2.get())
            if minZ not in Zs:
                self.frame.plot(Xs, Ys, "w")
                continue
            self.frame.plot(Xs, Ys, "w--")
        minZ = min([vertex.z for vertex in self.plane.vertexes])
        for edge in self.plane.get_edges():
            v1, v2 = edge
            Xs, Ys, Zs = zip(v1.get(), v2.get())
            if minZ not in Zs:
                self.frame.plot(Xs, Ys, "w")
                continue
            self.frame.plot(Xs, Ys, "w--")
        self.frame.fill(*list(zip(*(i.get()for i in self.plane.vertexes)))[:2], facecolor='#ff005a')

MAIN_FIG = plt.figure("CUBE", figsize=(6,7))
CB = Cube()
MAIN_FIG.set_facecolor("black")
MAIN_FIG.show()

Axes1 = MAIN_FIG.add_axes([0.2,0.10,0.5,0.04])
Axes2 = MAIN_FIG.add_axes([0.2,0.15,0.5,0.04])
Axes3 = MAIN_FIG.add_axes([0.2,0.20,0.5,0.04])
Slider1 = Slider(Axes1, "X", valmin=0, valmax=360, valinit=45, color="#ff005a")
Slider2 = Slider(Axes2, "Y", valmin=0, valmax=360, valinit=45, color="#ff005a")
Slider3 = Slider(Axes3, "Z", valmin=0, valmax=360, valinit=90, color="#ff005a")

Slider1.on_changed(lambda val: CB.change_angle(0, val))
Slider2.on_changed(lambda val: CB.change_angle(1, val))
Slider3.on_changed(lambda val: CB.change_angle(2, val))

plt.show()

# Made by SuperStas0 and DinoSlavik