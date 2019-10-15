import CreateSession
import pickle
import requests
import bs4
import json
import datetime
import json

with open('UserDetails.json','r') as f:
    loginDetails = json.load(f)


URL_HOME = "https://student.amizone.net/Home"
URL = "https://student.amizone.net/"

r = requests.Session()
r.headers.update({"Referer":URL})

l = CreateSession.Login()


def login():
    l.loadCookie()
    if cookiesIsExpired(l.cookies):
        l.login(loginDetails["user"],loginDetails["pwd"])
    r.cookies=l.cookies

    
def cookiesIsExpired(cookies):
    r.cookies=cookies
    if(r.get(URL_HOME).url==URL):
        r.cookies=None
        return True
    return False


def my_courses():
    a = r.get("https://student.amizone.net/Academics/MyCourses?X-Requested-With=XMLHttpRequest")
    b = bs4.BeautifulSoup(a.content,'html.parser')
    courseId = [c.button.get('onclick').split("'")[1] for c in b.find_all(attrs={"data-title":"Attendance"})]
    courseCode = [c.text for c in b.find_all(attrs={'data-title':"Course Code"})]
    courseName = [c.text for c in b.find_all(attrs={'data-title':"Course Name"})]
    attendance = [c.text.strip() for c in b.find_all(attrs={'data-title':"Attendance"})]

    print("Attendance : ")
    for i in range(len(courseCode)):
        print("{:10s} {:40s} {:10s}".format(courseCode[i],courseName[i],attendance[i]))
    return (courseId)

def parseDate(date):
    day, time, period = date.split()
    timeMin = ':'.join(time.split(':')[:-1]) + ' ' + period
    # dayMin = '/'.join(day.split('/')[:-1])
    return (day,timeMin)

def my_classes(date=None):
    if not date:
        dayStart=datetime.date.today()
        dayEnd=dayStart+datetime.timedelta(days=1)
        dayStart = dayStart.strftime("%Y-%m-%d")
        dayEnd = dayEnd.strftime("%Y-%m-%d")
    else:
        dayStart = datetime.date(*date[::-1])
        dayEnd = datetime.date(*date[::-1])+datetime.timedelta(days=1)

    url = "https://student.amizone.net/Calendar/home/GetDiaryEvents?start={}&end={}".format(dayStart,dayEnd)
    print(url)
    print("My Classes : ")
    a = r.get(url)
    js = json.loads(a.content)
    for i in js:
        dayStart,timeStart = parseDate(i['start'])
        dayEnd,timeEnd = parseDate(i['end'])
        faculty = i['FacultyName'].split(',')
        print("{:10s} {:40s} {:25s} {:10s} {:<8s} - {:>8s}".format(i['CourseCode'],i['title'],faculty[0],dayStart,timeStart,timeEnd))
        if len(faculty)>1:
            for s in faculty[1:]:
                print("{:10s} {:40s} {:25s} {:10s} {:8s}   {:8s}".format('','',s,'','',''))
        print()
    print()

def detailed_attendance(courseId):
    url = "https://student.amizone.net/Academics/MyCourses/_Attendance?id={}".format(courseId)
    a = r.get(url)
    b = bs4.BeautifulSoup(a.content,'html.parser')
    # print(b)
    sno = [c.text.strip() for c in b.find_all(attrs={'data-title':'Sno'})]
    dateOfClass = [c.text.strip() for c in b.find_all(attrs={'data-title':'Date Of Class'})]
    timingsOfClass = [c.text.strip() for c in b.find_all(attrs={'data-title':'Timings Of Class'})]
    present = [c.text.strip() for c in b.find_all(attrs={'data-title':'present'})]
    absent = [c.text.strip() for c in b.find_all(attrs={'data-title':'Absent'})]
    remarks = [c.text.strip() for c in b.find_all(attrs={'data-title':'Remarks'})]
    total = [c.text.strip() for c in b.find_all(attrs={'data-title':'Total'})]
    print("{:5s} {:15s} {:15s} {:2s} {:2s} {:5s}".format("Sno","Date Of Class","Timings","Present","Absent","Remarks"))
    print('--------------------------------------------------------------')
    for i in range(len(sno)):
        print("{:5s} {:15s} {:15s} {:7s} {:7s} {:7s}".format(sno[i],dateOfClass[i],timingsOfClass[i],present[i],absent[i],remarks[i]))
    print('--------------------------------------------------------------')
    print("{:5s} {:15s} {:15s} {:7s} {:7s} {:7s}".format('','',total[0],present[-1],absent[-1],remarks[-1]))

def sessionPlan(courseId):
    url = "https://student.amizone.net/Academics/MyCourses/_SessionPlansoldone?id={}".format(courseId)
    a = r.get(url)
    b = bs4.BeautifulSoup(a.content,'html.parser')
    sno = [c.text.strip() for c in b.find_all("td", attrs={'data-title':'S.No'})]
    title = [c.text.strip() for c in b.find_all("td", attrs={'data-title':'Title'})]
    filename = [c.text.strip() for c in b.find_all("td", attrs={'data-title':'File Name'})]
    downloads = [c.a.get('href') for c in b.find_all("td",attrs={'data-title':'Downloads'})]
    print("{:8s} {:30s} {:30s} {:60s}".format("S. No","Title","File Name","Downloads"))
    print('-----------------------------------------------------------------------------------------------------------------------------------------')
    for i in range(len(sno)):
        print("{:8s} {:30s} {:30s} {:60s}".format(sno[i],title[i],filename[i],downloads[i]))
    print()

def getCourseID():
    url = "https://student.amizone.net/Academics/MyCourses"
    a = r.get(url)
    b = bs4.BeautifulSoup(a.content,'html.parser')

        


if __name__ == "__main__":
    login()
    my_classes()
    my_courses()