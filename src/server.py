import sys; # used to get argv
import cgi; # used to parse Mutlipart FormData 
            # this should be replace with multipart in the future
import os
import math
import Physics
import glob
import json

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler;

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl;


# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):
    table = None
    svg_list = []
    player1Name = None
    player2Name = None
    gameName = None
    game= None
    turn = 1

    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        # check if the web-pages matches the list
        if parsed.path in [ '/index.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path );
            content = fp.read();

            is_empty = True
            # MyHandler.table = Physics.Table()
            for obj in MyHandler.table:
                if obj.__class__ == Physics.RollingBall or obj.__class__ == Physics.StillBall:
                    is_empty = False
                    break

            if is_empty:
                MyHandler.table.addBalls(MyHandler.table)
                print("I reached add balls safely\n")


            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();

        elif parsed.path in [ '/shoot.html' ]:
            
            fp = open( '.'+self.path );
            content = fp.read();

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.end_headers();
            with open('shoot.html', 'rb') as f:
                self.wfile.write(f.read())

        elif parsed.path in [ '/script.js' ]:
            
            fp = open( '.'+self.path );
            content = fp.read();

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.end_headers();
            with open('script.js', 'rb') as f:
                self.wfile.write(f.read())
            # send it to the browser
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();
        # check if the web-pages matches the list
        else:
            if os.path.exists and parsed.path.endswith(".svg"):
                fp = open( '.'+self.path );
                content = fp.read();

                # generate the headers
                self.send_response( 200 ); # OK
                self.send_header( "Content-type", "image/svg+xml" );
                self.send_header( "Content-length", len( content ) );
                self.end_headers();

                # send it to the broswer
                self.wfile.write( bytes( content, "utf-8" ) );
                fp.close();

            else:
                # generate 404 for GET requests that aren't the 3 files above
                self.send_response( 404 );
                self.end_headers();
                self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


    def do_POST(self):
        # handle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        if parsed.path in [ '/display.html' ]:

            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                   );
                                

            # open file for binary write
            data = {}
            # iterate over all form fields
            for field in form.keys():
                if field != 'Shoot!':  # ignoring the submit button
                    field_item = form[field]
                    data[field_item.name] = field_item.value

            # Access the values of finalX and finalY
            MyHandler.gameName = data['game_name']
            MyHandler.player1Name = data['player1_name']
            MyHandler.player2Name = data['player2_name']

            is_empty = True
            MyHandler.table = Physics.Table()
            for obj in MyHandler.table:
                if obj.__class__ == Physics.RollingBall or obj.__class__ == Physics.StillBall:
                    is_empty = False
                    break

            if is_empty:
                MyHandler.table.addBalls(MyHandler.table)
            # while MyHandler.table:
            #    table = MyHandler.table.segment();

            MyHandler.game = Physics.Game(None, MyHandler.gameName, MyHandler.player1Name, MyHandler.player2Name)
            # MyHandler.table, svg_list,highs,lows = game.shoot(gameName, player1, MyHandler.table, finalX, finalY)
            print("I reached shoot safely\n")

            html_response = generate_html_response(MyHandler.table, MyHandler.gameName, MyHandler.player1Name, MyHandler.player2Name)

            self.send_response(200)
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( html_response ) );
            self.end_headers();
            self.wfile.write(html_response.encode());

        elif parsed.path in [ '/game.html' ]:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            json_data = json.loads(post_data.decode('utf-8'))

            finalX = json_data['finalX']
            finalY = json_data['finalY']

            finalX = finalX * -1
            finalY = finalY * -1
            print(finalX)
            print(finalY)

            MyHandler.table, svg_list, highs, lows, game_end = MyHandler.game.shoot(MyHandler.gameName, MyHandler.player1Name, MyHandler.table, finalX, finalY)
            # svg_list_json = json.dumps(svg_list)
            html_response, MyHandler.turn = generate_html_response_new(MyHandler.table, svg_list, MyHandler.gameName, MyHandler.player1Name, MyHandler.player2Name, highs, lows, game_end, MyHandler.turn)

                
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(html_response))
            self.end_headers()
            self.wfile.write(html_response.encode())
            

def delete_svg():
        for svg_file in glob.glob('table-*.svg'):
            os.remove(svg_file)


def generate_html_response(table, gameName, player1Name, player2Name):
    print("entered generate html response")

    html_response = """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Pool Table Shot</title>
                    
                    <style>
                    h1, .title, .player-names {
                        text-align: center;
                        font-family: 'Comic Sans MS', cursive, sans-serif; /* Use a cartoony font */
                        color: black; /* Set a vibrant color */
                        font-size: 1.5em; /* Increase font size */
                        font-weight: bold; /* Make the text bold */
                        text-transform: uppercase; /* Convert text to uppercase */
                        letter-spacing: 2px; /* Add some letter spacing */
                        margin-bottom: 15px; /* Increase bottom margin for more separation */
                    }

                    svg {
                        /* Adjust height and width as needed */
                        height: 580px;
                        width: 300px;
                        border-radius: 10px;
                        display: inline-block;
                        text-align: center;
                    }

                    .container {
                        display: flex;
                        justify-content: center; /* Center horizontally */
                        align-items: center; /* Center vertically */
                        margin-top: 20px; /* Add some spacing above the container */
                    }

                    .container img {
                        max-width: 100%; /* Ensure the image doesn't exceed the container width */
                        max-height: 100%; /* Ensure the image doesn't exceed the container height */
                    }

                    body {
                        background-color: rgb(140, 179, 138);
                    }

                    .line {
                        stroke: black;
                        stroke-width: 10;
                        pointer-events: none; /* To ensure the line doesn't interfere with mouse events */
                    }

                    .cueContainer {
                        position: relative;
                        width: 500px;
                        height: 500px;
                        background-color: #f0f0f0;
                        margin: 50px auto;
                    }

                    #player1Name {
                        font-weight: bold;
                        color: red;
                    }

                </style>

                    </head>
                    <body>
                        """
                        # html_response += f'<div class="current-player">Current Player: {current_player}</div>'
 
    html_response += f'<div class="player-names" id="player1Name">Player 1: {player1Name}</div>'
    html_response += f'<div class="player-names">Player 2: {player2Name}</div>'
    html_response += f"""<h1 class="title">{gameName}</h1>
                                            <div class="container">"""

    html_response += MyHandler.table.svg()

    html_response += """</div>"""
                        
    html_response += """<script>
                            document.addEventListener('DOMContentLoaded', function() {
                            // Get the cueball element from the SVG
                            var cueball = document.getElementById('cueBall');
                            var line = document.getElementById('line');

                            line.setAttribute('x1', cueball.cx.baseVal.value);
                            line.setAttribute('y1', cueball.cy.baseVal.value);

                            // Define constants for scaling
                            var scale = 8; // Adjust as needed

                            // Variables to track mouse coordinates and dragging state
                            var isDragging = false;
                            var initX, initY; //Define initX and initY outside of the event listeners

                            // Function to handle mouse move
                            function handleMouseMove(event) {
                                if (isDragging) {
                                    var adjustedX = (event.clientX - initX) * scale + parseFloat(cueball.getAttribute('cx'));
                                    var adjustedY = (event.clientY - initY) * scale + parseFloat(cueball.getAttribute('cy'));
                                    // Update the line position to end at the adjusted mouse position
                                    line.setAttribute('x2', adjustedX);
                                    line.setAttribute('y2', adjustedY);
                                }
                            }

                            // Add mousedown event listener to start dragging
                            cueball.addEventListener('mousedown', function(event) {
                                isDragging = true;

                                initX = event.clientX; // Assign value to initX
                                initY = event.clientY; // Assign value to initY

                                // Show the line
                                line.style.display = 'block';

                                // Add mousemove event listener dynamically
                                document.addEventListener('mousemove', handleMouseMove);
                            });

                            // Add mouseup event listener to stop dragging
                            document.addEventListener('mouseup', function() {
                                isDragging = false;
                                var cueball = document.getElementById('cueBall');
                                var finalX = (event.clientX - initX) * scale;
                                var finalY = (event.clientY - initY) * scale;

                                console.log("this is final X" + finalX)
                                console.log(finalY)
                                // Hide the line when dragging stops
                                line.style.display = 'none';

                                // Remove the mousemove event listener
                                document.removeEventListener('mousemove', handleMouseMove);

                                // Send the final position to the server
                                // Check if finalX and finalY are valid numbers
                                if (!isNaN(finalX) && !isNaN(finalY)) {
                                    // Construct data object only if finalX and finalY are valid numbers
                                    var data = {
                                        finalX: finalX,
                                        finalY: finalY
                                    };

                                    // Send POST request only if data is valid
                                    fetch('http://localhost:59973/game.html', {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/json'
                                        },
                                        body: JSON.stringify(data)
                                    })
                                    .then(response => response.text())
                                    .then(html => {
                                        document.body.innerHTML = html;
                                    })
                                    .catch(error => {
                                        console.error('Error sending data', error);
                                    });
                                } else {
                                    console.error('finalX or finalY is not a valid number');
                                }
                            });
                        });

                        </script>"""

            # Display the lists of high and low balls
            # html_response += f'<div class="highs">High Balls: {highs}</div>'
            # html_response += f'<div class="lows">Low Balls: {lows}</div>' """

    html_response += """
                    </body>
                    </html>
                    """    
    
    return html_response
  
    
    return html_response



def generate_html_response_new(table, svg_list, gameName, player1Name, player2Name, highs, lows, game_end, turn):
    print("entered generate html new response")

    html_response = """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Pool Table Shot</title>
                    <style>
                    h1, .title, .player-names {
                        text-align: center;
                        font-family: 'Comic Sans MS', cursive, sans-serif; /* Use a cartoony font */
                        color: #000000;
                        font-size: 1.5em; /* Increase font size */
                        font-weight: bold; /* Make the text bold */
                        text-transform: uppercase; /* Convert text to uppercase */
                        letter-spacing: 2px; /* Add some letter spacing */
                        margin-bottom: 15px; /* Increase bottom margin for more separation */
                    }

                    svg {
                        /* Adjust height and width as needed */
                        height: 580px;
                        width: 300px;
                        border-radius: 10px;
                        display: inline-block;
                        text-align: center;
                    }

                    .container {
                        display: flex;
                        justify-content: center; /* Center horizontally */
                        align-items: center; /* Center vertically */
                        margin-top: 20px; /* Add some spacing above the container */
                    }

                    .container img {
                        max-width: 100%; /* Ensure the image doesn't exceed the container width */
                        max-height: 100%; /* Ensure the image doesn't exceed the container height */
                    }

                    body {
                        background-color: rgb(140, 179, 138);
                    }

                    .line {
                        stroke: black;
                        stroke-width: 10;
                        pointer-events: none; /* To ensure the line doesn't interfere with mouse events */
                    }

                    .cueContainer {
                        position: relative;
                        width: 500px;
                        height: 500px;
                        background-color: #f0f0f0;
                        margin: 50px auto;
                    }
                    </style>
                </head>
                <body>
                        """
                        # html_response += f'<div class="current-player">Current Player: {current_player}</div>'

            
                        # html_response += f'<div class="player-names"><span>{player1_name} ({assign_player1})</span><span>{player2_name} ({assign_player2})</span></div>'
                        # html_response += f'''
                        #    <div class="player-names">
                        #        <span class="assign-player1">{player1_name} ({assign_player1})</span>
                        #        <span class="assign-player2">{player2_name} ({assign_player2})</span>
                        #    </div>''' """

                        # Add the SVG representation of the table

    if turn % 2 == 0:
        html_response += f'<div class="player-names" style="font-weight: bold; color: red;">Player 1: {player1Name}</div>'
        turn+=1
    else:
        html_response += f'<div class="player-names" style="font-weight: bold; color: red;">Player 2: {player2Name}</div>'
        turn+=1

    html_response += f"""<h1 class="title">{gameName}</h1>
                                            <div class="container">"""

    if svg_list:  # Check if svg_list is not empty
        html_response += f"""{svg_list}"""
    
    print(svg_list)
            
    html_response += """</div>"""

    html_response += """<script>
                            document.addEventListener('DOMContentLoaded', function() {
                            // Get the cueball element from the SVG
                            var cueball = document.getElementById('bug');
                            var line = document.getElementById('line');

                            line.setAttribute('x1', cueball.cx.baseVal.value);
                            line.setAttribute('y1', cueball.cy.baseVal.value);

                            // Define constants for scaling
                            var scale = 8; // Adjust as needed

                            // Variables to track mouse coordinates and dragging state
                            var isDragging = false;
                            var initX, initY; //Define initX and initY outside of the event listeners

                            // Function to handle mouse move
                            function handleMouseMove(event) {
                                if (isDragging) {
                                    var adjustedX = (event.clientX - initX) * scale + parseFloat(cueball.getAttribute('cx'));
                                    var adjustedY = (event.clientY - initY) * scale + parseFloat(cueball.getAttribute('cy'));
                                    // Update the line position to end at the adjusted mouse position
                                    line.setAttribute('x2', adjustedX);
                                    line.setAttribute('y2', adjustedY);
                                }
                            }

                            // Add mousedown event listener to start dragging
                            cueball.addEventListener('mousedown', function(event) {
                                isDragging = true;

                                initX = event.clientX; // Assign value to initX
                                initY = event.clientY; // Assign value to initY

                                // Show the line
                                line.style.display = 'block';

                                // Add mousemove event listener dynamically
                                document.addEventListener('mousemove', handleMouseMove);
                            });

                            // Add mouseup event listener to stop dragging
                            document.addEventListener('mouseup', function() {
                                isDragging = false;
                                var cueball = document.getElementById('cueBall');
                                var finalX = (event.clientX - initX) * scale;
                                var finalY = (event.clientY - initY) * scale;

                                console.log("this is final X" + finalX)
                                console.log(finalY)
                                // Hide the line when dragging stops
                                line.style.display = 'none';

                                // Remove the mousemove event listener
                                document.removeEventListener('mousemove', handleMouseMove);

                                // Send the final position to the server
                                // Check if finalX and finalY are valid numbers
                                if (!isNaN(finalX) && !isNaN(finalY)) {
                                    // Construct data object only if finalX and finalY are valid numbers
                                    var data = {
                                        finalX: finalX,
                                        finalY: finalY
                                    };

                                    // Send POST request only if data is valid
                                    fetch('http://localhost:59973/game.html', {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/json'
                                        },
                                        body: JSON.stringify(data)
                                    })
                                    .then(response => response.text())
                                    .then(html => {
                                        document.body.innerHTML = html;
                                    })
                                    .catch(error => {
                                        console.error('Error sending data', error);
                                    });
                                } else {
                                    console.error('finalX or finalY is not a valid number');
                                }
                            });
                        });

                        </script>"""


    print("I reached the end of the function")

            # Display the lists of high and low balls
    html_response += f'<div class="highs">High Balls: {highs}</div>'
    html_response += f'<div class="lows">Low Balls: {lows}</div>'
    
    if game_end:
        if turn % 2 == 0:
            html_response += f"""
                            <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: #ff0000; color: #ffffff; padding: 20px; font-size: 24px; font-weight: bold; border-radius: 10px; text-align: center;">
                                Game Over
                                {player2Name} wins!
                            </div>
                            """
        else:
            html_response += f"""
                            <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: #ff0000; color: #ffffff; padding: 20px; font-size: 24px; font-weight: bold; border-radius: 10px; text-align: center;">
                                Game Over
                                {player1Name} wins!
                            </div>
                            """


    html_response += """
                </body>
                </html>
                    """    
    
    return html_response, turn


if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();

