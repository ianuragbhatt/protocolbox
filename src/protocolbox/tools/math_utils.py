"""pb_safe_math — Secure mathematical expression evaluator (no eval)."""

import ast
import math
import operator
from typing import Union

from protocolbox.server import mcp

# Allowed binary operators.
_BINARY_OPS: dict[type, object] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

# Allowed unary operators.
_UNARY_OPS: dict[type, object] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed math functions (name → callable).
_MATH_FUNCS: dict[str, object] = {
    "sqrt": math.sqrt,
    "floor": math.floor,
    "ceil": math.ceil,
    "abs": abs,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
}

# Type alias for numeric results.
Numeric = Union[int, float]


def _safe_eval(node: ast.AST) -> Numeric:
    """Recursively evaluate an AST node using only allowed operations.

    Args:
        node: An AST node from a parsed math expression.

    Returns:
        The numeric result of the expression.

    Raises:
        ValueError: If the expression contains disallowed operations.
    """
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.UnaryOp):
        op_func = _UNARY_OPS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return op_func(_safe_eval(node.operand))  # type: ignore[operator]

    if isinstance(node, ast.BinOp):
        op_func = _BINARY_OPS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return op_func(left, right)  # type: ignore[operator]

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed.")
        func_name = node.func.id
        func = _MATH_FUNCS.get(func_name)
        if func is None:
            raise ValueError(
                f"Unknown function: {func_name}. "
                f"Allowed: {', '.join(sorted(_MATH_FUNCS))}."
            )
        args = [_safe_eval(arg) for arg in node.args]
        return func(*args)  # type: ignore[operator]

    raise ValueError(
        f"Unsupported expression type: {type(node).__name__}. "
        "Only numbers, basic operators, and math functions are allowed."
    )


@mcp.tool()
def safe_math(expression: str) -> str:
    """Safely evaluate a mathematical expression without using eval().

    Supports basic arithmetic (+, -, *, /, **, %) and math functions
    (sqrt, floor, ceil, abs, sin, cos, tan, log).

    Args:
        expression: A string containing a math expression, e.g. "sqrt(16) + 2**3".

    Returns:
        The result as a string, or an error message if evaluation fails.
    """
    try:
        tree = ast.parse(expression.strip(), mode="eval")
        result = _safe_eval(tree)
        return str(result)
    except (ValueError, TypeError, SyntaxError, ZeroDivisionError) as e:
        return f"Error: Could not evaluate '{expression}'. {e}"
