import mechanize,webbrowser
from HTMLParser import HTMLParser
import time
from datetime import datetime
HP = '*'
VP = '|'
CP = 'x'
CHANGE = 0
TOTALRECHECK = 0
class TableParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.dat = []
        self.flag  = False
        self.tr = False
        self.td = False
        self.temp = []
        self.subli = []
        

    def handle_starttag(self, tag, attrs):
        
        if tag == "table":
            for name,value in attrs:
                if name=="id" and value == "grdgrade":
                    self.flag = True
       
        if self.flag:
            if tag =='tr':
                self.tr = True

            if tag =='td':
                self.td = True
                
              
    def handle_endtag(self, tag):
        if tag == "table":
            self.flag = False
        if tag =='tr':
            self.tr = False
            if len(self.temp) > 1 :
                self.subli.append(self.temp)
            self.temp = []

        if tag=='td':
            self.td = False
            

    def handle_data(self, data):
        if self.flag and self.td:
            tp = ' '.join(data.split())

            if len(tp)!=0:
                self.temp.append(tp)

    def show(self):
        global CHANGE
        print '\t'+VP*2 + ' '*80 + VP*2
        print '\t'+VP*2  +"Subject Code".center(15)+"Subject Name".center(45)+"Old Grade".center(10)+"New Grade".center(10)+ VP*2
        
        for each in self.subli:
            
            if each[3]!=each[2]:
                CHANGE += 1
                print "@"*100
                print "$"*100
                print "CHANGE IN GRADES"
                print 
               
            print '\t' + VP*2 + each[0].center(15)+ each[1].ljust(45)+each[2].center(10) +each[3].center(10) +VP*2
        
        print '\t' +CP*2   + HP*80 + CP*2
        return self.subli


class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.name = None
        self.enroll = None
        self.seat = None


        self.flag  = False
        self.value = None

    def handle_starttag(self, tag, attrs):
        self.flag = False
        if tag == "span":
            for name,value in attrs:
                if name=="id" and value in ["lblName","lblOldEnroll","lblExam"]:
                    self.flag = True
                    self.value = value
                
    def handle_endtag(self, tag):
        if tag == "span":
            self.flag = False
            

    def handle_data(self, data):
        if self.flag and data != "------------":
            if self.value == "lblName":
                self.name = data
            if self.value == "lblOldEnroll":
                self.enroll = data
            if self.value == "lblExam":
                self.seat = data

    def display(self):
        if None not in [self.name,self.enroll,self.seat]:
            print '\t' + CP + CP + HP*80 + CP + CP
            print "\t"+VP+VP+"  Name   :".ljust(8) + self.name.ljust(70) +VP+VP
            print "\t"+VP+VP+"  Enroll :".ljust(8) + self.enroll.ljust(70) +VP+VP
            print "\t"+VP+VP+"  Seat   :".ljust(8) + self.seat.ljust(70) +VP+VP

            return [self.name,self.enroll,self.seat]
        else:
            return False
            


def listexam():
    #url = "http://localhost/gturesults.in/recheckc393.html"
    url = "http://gturesults.in/recheck.aspx"
    br = mechanize.Browser()
    br.set_handle_robots(False) # ignore robots

    print "Establishing Connection with site...!!"
    try:
        br.open(url)
        print "Connected..!!"
    except:
        print "Couldn't Establish connection ..!!!"
    
    semli = []
    br.select_form("form1")
    control = br.form.find_control("ddlbatch")
    if control.type == "select":  # means it's class ClientForm.SelectControl
        i=0
        for item in control.items:
            str([label.text  for label in item.get_labels()])
            semdic[i] = [item.name, label.text]
            i+=1
            semli.append(label.text)
    for i in range(len(semli)):
        if 'BE' in semli[i]:
            print i,semli[i]
    print 
    print "Enter Your Choice : "
    cho = input()

    return cho

    

def hackgtu(strt=110320107000,end=110320107020,flag=False,cho=5):
    global TOTALRECHECK
    #url = "http://localhost/gturesults.in/recheckc393.html"
    url = "http://gturesults.in/recheck.aspx"
    br = mechanize.Browser()
    br.set_handle_robots(False) # ignore robots
    print "Establishing Connection with site...!!"
    try:
        br.open(url)
        print "Connected..!!"
    except:
        print "Couldn't Establish connection ..!!!"
    semdic = {}
    semli = []
    br.select_form("form1")
    control = br.form.find_control("ddlbatch")
    if control.type == "select":  # means it's class ClientForm.SelectControl
        i=0
        for item in control.items:
            str([label.text  for label in item.get_labels()])
            semdic[i] = [item.name, label.text]
            i+=1
            semli.append(label.text)

    print "EXAM RESULTS OF",semli[cho],semdic[cho][1]
    print "Enrollment No :",strt,"-",end

    br["ddlbatch"] = [semdic[cho][0]]

    ##select the file to write the result
    foo = open("result.txt",'w')
    foo.write('\t'.join(["Name","Enroll No","Seat No"])+'\n\n')
    count = 0 
    for i in range(strt,end+1):
        br.select_form("form1")
        br["ddlbatch"] = [semdic[cho][0]]
        br["txtenroll"] = str(i)

        print "Searching ",i
       
        res = br.submit()
        content = res.read()
        parserobj = Parser()
        tbparser = TableParser()
        
        parserobj.feed(content)
        tbparser.feed(content)
        li = parserobj.display()
        
        if li:
            subli = tbparser.show()
            count+=1

            if flag:
                with open("results.html", "w") as f:
                    f.write(content)
                webbrowser.open("results.html")
            foo.write('\t'.join(li)+'\n')

    print "Total Studnets for rechecking ",count
    TOTALRECHECK += count
    foo.close()

##06 - CIVIL ENGINEERING
##07 - COMPUTER ENGINEERING
##11 - ELECTRONICS COMMUNICATION ENGINEERING
##16 - INFORMATION TECHNOLOGY
##19 - MECHANICAL ENGINEERING

stick = time.time()
d1=datetime.now()

##print "$"*50
##print "\tCIVIL ENGINEERING"
##print "$"*50
##hackgtu(110320106000,110320106130)
##print "$"*50
##print "\tCOMPUTER ENGINEERING"
##print "$"*50
##hackgtu(110320107000,110320107135)
##print "$"*50
##print "\tELECTRONICS COMMUNICATION ENGINEERING"
##print "$"*50
##hackgtu(110320111000,110320111065)
##print "$"*50
##print "\tINFORMATION TECHNOLOGY"
##print "$"*50
##hackgtu(110320116000,110320116060)
##print "$"*50
##print "\tMECHANICAL ENGINEERING"
##print "$"*50
##hackgtu(110320119000,110320119130)

etick =time.time()
d2=datetime.now()
d3 = d2-d1
mn = 0
sc = d3.seconds
hr = 0

mn = sc/60
sc = sc%60

hr = mn/60
mn = mn%60

print "\n\n\n"
print "Total Rechecked : ",TOTALRECHECK
print "Change in grades : ",CHANGE

print "Start Time ",time.asctime( time.localtime(stick)),"         ",d1
print "End Time   ",time.asctime( time.localtime(etick)),"         ",d2
print "Duration : ",hr,"hour",mn,"min",sc,'sec'
print "Total Seconds " ,d3.seconds,"sec      ",(hr*60+mn*60+sc),"sec"
