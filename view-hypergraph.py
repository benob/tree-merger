#!/usr/bin/python

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import pygraphviz, re, sys, os

tmp="/tmp/hypergraph"

def draw_graph(lines, filename):
    graph = pygraphviz.AGraph(strict=False,directed=True,rankdir='LR', rank='min')
    for line in lines:
        tokens = line.strip().split()
        if len(tokens) > 3:
            graph.add_edge(tokens[0], tokens[1], label="%s/%s" % (tokens[2], tokens[3]), fontsize=32)
        elif len(tokens) > 2:
            if tokens[2] == "-OR-":
                graph.add_edge(tokens[0], tokens[1], arrowhead='none')
                node = graph.get_node(tokens[1])
                node.attr['shape'] = 'point'
            else:
                graph.add_edge(tokens[0], tokens[1], label=tokens[2], fontsize=32)
        elif len(tokens) == 1:
            graph.add_node(tokens[0], shape='doublecircle')
            graph.get_node(tokens[0]).attr['shape'] = 'doublecircle'
    graph.layout('dot')
    graph.draw(filename)
    return filename

files = []
lines = []
for line in sys.stdin:
    if line.strip() == "":
        files.append(draw_graph(lines, "%s.%d.pdf" % (tmp, len(files))))
        lines = []
    else:
        lines.append(line)

if len(lines) > 0:
    files.append(draw_graph(lines, "%s.%d.pdf" % (tmp, len(files))))

os.system("gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=" + tmp + ".pdf " + " ".join(files))
os.system('evince %s.pdf' % tmp)
os.system(('rm %s.pdf ' % tmp) + " ".join(files))
