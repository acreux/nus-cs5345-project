import StringIO
import socket
import requests

import socks  # SocksiPy module
import stem.process

from stem.util import term

def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

class Tor(object):

    def __init__(self, socks_port=7000, exit_node='ru'):
        # Set socks proxy
        self.socks_port = socks_port
        self.exit_node = exit_node
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', self.socks_port)
        socket.socket = socks.socksocket
        socket.getaddrinfo = getaddrinfo

        # Perform DNS resolution through the socket

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print exc_type, exc_value, traceback
        self.close()
        # return self

    def query(self, url):
      """
      Uses urllib to fetch a site using SocksiPy for Tor over the socks_port.
      """
      try:
        return requests.get(url).text
      except:
        return "Unable to reach %s" % url

    # Start an instance of Tor configured to only exit through Russia. This prints
    # Tor's bootstrap information as it starts. Note that this likely will not
    # work if you have another Tor instance running.

    def start(self):
        def print_bootstrap_lines(line):
            if "Bootstrapped " in line:
                print term.format(line, term.Color.BLUE)
        
        print term.format("Starting Tor:\n", term.Attr.BOLD)

        # self.tor_process = stem.process.launch_tor_with_config(
        #     config = {
        #         'SocksPort': str(self.socks_port),
        #         'ExitNodes': '{{{}}}'.format(self.exit_node)},
        #     init_msg_handler = print_bootstrap_lines,
        #     )
        self.tor_process = stem.process.launch_tor_with_config(
            config = {
                'SocksPort': str(self.socks_port)},
            init_msg_handler = print_bootstrap_lines,
            )

        print term.format("\nChecking our endpoint:\n", term.Attr.BOLD)
        print term.format(self.query("https://www.atagar.com/echo.php"), term.Color.BLUE)

    def close(self):
        self.tor_process.kill()  # stops tor

    def ip(self):
        return requests.get("http://my-ip.heroku.com").text


if __name__ == "__main__":

    with Tor() as a:
        print a.ip()
