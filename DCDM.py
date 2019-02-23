import mechanize
from clint.textui import progress
import requests
import re
import os
import keyboard
import time
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_equiv( True ) 
br.set_handle_gzip( True ) 
br.set_handle_redirect( True ) 
br.set_handle_referer( True )
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
def login():
    try:
        resp0=br.open("https://otakustream.tv/user/login/")
        br.select_form(nr=1)
        br.form["log"] = 'user@gmail.com'
        br.form["pwd"] = 'password'
        br.submit()
        print "Login Successful"
    except:
        print "Can't Login"
def fetchl():
    try:
        no=input("Enter the episode number from where you want to download till present : ")
        epl1=("https://otakustream.tv/anime/detective-conan/episode-"+str(no)+"/")
        return epl1
    except:
        print "Can't fetch links"
        return None
def getfnm(cd):
    if not cd:
        return "Anonymous"
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return "Anonymous"
    return fname[0]
def alreadydc():
    cwd=os.getcwd()
    for file in os.listdir(cwd):
        if file.endswith(".mp4"):
            if file==nfilename:
                return "Exists"
            else:
                pass
def renamer():
    respname=br.open("http://www.detectiveconanworld.com/wiki/Anime")
    eno=respname.read()
    eno1=eno.split('>'+filenamewoq[0:3]+' </td>')
    eno2=eno1[1]
    eno3=eno2.split('">')
    eno4=eno3[3]
    eno5=eno4.split('<')
    eno6=eno5[0]
    eno7=""
    for i in eno6:
        if i==":":
            eno7+="-"
        elif i in ["*","?","<",">","|",'"',"/"]:
            eno7+=" "
        else:
            eno7+=i
    global nfilename
    nfilename="Episode "+filenamewoq[0:3]+" "+eno7+".mp4"
def downloader(url):
    global filenamewq,filenamewoq
    r = requests.get(url,stream=True,allow_redirects=True)
    filenamewq = getfnm(r.headers.get('content-disposition'))
    filenamewoq = filenamewq[1:len(filenamewq)-1:1]
    renamer()
    cv=alreadydc()
    if cv == "Exists":
        print "File already downloaded or a file with same name is present."
    else:
        print "Downloading\n",nfilename
        with open(nfilename, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=64), expected_size=(total_length/64) + 1):
                if keyboard.is_pressed('esc'):
                    f.close()
                    os.rename(nfilename,nfilename+".part")
                    break
                elif chunk:
                    f.write(chunk)
                    f.flush()
            f.close()           
def eplc():
    global gepl
    l=gepl.split("/")
    xx=l[5]
    yy=xx.split("-")
    z=yy[1]
    q=int(z)+1
    gepl="https://otakustream.tv/anime/detective-conan/episode-"+str(q)
def epld():
    global gepl
    resp2=br.open(gepl)
    o=resp2.read()
    a=o.split('onclick="window.open(')
    b=a[1]
    c=b.split(",")
    d=c[0]
    e=d[1:len(d)-1]
    f="https://otakustream.tv"+e
    print "Downloading from --"+f
    return f
try:
    print "Welcome to Detective Conan Downloader."
    print "Opening OtakuStream.tv"
    login()
    gepl=fetchl()
    print "Starting Download"
    print time.asctime()
    while True:
        if gepl!=None:
            g=epld()
            resp3=br.open(g)
            content = resp3.get_data()
            content2=content.split("https://www.rapidvideo.com/")
            try:
                content3=content2[1]
            except IndexError:
                print "Link not found"
            else:
                content4=content3.split('"')
                content5=content4[0]
                linkf="https://www.rapidvideo.com/"+content5
                resp4=br.open(linkf)
                target_text2="Download"
                for link2 in br.links():
                    if target_text2 in link2.text:
                        dow=link2.url
                        break
                resp5=br.open(dow)
                for link3 in br.links():
                    if "480p" in link3.text:
                        dl=link3.url
                        break
                    else:
                        if "720p" in link3.text:
                            dl=link3.url
                            break
                        else:
                            if "1080p" in link3.text:
                                dl=link3.url
                                break
                            else:
                                if "360p" in link3.text:
                                    dl=link3.url
                                    break
                                else:
                                    dl=None
                if dl!=None:
                    downloader(dl)
                    print time.asctime()
                    eplc()
                else:
                    eplc()
        else:
            eplc()
except:
    print time.asctime()
    er=raw_input("An Error Occured")
