# -*- coding: utf-8 -*- 
import requests
import time
import f_voice as f_v
import f_hear as f_h
from multiprocessing import Process, current_process,Lock
import f_data as f_d

class session:
    m_a = "https://gpd-friday.herokuapp.com/"
    r_a = "https://gpd-friday.herokuapp.com/read?m_id="
    l_a = "https://gpd-friday.herokuapp.com/error?m_id="
    def create(self,user):
        self.user = user
    def ask(self,quest):
        requests.post(self.m_a,data={"user":self.user,"mes":quest})
        text = ""
        while True:
            time.sleep(3)
            text = requests.get(self.r_a+self.user).text    
            if len(text)>5:
                break
        requests.post(self.r_a+self.user,data={"dell":self.user})
        #work with added material
        return text.split("-&&-")[0]

    def log(self):
        q = requests.get(self.l_a+self.user).text
        requests.post(self.l_a+self.user,data={"dell":self.user})
        return q

class assistant:
    cou  = 0
    lock = Lock()
    def create(self,name):
        self.user = name
        self.brain = self.smart_brain()
        self.proc = []
        
    def do(self,quest):
        p = Process(target= self.brain.brain_storm,name = self.user+"_process_"+str(self.cou),args=(quest,self.lock))
        self.proc.append(p)
        p.start()
        self.cou += 1
    
    def does(self,d):
        self.ear = f_h.talk()
        self.ear.create(d)
        p = Process(target=self.ear.start_proc ,name = "SpeechRecognition",args=())
        self.proc.append(p)
        p.start()
        
        
    class smart_brain:
        def brain_storm(self,quest,loc):
            my_p = current_process().name
            search = session()
            search.create(my_p)
            ans = search.ask(quest)
            say = f_v.audio()
            sound_proc = Process(target= say.tts,name = "Audio",args=(loc,ans,"voice_"+my_p+".mp3"))
            sound_proc.start()
            sound_proc.join()
    
def start():
    db = f_d.data()
    db.create()
    fri = assistant()
    fri.create("friday")
    fri.does(db)
    
    while True :
        e = db.read_cou() 
        if e != 0:
            fri.do(db.read("audio_"+str(int(e)-1)))
            db.minus_counter()
            db.delete_item("audio_"+str(int(e)-1))
    
    for y in fri.proc:
        y.join()
    
if __name__ == "__main__":
    start()
