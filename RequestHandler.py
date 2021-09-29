#!/usr/bin python3
# Copyright 2020-2021 Konrad Sekuła
import io
import sys
from http.server import BaseHTTPRequestHandler
from os import curdir, sep


def interpret(html_file):
    f = html_file.read()
    from bs4 import BeautifulSoup  # pip install beautifulsoup4
    soup = BeautifulSoup(f, 'html.parser')
    scripts = soup.find_all("script", language="python")
    for script in scripts:
        script_ = script.get_text().strip()
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        ret_val = exec(script_)  # should do some debuggable shit I guess
        res = sys.stdout.getvalue()
        sys.stdout = old_stdout
        script.string = res
        script.unwrap()
    return soup  # BUG: &lt;tags&gt; generated from scripts are always like this


class RequestHandler(BaseHTTPRequestHandler):

    # def send_error(self, code: int, message: Optional[str] = ..., explain: Optional[str] = ...) -> None:

    def do_GET(self):
        mime_type = "text/html"
        if self.path == '/':
            self.path = '/index.html'
        try:
            send_html = False
            # send_audio = False
            # send_img = False
            # send_octet = False
            # TODO: other file types right below
            if self.path.endswith(".html"):
                send_html = True

            f = open(curdir + sep + self.path)
            if send_html:
                self.send_response(200)
                self.send_header('Content-type', mime_type)
                self.end_headers()
                import html
                self.wfile.write(bytes(str(interpret(f)), "utf-8"))
                f.close()

            return
        except IOError:
            self.send_error(404, 'File not found!')
