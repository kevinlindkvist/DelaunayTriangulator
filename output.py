def output(filename,e,vertices, bounding_box, type_f):
    output_edges = {}
    output_triangles = []
    def printtriangle(edge):
        if edge in output_edges:
            return
        v1 = edge.origin
        edge = edge.rNext()
        if edge in output_edges:
            return
        v2 = edge.origin
        edge = edge.rNext()
        if edge in output_edges:
            return
        v3 = edge.origin
        if v1 in bounding_box or v2 in bounding_box or v3 in bounding_box:
            return
        output_triangles.append(((v1.x, v1.y),(v2.x, v2.y),(v3.x, v3.y)))

    def bfs(edge):
        stack = []
        stack.append(edge)
        while len(stack):
            edge = stack.pop()
            if edge.next_edge not in output_edges:
                stack.append(edge.next_edge)
            if edge.sym().next_edge not in output_edges:
                stack.append(edge.sym().next_edge)
            printtriangle(edge)
            printtriangle(edge.sym())
            output_edges[edge] = True
            output_edges[edge.sym()] = True

    if type_f == "ele":
        bfs(e)

        o = open(filename[:-5] + ".ele", 'w')
        o.write(str(len(output_triangles)) + " 3 0\n")
        counter = 0
        for triangle in output_triangles:
            counter += 1
            o.write(str(counter) + " " + vertices[triangle[0]] \
                    + " " + vertices[triangle[1]] + " "\
                    + vertices[triangle[2]] + "\n")
        o.close()
    if type_f == "edge":
        o = open(filename[:-5] + ".edge", 'w')
        counter = 0
        l = []
        for edge in e:
            edge = edge.edges[0]
            if edge.origin in bounding_box or edge.destination in bounding_box:
                continue
            counter += 1
            l.append(str(counter) + " " + vertices[(edge.origin.x, edge.origin.y)] + " " + vertices[(edge.destination.x, edge.destination.y)] + "\n")
        o.write(str(len(l)) + " 0\n")
        for i in l:
            o.write(i)
        o.close()


