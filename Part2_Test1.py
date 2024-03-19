"""
** This test case is meant to check for faults in the
** Python implementation of the C library, this includes
** swig, wrappers, function calls to C code, etc...
"""

import math
import Physics

def main():
    #2 -- Create the table
    table = Physics.Table()

    #3 -- Calculate the position for the StillBall 
    pos_x = Physics.TABLE_WIDTH / 2.0 - math.sqrt((Physics.BALL_DIAMETER ** 2 )/ 2.0)
    pos_y = Physics.TABLE_LENGTH / 4.0 - math.sqrt((Physics.BALL_DIAMETER ** 2 )/ 2.0)
    pos = Physics.Coordinate(pos_x, pos_y)

    # 4. Create and store the StillBall
    sb = Physics.StillBall(1, pos)

    # 5. Calculate position, velocity, and acceleration for RollingBall
    pos_rb = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0, Physics.TABLE_LENGTH - Physics.TABLE_WIDTH / 2.0)
    vel = Physics.Coordinate(0.0, -1000.0)  # moving up along the table's center
    acc = Physics.Coordinate(0.0, 180.0)

    # 6. Create and store the RollingBall
    rb = Physics.RollingBall(0, pos_rb, vel, acc)

     # 7. Add the StillBall to the table
    table += sb

    # 8. Add the RollingBall to the table
    table += rb

    # 9. Print the initial state of the table
    print(table)

    # 10. Simulate and print until no more segments
    while table is not None:
        table = table.segment()
        if table:
            print(table)
        else:
            break

if __name__ == "__main__":
    main()