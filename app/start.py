#-*- encoding: utf-8 -*-

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import config


class Application(tornado.web.Application):
    def __init__(self):        
        tornado.web.Application.__init__(self, config.route, **(config.settings))


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(9100)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()