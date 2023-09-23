import numpy as np
import pandas as pd
import re

class loadTecPlot:
    def __init__(self, filename):
        self.file = filename
        self.data = np.empty((0), dtype="object")
        self.noI = np.empty((0), dtype="int")
        self.noJ = np.empty((0), dtype="int")
        self.zones = np.empty((0), dtype="object")

    def loadFile(self):
        ndata = 0
        datas = np.empty(0, dtype="float")
        f = open(self.file, 'r')
        for line in f:
            line = line.lstrip()
            if line.startswith('title') or line.startswith('TITLE'):
                title = re.findall('"(.*?)"', line)
            elif line.startswith('variables') or line.startswith('VARIABLES'):
                vars = re.findall('"(.*?)"', line)
                vars = np.array(vars)
                nvars = len(vars)
            elif line.startswith('zone') or line.startswith('ZONE'):
                self.zones = np.append(self.zones, re.findall('"(.*?)"', line))
                self.noI = np.append(self.noI, int(re.findall('[0-9]+', line)[0]))
                self.noJ = np.append(self.noJ, int(re.findall('[0-9]+', line)[1]))
            elif not line:
                continue
            else:
                nums = line.split(' ')
                for num in nums:
                    try:
                        num = float(num)
                    except ValueError:
                        continue
                    datas = np.append(datas, num)
                ndata += 1
        f.close()

        size = np.empty(self.zones.size + 1, dtype="int")
        size[0] = 0
        for i in range(self.zones.size):
            size[i + 1] = size[i] + self.noI[i] * self.noJ[i]
        indicies = np.empty(np.sum(self.noI*self.noJ), dtype="object")
        for i in range(self.zones.size):
            indicies[size[i]:size[i + 1]] = self.zones[i]

        datas = datas.reshape(np.sum(self.noI*self.noJ), nvars)
        self.data = pd.DataFrame(datas, columns=vars, index=indicies)
        print(self.data)
