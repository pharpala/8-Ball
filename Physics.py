import phylib

################################################################################
# import constants from phylib to global variables
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS =phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH =phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH =phylib.PHYLIB_TABLE_WIDTH
SIM_RATE =phylib.PHYLIB_SIM_RATE
VEL_EPSILON =phylib.PHYLIB_VEL_EPSILON
DRAG =phylib.PHYLIB_DRAG
MAX_TIME =phylib.PHYLIB_MAX_TIME
MAX_OBJECTS =phylib.PHYLIB_MAX_OBJECTS

# add more here
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    def svg (self):
        return f'<circle cx="{self.obj.still_ball.pos.x}" cy="{self.obj.still_ball.pos.y}" r="{BALL_RADIUS}" fill="{BALL_COLOURS[self.obj.still_ball.number]}" />\n'


class RollingBall( phylib.phylib_object ):

    def __init__( self, number, pos, vel, acc):

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 )
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall


    # add an svg method here
    def svg (self):
        return f'<circle cx="{self.obj.rolling_ball.pos.x}" cy="{self.obj.rolling_ball.pos.y}" r="{BALL_RADIUS}" fill="{BALL_COLOURS[self.obj.rolling_ball.number]}" />\n'

class Hole( phylib.phylib_object ):

    def __init__( self, pos):

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0 )
      
        # this converts the phylib_object into a Hole class
        self.__class__ = Hole


    # add an svg method here
    def svg (self):
        return f'<circle cx="{self.obj.hole.pos.x}" cy="{self.obj.hole.pos.y}" r="{BALL_RADIUS}" fill="black" />\n'



class HCushion( phylib.phylib_object ):

    def __init__( self, y):

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y )
      
        # this converts the phylib_object into a HCushion class
        self.__class__ = HCushion
        

    # add an svg method here
    def svg (self):
        if self.obj.hcushion.y == 0:
            y_val = -25
        else: 
            y_val = 2700

        return (""" <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" %y_val )

        

class VCushion( phylib.phylib_object ):

    def __init__( self, x):

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       None, None, None, 
                                       x, 0.0 )
      
        # this converts the phylib_object into a VCushion class
        self.__class__ = VCushion


    # add an svg method here
    def svg (self):
        if self.obj.vcushion.x == 0:
            x_val = -25
        else: 
            x_val = 1350
        return f'<rect width="25" height="2750" x="{x_val}" y="-25" fill="darkgreen" />\n'
    



################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self):
        svg_elements = []

        for obj in self:
            if obj is not None:
                svg_elements.append(obj.svg())

        return HEADER +"\n" + "".join(svg_elements) + FOOTER



