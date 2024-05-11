"""
** This test case is meant to check for the correct making
** of SVG files by the program, this will create 4 SVG files
** To check for right implementation, use "Svg Preview" extension
"""

import math
import Physics

def main():
    index = 0  # Initialize index for the filename

    # Create the table
    table = Physics.Table()

    # Calculate the position for the StillBall 
    pos_x = Physics.TABLE_WIDTH / 2.0 - math.sqrt((Physics.BALL_DIAMETER ** 2 )/ 2.0)
    pos_y = Physics.TABLE_LENGTH / 4.0 - math.sqrt((Physics.BALL_DIAMETER ** 2 )/ 2.0)
    pos = Physics.Coordinate(pos_x, pos_y)

    # Create and store the StillBall
    sb = Physics.StillBall(1, pos)

    # Calculate position, velocity, and acceleration for RollingBall
    pos_rb = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0, Physics.TABLE_LENGTH - Physics.TABLE_WIDTH / 2.0)
    vel = Physics.Coordinate(0.0, -1000.0)  # moving up along the table's center
    acc = Physics.Coordinate(0.0, 180.0)

    # Create and store the RollingBall
    rb = Physics.RollingBall(0, pos_rb, vel, acc)

    # Add the StillBall to the table
    table += sb

    # Add the RollingBall to the table
    table += rb

    # Write the initial state of the table to a file
    with open(f"table-{index}.svg", "w") as svg_file:
        svg_file.write(table.svg())

    # Simulate and write to files until no more segments
    while table is not None:
        table = table.segment()
        if table:
            index += 1
            with open(f"table-{index}.svg", "w") as svg_file:
                svg_file.write(table.svg())
        else:
            break

if __name__ == "__main__":
    main()
