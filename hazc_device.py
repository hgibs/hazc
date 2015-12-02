#!/usr/local/bin/python3
from zeroconf import Zeroconf, ServiceInfo
import socket
import configparser
import const
import hazc_cmd

class hazc_device:

    def __init__(self, ipaddr):
        self.version = "0.1"
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.MSGLEN = 1024
        self.END_OF_MSG = '*'
        self.ip = ipaddr
        self.buffer = 20
        self.commands = {'version?':self.version_cmd,'commands?':self.commands_cmd,'status?':self.status_cmd}
        
        hcvc = hazc_cmd.hazc_cmd('version?',self.version_cmd
        self.commands2 = {'version?': hcvc, 

    def addFunction(self, name, handler, statushandler):
        self.commands

    def advertise(self):
        postfix = self.config['global']['service_prefix']
        self.port = int(self.config['global']['port'])
        #print(self.config['device']['hostname']+postfix)
        info = ServiceInfo(postfix, self.config['device']['hostname']+postfix,
                       socket.inet_aton(self.ip), self.port, 0, 0,
                       {'info': self.config['device']['description']}, "hazc.local.")

        self.bindConnection()

        zeroconf = Zeroconf()
        zeroconf.register_service(info)


        try:
            while True:
#                 try:
                print("Ready")
                self.conn, self.addr = self.webcontrol.accept()
                self.listen()
                self.conn.close()
        except KeyboardInterrupt:
            pass
        finally:
            print()
            print("Unregistering...")
            zeroconf.unregister_service(info)
            zeroconf.close()

        try:
            print("Shutting down socket")
            self.webcontrol.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(e)

    def listen(self):
        data = bytes()
        rbytes = 0
        while rbytes < self.MSGLEN:
            d = self.conn.recv(self.buffer)
            if not d: break
            data += d
            rbytes += len(d)

#         print data.decode('utf-8')
        self.handledata(data)

    def handledata(self, data):
        command = self.cleanandstringdata(data)
        print('->' + command)

        replystr = "ERROR"

        replystr = self.commands[command]()

        print(replystr)
        self.reply(replystr)


    def reply(self, msg):
        longmsg = msg
        while len(longmsg) < self.MSGLEN:
            longmsg += self.END_OF_MSG
#         print(longmsg)
        self.conn.send(longmsg.encode('utf-8'))

    def cleanandstringdata(self, data):
        dstr = data.decode('utf-8')
        return dstr.strip(self.END_OF_MSG)
        
#     This adds a remotely-called function from the web control with no arguments.
    def addCommand(self, function, title):
        self.commands[title] = function
        
    def addCommand(self, function, title, argument_type):
        self.commands[title] = function
        
    def addStatus(self, function, title):
    

    def bindConnection(self):
        try:
            self.webcontrol = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.webcontrol.bind((self.ip, self.port))
            self.webcontrol.listen(1)
        except OSError as e:
            print(e)
            quit()

    def version_cmd(self):
        return self.version

    def commands_cmd(self):
        rstr = ""
        for key in self.commands:
            rstr += key + ";"
        return rstr

    def status_cmd(self):
        return "some status..."