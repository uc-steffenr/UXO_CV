def pretty_print(matrix, name):
    print(f"\n{name} = \n")
    print(
        "\n".join(["\t".join([str(round(cell, 3)) for cell in row]) for row in matrix])
    )
    print("\n")


def pretty_print_symbollic(matrix, name):
    print(f"\n{name} = \n")
    print("\n".join(["\t".join([str(cell) for cell in row]) for row in matrix]))
    print("\n")
