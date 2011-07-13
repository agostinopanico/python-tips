import tornado.httpserver  
import tornado.ioloop  
import tornado.web  
  
class BaseHandler(tornado.web.RequestHandler):  
    def get_current_user(self):  
        return self.get_secure_cookie("user")  
  
  
class MainHandler(BaseHandler):  
    def get(self):  
  
        if not self.current_user:  
            self.redirect("/login")  
            return  
        name = tornado.escape.xhtml_escape(self.current_user)  
        self.write("Hello, " +  name)  
  
class LoginHandler(BaseHandler):  
  
    def get(self):  
        self.set_cookie("checkflag", "true")  
        self.render("templates/logintest/login.html")  
  
    def post(self):  
        if not self.request.headers.get("Cookie"):  
            self.render("templates/logintest/require_enable_cookie.html")  
            return  
        self.set_secure_cookie("user", self.get_argument("name"))  
        self.redirect("/")  
  
  
application = tornado.web.Application([  
    (r"/", MainHandler),  
    (r"/login", LoginHandler),  
], cookie_secret="hello")  
  
if __name__ == "__main__":  
    http_server = tornado.httpserver.HTTPServer(application)  
    http_server.listen(8081)  
    tornado.ioloop.IOLoop.instance().start()  
