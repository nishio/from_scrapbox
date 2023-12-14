def get_indentation(line):
    """Helper function to determine the indentation level of a line."""
    return len(line) - len(line.lstrip())


def get_block(lines, line_index):
    """Extracts the block of code starting from the line at `line_index`."""
    if line_index >= len(lines):
        return []  # Invalid line index

    block = []
    base_indent = get_indentation(lines[line_index])

    for line in lines[line_index:]:
        current_indent = get_indentation(line)
        if line.strip() == "" or current_indent < base_indent:
            break  # End of the block
        block.append(line)

    return block


# Example usage
lines = [
    "def example_function():",
    "    print('Hello, world!')",
    "    if True:",
    "        return 'Inside if'",
    "    print('End of function')",
    "print('Outside function')",
]

block = get_block(lines, 1)
print("\n".join(block))
