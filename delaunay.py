from quadedge import *

def delaunay(profiling, fast=False):
    import sys
    import time
    import gc
    filename = sys.argv[-1]
    use_conflict = False
    g_ele = True
    bounding_box = []
    g_verbose = False
    g_edge = False

    if "-h" in sys.argv:
        print """usage: python delaunay.py inputfile [option]\n
        Options:
        -v      : verbose mode
        -edge   : produce .edge file
        -nele   : suppress .ele file
        -c      : use conflict list (faster)
        -nfs    : need for speed (turn off garbage collection)
        -p      : profiling (uses file ttimeu10000.node and prints profiling information)
        -mp     : prints garbage collection details

        Enjoy."""
        return

    if "-v" in sys.argv or profiling:
        g_verbose = True
    if "-nele" in sys.argv:
        g_ele = False
    if "-edge" in sys.argv:
        g_edge = True
    if "-c" in sys.argv or profiling:
        use_conflict = True
    if "-nfs" in sys.argv or fast:
        gc.disable()
    if "-p" in sys.argv and not profiling:
        import cProfile
        cProfile.run('delaunay(True, True)')
        return
    if "-mp" in sys.argv:
        gc.set_debug(gc.DEBUG_STATS)
    if profiling:
        filename = "ttimeu100000.node"


    f = open(filename, 'r')
    index = 0
    points = []
    vertices = {}
    max_x = float("-inf")
    max_y = float("-inf")
    min_x = float("inf")
    min_y = float("inf")
    if g_verbose:
        sys.stdout.write("Reading file...\n")
        sys.stdout.flush()

    for line in f:
        if index == 0:
            index = 1
            continue
        arr = line.split()
        x = float(arr[1])
        max_x = max_x if max_x > x else x
        min_x = min_x if min_x < x else x
        y = float(arr[2])
        max_y = max_y if max_y > y else y
        min_y = min_y if min_y < y else y
        vertices[(x, y)] = arr[0]
        points.append(Point((x,y)))

    l1 = Line(min_x-100, max_y+100, 1/2.0)
    l2 = Line(max_x+100, max_y+100, -1/2.0)
    l3 = Line(min_x-100, min_y-100, 0)

    p1 = Point((l1.intersection(l2), l1.slope*l1.intersection(l2) + l1.intersect))
    p2 = Point((l1.intersection(l3), min_y - 100))
    p3 = Point((l2.intersection(l3), min_y - 100))

    s = Subdivision(p1,p2,p3)
    if use_conflict:
        s.use_conflict = True
    bounding_box.append(p1)
    bounding_box.append(p2)
    bounding_box.append(p3)

    g_edges[0].edges[0].data = []
    g_edges[1].edges[0].data = []
    g_edges[2].edges[0].data = []
    if s.use_conflict:
        if g_verbose:
            sys.stdout.write("Setting up the conflict list...\n");
            sys.stdout.flush()

        for i in range(len(points)):
            points[i].conflicting_edge = g_edges[0].edges[0]
            g_edges[0].edges[0].data.append(points[i])
            g_edges[1].edges[0].data.append(points[i])
            g_edges[2].edges[0].data.append(points[i])

    numPoints = float(len(points))
    t = time.time()
    one_percent = max(min(int(numPoints/1000),1000), 1)
    if one_percent == 0:
        one_percent += 1
    for i in range(int(numPoints)):
        if g_verbose and i % one_percent == 0:
            sys.stdout.write('\r%.2f %%' % (i/numPoints*100))
            sys.stdout.flush()
        s.InsertSite(points[i])
    if g_verbose:
        sys.stdout.write('\rDone        \n')
        sys.stdout.flush()
    t2 = time.time()
    if g_verbose:
        sys.stdout.write("Inserting vertices took %.1f seconds\n" % (t2-t))
        sys.stdout.flush()
    import output
    if g_ele:
        output.output(filename, g_edges[0].edges[0], vertices, bounding_box, "ele")
        if g_verbose:
            print "Wrote to", filename[:-5] + ".ele"
    if g_edge:
        output.output(filename, g_edges, vertices, bounding_box, "edge")
        if g_verbose:
            print "Wrote to", filename[:-5] + ".edge"

if __name__ == "__main__":
    delaunay(False)
