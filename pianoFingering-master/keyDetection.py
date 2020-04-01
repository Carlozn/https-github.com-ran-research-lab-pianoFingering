import numpy as np 
import cv2 as cv
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from operator import itemgetter
import statistics
from numpy import array

def colorShow(img):
    plt.figure(figsize = (9,6))
    # plt.show(img)
    
def bwShow(img):
    plt.figure(figsize = (6,4))
    # plt.show(img)

# fileName = "images/examples/piano-from-above-samiksa-art.jpg"
# fileName = "images/examples/blackkeybd.jpg"
# fileName = "images/examples/redkbd.jpg"
# fileName = "images/examples/paul01.jpg"
fileName = "images/examples/piano02.jpg"
# fileName = "images/examples/1.jpg"
# fileName = "images/examples/2.jpg" #No identifica nota y pone los contours en los lower edges de las negras
# fileName = "images/examples/3.jpg" #identifica nota pero no los contours (los pone mal)
# fileName = "images/examples/4.jpg"
# fileName = "images/examples/pianoposter.jpg"
#fileName = "images/examples/pianoposter2.jpg"
img = cv.imread(fileName,-1)




# text = []
coords = [] 
topBar = 10

def onclick(event):
    tx = 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f' % (event.button, event.x, event.y, event.xdata, event.ydata)
    # text.set_text(tx)
    coords.append([event.xdata, event.ydata])

def pickPoints():
    fig = plt.figure(figsize = (9,6))
    ax = fig.add_subplot(111)
    plt.xticks([]), plt.yticks([])
    ax.imshow(img)
    # text=ax.text(0,0, "", va="bottom", ha="left")
    # coords = []
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

def cropAndFilter():
    crop_img = img[int(coords[0][1]):int(coords[1][1]), int(coords[0][0]):int(coords[1][0])]

    imgBW = cv.cvtColor(crop_img, cv.COLOR_BGR2GRAY) 
    imgBW = cv.medianBlur(imgBW, 5)
    thresh1 = cv.threshold(imgBW, 120, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)[1] 

    marron = thresh1

    # the number of lines added to the top to distinguish the keys
    topBar = 10

    marron = np.append(topBar*[[255]*thresh1.shape[1]],(thresh1))
    marron = marron.reshape(thresh1.shape[0]+topBar,thresh1.shape[1])

    marron = marron.astype(int)
    marron = np.array(marron,dtype='uint8')
                    
    # bwShow(marron)
    fig = plt.figure(figsize = (9,6))
    ax = fig.add_subplot(111)
    ax.imshow(marron)
    plt.show()
    return marron

def findKeys(filtered):
    im2, contours, hierarchy = cv.findContours(filtered, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    fig,ax = plt.subplots(1)

    plt.figure(figsize = (9,6))
    ax.figure.set_size_inches(19,16)

    ax.imshow(img,cmap='gray', vmin=0, vmax=255,interpolation='nearest', aspect='auto')
        #plt.figure(figsize = (9,6))
        #plt.imshow(img, cmap='gray', vmin=0, vmax=255,interpolation='nearest', aspect='auto')

    listOfAreas = []
    for p in contours:
        listOfAreas.append(cv.contourArea(p))
    medianArea = statistics.median(listOfAreas)
    deltaX = int(coords[0][0]) 
    deltaY = int(coords[0][1]) - topBar

    centroidXList = []
    i = 0
    for p in contours:
        if cv.contourArea(p) < 10 * medianArea and cv.contourArea(p) > .1 * medianArea:
            reshapedP = p.reshape(p.shape[0],2)
            reshapedP = reshapedP + [int(coords[0][0]),deltaY]
            
            M = cv.moments(p)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            centroid = [cx + deltaX,cy + deltaY]
            
            centroidXList.append([ centroid[0], i ]);
            
            poly = patches.Polygon(reshapedP,linewidth=1,edgecolor='r',facecolor='none')
            ax.add_patch(poly)
            circ = patches.Circle(centroid,radius=5,edgecolor='b',facecolor='g')
            ax.add_patch(circ)
        i = i + 1

            

    centroidXList = sorted(centroidXList, key=itemgetter(0))
    print(centroidXList)

    diffList = []
    for i in range(len(centroidXList)-1):
        diffList.append(centroidXList[i + 1][0] - centroidXList[i][0])

    print(diffList)
    maxVal =  max(diffList)
    minVal =  min(diffList)
    halfVal = (maxVal + minVal) / 2

    meanLow = statistics.mean([x for x in diffList if x <= halfVal])
    meanHigh = statistics.mean([x for x in diffList if x > halfVal])

    distList = []
    for i in diffList:
        if abs(i - meanLow) < abs(i - meanHigh):
            distList.append(0)
        else:
            distList.append(1)

    print(meanLow, meanHigh)
    print(distList)
    plt.hist(diffList)
            
    distNoteMap = {'10100': "Bb", '01001': "C#", '10010': "D#", '00101': "F#",'01010': "G#"}

    stDistChunck = ''.join(str(e) for e in distList[0:5])

    print(stDistChunck)
    if stDistChunck in distNoteMap:
        print(distNoteMap[stDistChunck])


    plt.show()


pickPoints()
filtered = cropAndFilter()
#Code goes here
rows = filtered.shape[0]
columns = filtered.shape[1]
sum_vector = np.zeros(rows)
for i in range(0,rows):
    for j in range(0,columns):
        sum_vector[i] += filtered[i,j]
        
#standard deviation from the vector holding the sum from the image rows
std = np.std(sum_vector) 
#mean of the vector holding the sum from the image rows
mean = np.mean(sum_vector) 
#Index where the abrupt change happens in sum_vector
cut_index = 0
#This for loop gives me the index where the abrupt change happens in the sum_vector
for index, cell in enumerate(sum_vector):
      if(np.absolute(cell - mean) > (2 * std)):
            cut_index = index 
            break
            


for i in range(cut_index,rows):
    for j in range(0,columns):
        filtered[i,j] = 255

findKeys(filtered)



