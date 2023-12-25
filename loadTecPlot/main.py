import numpy as np
import pandas as pd
import re

class loadTecPlot:
    def __init__(self, filename):
        self.file = filename
        self.noI = np.empty((0), dtype="int")
        self.noJ = np.empty((0), dtype="int")
        self.zones = np.empty((0), dtype="object")

    def loadFile(self):
        ndata = 0
        with open(self.file, 'r') as f:
            data = f.read().splitlines()
        nTitle = [i for i, s in enumerate(data) if "TITLE" in s]
        nVariable = [i for i, s in enumerate(data) if "VARIABLES" in s]
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
