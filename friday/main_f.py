import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import brain_f as bf
import data_f as df

data = df.data()
data.create_con()
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("FRIDAY")
        self.write("__designed and created by Paul Gorbunov__")
    def post(self):
        global data
        user = self.get_argument('user')
        quest = self.get_argument('mes')
        brain = bf.admin()
        ans = brain.search(quest)
        if (len(brain.obj.errors) != 0):
            data.add_error(user,brain.obj.errors[0])
        if type(ans) == str:
            data.add_item(user,ans)
        else:
            for i in ans:
                data.add_long(user,i)
        del brain
        
class AnsHandler(tornado.web.RequestHandler):
    def get(self):
        global data
        my_id = self.get_argument('m_id')
        text = data.read_db(my_id)
        self.write(text)
    def post(self):
        global data
        dell = self.get_argument("dell")
        data.delete_item(dell)
        
class ErrHandler(tornado.web.RequestHandler):
    def get(self):
        global data
        my_id = self.get_argument('m_id')
        text = data.read_log(my_id)
        for u in text:
            for t in u:
                self.write(t+" ")
            self.write("-&&-")
    def post(self):
        global data
        dell = self.get_argument("dell")
        data.empty_error(dell)
        
class LisHandler(tornado.web.RequestHandler):
    def get(self):
        global data
        my_id = self.get_argument('m_id')
        text = data.read_long(my_id)
        for t in text:
            self.write(t)
            self.write("-&&-")
    def post(self):
        global data
        dell = self.get_argument("dell")
        data.delete_long(dell)
    
def main():
    application = tornado.web.Application([
        (r"/", MainHandler),(r"/read",AnsHandler),(r"/error",ErrHandler),(r"/list",LisHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
 
if __name__ == "__main__":
    main()
