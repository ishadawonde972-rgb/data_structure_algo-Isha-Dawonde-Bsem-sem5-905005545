

import re
from pathlib import Path


class Stack:
    """A simple stack implemented with a Python list."""

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise ValueError("Cannot pop from an empty stack.")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise ValueError("Cannot peek at an empty stack.")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0


def tokenize(expression):
    """Convert an expression into numbers, operators, and parentheses."""
    tokens = re.findall(r"\d+(?:\.\d+)?|[()+*/-]", expression.replace(" ", ""))
    if "".join(tokens) != expression.replace(" ", ""):
        raise ValueError("Expression contains an unsupported character.")
    if not tokens:
        raise ValueError("Expression is empty.")

   
    result = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        previous = result[-1] if result else None
        unary_position = previous is None or previous in ("(", "+", "-", "*", "/")
        if token in ("+", "-") and unary_position and i + 1 < len(tokens):
            next_token = tokens[i + 1]
            if re.fullmatch(r"\d+(?:\.\d+)?", next_token):
                result.append(float(next_token) * (-1 if token == "-" else 1))
                i += 2
                continue
        result.append(float(token) if re.fullmatch(r"\d+(?:\.\d+)?", token) else token)
        i += 1
    return result


def to_postfix(tokens):
    """Use an operator stack to convert infix tokens to postfix notation."""
    output = []
    operators = Stack()
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}

    for token in tokens:
        if isinstance(token, float):
            output.append(token)
        elif token == "(":
            operators.push(token)
        elif token == ")":
            while not operators.is_empty() and operators.peek() != "(":
                output.append(operators.pop())
            if operators.is_empty():
                raise ValueError("Mismatched parentheses.")
            operators.pop()
        elif token in precedence:
            while (not operators.is_empty()
                   and operators.peek() in precedence
                   and precedence[operators.peek()] >= precedence[token]):
                output.append(operators.pop())
            operators.push(token)
        else:
            raise ValueError(f"Unsupported token: {token}")

    while not operators.is_empty():
        operator = operators.pop()
        if operator in ("(", ")"):
            raise ValueError("Mismatched parentheses.")
        output.append(operator)
    return output


def evaluate_postfix(postfix):
    """Evaluate postfix notation using a stack."""
    values = Stack()
    for token in postfix:
        if isinstance(token, float):
            values.push(token)
        else:
            if len(values.items) < 2:
                raise ValueError("Invalid expression.")
            right = values.pop()
            left = values.pop()
            if token == "+":
                answer = left + right
            elif token == "-":
                answer = left - right
            elif token == "*":
                answer = left * right
            elif token == "/":
                if right == 0:
                    raise ZeroDivisionError("Division by zero.")
                answer = left / right
            else:
                raise ValueError(f"Unsupported operator: {token}")
            values.push(answer)

    if len(values.items) != 1:
        raise ValueError("Invalid expression.")
    return values.pop()


def evaluate_expression(expression):
    """Parse and evaluate one mathematical expression."""
    return evaluate_postfix(to_postfix(tokenize(expression)))


def format_result(value):
    """Avoid unnecessary .0 in whole-number results."""
    if abs(value - round(value)) < 1e-10:
        return str(int(round(value)))
    return f"{value:.10g}"


def process_file(input_file="input.txt", output_file="output.txt"):
    """Evaluate expressions separated by lines containing only hyphens."""
    input_path = Path(input_file)
    output_path = Path(output_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    raw_text = input_path.read_text(encoding="utf-8")
    chunks = re.split(r"(?m)^\s*-{3,}\s*$", raw_text.strip())
    output_chunks = []

    for chunk in chunks:
        expressions = [line.strip() for line in chunk.splitlines() if line.strip()]
        if not expressions:
            continue
        # Each section is expected to contain one expression.
        expression = " ".join(expressions)
        try:
            result = format_result(evaluate_expression(expression))
            output_chunks.append(result)
        except Exception as error:
            output_chunks.append(f"ERROR: {error}")

    output_path.write_text("\n-----\n".join(output_chunks) + "\n", encoding="utf-8")
    print(f"Processed {len(output_chunks)} expression(s). Results saved to {output_path}.")


if __name__ == "__main__":
    process_file()
