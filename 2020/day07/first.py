def parse_relations(line):
    contains = line.split(" bags contain ")
    start = contains[0]
    rules = contains[1].split(",")
    edges = []
    for r in rules:
        rule = r.strip().split(" ")
        if rule[0] == "no":
            continue
        edges.append((int(rule[0]), "{} {}".format(rule[1], rule[2])))
    return (start, edges)


def parse_graph(content):
    graph = {}
    for line in content:
        start, edges = parse_relations(line.strip())
        graph[start] = edges
    return graph


def invert_graph(graph):
    inverted = {node: [] for node in graph}
    for node, edges in graph.items():
        for edge in edges:
            count, name = edge
            inverted[name].append((count, node))
    return inverted


def count_outermost(graph, start):
    ways = ways_to_hold(graph, start)
    outers = set(ways)
    return len(outers - {start})


def ways_to_hold(graph, node):
    ways = []
    for edge in graph[node]:
        count, name = edge
        ways.append(name)
        ways.extend(ways_to_hold(graph, name))
    return ways


def main():
    pathname = "input.txt"
    graph = {}
    with open(pathname) as f:
        content = f.readlines()
        graph = parse_graph(content)
    inverse_graph = invert_graph(graph)
    target = "shiny gold"
    outers = count_outermost(inverse_graph, target)
    print("The number of bags that can eventually contain a {} bag is {}".format(target, outers))

if __name__ == "__main__":
    main()
