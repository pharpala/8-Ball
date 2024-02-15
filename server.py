import sys; # used to get argv
import cgi; # used to parse Mutlipart FormData 
            # this should be replace with multipart in the future

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
        elif parsed.path in [ '/table-?.svg' ]:
            # get the form data and turn it into a dictionary
            form_data = dict( parse_qsl( parsed.query ) );

            # retreive the HTML file & insert form data into the HTML file
            fp = open( '.'+parsed.path );
            content = fp.read() % form_data;

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the browser
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

            # read the HTML file and insert the form data
            fp = open( '.'+parsed.path );
            content = fp.read() % form;

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the browser
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();

        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );
