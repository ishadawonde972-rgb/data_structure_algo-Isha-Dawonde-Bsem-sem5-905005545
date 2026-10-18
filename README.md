
- `stack_evaluator.py`: Python source code.
- `input.txt`: sample expressions; sections are separated by a line containing hyphens.
- `output.txt`: expected output for the supplied sample.
- `Assignment_Report.docx`: report template/content for the assignment.

.

## How to run
1. Place `stack_evaluator.py` and `input.txt` in the same folder.
2. Open a terminal in that folder.
3. Run: `python stack_evaluator.py`
4. Read the results in `output.txt`.

## Supported syntax and assumptions
- Supported binary operators: `+`, `-`, `*`, `/`.
- Parentheses are supported.
- Multiplication and division have higher precedence than addition and subtraction.
- Operators of equal precedence are evaluated from left to right.
- Decimal numbers and unary signs directly before numbers are supported.
- Each expression is placed in its own section. Sections are separated by a line containing at least three hyphens.
- Exponentiation (`**`) is not supported because it is not listed among the required operators in the assignment brief.
- Invalid expressions and division by zero are reported as `ERROR: ...` in the output.

## Example
Input:
```text
3 + 5 * 2
-----
(8 / 4) + 7 * 2
-----
10 - (2 + 3) * 4
```

Output:
```text
13
-----
16
-----
-10
```

