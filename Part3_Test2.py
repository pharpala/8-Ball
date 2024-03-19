"""
/* This test case is meant to visualize the balls colliding                                    */
/* This program will create 10 svg files, each simbolyzing a collision / stop in the table     */
/* Use "Svg preview" in VS Code extensions to visualize the svg without needing to run         */
"""

import Physics;

def write_svg( table_id, table ):
    with open( "table%02d.svg" % table_id, "w" ) as fp:
        fp.write( table.svg() );

db = Physics.Database();

table_id = 0;
table = db.readTable( table_id );

write_svg( table_id, table );

while table:
    table_id += 1;
    table = db.readTable( table_id );
    if not table:
        break;
    write_svg( table_id, table );

db.close();