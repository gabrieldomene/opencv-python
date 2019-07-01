import numpy as np
import math
import copy

#         y, x

def main():
    print("--> Reader for PGM/PPM images <--")
    name = input('Enter file name: ')
    if(name.endswith('.pgm')):
        print('File [{0}] loaded, select the options from menu below.\n' .format(name))
        print('[1] - Threshold      [2] - Double Threshold\n[3] - Inverse Gray   [4] - Add Gray')
        print('[5] - Contrast       [6] - ImageG\n')
        menu = int(input('Choose number, 0 for exit: '))
        pgmImage = PGM(name)

        name_tmp = name.split('.')
        output = name_tmp[0] + '-out.pgm'

        data_matriz = pgmImage.readPGM()
        while(menu != 0):
            if(menu == 1):
                result = pgmImage.threshold(data_matriz)
            elif(menu == 2):
                result = pgmImage.thresholdDouble(data_matriz)
            elif(menu == 3):
                result = pgmImage.inverseGray(data_matriz)
            elif(menu == 4):    
                result = pgmImage.addGray(data_matriz)
            elif(menu == 5):
                result = pgmImage.contrastGray(data_matriz, 0.7)
            elif(menu == 6):    
                print('Option 6')
                # result = pgmImage.imageG(result)
            menu = int(input('Choose new option, 0 for exit: '))
        pgmImage.savePGM(output, result)
    elif(name.endswith('.ppm')):
        print('.ppm file loaded')
        ppmImage = PPM(name)

        name_temp = name.split('.')
        output = name_temp[0] + '-out2.ppm'

        data_matriz = ppmImage.readData()
        #  -----------------Manipulating pixels -------------
     
        flood_result = ppmImage.flood(0, 0, data_matriz)

        # result_conv = ppmImage.linear(data_matriz)
        # result = ppmImage.linear(result)
        # result = ppmImage.linear(result)
        # result = ppmImage.linear(result)
        # result_conv = ppmImage.l2Norm('points.txt', data_matriz)
        # ppmImage.l1Norm('points.txt')
        # result_color = ppmImage.addColor(0, 25, 0, data_matriz)
        # result_inverse = ppmImage.inverseColor(data_matriz)
        # result_gray = ppmImage.rgb2gray(data_matriz)
        # result = ppmImage.selectiveFilter(data_matriz)

        # ------------------SAVING FILES --------------------
        # ppmImage.savePPM(output, result)
        # ppmImage.savePPM(output, result_color)
        # ppmImage.savePPM(output, result_inverse)
        # ppmImage.savePPM(output, result_gray)
        # ppmImage.savePPM(output, flood_result)
    else:
        print('Invalid format')
    

class PGM:  
    def __init__(self, name):
        self.name = name
        self.tipo = ''
        self.width = 0
        self.height = 0
    
    def __str__(self):
        return self.name

    # Gray image methods
    def readPGM(self):
        f = open(self.name, 'r')
        contentList = []

        for line in f:
            contentList.append(line.strip())
        self.tipo = contentList.pop(0)
        temp = contentList.pop(0)
        info = []
        info = temp.split(' ')
        self.width = int(info[0])
        self.height = int(info[1])
        self.maxValue = int(info[2])
        contentList = list(map(int, contentList))
        f.close()

        return contentList
    
    def savePGM(self, name, data):
        print('Saving image...')
        f = open(name, 'w')
        f.write('P2\n')
        f.write('{0} {1} {2}\n' .format(self.width, self.height, self.maxValue))
        # np.savetxt(name, self.dataMatriz, fmt="%s")
        for element in data:
            f.write('{0}\n' .format(element))
        # for i in range(self.width):
        #     for j in range(self.height):
        #         f.write('{0}\n' .format(self.dataMatriz[i][j]))
        f.close()

    def threshold(self, data):
        th = int(input('Insert threshold value: '))
        if(th >= 0 and th <= 255):
            print('Applying threshold...')
            for i in range(0, self.width*self.height):
                    if(data[i] < th):
                        data[i] = 0
                    else:
                        data[i] = 255
        else:
            print('Th fora do padrão')

        return data 
    
    def thresholdDouble(self, data):
        th1 = int(input('Insert value threshold 1: '))
        th2 = int(input('Insert value threshold 2: '))
        if(th1 <= 255 and th1 >= 0 and th2 >= 0 and th2 <= 255):    
            print('Applying double threshold...')
            for i in range(0, self.width*self.height):
                if(data[i] > th1):
                    data[i] = 0
                elif((data[i] >= th2) and (data[i] <= th1)):
                    data[i] = 128
                else:
                    data[i] = 0
        else:
            print('Os valores devem ser entre 0-255, th1 = {0} th2 = {1}' .format(th1, th2))
        
        return data
    
    def addGray(self, data):
        value = int(input('Insert upscale value: '))
        if(type(value) == int):    
            print('Upscalling pixels by {0}' .format(value))
            for i in range(0, self.height*self.width):
                if(data[i] + value > 255):
                    data[i] = 255
                elif(data[i] + value < 0):
                    data[i] = 0
                else:
                    data[i] += value
        else:
            print('Value must be int')
        
        return data
    
    def inverseGray(self, data):
        print('Inversing gray...')
        for i in range(0, self.width*self.height):
            data[i] = 255 - data[i]

        return data
    
    def contrastGray(self, data, contrast):
        print('Contrast...')
        for i in range(0, self.height*self.width):
            if ((data[i]*contrast) > 255):
                data[i] = 255
            else:
                data[i] = int(data[i]*contrast)
        return data
    
    def imageG(self, data):
        print(data[:10])

class PPM:
    def __init__ (self, name):
        self.name = name
        self.tipo = ''
        self.width = 0
        self.height = 0
        self.maxValue = 0
        self.matriz = []
        self.lista = []

    def readData(self):
        file_data = open(self.name, 'r')
        content = file_data.readlines()
        
        count = 0
        listContent = []

        for line in content:
            if(count < 2):
                listContent.append(line.replace('\n', ''))
                count += 1
            else:
                listContent.append(int(line.replace('\n', '')))

        self.tipo = listContent[0]
        self.width, self.height, self.maxValue = listContent[1].split(' ')
        self.width = int(self.width)
        self.height = int(self.height)
        self.maxValue = int(self.maxValue)
        del listContent[:2]
        # Armazena nova lista, independente da antiga
        
        self.dataMatriz = listContent[:]
        dataRead = copy.deepcopy(listContent)
        self.mapa = [0]*self.width*self.height*3

        return dataRead
    
    # Older read file
    def readPPM(self):
        file_data = open(self.name, 'r')
        contentList = []

        for line in file_data:
            contentList.append(line.strip())
        self.tipo = contentList.pop(0)
        (self.width, self.height, self.maxValue) = [int(x) for x in contentList[0].split(" ")]
        self.matrizLength = self.width*self.height*3
        contentList.pop(0)
        self.dataMatriz = np.zeros((self.width*self.height)*3, int)
        for i in range(0, len(contentList)-3, 3):
            self.dataMatriz[i] = contentList[i]
            self.dataMatriz[i+1] = contentList[i+1]
            self.dataMatriz[i+2] = contentList[i+2]

    def savePPM(self, name, data):
        print('Saved as ' + name)
        f = open(name, 'w')
        f.write('P3\n')
        f.write('{0} {1} {2}\n' .format(self.width, self.height, self.maxValue))
        for i in range(0, len(data)):
            f.write('{0}\n' .format(data[i]))
        f.close()

    def addColor(self, valueR, valueG, valueB, data):
        print('Adding color...')
        outMatriz = data[:]
        
        for i in range(0, self.height):
            for j in range(0, self.width):

                if((data[i*self.width*3 + j*3] + valueR) > 255):
                    outMatriz[i*self.width*3 + j*3] = 255
                elif((data[i*self.width*3 + j*3] + valueR) < 0):
                    outMatriz[i*self.width*3 + j*3] = 0
                else:
                    outMatriz[i*self.width*3 + j*3] += valueR

                if((data[i*self.width*3 + j*3+1] + valueG) > 255):
                    outMatriz[i*self.width*3 + j*3+1] = 255
                elif((data[i*self.width*3 + j*3+1] + valueG) < 0):
                    outMatriz[i*self.width*3 + j*3+1] = 0
                else:
                    outMatriz[i*self.width*3 + j*3+1] += valueG
                
                if((data[i*self.width*3 + j*3+2] + valueB) > 255):
                    outMatriz[i*self.width*3 + j*3+2] = 255
                elif((data[i*self.width*3 + j*3+2] + valueB) < 0):
                    outMatriz[i*self.width*3 + j*3+2] = 0
                else:
                    outMatriz[i*self.width*3 + j*3+2] += valueB
        
        return outMatriz

    def inverseColor(self, data):
        print('Inversing colors...')
        outMatriz = [0]*self.width*self.height*3

        for i in range(len(data)):
            outMatriz[i] = 255 - data[i]
        
        return outMatriz

    def rgb2gray(self, data):
        print('Converting to gray')
        outMatriz = [0]*self.width*self.height*3
        # 0.2126 R + 0.7152 G + 0.0722 B
        for i in range(self.height):
            for j in range(self.width):
                indexR = i*self.width*3 + j*3
                indexG = i*self.width*3 + j*3+1
                indexB = i*self.width*3 +j*3+2

                value = int(0.2126*data[indexR] + 0.7152*data[indexG]
                + 0.0722*data[indexB])

                indexGray = i*self.width+j
                outMatriz[indexGray] = value

        return outMatriz

    def l2Norm(self, file_name, data_matriz):
        # Abertura dos pontos médios
        data = open(file_name, 'r')
        points = []
        r, g, b = 0, 0, 0
        for line in data:
            points.append(line.strip())


        data.close()
        for i in points:
            temp = i.split(' ')
            r += int(temp[0])
            g += int(temp[1])
            b += int(temp[2])
        rMed = int(r/len(points))
        gMed = int(g/len(points))
        bMed = int(b/len(points))

        pointRef = []
        pointRef.append(rMed)
        pointRef.append(gMed)
        pointRef.append(bMed)

        soma = 0
        dist = 0

        for i in range(0, self.height):
            for j in range(0, self.width):
                soma = (data_matriz[i*self.width*3 + j*3] - pointRef[0]) * (data_matriz[i*self.width*3 + j*3] - pointRef[0]) + (data_matriz[i*self.width*3 + j*3+1] - pointRef[1]) * (data_matriz[i*self.width*3 + j*3+1] - pointRef[1]) + (data_matriz[i*self.width*3 + j*3+2] - pointRef[2]) * (data_matriz[i*self.width*3 + j*3+2] - pointRef[2])

                dist = int(math.sqrt(soma))

                if (dist < 50):
                    data_matriz[i*self.width*3 + j*3] = 255
                    data_matriz[i*self.width*3 + j*3+1] = 0
                    data_matriz[i*self.width*3 + j*3+2] = 0
    
        return data_matriz

    def l1Norm(self, file_name):
        data = open(file_name, 'r')
        points = []
        r, g, b = 0, 0, 0

        for line in data:
            points.append(line.strip())
        
        data.close()

        for i in points:
            temp = i.split(' ')
            r += int(temp[0])
            g += int(temp[1])
            b += int(temp[2])

        rMed = int(r/len(points))
        gMed = int(g/len(points))
        bMed = int(b/len(points))

        pointRef = []
        pointRef.append(rMed)
        pointRef.append(gMed)
        pointRef.append(bMed)

        dist = 0
        for i in range(0, self.height):
            for j in range(0, self.width):
                # r = self.dataMatriz[i*self.width*3 + j*3]
                # g = self.dataMatriz[i*self.width*3 + j*3+1]
                # b = self.dataMatriz[i*self.width*3 + j*3+2]

                dist = abs(self.dataMatriz[i*self.width*3 + j*3] - pointRef[0]) + abs(self.dataMatriz[i*self.width*3 + j*3+1] - pointRef[1]) + abs(self.dataMatriz[i*self.width*3 + j*3+2] - pointRef[2])

                if (dist < 100):
                    self.dataMatriz[i*self.width*3 + j*3] = 0
                    self.dataMatriz[i*self.width*3 + j*3+1] = 0
                    self.dataMatriz[i*self.width*3 + j*3+2] = 0

    def linear(self, data):
        # Matriz de entrada * kernel = output Matriz
        # Porque uma mudança da lista está alterando as outras
        outMatriz = [0]*self.width*self.height*3
        kernelSum = 0
        
        kernel = [[1,1,1],[1,1,1],[1,1,1]]

        for i in kernel:
            temp = 0
            for j in i:
                temp += j
            kernelSum += temp
        kernelWeight = 1/kernelSum
        
        # Data é a matriz que eu recebo
        for i in range(1, self.height-1):
            for j in range(1, self.width-1):
                
                indexR = i*self.width*3 + j*3
                indexG = i*self.width*3 + j*3+1
                indexB = i*self.width*3 + j*3+2

                # for i in range(0, len(kernel)):
                #     for j in range(0, len(kernel)):
                #         outMatriz[indexR] = 
                # Variança dentro do kernel
                outMatriz[indexR] = int((data[(i-1)*self.width*3+(j-1)*3]*kernel[0][0]
                + data[(i-1)*self.width*3+(j+0)*3]*kernel[0][1]
                + data[(i-1)*self.width*3+(j+1)*3]*kernel[0][2]
                + data[(i+0)*self.width*3+(j-1)*3]*kernel[1][0]
                + data[(i+0)*self.width*3+(j+0)*3]*kernel[1][1]
                + data[(i+0)*self.width*3+(j+1)*3]*kernel[1][2]
                + data[(i+1)*self.width*3+(j-1)*3]*kernel[2][0]
                + data[(i+1)*self.width*3+(j+0)*3]*kernel[2][1]
                + data[(i+1)*self.width*3+(j+1)*3]*kernel[2][2]) * kernelWeight)

                outMatriz[indexG] = int((data[(i-1)*self.width*3+(j-1)*3+1]*kernel[0][0]
                + data[(i-1)*self.width*3+(j+0)*3+1]*kernel[0][1]
                + data[(i-1)*self.width*3+(j+1)*3+1]*kernel[0][1]
                + data[(i+0)*self.width*3+(j-1)*3+1]*kernel[1][0]
                + data[(i+0)*self.width*3+(j+0)*3+1]*kernel[1][1]
                + data[(i+0)*self.width*3+(j+1)*3+1]*kernel[1][2]
                + data[(i+1)*self.width*3+(j-1)*3+1]*kernel[2][0]
                + data[(i+1)*self.width*3+(j+0)*3+1]*kernel[2][1]
                + data[(i+1)*self.width*3+(j+1)*3+1]*kernel[2][2]) * kernelWeight)

                outMatriz[indexB] = int((data[(i-1)*self.width*3+(j-1)*3+2]*kernel[0][0]
                + data[(i-1)*self.width*3+(j+0)*3+2]*kernel[0][1]
                + data[(i-1)*self.width*3+(j+1)*3+2]*kernel[0][1]
                + data[(i+0)*self.width*3+(j-1)*3+2]*kernel[1][0]
                + data[(i+0)*self.width*3+(j+0)*3+2]*kernel[1][1]
                + data[(i+0)*self.width*3+(j+1)*3+2]*kernel[1][2]
                + data[(i+1)*self.width*3+(j-1)*3+2]*kernel[2][0]
                + data[(i+1)*self.width*3+(j+0)*3+2]*kernel[2][1]
                + data[(i+1)*self.width*3+(j+1)*3+2]*kernel[2][2]) * kernelWeight)
                
        return outMatriz

    def selective_filter(self, data):
        outMatriz = [0]*self.width*self.height*3
        kernelSum = 0
        
        kernel = [[1,1,1],[1,1,1],[1,1,1]]

        for i in kernel:
            temp = 0
            for j in i:
                temp += j
            kernelSum += temp
        kernelWeight = 1/kernelSum
        
        for i in range(1, self.height-1):
            for j in range(1,self.width-1):
                
                med_r = data[(i+0)*self.width*3+(j+0)*3]

                var_r = 0
                # print('Pixel value: {0}{1} = {2}' .format(i, j, med_r))
                
                # print('''                    {0}  {1}  {2}
                #     {3} {4} {5}
                #     {6} {7} {8}
                # '''.format(data[(i-1)*self.width*3+(j-1)*3], data[(i-1)*self.width*3+(j-0)*3], data[(i-1)*self.width*3+(j+1)*3], data[(i-0)*self.width*3+(j-1)*3], data[(i-0)*self.width*3+(j-0)*3],data[(i-0)*self.width*3+(j+1)*3], data[(i+1)*self.width*3+(j-1)*3], data[(i+1)*self.width*3+(j-0)*3], data[(i+1)*self.width*3+(j+1)*3]))

                indexR = i*self.width*3 + j*3
                indexG = i*self.width*3 + j*3+1
                indexB = i*self.width*3 + j*3+2

                var_r = (data[(i-1)*self.width*3+(j-1)*3] - med_r)**2 + (data[(i-1)*self.width*3+(j+0)*3] - med_r)**2 + (data[(i-1)*self.width*3+(j+1)*3] - med_r)**2 + (data[(i+0)*self.width*3+(j-1)*3] - med_r)**2 + (data[(i+0)*self.width*3+(j+0)*3] - med_r)**2 + (data[(i+0)*self.width*3+(j+1)*3] - med_r)**2 + (data[(i+1)*self.width*3+(j-1)*3] - med_r)**2 + (data[(i+1)*self.width*3+(j+0)*3] - med_r)**2 + (data[(i+1)*self.width*3+(j+1)*3] - med_r)**2

                variancia = math.floor(var_r/9)
                desv = math.floor(math.sqrt(variancia))
                # print('[{0}][{1}] = {2}, desv = {3}'.format(i, j,variancia, desv))
                # se desvio padrao for > 10 mudar o kernel

                if (desv > 10):
                    kernel = [[1,1,1],[1,1,1],[1,1,1]]
                    print(desv)
                    for i in range(0, len(kernel)):
                        for j in range(0, len(kernel)):
                            kernel[i][j] = 3*kernel[i][j]
                
                # Variança dentro do kernel
                outMatriz[indexR] = int((data[(i-1)*self.width*3+(j-1)*3]*kernel[0][0]
                + data[(i-1)*self.width*3+(j+0)*3]*kernel[0][1]
                + data[(i-1)*self.width*3+(j+1)*3]*kernel[0][2]
                + data[(i+0)*self.width*3+(j-1)*3]*kernel[1][0]
                + data[(i+0)*self.width*3+(j+0)*3]*kernel[1][1]
                + data[(i+0)*self.width*3+(j+1)*3]*kernel[1][2]
                + data[(i+1)*self.width*3+(j-1)*3]*kernel[2][0]
                + data[(i+1)*self.width*3+(j+0)*3]*kernel[2][1]
                + data[(i+1)*self.width*3+(j+1)*3]*kernel[2][2]) * kernelWeight)

                outMatriz[indexG] = int((data[(i-1)*self.width*3+(j-1)*3+1]*kernel[0][0]
                + data[(i-1)*self.width*3+(j+0)*3+1]*kernel[0][1]
                + data[(i-1)*self.width*3+(j+1)*3+1]*kernel[0][1]
                + data[(i+0)*self.width*3+(j-1)*3+1]*kernel[1][0]
                + data[(i+0)*self.width*3+(j+0)*3+1]*kernel[1][1]
                + data[(i+0)*self.width*3+(j+1)*3+1]*kernel[1][2]
                + data[(i+1)*self.width*3+(j-1)*3+1]*kernel[2][0]
                + data[(i+1)*self.width*3+(j+0)*3+1]*kernel[2][1]
                + data[(i+1)*self.width*3+(j+1)*3+1]*kernel[2][2]) * kernelWeight)

                outMatriz[indexB] = int((data[(i-1)*self.width*3+(j-1)*3+2]*kernel[0][0]
                + data[(i-1)*self.width*3+(j+0)*3+2]*kernel[0][1]
                + data[(i-1)*self.width*3+(j+1)*3+2]*kernel[0][1]
                + data[(i+0)*self.width*3+(j-1)*3+2]*kernel[1][0]
                + data[(i+0)*self.width*3+(j+0)*3+2]*kernel[1][1]
                + data[(i+0)*self.width*3+(j+1)*3+2]*kernel[1][2]
                + data[(i+1)*self.width*3+(j-1)*3+2]*kernel[2][0]
                + data[(i+1)*self.width*3+(j+0)*3+2]*kernel[2][1]
                + data[(i+1)*self.width*3+(j+1)*3+2]*kernel[2][2]) * kernelWeight)
                
        return outMatriz

    def flood(self, i, j, data):
        # empilha primeiro ponto
        # print(self.lista)
        index = i*self.width*3 + j*3
 
        pos = self.validate(i, j, index, data)
        if(pos == 0): 
            print('Erro i={} j={}'.format(i, j))
            # volta pixel
        elif(pos == 1):
            # mapa pra regiao 1
            print('Ponto atual i={} j={}' .format(i, j))
            print('Subiu')
            self.flood(i-1, j, data)
        elif(pos == 2):
            print('Ponto atual i={} j={}' .format(i, j))
            print('Direita')
            self.flood(i, j+1, data)
        elif(pos == 3):
            print('Ponto atual i={} j={}' .format(i, j))
            print('Desceu')
            self.flood(i+1, j, data)
        elif(pos == 4):
            print('Ponto atual i={} j={}' .format(i, j))
            print('Esquerda')
            self.flood(i, j-1, data)
        # print('{} items na pilha' .format(len(self.lista)))
        # print(self.mapa)
        return data

    def validate(self, i, j, index, data):
        # self.mapa[i*self.width*3 +j*3]
        # Up
        
        distUp = int(self.distancia(i, j, i-1, j, data))
        distRight = int(self.distancia(i, j, i, j+1, data))
        distDown = int(self.distancia(i, j, i+1, j, data))
        distLeft = int(self.distancia(i, j, i, j-1, data))

        # th = 30
        print('Distancias: U=[{}] R=[{}] D=[{}] L=[{}]' .format(distUp, distRight, distDown, distLeft))
        print('Validando i={} j={}' .format(i, j))
        if ((i-1 >= 0) and (self.mapa[(i-1)*self.width*3 + j*3] == 0) and (distUp < 10)):
            # Subindo
            # print('Validando x={} y={}' .format(j, i))
            # print(self.distancia(i, j, i-1, j, data))
            
            # marca pixel, marca pai

            self.mapa[index] = 1
            self.mapa[index+1] = 1
            self.mapa[index+2] = 1
            
            return 1
        elif ((j+1 < self.width) and (self.mapa[i*self.width*3 + (j+1)*3] == 0) and (distRight < 10)):
            # Direita
            self.mapa[index] = 2
            self.mapa[index+1] = 2
            self.mapa[index+2] = 2
            return 2
        elif ((i+1 < self.height) and (self.mapa[(i+1)*self.width*3 + j*3] == 0) and (distDown < 10)):

            
            self.mapa[index] = 3
            self.mapa[index+1] = 3
            self.mapa[index+2] = 3
            # Baixo
            return 3
        elif ((j-1 >= 0) and (self.mapa[i*self.width*3 + (j-1)*3] == 0) and (distLeft < 10)):
            # Esquerda
            self.mapa[index] = 4
            self.mapa[index+1] = 4
            self.mapa[index+2] = 4
            return 4
        else:
            return 0
        
    def distancia(self, i, j, y, x, data):
        dist = math.sqrt((data[i*self.width*3 + j*3] - data[y*self.width*3 + x*3])**2 + (data[i*self.width*3 + j*3+1] - data[y*self.width*3 + x*3+1])**2 + (data[i*self.width*3 + j*3+2] - data[y*self.width*3 + x*3+2])**2)
        # print('Dist = {} --- x1={} y1={}------x2={} y2={}\n' .format(int(dist), i, j, x, y))
        return dist


if __name__ == "__main__":
    main()
