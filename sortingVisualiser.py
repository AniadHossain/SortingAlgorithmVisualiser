import pygame
import math
import random
pygame.font.init()

class info:
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    BLUE = (0,0,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BACKGROUND_COLOUR = BLACK
    GRAD = [
        (128,128,128),
        (160,160,160),
        (190,190,190)
    ]
    SIDE_PAD = 100
    UP_PAD = 150

    FONT = pygame.font.SysFont('comicsans',20)
    LARGE_FONT = pygame.font.SysFont('comicsans',30)

    time = 0

    def __init__(self,width,height,lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Visualiser")
        self.setList(lst)

    def setList(self, lst):
        self.lst = lst
        self.max = max(lst)
        self.min  = min(lst)
        self.blockWidth = int((self.width - self.SIDE_PAD) / len(lst))
        self.blockHeightMultiplier = int((self.height - self.UP_PAD)/(self.max-self.min))
        self.startX = self.SIDE_PAD // 2

    def draw(self):
        self.window.fill(self.BACKGROUND_COLOUR)

        controls = self.FONT.render("R: Reset | A: Ascending| D: Descending | T: Decrease Size | Y: Increase Size",True,self.WHITE)
        sorting = self.FONT.render("B: Bubble | I: Insertion | M: Merge | Q: Quick | H: Heap",True,self.WHITE)
        self.window.blit(controls, ((self.width/2)-(controls.get_width()/2),5))
        self.window.blit(sorting, ((self.width/2)-(sorting.get_width()/2),35))
        
        self.drawLst()
    
    def drawLst(self,colourPos = {}, clearBg = False):
        if clearBg:
            clearRect = (self.SIDE_PAD//2, self.UP_PAD, self.width - self.SIDE_PAD, self.height)
            pygame.draw.rect(self.window,self.BACKGROUND_COLOUR,clearRect)
        
        for i, n in enumerate(self.lst):
            x = self.startX + i * self.blockWidth
            y = self.height - ((n - self.min) * self.blockHeightMultiplier)
            colour = self.GRAD[i%3]
            if i in colourPos:
                colour = colourPos[i]

            pygame.draw.rect(self.window, colour, (x,y, self.blockWidth, self.height))
        pygame.display.update()
        pygame.time.delay(500//len(self.lst))


def generateRandomArray(numberOfElements, min, max):
    lst = []
    for i in range (numberOfElements):
        lst.append(random.randint(min,max))
    return lst


def bubbleSort(drawInfo, asc = True):
    
    lst = drawInfo.lst

    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            pygame.event.pump()
            if (lst[j] > lst[j+1] and asc) or (lst[j] < lst[j+1] and not asc):
                lst[j] , lst[j+1] = lst[j+1], lst[j]
                drawInfo.drawLst({j: drawInfo.BLUE, j + 1: drawInfo.RED},True)
    return True

def insertionSort(drawInfo, asc = True):
    lst = drawInfo.lst
    
    for i in range(1,len(lst)):
        temp = lst[i]
        while(True):
            pygame.event.pump()
            ascending = i>0 and lst[i-1] > temp and asc
            descending = i>0 and lst[i-1] < temp and not asc
            if not ascending and not descending:
                break

            lst[i] = lst[i-1]
            i -= 1
            lst[i] = temp
            drawInfo.drawLst({i-1: drawInfo.BLUE, i: drawInfo.RED},True)
    
    return lst

def mergeSort(drawInfo, l , r, asc = True):
    m = (l+r)//2
    if(l<r):
        mergeSort(drawInfo,l,m, asc)
        mergeSort(drawInfo,m+1,r,asc)
        merge(drawInfo,l,m,m+1,r, asc)

def merge(drawInfo,x1,y1,x2,y2,asc):
    i = x1
    j = x2
    temp = []
    pygame.event.pump()
    while i <= y1 and j <= y2:
        drawInfo.drawLst({i: drawInfo.BLUE, j:drawInfo.RED}, True)
        if ((drawInfo.lst[i] < drawInfo.lst[j]) and asc) or ((drawInfo.lst[i] > drawInfo.lst[j]) and not asc):
            temp.append(drawInfo.lst[i])
            i +=1
        else:
            temp.append(drawInfo.lst[j])
            j+=1
    while i <= y1:
        drawInfo.drawLst({i: drawInfo.BLUE}, True)
        temp.append(drawInfo.lst[i])
        i += 1

    while j <= y2:
        drawInfo.drawLst({j:drawInfo.RED}, True)
        temp.append(drawInfo.lst[j])
        j += 1
    j = 0
    for i in range(x1, y2+1):
        pygame.event.pump()
        drawInfo.lst[i] = temp[j]
        j += 1
        drawInfo.drawLst({i: drawInfo.GREEN}, True)

def quickSort(drawInfo, start , end, asc = True):
    if (start < end):
        pivot = findPivot(drawInfo,start,end, asc)
        quickSort(drawInfo, start , pivot - 1, asc)
        quickSort(drawInfo,pivot + 1, end, asc)

def findPivot(drawInfo, start ,end, asc):
    pivot = drawInfo.lst[end]
    l = start -1
    drawInfo.drawLst({end: drawInfo.GREEN },True)
    for r in range(start,end + 1):
        pygame.event.pump()
        if ((drawInfo.lst[r] < pivot) and asc) or ((drawInfo.lst[r] > pivot) and not asc):
            l += 1
            drawInfo.drawLst({end: drawInfo.GREEN ,l: drawInfo.BLUE, r: drawInfo.RED},True)
            temp = drawInfo.lst[l]
            drawInfo.lst[l] = drawInfo.lst[r]
            drawInfo.lst[r] = temp
        
    l += 1
    drawInfo.drawLst({l: drawInfo.BLUE, r: drawInfo.RED},True)
    temp = drawInfo.lst[l]
    drawInfo.lst[l] = drawInfo.lst[end]
    drawInfo.lst[end] = temp
    return l

def heapSort(drawInfo,asc = True):
    lst = drawInfo.lst;
    n = len(lst)

    for i in range((n//2)-1,-1,-1):
         heapify(drawInfo,n,i,asc)

    for r in range(n-1,0,-1):
        drawInfo.drawLst({r: drawInfo.BLUE, 0: drawInfo.RED},True)
        (lst[r],lst[0]) = (lst[0], lst[r])
        heapify(drawInfo,r,0,asc)

def heapify(drawInfo, n, i, asc):
    lst = drawInfo.lst
    minMax = i
    l = (i*2) + 1
    r = (i*2) + 2

    if l < n and (((lst[i] < lst[l]) and asc) or ((lst[i] > lst[l]) and not asc)):
        minMax = l

    if r < n and ((lst[minMax] < lst[r] and asc) or ((lst[minMax] > lst[r] and not asc))):
        minMax = r 

    if minMax != i:
        pygame.event.pump()
        drawInfo.drawLst({i:drawInfo.BLUE , minMax: drawInfo.RED},True)
        (lst[i],lst[minMax]) = (lst[minMax],lst[i])

        heapify(drawInfo, n, minMax, asc)


def main():
    run = True
    asc = True
    n = 500
    min = 25
    max = 125

    lst = generateRandomArray(n, min, max)
    drawInfo = info(1100,650,lst)
    win = drawInfo.window

    while run:
        drawInfo.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    lst = generateRandomArray(n, min, max)
                    drawInfo.setList(lst)

                elif event.key == pygame.K_t:
                    if(n >= 100):
                        n -= 50
                        lst = generateRandomArray(n, min, max)
                        drawInfo.setList(lst)

                elif event.key == pygame.K_y:
                    if(n <= 450):
                        n += 50
                        lst = generateRandomArray(n, min, max)
                        drawInfo.setList(lst)
            
                elif event.key == pygame.K_a:
                    asc = True
                    
                elif event.key == pygame.K_d:
                    asc = False

                elif event.key == pygame.K_b:
                    bubbleSort(drawInfo, asc)

                elif event.key == pygame.K_i:
                    insertionSort(drawInfo, asc)

                elif event.key == pygame.K_m:
                    mergeSort(drawInfo,0,len(drawInfo.lst)-1, asc)

                elif event.key == pygame.K_q:
                    quickSort(drawInfo,0,len(drawInfo.lst)-1,asc)


                elif event.key == pygame.K_h:
                    heapSort(drawInfo, asc)
    
    pygame.quit()

if __name__ == "__main__":
    main()