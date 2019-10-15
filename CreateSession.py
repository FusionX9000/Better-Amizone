import requests
import bs4
import pickle

class Login:
    URL = "https://student.amizone.net"
    URL_LOGIN = URL + "/Login/Login"

    def __init__(self):
        self.filename = "cookies"
        self.cookies = None

    def saveCookie(self,requestsCookieJar):
        with open("./"+self.filename,'wb') as f:
            pickle.dump(requestsCookieJar,f)
        self.cookies=requestsCookieJar

    def loadCookie(self):
        with open("./"+self.filename,'rb') as f:
            self.cookies = pickle.load(f)

    def create_form_data(self,user,pwd, rvt, recaptcha_token):
        data = {
            "_UserName":user,
            "_Password":pwd,
            "g-recaptcha-response":recaptcha_token,
            "__RequestVerificationToken":rvt
        }
        return data

    def login(self,user,pwd,recaptcha_token=None):
        session = requests.Session()
        session.headers.update({"Referer":self.URL})
        defaultPage=session.get(self.URL)
        htmlObject = bs4.BeautifulSoup(defaultPage.content,'html.parser')
        rvt = htmlObject.find(id="loginform").input['value']
        data = self.create_form_data(user,pwd,rvt,recaptcha_token)
        logged = session.post(self.URL_LOGIN,data=data)
        self.saveCookie(session.cookies)
        


