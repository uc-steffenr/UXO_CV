from math import floor


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


def long2UTM(long_of_location):
    return (floor((long_of_location + 180) / 6) % 60) + 1


def deg2mins(angle_deg):
    # 1° 1' 1''
    deg = int(angle_deg)
    min_deg = int((angle_deg - deg) * 60)
    s_deg = (angle_deg - deg - min_deg / 60) * 3600
    print(deg, min_deg, s_deg)
    # return deg, min_deg, round(s_deg, 2)
    s_deg = round(s_deg, 2)
    print(f"{deg} {min_deg}' {s_deg}\"")
    return f"{deg} {min_deg} {s_deg}"


deg2mins(71.354)
