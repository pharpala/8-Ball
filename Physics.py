import phylib
import sqlite3
import os
import math

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
FRAME_RATE = 0.01

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
    
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );

                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                      Coordinate( ball.obj.still_ball.pos.x,
                                      ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new

    def cueBall(self):
        # Find the cue ball object with number 0
        cue_ball = None
        for obj in self:
            if isinstance(obj, StillBall) and obj.obj.still_ball.number == 0:
                cue_ball = obj
                break
        return cue_ball



###########################################################################
    
class Database ():

    def __init__(self, reset=False):
        if os.path.exists( 'phylib.db' ) and reset == True:
            os.remove( 'phylib.db' )
            
        self.conn = sqlite3.connect('phylib.db')
        self.cursor = self.conn.cursor()
    
    # Method closes cursor and commits, does not close connection
    def closeCurr (self):
        self.conn.commit()
        self.cursor.close()

    def close (self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def createDB (self):
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Ball
                           (BALLID      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            BALLNO      INTEGER NOT NULL,
                            XPOS        FLOAT NOT NULL,
                            YPOS        FLOAT NOT NULL,
                            XVEL        FLOAT,
                            YVEL        FLOAT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS TTable
                           (TABLEID     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            TIME        FLOAT NOT NULL)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS BallTable
                           (BALLID               INTEGER NOT NULL,
                            TABLEID              INTEGER NOT NULL,
                            FOREIGN KEY(BALLID)  REFERENCES Ball(BALLID),
                            FOREIGN KEY(TABLEID) REFERENCES TTable(TABLEID))''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Shot
                           (SHOTID                INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            PLAYERID              INTEGER NOT NULL,
                            GAMEID                INTEGER NOT NULL,
                            FOREIGN KEY(PLAYERID) REFERENCES Player(PLAYERID),
                            FOREIGN KEY(GAMEID)   REFERENCES Game(GAMEID))''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS TableShot
                           (TABLEID              INTEGER NOT NULL,
                            SHOTID               INTEGER NOT NULL,
                            FOREIGN KEY(TABLEID) REFERENCES TTable(TABLEID),
                            FOREIGN KEY(SHOTID)  REFERENCES Shot(SHOTID))''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Game
                           (GAMEID        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            GAMENAME      INTEGER NOT NULL)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Player
                           (PLAYERID            INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            GAMEID              INTEGER NOT NULL,
                            PLAYERNAME          VARCHAR(64) NOT NULL,
                            FOREIGN KEY(GAMEID) REFERENCES Game(GAMEID))''')
        
        self.closeCurr()

    def readTable(self, tableID):
        self.cursor = self.conn.cursor()
        self.cursor.execute('''SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL
                            FROM Ball
                            JOIN BallTable ON Ball.BALLID = BallTable.BALLID
                            WHERE BallTable.TABLEID = ?''', (tableID,))
        balls_data = self.cursor.fetchall()

        if not balls_data:
            return None  # TABLEID does not exist in BallTable

        table = Table()

        for ball_data in balls_data:
            ball_id, ball_no, xpos, ypos, xvel, yvel = ball_data

            # print(f" tell me xpos and ypos {xvel} {yvel}")
            position = Coordinate(xpos, ypos)

            if xvel is None and yvel is None:
                ball = StillBall(ball_no, position)
            else:
                velocity = Coordinate(xvel, yvel)
                ball = RollingBall(ball_no, position, velocity, velocity)  # Assuming acceleration is same as velocity

            table += ball

        self.cursor.execute('''SELECT TIME FROM TTable WHERE TABLEID = ?''', (tableID,))
        time_data = self.cursor.fetchone()
        if time_data:
            table.time = time_data[0]

        self.closeCurr()
        return table
    
    def writeTable(self, table):
        # Store balls in Ball table and get their IDs
        self.cursor = self.conn.cursor()
        ball_ids = []
        for obj in table:
            if isinstance(obj, StillBall):
                xvel = None
                yvel = None
                # print(f"number is {obj.obj.still_ball.number}")
            elif isinstance(obj, RollingBall):
                xvel = obj.obj.rolling_ball.vel.x
                yvel = obj.obj.rolling_ball.vel.y
            else:
                xvel = None
                yvel = None

            if isinstance(obj, StillBall):
                self.cursor.execute('''INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                                    VALUES (?, ?, ?, ?, ?)''', (obj.obj.still_ball.number, obj.obj.still_ball.pos.x, obj.obj.still_ball.pos.y, xvel, yvel))
                ball_ids.append(self.cursor.lastrowid)
            
            if isinstance(obj, RollingBall):
                self.cursor.execute('''INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                                    VALUES (?, ?, ?, ?, ?)''', (obj.obj.rolling_ball.number, obj.obj.rolling_ball.pos.x, obj.obj.rolling_ball.pos.y, obj.obj.rolling_ball.vel.x, obj.obj.rolling_ball.vel.y))
                ball_ids.append(self.cursor.lastrowid)

        # Store table time in TTable
        self.cursor.execute('''INSERT INTO TTable (TIME) VALUES (?)''', (table.time,))
        table_id = self.cursor.lastrowid - 1  # Adjust for SQL's auto-increment behavior

        # Map balls to the table in BallTable
        for ball_id in ball_ids:
            self.cursor.execute('''INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)''', (ball_id, table_id))

        self.closeCurr()
        return table_id
    
    
    def getGame (self, gameID):
        # to account for sql start from 1 
        gameID = gameID + 1 
        game_data = Database().execute("""SELECT GameID, GameName, PlayerID, PlayerName 
                                          FROM Game, Player  
                                          JOIN Player ON Game.GameID = Player.GameID
                                          WHERE Game.GameID = ?''', (GameID)""", (gameID)).fetchone()
        
        return game_data
    
    def newShot(self, gameID, playerID):
        """
        Add a new shot to the Shot table for the given gameID and playerID.
        Returns the shotID of the newly added shot.
        """
        self.cursor = self.conn.cursor()
        self.cursor.execute('''INSERT INTO Shot (GAMEID, PLAYERID) VALUES (?, ?)''', (gameID, playerID))
        shotID = self.cursor.lastrowid
        self.conn.commit()
        return shotID


class Game ():

    def __init__ (self, gameID=None, gameName = None, player1Name = None, player2Name = None) :
        self.db = Database()
        if gameID is not None and (gameName is not None or player1Name is not None or player2Name is not None):
            raise TypeError("Invalid constructor arguments")
        elif gameID is None and (gameName is None or player1Name is None or player2Name is None):
            raise TypeError("Invalid constructor arguments")

        # Initialize member variables
        self.gameID = None
        self.gameName = None
        self.player1Name = None
        self.player2Name = None

        # If gameID is provided, retrieve game details from the database
        if gameID is not None:
            game_data = self.db.getGame(gameID)
            print(f"Game data is {game_data}")
            if game_data:
                self.gameID = game_data[0] 
                self.gameName = game_data[1]
                # Retrieve player names from the Player table based on GAMEID
                player_data = self.db.cursor.execute("SELECT PLAYERNAME FROM Player WHERE GAMEID = ?", (gameID,)).fetchall()
                if len(player_data) >= 2:
                    self.player1Name = player_data[0][0]
                    self.player2Name = player_data[1][0]

        # If gameID is None, create a new game and add it to the database
        else:
            cursor = self.db.cursor
            cursor.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))
            self.gameID = cursor.lastrowid

            cursor.execute("INSERT INTO Player (PLAYERNAME, GAMEID) VALUES (?, ?)", (player1Name, self.gameID))
            cursor.execute("INSERT INTO Player (PLAYERNAME, GAMEID) VALUES (?, ?)", (player2Name, self.gameID))

            # Assign player names directly from the provided arguments
            self.player1Name = player1Name
            self.player2Name = player2Name           

    def shoot(self, gameName, playerName, table, xvel, yvel):
        # Get the playerID from the playerName
        cursor = self.db.cursor
        player_data = cursor.execute("SELECT PLAYERID FROM Player WHERE PLAYERNAME=?", (playerName,)).fetchone()
        if player_data is None:
            raise ValueError("Player not found")

        playerID = player_data[0]

        # Add a new shot to the Shot table
        shotID = self.db.newShot(self.gameID, playerID)

        # Find the cue ball object
        cue_ball = table.cueBall()
        if cue_ball is None:
            raise ValueError("Cue ball not found")

        # Retrieve the x and y values of the cue ball's position
        xpos = cue_ball.obj.still_ball.pos.x
        ypos = cue_ball.obj.still_ball.pos.y

        # Set the type attribute of the cue ball to ROLLING_BALL
        cue_ball.type = phylib.PHYLIB_ROLLING_BALL

        # Set all attributes of the cue ball
        cue_ball.obj.rolling_ball.pos.x = xpos
        cue_ball.obj.rolling_ball.pos.y = ypos
        cue_ball.obj.rolling_ball.vel.x = xvel
        cue_ball.obj.rolling_ball.vel.y = yvel

        rollingVelX = float(xvel) 
        # print("this is rolling vel", rollingVelX)
        rollingVelY = float(yvel)
        # print("this is rolling vel", rollingVelY)

        velMag = math.sqrt((rollingVelX * rollingVelX) + (rollingVelY * rollingVelY))
        # print("this is velmag", velMag)
            
        # prevent divide by 0
        if velMag != 0:

        # as long as denominator not 0, we calculate the new velocity
            newVelX = rollingVelX/velMag
            newVelY = rollingVelY/velMag
            # print("this is new vel", newVelY)
            accX = -newVelX * DRAG
            # print(accX)
            accY = -newVelY * DRAG
            # print("this is acc of y", accY)

        cue_ball.obj.rolling_ball.acc.x = accX
        cue_ball.obj.rolling_ball.acc.y = accY
        cue_ball.obj.rolling_ball.number = 0

        
        segment_length = 0
        start_time = table.time
        
        while table:
            table = table.segment()
            if table is None:
                break
            
            end_time = table.time
            segment_length = (end_time - start_time) / FRAME_RATE
            segment_length = int(segment_length)
                
            for i in range(segment_length):
                time_passed = i * FRAME_RATE
                new_table = table.roll(time_passed)
                new_table.time = start_time + time_passed
                new_table.id = self.db.writeTable(new_table)

                shotID = self.db.newShot(self.gameID, playerID)  # Get the shot ID
                self.db.cursor.execute("INSERT INTO TableShot (SHOTID, TABLEID) VALUES (?, ?)", (shotID, new_table.id))
        
            start_time = end_time

