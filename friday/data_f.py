import sqlite3
from time import gmtime, strftime
class data:
    def create_con(self):
        self.conn = sqlite3.connect('friday_db.db')
        self.c = self.conn.cursor()
    def delete_con(self):
        self.c.close()
        self.conn.close()
    def add_item(self,user,text):
        try :
            self.c.execute("INSERT INTO answers (user,answer) VALUES (:user,:ans)",{"user":user,"ans":text})
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def add_long(self,user,l_ans):
        try:
            self.c.execute("INSERT INTO list (user,item) VALUES (:user,:text)",{"user":user,"text":l_ans})
            self.conn.commit()
            return True
        except:
            return False
        
        
    def add_error(self,user,error):
        try :
            t = strftime("%D:%H:%M +0003", gmtime())
            self.c.execute("INSERT INTO errors (user,time,error) VALUES (:user,:time,:er)",{"user":user,"time":t,"er":error})
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    def empty_error(self,user):
        self.c.execute("DELETE FROM errors WHERE user = :user",{"user":user})
        self.conn.commit()
    def delete_item(self,user):
        self.c.execute("DELETE FROM answers WHERE user = :user",{"user":user})
        self.conn.commit()
    def delete_long(self,user):
        self.c.execute("DELETE FROM list WHERE user = :user",{"user":user})
        self.conn.commit()
        
    def read_db(self,user):
        try :
            text = self.c.execute('SELECT answer FROM answers WHERE user = :user',{"user":user})
            return text.fetchone()[0]
        except TypeError:
            return ""
    def read_log(self,user):
        try :
            e_l = []
            text = self.c.execute('SELECT time,error FROM errors WHERE user = :user',{"user":user})
            row = text.fetchone()
            while row is not None:
                e_l.append(row)
                row = text.fetchone()
            return e_l
        except TypeError:
            return [""]
        
    def read_long(self,user):
        try :
            e_l = []
            text = self.c.execute('SELECT item FROM list WHERE user = :user',{"user":user})
            row = text.fetchone()
            while row is not None:
                e_l.append(row)
                row = text.fetchone()
            return e_l
        except TypeError:
            return [""]

