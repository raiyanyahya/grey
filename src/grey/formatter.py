import ast
from sys import argv, stdin


class TopLevelAndMethodInserter(ast.NodeVisitor):
    def __init__(self):
        # Store line numbers where blank lines should be inserted
        self.line_numbers_to_insert = []

    # pylint: disable=invalid-name
    def visit_FunctionDef(self, node):
        if isinstance(node.parent, ast.Module):  # Top-level function
            self.line_numbers_to_insert.append(node.lineno - 1)  # Line before function
        elif isinstance(node.parent, ast.ClassDef):  # Method inside a class
            # Line before method, only if it's not the first element inside the class
            if node.parent.body[0] != node:
                self.line_numbers_to_insert.append(node.lineno - 1)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        if isinstance(node.parent, ast.Module):  # Top-level class
            self.line_numbers_to_insert.append(node.lineno - 1)  # Line before class
            # Line after class name, before first method or class member
            if node.body:
                self.line_numbers_to_insert.append(node.body[0].lineno - 1)
        self.generic_visit(node)

def format_code(source_code):
    tree = ast.parse(source_code)

    # Add parent references to each node
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

    inserter = TopLevelAndMethodInserter()
    inserter.visit(tree)

    # Sort and remove duplicate line numbers
    line_numbers = sorted(set(inserter.line_numbers_to_insert))

    lines = source_code.splitlines()

    # Offset to account for newly inserted lines
    offset = 0
    for lineno in line_numbers:
        index = lineno + offset
        if index < len(lines) and lines[index].strip() != '':
            lines.insert(index, '')
            offset += 1

    return '\n'.join(lines)


def main():
    # Read source code from a file or standard input
    if len(argv) > 1:
        with open(argv[1], 'r', encoding="UTF-8") as file:
            source_code = file.read()
    else:
        source_code = stdin.read()

    formatted_code = format_code(source_code)
    print(formatted_code)

if __name__ == "__main__":
    main()
