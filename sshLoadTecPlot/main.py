import numpy as np
import pandas as pd
import re
import paramiko

class sshLoadTecPlot:
    def __init__(self, hostname, username, key_filename, data_filename):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(
                hostname=hostname,
                username=username,
                key_filename=key_filename
                )
        self.sftp = self.client.open_sftp()

        self.file = data_filename
        self.noI = np.empty((0), dtype="int")
        self.noJ = np.empty((0), dtype="int")
        self.zones = np.empty((0), dtype="object")

    def checkFile(self):
        try:
            with self.sftp.open(self.file, 'r') as f:
                return True
        except FileNotFoundError:
            return False

    def loadFile(self):
        ndata = 0
        with self.sftp.open(self.file, 'r') as f:
            data = f.read().decode().splitlines()
        nTitle = [i for i, s in enumerate(data) if "TITLE" in s]
        nVariable = [i for i, s in enumerate(data) if "VARIABLE" in s]
        nZone = [i for i, s in enumerate(data) if "ZONE" in s]

        ###    load TITLE    ###
        title = re.findall('"(.*?)"', data[nTitle[0]])

        ###    load VARIABLES    ###
        vars = re.findall('"(.*?)"', data[nVariable[0]])
        vars = np.array(vars)
        nvars = len(vars)

        ###    load ZONE    ###
        self.zones = np.append(self.zones, re.findall('"(.*?)"', data[nZone[0]]))
        self.noI = np.append(self.noI, int(re.findall('[0-9]+', data[nZone[0]])[0]))
        self.noJ = np.append(self.noJ, int(re.findall('[0-9]+', data[nZone[0]])[1]))

        ###    load data    ###
        ### TODOs  extend the method for multiple ZONE data ###
        vals = [i for i in data[nZone[0]+1:] if i != ' ']
        val = map(lambda vallist: vallist.split(), vals)
        datas = np.array(list(val), dtype='float')

        size = np.empty(self.zones.size + 1, dtype="int")
        size[0] = 0
        for i in range(self.zones.size):
            size[i + 1] = size[i] + self.noI[i] * self.noJ[i]
        indicies = np.empty(np.sum(self.noI*self.noJ), dtype="object")
        for i in range(self.zones.size):
            indicies[size[i]:size[i + 1]] = self.zones[i]

        self.data = pd.DataFrame(datas, columns=vars, index=indicies)

    def close(self):
        self.client.close()
