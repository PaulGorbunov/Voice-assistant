# -*- coding: utf-8 -*- 
import os, sys
with open(os.devnull, 'w') as f:
    oldstdout = sys.stdout
    sys.stdout = f
    import pygame
    sys.stdout = oldstdout
    
import time
from gtts import gTTS
from pygame import mixer

class audio:
    def tts (self,lock,text,location,lang = "ru"):
        lock.acquire()
        try:
            e = self.text_change(text)
            tts = gTTS(text= e, lang=lang)
            tts.save(location)
            print (text)
            self.say(self.delay(e),location)
            os.remove(location)
        finally:
            lock.release()
    
    def text_change(self,text):
        r = text.split("/-/")
        if len(r) == 1 :
            t = text.split(".")
            if len(t) > 1 :
                if len(t[0] + t[1])<250:
                    return t[0]+"."+t[1]+"."
                else:
                    return t[0]+"."
            else:
                return text
        else:
            return r[0]
        
    def say(self,sleep,mp3 ):
        mixer.init()
        mixer.music.load(mp3)
        mixer.music.play()
        time.sleep(sleep)
        mixer.music.stop()
    
    def delay(self,text):
        if u"м/с ветер" in text:
            return 10
        else:
            u = len(text)*0.15
            return u
    
