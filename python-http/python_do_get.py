# -*- coding:UTF-8 -*-  
  
import os  
import BaseHTTPServer  
import time  
import threading  
import urlparse  
  
class ServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):  
      
    '''  
    简单的Http服务器，处理get请求  
    '''  
      
    #处理用户的GET请求  
    def do_GET(self):  
        try:  
            str = urlparse.urlparse(self.path)  
            print str  
            #请求的参数  
            args = dict(urlparse.parse_qsl(str.query))  
            #请求的路径  
            filepath = os.curdir+os.sep+self.path  
            #请求路径不能正确打开  
#            if ( False == os.path.isfile(filepath)):  
#                self.send_response(404)  
#                self.end_headers()   
#                return  
              
            #处理普通的链接请求  
            content = None;  
            if ( filepath[-5:] == ".html"  ):  
                content = "text/html; charset=utf-8";  
            elif ( filepath[-4:] == ".css" ):  
                content = "text/css";  
            elif ( filepath[-3:] == ".js" ):  
                content = "application/x-javascript";  
            elif ( filepath[-4:] == ".png" ):  
                content = "image/png";  
            elif ( filepath[-4:] == ".gif" ):  
                content = "image/gif";  
            elif ( filepath[-4:] == ".jpg" ):  
                content = "image/jpg";                                  
            elif ( filepath[-4:] == ".mp3" ):  
                content = "audio/mpeg";                  
            elif ( filepath[-4:] == ".xml" ):  
                content = "text/xml; charset=utf-8";    
                  
            #请求是以上文件类型  
            if ( content <> None ):  
                self.send_response(200)  
                self.send_header("Content-Length", os.path.getsize(filepath))  
                self.send_header("Content-type", content)  
                self.end_headers()          
                with open(filepath , "rb" ) as f:  
                    self.wfile.write(f.read());  
                    self.wfile.flush();                  
                return  
              
            #请求不包含操作，直接返回，否则特殊处理  
            if (False == args.has_key('cmd') ):  
                return  
            cmd = args['cmd']  
              
            #若请求包含操作  
            if cmd == 'searchUser':  
                self.send_response(200);  
                self.send_header("Content-Type", 'text/html')  
                self.end_headers()  
                self.wfile.write('<b>成功</b>')  
                self.wfile.close()  
              
        except:  
            print '出现异常'  
            self.send_error(404, 'File Not Found:%s' % filepath)  
      
  
class Server:  
    def startServer(self):  
        server_address = ('', 8000)  
        httpd = BaseHTTPServer.HTTPServer(server_address, ServerHandler)  
        server_thread = threading.Thread(target=httpd.serve_forever)  
        server_thread.setDaemon(True)  
        server_thread.start()  
          
          
if __name__ == '__main__':  
      
    server = Server()  
    server.startServer()  
    starttime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))    
    print '%s 服务器已启动' % starttime  
    time.sleep(50000)  
