# -*- coding: utf-8 -*- 
from bs4 import BeautifulSoup
from multiprocessing import Process, current_process,Pipe
import requests
import data_f as d_f

class admin :
    def search (self,a):
        res = "" 
        keyword = [u"новости",u"новость",u"погода",u"погоду"]
        s_keyword = ["alarm"]
        for k in  a.split() :
            if k in s_keyword :
                if (s_keyword[0] in a):
                    self.obj = alarm()
                    res =  " "
                    break
                   
            if k in keyword :
                if (keyword[0] in a) or (keyword[1] in a):
                    self.obj = media()
                    res = " "
                    break
                if (keyword[2] in a) or (keyword[3] in a):
                    self.obj = weather()
                    res = " "
                    break
                
                
        if res != " ":
            self.obj = wikipedia()
            
        self.obj.create()
        res = self.obj.act(a)
        
        ans = ans_generator(self.obj,res)        
        return ans
    
def ans_generator (obj,res) :
    if (len(obj.errors) == 0) and (len(obj.warnings) == 0):
        key = text_style()
        ans = key.clean(res.lower())
    else:
        if (len(obj.warnings) > 0):
            ans = obj.warnings[len(obj.warnings)-1]
        else:
            ans = "failed to find - check logs"
            
    return ans


class wikipedia:
    def create(self):
        self.errors = []
        self.warnings = []
    def act(self,a):
        key = text_style()
        adress = 'https://ru.wikipedia.org/w/index.php?search='+key.code(a,False)+'&title='+key.code(a,False)+'&searchToken=2bf74pmivw0bjp0lxtcpkcmw7'
        z = requests.get(adress).text
        try :
            soup = BeautifulSoup(z ,"html.parser")
            t = soup.find('div',{'id': "bodyContent",'class':"mw-body-content"})
            t = t.find('div',{'class':"mw-search-result-heading"}).find('a')
            t = t.get('href')
            t = 'https://ru.wikipedia.org'+t
            res = self.scan_wikipedia(t)
        except AttributeError:
            res = self.scan_wikipedia(adress)
        return res
    def scan_wikipedia(self,a):
        k =  0
        res = ""
        z_res = ""
        adress = a
        z = requests.get(adress).text
        soup = BeautifulSoup(z ,"html.parser")
        t = soup.find('div',{'class': "mw-parser-output"})
        try:
            t.table.extract()
        except AttributeError:
            pass
        except TypeError:
            pass
        try :
            f = t.find_all("p")
            for i in f:
                try :
                    y = i.find("b").text 
                    i = i.text
                    if (len(i)>len(res)):
                        res = i
                        if (len(res)>90):
                             break
                except AttributeError:
                    if (len(i)>len(res)):
                        z_res = i.text
                    pass
            if (len(res)<40 and len(z_res)>40):
                res = z_res
            if (len(res)<90):
                f2 = t.find_all("li")
                for i2 in f2:
                    if len(i2.text)>40 and len(i2.text)>len(res):
                        res = i2.text
                        break
        except AttributeError:
            k = 1
            res = ""
        except TypeError:
            pass
        if k == 0 and res != "":
            if (len(res)>70):
                res = self.wikiclear(res)
            res = res + "-&&-"+a
            return res
        else:
            self.errors.append("error in parsing - bad content")
            return "error"
        
    def wikiclear(self,wiki):
        i = 0
        w = True
        q = []
        cou = 0
        while (i<len(wiki)):
            if wiki[i] =='(' and not w:
                cou = cou + 1
            if wiki[i] =='(' and w:
                q.append(i)
                w = False
            if wiki[i] ==')' and not w and cou == 0:
                q.append(i)
                w = True
            if wiki[i] == ')' and not w and cou != 0:
                cou = cou - 1
            if w and len(q) == 2:
                wiki = wiki[:q[0]]+" "+wiki[q[1]+1:]
                i = q[0]
                q = []
            i = i + 1
        r = 0
        b = 0
        b1 = 0
        b2 = 0
        b3 = 0
        fl = False
        l = len(wiki)
        while r < l:
            if r < len(wiki):
                if wiki[r] =='[':
                    b = r
                if wiki[r] ==']':
                    b1 = r
                if wiki[r] == '(' and not fl:
                    b2 = r
                    fl = True
                if wiki[r] == ')' and fl:
                    b3 = r
                    fl = False
                if b != 0 and b1 != 0:
                    wiki =  wiki[:b] + wiki[b1+1:]
                    r = r - 6
                    b = 0
                    b1 = 0
                if b2!=0 and b3!=0:
                    wiki =  wiki[:b2] + wiki[b3+1:]
                    r = b2
                    b2 = 0
                    b3 = 0
                r = r + 1
            else:
                break
        return wiki

class media:    
    def create(self):
        self.errors = []
        self.warnings = []
    def act(self,a):
        res = ""
        a = a.split()
        var = []
        if len(a) == 1:
            adress = "https://ria.ru/"
            try :
                z = requests.get(adress).text
                soup = BeautifulSoup(z ,"html.parser")
                mai = soup.find('div',{'class':"b-index__main-wr"})
                t = mai.find("div",{'class':"b-index__main-news-title"}).find('span').text
                t = t + " /-/ " + mai.find("div",{"class":'b-index__main-news-announce'}).find('span').text
                s = mai.find('div',{'class':"b-index__main-list-place"}).find_all('a')
                for elem in s:
                    t = t + " /-/ " + elem.text
                res = t+"."
            except :
                self.errors.append("error in parsing news")
                
        else:
            for elem in a:
                if ("политика" in elem) or ("политик" in elem):
                    r = self.spec_news("https://ria.ru/politics/")
                    if (r != "") and (len(self.errors) == 0):
                        res = res + u" Политика: "+r
                elif ("экономика" in elem) or ("эконом" in elem):
                    r = self.spec_news("https://ria.ru/economy/")
                    if (r != "") and (len(self.errors) == 0):
                        res = res + u" Экономика: "+r
                elif ("наука" in elem):
                    adress = "https://ria.ru/science/"
                    try:
                        z = requests(adress).text
                        soup = BeautifulSoup(z ,"html.parser")
                        mai = soup.find('div',{'class':"b-themespec__main "})
                        t = mai.find('span',{'class':"b-themespec__main-news-title"}).find('span').text
                        s = mai.find('div',{'class':"b-themespec__feed-list"}).find_all("span")
                        for elem in s:
                            elem = elem.text
                            if len(elem)>5:
                                t = t + " /-/ "+elem
                        res = res + " Наука: "+t+"."
                    except:
                        self.errors.append("error in parsing science_news")
                    
                else:
                    if u"новост" not in elem:
                        var.append(elem)
            if len(var) != 0:
                u = self.hist_news(var)
                if (len(u) > 5):
                    if (len(self.errors) == 0):
                        res = res + " Новости по теме: "+ u
                else:
                    if (len(self.errors) == 0):
                        res = res + " Новости по теме: не найдены."
                    else:
                        res = ""
                
        if len(res) > 0 and len(self.errors) == 0:
            return res
        else :
            self.errors.append("unexpected error in media")
            return "error"

    def spec_news(self,a):
        k = 0
        res = ""
        adress = a
        try :
            z = requests.get(adress).text
            soup = BeautifulSoup(z ,"html.parser")
            mai = soup.find('div',{'class':"b-rubric-top"})
            t = mai.find('span',{'class':"b-rubric-top__main-news-desc"}).find('span').text
            s = mai.find('div',{'class':"b-rubric-top__announce-list"}).find_all("span",{"class":'b-rubric-top__announce-title'})
            for elem in s:
                t = t + " /-/ "+elem.text
            return  t+"."
        
        except :
            self.errors.append("error in parsing spec_news")
            return ""
        
    def hist_news(self,a):
        for i in range(len(a)):
            if len(a[i]) > 5:
                a[i] = a[i][:len(a[i])-2]
        num = 1
        stop = 0
        res = ""
        for num in range(13):
            adress ="https://svpressa.ru/all/news-archive/?page="+str(num+1)
            try:
                z = requests.get(adress).text
                soup = BeautifulSoup(z ,"html.parser")
                mai = soup.find('div',{'class':"b-text__block"}).find_all("article")
                for e in mai:
                    kof = 0
                    s = e.find('div',{'class':"b-article__content_item b-article__content_item_no_img"}).find('a').text
                    s = s + " -:- "+e.find('div',{'class':"b-article__content_item b-article__content_item_no_img"}).find('p').text
                    for q in range(len(a)):
                        if (a[q] in s.lower()):
                            kof = kof + 1
                    if kof == len(a):
                        res = res + s +"  /-/  "
                        stop = stop + 1
                if stop == 3:
                    break
            except:
                self.errors.append("error in parsing hist_news")
                break
        return res

            
class weather :
    def create(self):
        self.errors = []
        self.warnings = []
    def act(self,a):
        res = ""
        if len(a) < 9:
            try:
                z = requests.get('https://www.pogoda.com/moscow.htm?gclid=CjwKCAiAhMLSBRBJEiwAlFrsTgdLUxeXGOUG_3XhQ2A20sKvKpnonw2lEbY2fNCxkLr9bYOplUlWXxoCvTEQAvD_BwE').text
                soup = BeautifulSoup(z ,"html.parser")
                t = soup.find('dl',{'id': "hActual"})
                actual = t.find('dd',{'title':"Описание "}).text
                temper = t.find('dd',{'title': "° C"}).text
                fut = t.find('dd',{'id':'ddDescrip'}).find('span',{'id':'divInfo'}).text
                res = actual + " "+temper+","+ fut+"."
                return res
            except :
                self.errors.append("error in get_weather")
                return "error"
        else:
            key = text_style()
            adress = ('https://yandex.ru/search/?lr=213&msid=1494272649.9653.22884.18849&text=' + key.code(a,True))
            try:
                z = requests.get(adress).text
                soup = BeautifulSoup(z ,"html.parser")
                mai = soup.find('div',{'class':"weather-forecast__current"})
                res = mai.find('div',{'class':"weather-forecast__current-temp"}).text
                #satae = mai.find('div',{'class':"weather-forecast__current-details"}).text
                #print(state)
                add= mai.find('div',{'class':"weather-forecast__current-details"}).find('div',{'class':"weather-forecast__desc-list"})
                add_r = add.find_all("div")
                add_det = ""
                for u in add_r:
                    add_det = add_det + " "+u.text
                res = res + ","+add_det+"."
                return res
            except :
                self.warnings.append("error in weather point")
                return "error"
class alarm:
    def create(self):
        self.errors = []
        self.warnings = []
    def act(self,a):
        self.warnings.append([])
        self.pro = []
        p_conn2, c_conn2 = Pipe()
        p_conn4, c_conn4 = Pipe()
        self.pro.append(Process(target=self.lego_brick ,name='lego_b_2', args=(weather(),"погода иннополис",c_conn2)))
        self.pro.append(Process(target=self.lego_brick ,name='lego_b_4', args=(media(),"новости",c_conn4)))
        for u in self.pro:
            u.start()
        for y in self.pro:
            y.join()
        self.warnings[0].append(p_conn2.recv())
        self.warnings[0].append(p_conn4.recv())
        if len(self.warnings[0]) == 2:
            return "value"
        else:
            self.errors.append("error in acting alarm")
            return "failed to find - check logs"
            
    def lego_brick(self,obj,text,conn):
        obj.create()
        res = obj.act(text)
        ans = ans_generator(obj,res)
        conn.send(ans)
        conn.close()

class text_style:    
    def code (self,d,flag):
        d = d.lower()
        li  = u'абвгдежзийклмнопрстуфхцчшщъыьэюя'
        li2 = "abcdefghijklmnopqrstuvwxyz"
        li1 = '1234567890'
        nz = ['%d0%b0', '%d0%b1', '%d0%b2', '%d0%b3', '%d0%b4', '%d0%b5', '%d0%b6', '%d0%b7', '%d0%b8', '%d0%b9', '%d0%ba', '%d0%bb', '%d0%bc', '%d0%bd', '%d0%be', '%d0%bf', '%d1%80', '%d1%81', '%d1%82', '%d1%83', '%d1%84', '%d1%85', '%d1%86', '%d1%87', '%d1%88', '%d1%89', '%d1%8a', '%d1%8b', '%d1%8c', '%d1%8d', '%d1%8e', '%d1%8f']
        res = ''
        for i in range (len(d)):
            for v in range (len(li)):
                if d[i] == li [v]:
                    res = res + nz[v]
                    break
                if d[i] in li1 :
                    res = res + d[i]
                    break
                if d[i] == ' ':
                    if flag == False:
                        res = res + '+'
                    else:
                        res = res + '%20'
                    break
                if d[i] == u'ё':
                    res = res + '%d0%b5'
                    break
                if d[i] in li2:
                    res = res + d[i]
                    break
        return res

    def clean(self,a):
        alp = u"абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        alp2 = "1234567890abcdefghijklmnopqrstuvwxyz.,+-/:;()&%_=? "
        res = ""
        for i in a:
            if (i in alp) or (i in alp2):
                res = res + i
        return res
       
def command (a):
    try:
        return admin(a)
    except:
        return "bad error"


