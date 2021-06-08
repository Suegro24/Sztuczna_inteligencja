from PIL import Image
globalFeatureMap = []


def printArray(array, description = ''):
    if description != '':
        print(description)
    for item in array:
        print(item)


def changeImageColorToWhite(img):
    width, height = img.size
    pix = img.load()
    for x in range(width):
        for y in range(height):
            pix[x, y] = (255, 255, 255)
    return img


def createTestImages():
    img = Image.new("RGB", (9, 9))
    img = changeImageColorToWhite(img)
    pix = img.load()
    pix[3, 0] = (0, 0, 0)
    pix[4, 0] = (0, 0, 0)
    pix[5, 0] = (0, 0, 0)
    pix[3, 1] = (0, 0, 0)
    pix[3, 2] = (0, 0, 0)
    pix[4, 2] = (0, 0, 0)
    pix[5, 2] = (0, 0, 0)
    pix[5, 1] = (0, 0, 0)
    pix[5, 3] = (0, 0, 0)
    pix[5, 4] = (0, 0, 0)
    pix[4, 4] = (0, 0, 0)
    pix[3, 4] = (0, 0, 0)
    checkImageForNumberNine(img)
    img.save('./images/test.png', 'PNG')



def loadImage(src):
    img = Image.open(src)
    return img



def getPattern(index):
    if index == 0:
        # loop
        return [[1, 1, 1], [1, -1, 1], [1, 1, 1]]
    elif index == 1:
        # left tail 1
        return [[1, -1, 1], [1, 1, -1], [1, -1, -1]]
    elif index == 2:
        # left tail 2
        return [[1, -1, 1], [1, -1, 1], [1, 1, -1]]
    elif index == 3:
        # left tail 3
        return [[1, -1, 1], [1, -1, 1], [1, 1, 1]]



def checkPattern(pattern, img, startWidth, startHeight):
    result = []
    for i in range(len(pattern)):
        array = []
        for j in range(len(pattern)):
            currentPixel = img.getpixel((startHeight + i, startWidth + j))
            if currentPixel[0] == 255 and currentPixel[1] == 255 and currentPixel[2] == 255:
                array.append(-1)
            else:
                array.append(1)
        result.append(array)
    sum = 0
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            sum += pattern[j][i]*result[j][i]
    return sum/(len(pattern)*len(pattern))



def checkImageForNumberNine(img):
    width, height = img.size
    NUMBEROFPATTERNS = 4
    for n in range(NUMBEROFPATTERNS):
        featureMap = []
        pattern = getPattern(n)
        for i in range(width-2):
            map = []
            for j in range(height-2):
                map.append(checkPattern(pattern, img, i, j))
            featureMap.append(map)
        globalFeatureMap.append(featureMap)
    for i in range(len(globalFeatureMap)):
        globalFeatureMap[i] = pooling(globalFeatureMap[i])
        printArray(globalFeatureMap[i])

    head = []
    body = []
    for i in range(len(globalFeatureMap)):
        if i == 0:
            for j in range(len(globalFeatureMap[i])):
                for k in range(len(globalFeatureMap[i][j])):
                    if globalFeatureMap[i][j][k] > 0.7:
                        head.append([j, k])
        else:
            for j in range(len(globalFeatureMap[i])):
                for k in range(len(globalFeatureMap[i][j])):
                    if globalFeatureMap[i][j][k] > 0.7:
                        body.append([j, k])

    isFound = False
    for h in head:
        for b in body:
            if h[0] == b[0] and h[1] < b[1]:
                print('Ten obrazek zawiera liczbe 9!')
                isFound = True
                break


def getMaxFeature(array):
    max = array[0]
    for i in range(1, len(array)):
        if array[i] > max:
            max = array[i]
    return max


def pooling(featureMap):
    # printArray(featureMap)
    result = []
    array = []
    x = 0
    y = 0
    index = 0
    while y < len(featureMap):
        # print(x, y)
        if x+3 >= len(featureMap):
            # print(featureMap[x][y:y + 2] + featureMap[x+1][y:y + 2] + featureMap[x+2][y:y + 2])
            array.append(getMaxFeature(featureMap[x][y:y + 2] + featureMap[x+1][y:y + 2] + featureMap[x+2][y:y + 2]))
            x = -2
            y += 2
        else:
            # print('\n', featureMap[x][y:y+2] + featureMap[x+1][y:y+2])
            array.append(getMaxFeature(featureMap[x][y:y+2] + featureMap[x+1][y:y+2]))

        if (index+1) % 3 == 0:
            result.append(array)
            array = []
        index += 1
        x += 2
    # return [j for i in result for j in i]
    return result

createTestImages()
