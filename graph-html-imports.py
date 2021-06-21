from html.parser import HTMLParser
from os import name
from pathlib import Path
from graphviz import Digraph
import argparse
import glob


class Node:
    all_edges = set()

    def __init__(self, filepath) -> None:
        self.filepath = Path(filepath).resolve()
        self.children = []
        dot.node(str(self.filepath), self.filepath.name)

    def add(self, dependency):
        full_path = (self.filepath.parent.resolve() / dependency).resolve()
        if str(full_path) not in excluded_files:
            child_node = Node(full_path)
            self.children.append(child_node)
            edge = (str(self.filepath), str(child_node.filepath))
            if edge not in self.all_edges:
                dot.edge(edge[0], edge[1])
                self.all_edges.add(edge)

    def parse(self):
        try:
            with open(self.filepath, 'r') as f:
                content = f.read()
        except:
            ipdb.set_trace()
        parser = MyParser()
        parser.currentNode = self
        parser.feed(content)
        for child in self.children:
            child.parse()


class MyParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and attrs.get('rel') == 'import':
            self.currentNode.add(attrs.get('href').strip())


def main():
    parser = argparse.ArgumentParser(
        description='Render the dependency graph of html imports')
    parser.add_argument('entry')
    parser.add_argument('-o', '--out', default='.')
    parser.add_argument(
        '-f', '--format', choices=['svg', 'png', 'gv', 'dot'], default='png')
    parser.add_argument('-e', '--exclude')
    args = parser.parse_args()
    global excluded_files
    excluded_files = glob.glob(
        args.exclude, recursive=True) if args.exclude else []
    global dot
    dot = Digraph(name=Path(args.entry).stem)
    root = Node(args.entry)
    root.parse()
    out = Path(args.entry).parent if not args.out else Path(args.out)
    kwargs = {'directory': out} if out.is_dir() else {'filename': out}
    dot.render(cleanup=True, format=args.format, **kwargs)


if __name__ == '__main__':
    main()
