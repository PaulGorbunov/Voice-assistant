import sqlite3

class data:
    def create(self):
        self.conn = sqlite3.connect('yoda.db')
        self.c = self.conn.cursor()
        try:
            self.c.executescript('DELETE FROM WIZDOM;')
            self.conn.commit()
            self.delete_item("main","COUNT")
            self.c.execute("INSERT INTO COUNT (id,counter) VALUES (:i,:k)",{"i":"main","k":0})
            self.conn.commit()
            return True
        except:
            return False
      
    def delete(self):
        self.c.close()
        self.conn.close()
        
    def add_item(self,m_id,text):
        try :
            self.c.execute("INSERT INTO WIZDOM (id,text) VALUES (:id,:text)",{"id":m_id,"text":text})
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    def plus_counter(self):
        m = int(self.read_cou("main"))
        self.c.execute("UPDATE COUNT SET counter = :c WHERE id = 'main' ",{"c":str(m+1)})
        self.conn.commit()
    def minus_counter(self):
        m = int(self.read_cou("main"))
        if m > 0 :
            self.c.execute("UPDATE COUNT SET counter = :c WHERE id = 'main' ",{"c":str(m-1)})
            self.conn.commit()
        else:
            self.c.execute("UPDATE COUNT SET counter = :c WHERE id = 'main' ",{"c":"0"})
            self.conn.commit()
    def delete_item(self,c,table = "WIZDOM"):
        if table == "WIZDOM":
            self.c.execute("DELETE FROM WIZDOM WHERE id = :cou",{"cou":c})
        else:
            self.c.execute("DELETE FROM COUNT WHERE id = :cou",{"cou":c})
        self.conn.commit()
        
    def read_cou(self,s = "main"):
        try :
            text = self.c.execute('SELECT counter FROM COUNT WHERE id = :s',{"s":s})
            return text.fetchone()[0]
        except TypeError:
            return ""
    def read(self,user):
        try :
            text = self.c.execute('SELECT text FROM WIZDOM WHERE id = :user',{"user":user})
            return text.fetchone()[0]
        except TypeError:
            return "error"
 
