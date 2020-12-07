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


def count_inners(graph, target):
    total = 0
    for edge in graph[target]:
        count, name = edge
        total += count * (count_inners(graph, name) + 1)
    return total


def main():
    pathname = "input.txt"
    graph = {}
    with open(pathname) as f:
        content = f.readlines()
        graph = parse_graph(content)
        target = "shiny gold"
        inners = count_inners(graph, target)
        print("The number of bags in a {} bag is {}".format(target, inners))

if __name__ == "__main__":
    main()
