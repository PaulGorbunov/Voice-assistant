# -*- coding: utf-8 -*- 
import speech_recognition as sr
import f_data as f_d

class talk :
    def create(self,d):
        self.rec = sr.Recognizer()
        self.db = d
        
    def start_proc(self):
        while True:
            text = self.listen()
            if "!failed" not in text and u"пятница" in text:
                text = self.clean(text)
                e = self.db.read_cou()
                self.db.add_item("audio_"+str(e),text)
                self.db.plus_counter() 
                print text
                
    def clean(self,text):
        r = ""
        flag = False
        for y in text.split(" "):
            if y != u"пятница" or flag:
              r = r + y + " "
            else:
                flag = True
        return r
        
    def listen(self):
        with sr.Microphone() as source:
            audio = self.rec.listen(source)
        try:
            text = self.rec.recognize_google(audio, language="ru-Ru")
        except sr.UnknownValueError:
            text = "!failed to hear"
        except sr.RequestError as e:
            text = ("!failed server error")
        return text.lower() 
