import time
from getJson import *
import smtplib
from twilio.rest import Client


def getData(ips, levels, warnings):
    type = 'm'
    for i in range(len(ips)):
        if i == 1:
            type = "th"
        elif i == 2:
            type = "l"
        for j in range(len(ips[i])):
            levels[i][j] = get(ips[i][j], type)
            print(ips[i][j])
            checkLevel(ips, levels, warnings, levels[i][j], type, j)

def checkLevel(ips, levels, warnings, data, which, j):
    if which == 'm':
        if data < 1000:
            warnings[0][j] = -1
    elif which == 'th':
        for i in range(len(data)):
            if i == 0:
                curr = data[i][1]
                if curr < 1000:
                    warnings[1][j][i] = -1
                elif curr > 95:
                    warnings[1][j][i] = -2
            elif i == 1:
                curr = data[i]
                if curr < 1000:
                    warnings[1][j][i] = -1
                elif curr > 95:
                    warnings[1][j][i] = -2
    elif which == 'l':
        for i in range(len(data)):
            curr = data[i]
            if i == 0:
                curr = data[i]
                if curr < 1000:
                    warnings[2][j][i] = -1
                elif curr > 95:
                    warnings[2][j][i] = -2
            elif i == 1:
                if curr < 1000:
                    warnings[2][j][i] = -1
                elif curr > 95:
                    warnings[2][j][i] = -2

def createMessage(warnings, levels):
    header = "ALERT! Dangerous conditions in Green House\n==========================================\n"
    message = ""
    for i in range(len(warnings)):
        for j in range(len(warnings[i])):
            if i == 0:
                state = warnings[i][j]
                kind = "Moisture"
                if state == -1:
                    level = "low"
                    num = j + 1
                    val = levels[i][j]
                    message += "%s level dangerously %s at sensor #%d ( %d ).\n" % (kind, level, num, val)
            else:
                for k in range(len(warnings[i][j])):
                    state = warnings[i][j][k]
                    if state != 0:
                        if state == -1:
                            level = "low"
                        elif state == -2:
                            level = "high"
                        if i == 1:
                            num = 6 + j
                            if k == 0:
                                kind = "Temperature"
                                val = levels[i][j][k][1]
                            elif k == 1:
                                kind = "Humidity"
                                val = levels[i][j][k]
                        elif i == 2:
                            num = 8 + j
                            if k == 0:
                                kind = "Light intensity"
                            elif k == 1:
                                kind = "UV light"
                            val = levels[i][j][k]
                    message += "%s level dangerously %s at sensor #%d ( %d ).\n" % (kind, level, num, val)
    if message:
        sendAlerts(header + message)

def sendAlerts(text):
    print("sending")
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login('DUGreenhouseAlerts@gmail.com', 'TeamGreen4')
    mail.sendmail('DUGreenhouseAlerts@gmail.com', 'salcbrau@my.dom.edu', text)
    mail.close()

    account_sid="ACc3ef768bb932aa094df21c031c070e84" #you get this from your twilio account
    auth_tokken="9bbc933b853e34e50250fdbc1e60db07"#you also get this
    client = Client(account_sid, auth_tokken)
    message = client.api.account.messages.create(to="+16307475480",from_="+17738325163",body=text)
                    
if __name__ == '__main__':
    warnings = [[0, 0, 0, 0, 0],[[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0]]]
    levels = [[0, 0, 0, 0, 0],[[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0]]]

    MIN_MOIST = 50
    MIN_TEMP = 40
    MIN_HUMI = 20
    MAX_TEMP = 95
    MAX_HUMI = 90
    print(warnings)
    while(True):
        getData(ips, levels, warnings)
        createMessage(warnings, levels)
        time.sleep(5)
