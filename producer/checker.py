import re
import os

class checker:

    def __init__(self):
        # Rutas configurables por variables de entorno
        self.hosts_file = os.environ.get('HOSTS_FILE', '/app/hosts.txt')
        self.dictionary_file = os.environ.get('DICTIONARY_FILE', '/app/dictionary.txt')

    def getIPs(self, thefile):  # Lee todas las IPs del archivo y devuelve una lista
        logfile = list(open(str(thefile), 'r').read().split('\n'))
        newip = []
        for entry in logfile:
            ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}', entry)
            for ip in ips:
                newip.append(ip)
        return newip

    def readFile(self, thefile):  # Devuelve un diccionario {IP: hostname}
        with open(str(thefile), 'r') as f:  # formato: "IP<space>hostname"
            auxlist = []
            for line in f:
                auxlist.append(line.rstrip())

        dictionary = {}
        for i in range(len(auxlist)):
            if auxlist[i]:  # ignorar líneas vacías
                auxlist[i] = auxlist[i].split(" ")
        dictionary = dict(auxlist)

        return dictionary

    def getHostname(self, IP, thefile):  # Dada una IP, devuelve el hostname
        data = self.readFile(thefile)
        return data.get(IP)

    def getHosts(self):
        hostsList = []
        keylist = self.getIPs(self.hosts_file)  # IPs desde hosts.txt
        for i in range(len(keylist)):
            hostsList.append(self.getHostname(keylist[i], self.dictionary_file))
        return hostsList