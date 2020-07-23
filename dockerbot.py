import time
import re
import random
import datetime
from datetime import timedelta
import telepot
from subprocess import call
import subprocess
import os
import sys
import docker
from telepot.loop import MessageLoop
import requests

def getCommandHelp(line):
    if "#[" in line:
        start = line.find("#[") + len("]#")
        end = line.find("]#")
        return line[start:end]
    return ""

def uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        days = divmod(uptime_seconds, 86400)
        hours = divmod(days[1], 3600)
        minutes = divmod(hours[1], 60)
        return "up %i days, %i hours, %i minutes, %i seconds" % (days[0], hours[0], minutes[0], minutes[1])

#Auto Commmand List
def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                if ("/?" not in line and not "o/" in line and not "," in line):
                    command = line
                    number = command.rfind("/")
                    command = command[number:]
                    number = command.rfind("'")
                    command = command[:number]
                    command = command + " " + getCommandHelp(line)  +"\n"
                    # If yes, then add the line number & line as a tuple in the list
                    list_of_results.append(command)
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    if 'ALLOWED_IDS' not in os.environ or os.environ['ALLOWED_IDS'] == '':
      try:
          with open(os.environ['ALLOWED_IDS_FILE']) as fp:
              allowed_ids = fp.read().replace(',','\n').split()
      except KeyError:
        print("ALLOWED_IDS_FILE not specified")
        sys.exit()
    else:
      allowed_ids = os.environ['ALLOWED_IDS']

    if str(chat_id) not in allowed_ids:
        bot.sendPhoto(chat_id,"https://github.com/t0mer/dockerbot/raw/master/No-Trespassing.gif")
        return ""

    print ('Got command: %s' % command)
    if command == '/time': #[ Get local time ]#
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    if command == '/uptime': #[ Get uptime ]#
        bot.sendMessage(chat_id, uptime())
    elif command == '/speed': #[ Run Speedtest ]#
        x = subprocess.check_output(['speedtest-cli','--share']).decode('utf-8')
        photo = re.search("(?P<url>https?://[^\s]+)", x).group("url")
        bot.sendPhoto(chat_id,photo)
    elif command == '/ip': #[ Get public IP ]#
        #x = subprocess.check_output(['curl','ipinfo.io/ip'])
        x = requests.get('http://ipinfo.io/ip').content
        bot.sendMessage(chat_id,x)
    elif command == '/disk': #[ Get disk space ]#
        x = subprocess.check_output(['df', '-h'])
        bot.sendMessage(chat_id,x)
    elif command == '/mem': #[ Get memeory ]#
        x = subprocess.check_output(['cat','/proc/meminfo'])
        bot.sendMessage(chat_id,x)
    elif command == '/stat': #[ Get bot status ]#
        bot.sendMessage(chat_id,'Number five is alive!')
    elif command == '/list_containers': #[ List docker containers status ]#
        try:
            client = client = docker.from_env()
            containers = client.containers.list(all=True)
            for f in containers:
                bot.sendMessage(chat_id,str(f.name) + " : " + str(f.status) + "\n( /" +f.name +"_restart \n /" +f.name +"_stop \n /" +f.name +"_start )")
        except Exception as e:
            x = str(e)
            bot.sendMessage(chat_id,x)
    elif '_restart' in command:
        try:
            commands = command.split('_')
            commands[0] = commands[0].replace('/','')
            client = client = docker.from_env()
            containers = client.containers.list(all=True, filters={'name':commands[0]})
            bot.sendMessage(chat_id,'Restarting ' + commands[0])
            containers[0].restart()
            time.sleep(5)
            bot.sendMessage(chat_id, commands[0] + ' is: ' + containers[0].status)
        except Exception as e:
            x = str(e)
            bot.sendMessage(chat_id,x)
    elif '_stop' in command:
        try:
            commands = command.split('_')
            commands[0] = commands[0].replace('/','')
            client = client = docker.from_env()
            containers = client.containers.list(all=True, filters={'name':commands[0]})
            bot.sendMessage(chat_id,'Stopping ' + commands[0])
            containers[0].stop()
            time.sleep(5)
            bot.sendMessage(chat_id, commands[0] + ' is: ' + containers[0].status)
        except Exception as e:
            x = str(e)
            bot.sendMessage(chat_id,x)
    elif '_start' in command:
        try:
            commands = command.split('_')
            commands[0] = commands[0].replace('/','')
            client = client = docker.from_env()
            containers = client.containers.list(all=True, filters={'name':commands[0]})
            bot.sendMessage(chat_id,'Starting ' + commands[0])
            containers[0].start()
            time.sleep(5)
            bot.sendMessage(chat_id, commands[0] + ' is: ' + containers[0].status)
        except Exception as e:
            x = str(e)
            bot.sendMessage(chat_id,x)
    elif command in { '/?', "/start" }:
        array = search_string_in_file(__file__, "/")
        s = "Command List:\n"
        for val in array:
            if ")" not in val:
                s+=str(val)
        x = s
        bot.sendMessage(chat_id,x)

if 'API_KEY' not in os.environ or os.environ['API_KEY'] == '':
  try:
    f = open(os.environ['API_KEY_FILE'])
    bot = telepot.Bot(f.read().rstrip())
    f.close()
  except KeyError:
    print("API_KEY_FILE not specified")
    sys.exit()
else:
  bot = telepot.Bot(os.environ['API_KEY'])

MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')

while 1:
    time.sleep(10)
