import sys; # used to get argv
import cgi; # used to parse Mutlipart FormData 
            # this should be replace with multipart in the future
import os
import math
import Physics

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler;

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl;


# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        # check if the web-pages matches the list
        if parsed.path in [ '/shoot.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
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
        # hanle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        if parsed.path in [ '/display.html' ]:

            # get data send as Multipart FormData (MIME format)
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

            print("Collected Data:", data)
            # generate the headers
            with open('display.html', 'rb') as fp:
                content = fp.read()

            # delete my svg files with helper function
            delete_svg()

            rollingVelX = float(data['rb_dx']) 
            #print("this is rolling vel", rollingVelX)
            rollingVelY = float(data['rb_dy'])
            print("this is rolling vel", rollingVelY)

            velMag = math.sqrt((rollingVelX * rollingVelX) + (rollingVelY * rollingVelY))
            print("this is velmag", velMag)
            
            # prevent divide by 0
            if velMag != 0:

            # as long as denominator not 0, we calculate the new velocity
                newVelX = rollingVelX/velMag
                newVelY = rollingVelY/velMag
                print("this is new vel", newVelY)
                accX = -newVelX * Physics.DRAG
                print(accX)
                accY = -newVelY * Physics.DRAG
                print("this is acc of y", accY)


            table = Physics.Table()
            index = 0
            # Calculate the position for the StillBall 
            pos_x = float(data["sb_x"])
            pos_y = float(data["sb_y"])
            pos = Physics.Coordinate(pos_x, pos_y)

            # Create and store the StillBall
            sb = Physics.StillBall(int(data["sb_number"]), pos)

            # Calculate position, velocity, and acceleration for RollingBall
            pos_rb = Physics.Coordinate(float(data["rb_x"]), float(data["rb_y"]))
            vel = Physics.Coordinate(rollingVelX, rollingVelY)  # moving up along the table's center
            acc = Physics.Coordinate(accX, accY)

            # Create and store the RollingBall
            rb = Physics.RollingBall(int(data["rb_number"]), pos_rb, vel, acc)

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
            
            # add nice string here
            html_content = generate_webpage()

            if content:
                self.send_response( 200 ); # OK
                self.send_header( "Content-type", "text/html" );
                self.send_header( "Content-length", len( html_content ) );
                self.end_headers();

                # send it to the browser
                self.wfile.write(html_content.encode());
                fp.close();
            else:
                self.send_error(500, 'Error reading display.html')


        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


def delete_svg():
        directory = '/home/undergrad/3/pharpala/CIS2750/A2'
        files = os.listdir(directory)

        for file in files:
            if file.endswith('.svg'):
                file_path = os.path.join(directory, file)
                os.remove(file_path)


def generate_webpage():

    html_content = "<html>\n<head>\n<title>Ball Positions and Velocities</title>\n</head>\n<body>\n"

    # Add a "Back" link to navigate back to "/shoot.html" page
    html_content += "<p><a href=\"/shoot.html\">Back</a></p>\n"

    # Add description of the original ball positions and velocities
    html_content += "<h1>Ball Positions and Velocities Visual</h1>\n"

    # Get a list of all SVG files in the directory
    svg_files = [file for file in os.listdir() if file.endswith('.svg')]

    # Generate <img> tags for each SVG file
    for svg_file in sorted(svg_files):
        html_content += f"<img src=\"{svg_file}\" alt=\"{svg_file}\">\n"

    # Close the HTML body and document
    html_content += "</body>\n</html>"

    return html_content

if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();

