g_edges = []
g_use_conflict = True
class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __eq__(self, other):
        counter = 0
        if self.a == other.a or self.a == other.b or self.a == other.c:
            counter += 1
        if self.b == other.a or self.b == other.b or self.b == other.c:
            counter += 1
        if self.c == other.a or self.c == other.b or self.c == other.c:
            counter += 1
        return counter == 3

class Point:
    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.conflicting_edge = None
    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
    def __lt__(self, other):
        return self.x < other.x if self.x != other.x else self.y < other.y
    def __gt__(self, other):
        return self.x > other.x if self.x != other.x else self.y > other.y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __le__(self, other):
        return self.x <= other.x if self.x != other.x else self.y <= other.y
    def __ge__(self, other):
        return self.x >= other.x if self.x!= other.x else self.y >= other.y
    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

class Edge:
    def __init__(self):
        self.num = 0
        self.next_edge = None
        self.data = []
        self.quad = None
    def __init__(self, i, quad):
        self.num = i
        self.next_edge = None
        self.data = []
        self.quad = quad

    def __repr__(self):
        return str(self.origin) + " -> " + str(self.destination)
    def __lt__(self, other):
        return self.origin < other.origin

    def rot(self):
        return self.quad.edges[(self.num + 1) % 4]
    def invRot(self):
        return self.quad.edges[(self.num - 1) % 4]
    def sym(self):
        return self.quad.edges[(self.num + 2) % 4]
    def oNext(self):
        return self.next_edge
    def oPrev(self):
        return self.quad.edges[(self.num + 1) % 4].next_edge.rot()
    def dNext(self):
        return self.sym().oNext().sym()
    def dPrev(self):
        return self.invRot().oNext().invRot()
    def lNext(self):
        return self.quad.edges[(self.num - 1) % 4].next_edge.rot()
    def lPrev(self):
        return self.oNext().sym()
    def rNext(self):
        return self.rot().oNext().invRot()
    def rPrev(self):
        return self.sym().oNext()
    def fNext(self):
        return self.sym().oPrev()

    """ Data pointers """
    def setOriginDest(self, origin, destination):
        self.origin = origin
        self.destination = destination
        self.sym().origin = destination
        self.sym().destination = origin

class QuadEdge:
    def __init__(self):
        e0 = Edge(0, self)
        e1 = Edge(1, self)
        e2 = Edge(2, self)
        e3 = Edge(3, self)

        e0.next_edge = e0
        e1.next_edge = e3
        e2.next_edge = e2
        e3.next_edge = e1
        self.edges = [e0, e1, e2, e3]

def MakeEdge():
    quad = QuadEdge()
    g_edges.append(quad)
    return quad.edges[0]

def Splice(a, b):
    t1 = b.oNext()
    t2 = a.oNext()
    alpha = t1.rot()
    beta = t2.rot()
    t3 = beta.oNext()
    t4 = alpha.oNext()

    a.next_edge = t1
    b.next_edge = t2
    alpha.next_edge = t3
    beta.next_edge = t4

def Delete(edge):
    Splice(edge, edge.oPrev())
    Splice(edge.sym(), edge.sym().oPrev())
    g_edges.remove(edge.quad)

def Connect(a, b):
    e = MakeEdge()
    Splice(e, a.lNext())
    Splice(e.sym(), b)
    e.setOriginDest(a.destination, b.origin)
    return e

def Swap(edge):
    e1 = edge.oPrev()
    e2 = edge.sym().oPrev()
    Splice(edge, e1)
    Splice(edge.sym(), e2)
    Splice(edge, e1.lNext())
    Splice(edge.sym(), e2.lNext())
    edge.setOriginDest(e1.destination, e2.destination)

def TriangleArea(a, b, c):
    return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)

def InCircle(a,b,c,d):

    return ((a.x*a.x + a.y*a.y) *((c.x - b.x)*(d.y - b.y) - (c.y - b.y)*(d.x - b.x)) -
            (b.x*b.x + b.y*b.y) *((c.x - a.x)*(d.y - a.y) - (c.y - a.y)*(d.x - a.x)) +
            (c.x*c.x + c.y*c.y) *((b.x - a.x)*(d.y - a.y) - (b.y - a.y)*(d.x - a.x)) -
            (d.x*d.x + d.y*d.y) * ((b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x))) > 0

def ccw(a, b, c):
    return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x) > 0

def RightOf(x, e):
    b = e.destination
    c = e.origin
    return (b.x - x.x)*(c.y - x.y) - (b.y - x.y)*(c.x - x.x) > 0
def LeftOf(x, e):
    b = e.origin
    c = e.destination
    return (b.x - x.x)*(c.y - x.y) - (b.y - x.y)*(c.x - x.x) > 0

def Valid(e, basel):
    return not LeftOf(e.destination, basel)

import time
class Subdivision:

    def __init__(self, a, b, c):
        point_a = a
        point_b = b
        point_c = c

        edge_a = MakeEdge()
        edge_a.setOriginDest(point_a, point_b)
        edge_b = MakeEdge()
        Splice(edge_a.sym(), edge_b)
        edge_b.setOriginDest(point_b, point_c)
        edge_c = MakeEdge()
        Splice(edge_b.sym(), edge_c)
        edge_c.setOriginDest(point_c, point_a)
        Splice(edge_c.sym(), edge_a)
        self.startingEdge = edge_a
        self.use_conflict = False

    def Locate(self,point):
        ro = RightOf
        if self.use_conflict:
            return point.conflicting_edge

        edge = self.startingEdge
        while True:
            if point == edge.origin or point == edge.destination:
                return edge
            elif ro(point, edge):
                edge = edge.sym()
            elif not ro(point, edge.oNext()):
                edge = edge.oNext()
            elif not ro(point, edge.dPrev()):
                edge = edge.dPrev()
            else:
                return edge

    def InsertSite(self, point):
        e = self.Locate(point)
        conflicting_points = e.data
        if conflicting_points == None:
            conflicting_points = []

        base = MakeEdge()
        first = e.origin
        base.setOriginDest(first, point)
        Splice(base, e)

        while True:
            base = Connect(e, base.sym())
            e = base.oPrev()
            if e.destination == first:
                break

        e = base.oPrev()
        lo = LeftOf
        ro = RightOf
        ic = InCircle
        while True:
            t = e.oPrev()
            if ro(t.destination, e) and ic(e.origin, t.destination, e.destination, point):
                ed1 = e.sym()
                ed2 = ed1.fNext()
                ed3 = ed2.fNext()
                conflicting_points.extend(ed1.data)
                conflicting_points.extend(ed2.data)
                conflicting_points.extend(ed3.data)
                Swap(e)
                e = e.oPrev()
            elif e.origin == first:
                conflict_triangles = getTriangles(base.sym())
                p_taken = []
                for triangle in conflict_triangles:
                    t = triangle[0]
                    t1 = triangle[1]
                    t2 = triangle[2]
                    b = t.origin
                    c = t.destination
                    bb = t2.origin
                    cc = t2.destination
                    for point in conflicting_points:
                        if ((b.x - point.x)*(c.y - point.y) - (b.y - point.y)*(c.x - point.x)) > 0 and ((bb.x - point.x)*(cc.y - point.y) - (bb.y - point.y)*(cc.x - point.x)) > 0:
                            t.data.append(point)
                            point.conflicting_edge = t
                return
            else:
                e = e.oNext().lPrev()

def getTriangles(e):
    triangles = []
    starting_edge = e
    while True:
        face_edges = []
        tri_edge = starting_edge

        face_edges.append(tri_edge)
        tri_edge.data = []
        tri_edge = tri_edge.fNext()
        face_edges.append(tri_edge)
        tri_edge.data = []
        tri_edge = tri_edge.fNext()
        face_edges.append(tri_edge)
        tri_edge.data = []
        tri_edge = tri_edge.fNext()

        starting_edge = starting_edge.oNext()
        triangles.append(face_edges)
        if starting_edge == e:
            return triangles
class Line:
    def __init__(self, x,y, slope):
        self.x = x
        self.y = y
        self.slope = slope
        self.intersect = self.y - self.slope*x

    def intersection(self, line):
        return (line.intersect - self.intersect)/(self.slope - line.slope)
