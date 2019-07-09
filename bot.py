import telegram
from telegram.ext import Updater,CommandHandler,MessageHandler, Filters
import logging
import subprocess as sp
import requests
import json
import threading
from bomber import kill
import shodan
import speech_recognition as sr
from pydub import AudioSegment
import re

enabled_users=[]
ippsec_list=[]

# api required 
bot=telegram.Bot("<token>")
updater = Updater(token='<token>')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
SHODAN_API_KEY = "<token>"
api = shodan.Shodan(SHODAN_API_KEY)

def banner():
    c="=========================="
    c+="\nWelcome To personal Hack Machine"
    c+="\n      To start Login:- /verify <password>"
    c+="\n========================"
    return (c)


def sender(update,text):
    bot.send_message(chat_id=update.message.chat_id, text=text)

def banned(update):
    bot.send_message(chat_id=update.message.chat_id,text="Login First !!")

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=banner())

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def verify(bot,update,args):
    if args:
        if args[0]=="haha@123":
            sender(update,"Successfully logged in")
            enabled_users.append(update.message.from_user.id)
        else:
            banned(update)

verify_handler = CommandHandler('verify', verify,pass_args=True)
dispatcher.add_handler(verify_handler)

def echo(bot, update):
    sender(update,"Use /help For more :)")

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


def voice_handler(bot, update):
    
    r = sr.Recognizer()
    file = bot.getFile(update.message.voice.file_id)
    sender(update,"Processing the command")
    file.download('voice.ogg')
    ogg_version = AudioSegment.from_ogg("voice.ogg")
    ogg_version.export("voice.wav", format="wav")
    harvard = sr.AudioFile('voice.wav')
    with harvard as source:
        audio = r.record(source)
        analyser(bot,update,r.recognize_google(audio))    

echoaudio_handler = MessageHandler(Filters.voice, voice_handler)
dispatcher.add_handler(echoaudio_handler)    

def exit(bot, update):
    sender(update,"Logged out Successfully")
    enabled_users.remove(update.message.from_user.id)
    

exit_handler = CommandHandler('exit', exit)
dispatcher.add_handler(exit_handler)


def cmd2(bot,update,args):
    if update.message.from_user.id in enabled_users:
        if args:
            output = sp.getoutput(args)
            sender(update,output)
        else:
            sender(update,"Enter a command dumbass !!")
    else:
        banned(update)


def ippsec(bot,update,args):
    if update.message.from_user.id in enabled_users:
        target=args[0]
        temp=['empty life']
        global ippsec_list
        if ippsec_list:
            count=0
            sender(update,"Keyword: {}".format(target))
            for i in ippsec_list:
                count+=1
                i=i.lower()
                if i.find(target)>=0:
                    location=count-1
                    flag=0
                    while flag==0:
                        s=ippsec_list[location]
                        if s.find("HackTheBox")==0:
                            if ippsec_list[location+1] in temp:
                                flag=1
                            else:
                                temp.append(ippsec_list[location+1])    
                                output="Machine: {}\nLink: {}".format(s,ippsec_list[location+1])
                                sender(update,output)
                                flag=1
                        else:
                            location=location-1
        else:
            url="https://gist.githubusercontent.com/sminez/571bd7bafb1b88630b85c85a0cd66e3a/raw/68fe21504be4654b739a577a482d91587524f683/ippsec-details.txt"
            r=requests.get(url)
            ippsec_list=r.text.split('\n')
            ippsec(bot,update,args)                        
    else:
        banned(update)


def ippsec_start(bot,update,args):
    commands=""
    lists=[]
    for i in range(len(args)):
        commands+=args[i]
        commands+=" "
    commands.split()   
    lists.append(commands)
    print(lists)
    ippsec(bot,update,lists)   

help_handler = CommandHandler('youtube', ippsec_start,pass_args=True)
dispatcher.add_handler(help_handler) 

 


def analyser(bot,update,commands):
    commands=commands.lower()
    if re.match("cmd",commands):
        commands=commands.replace("cmd","")
        
        cmd2(bot,update,commands)
    elif re.match("shodan",commands):
        commands=commands.replace("shodan","")
        text = commands.split(' ')
        text.remove('')
        
        shodansearch(bot,update,text)
    elif re.match("sms",commands):
        commands=commands.replace("sms","").replace(" ","")
        text = commands.split(' ')
        
        sender(update,"Target: {}".format(text[0]))
        bomb(bot,update,text)

    elif re.match("verify",commands):
        commands=commands.replace("verify","").replace(" ","")
        text = commands.split(' ')
        
        sender(update,"Password Entered: {}".format(text[0]))
        verify(bot,update,text)

    elif re.match("help",commands):
        help(bot,update)

    elif re.match("exit",commands):
        exit(bot,update)

    elif re.match("youtube",commands):
        text=[]
        commands=commands.replace("youtube","")
        text.append(commands)
        ippsec(bot,update,text)  
        
    else:
        sender(update,"Process failed try again :(\nraw output: {}".format(commands))    

def help(bot,update):
    sender(update,"- /verify <password>\n- /cmd <command>\n- /exit\n- /track <phone-number-with-country-prefix>\n- /bomber <indian-phone-number-without-country-code\n- /shodan <For instructions>\n- /voice <For instructions>\n- /youtube <keyword-to-search-in-ippsec-videos>")

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler) 


def voice_help(bot,update):
    sender(update,"[Below commands should be spoken clearly and you can only use voice command and control from personal chat with bot and by replying to bot in group chats]\n\n[To start chat with bot click here:- \n\nhttps://telegram.me/callmedaddbot ]\n- help\n- verify <password>\n- sms <number to bomb>\n- shodan find/ip <ip/http/ftp/service>\n- cmd <command-to-execute>\n- youtube <keyword-to-search-in-ippsec-videos>\n- exit ")

voicehelp_handler = CommandHandler('voice', voice_help)
dispatcher.add_handler(voicehelp_handler) 

def cmd(bot,update,args):
    if update.message.from_user.id in enabled_users:
        if args:
            command=""
            for i in range(len(args)):
                command+=args[i]
                command+=" "
            output = sp.getoutput(command)
            sender(update,output)
        else:
            sender(update,"Enter a command dumbass !!")
    else:
        banned(update)

caps_handler = CommandHandler('cmd', cmd, pass_args=True)
dispatcher.add_handler(caps_handler) 


def callsearch(bot,update,args):
    if update.message.from_user.id in enabled_users:
        if args:
            args=args[0].replace("+","")
            r=requests.get("http://apilayer.net/api/validate?access_key=<token>&number={}&country_code=&format=1".format(args))
            data=json.loads(r.text)
            sendback="Phone Number:-{}\nCountry Prefix:-{}\nLocation:-{}\nCountry:-{}\nCarrier:-{}".format(data['international_format'],data['country_prefix'],data['location'],data['country_name'],data['carrier'])
            sender(update,sendback)
    else:
        banned(update)
call_handler = CommandHandler('track', callsearch, pass_args=True)
dispatcher.add_handler(call_handler) 

def bomb(bot,update,args):
    if update.message.from_user.id in enabled_users:
        if args:
            num=args[0].replace("+91","")
            threading.Thread(target=kill,args=(num,)).start()
            sender(update,"Hiroshima is Done for, sire :)")
        else:
            sender(update,"/bomber <indian-phone-number-without-country-code")    
    else:
        banned(update)

bomb_handler = CommandHandler('bomber', bomb, pass_args=True)
dispatcher.add_handler(bomb_handler) 

def shodansearch(bot,update,args):
    if update.message.from_user.id in enabled_users:
        if args:
            if len(args)<=2:
                if args[0]=="ip":
                    try:
                        a=api.host('{}'.format(args[1]))
                        ports=str(a['ports']).replace("[","").replace("]","")
                        a="ip:{}\nports opened:{}\nCity:{}\ncountry code:{}\nISP:{}\nlongitude:{}\nlatitude:{}".format(a['ip_str'],ports,a['data'][0]['location']['city'],a['data'][0]['location']['country_code3'],a['isp'],a['longitude'],a['latitude'])
                        sender(update,a)
                    except:
                        sender(update,"No information available on this ip")
                if args[0]=="find":
                    query=str(args[1])
                    
                    a=api.search(query,page=1,limit=3)
                    for i in a['matches']:
                        s="\norganistaion {}\nISP: {}\nIP: {}\n".format(i['org'],i['isp'],i['ip_str'])
                        sender(update,s)
            elif len(args)>2:            
                if args[0]=="find" and args[1]=="limit":
                    limits=int(args[2])
                    if limits<=10:
                        query=str(args[3])
                        a=api.search(query,page=1,limit=limits)
                        for i in a['matches']:
                            s="\norganistaion {}\nISP: {}\nIP: {}\n".format(i['org'],i['isp'],i['ip_str'])
                            sender(update,s)
                    else:
                        sender(update,"Limit Crossed")                             
        else:
            a="- /shodan ip <ipaddress>\n- /shodan find <http/ssh/ftp/port/city/software> [MAX LIMIT 3]\n- /shodan find limit <enter b/w 1 to 10> <http/ssh/ftp/port/city/software>  [MAX LIMIT 10]" 
            sender(update,a)       
    else:
        banned(update)            

shodan_handler = CommandHandler('shodan', shodansearch, pass_args=True)
dispatcher.add_handler(shodan_handler) 




updater.start_polling()
