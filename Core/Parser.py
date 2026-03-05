import ast


class NormalizeCode(ast.NodeTransformer):

    def visit_Name(self, node):
        # Replace all variable names
        return ast.copy_location(
            ast.Name(id="VAR", ctx=node.ctx),
            node
        )

    def visit_arg(self, node):
        # Replace function argument names
        node.arg = "ARG"
        return node

    def visit_Constant(self, node):
        # Normalize numeric and string constants
        if isinstance(node.value, (int, float, str)):
            return ast.copy_location(
                ast.Constant(value="CONST"),
                node
            )
        return node


def extract_node_sequence(code):
    tree = ast.parse(code)

    # Apply normalization
    normalizer = NormalizeCode()
    tree = normalizer.visit(tree)
    ast.fix_missing_locations(tree)

    sequence = []

    ignore_nodes = {"Load", "Store", "Expr", "Module"}

    def dfs(node):
        node_type = type(node).__name__

        if node_type not in ignore_nodes:
            sequence.append(node_type)

        for child in ast.iter_child_nodes(node):
            dfs(child)

    dfs(tree)
    return sequence