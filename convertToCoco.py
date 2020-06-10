import json
import pprint
import cv2
import glob

filename = './cocoAnnotations/instances_val2017.json'
data = {}
with open(filename) as inpJson:
    data = json.load(inpJson)

categoriesData = {}
with open('initialAnnotations.json') as inpJson:
    categoriesData = json.load(inpJson)

# del data['annotations']
del data['licenses']
del data['info']

# data['annotations'] = []

imageId = {}

allImgs = glob.glob("images/*.jpg")
images = []
idImg = 1
for img in allImgs:
    newDict = {}
    newDict['file_name'] = img.split('/')[1]
    newDict['id'] = idImg
    imageId[img.split('/')[1].split('.')[0]] = idImg
    myimg = cv2.imread(img)
    height, width, channels = myimg.shape
    newDict['height'] = height
    newDict['width'] = width
    images.append(newDict)
    idImg += 1

allAnnotations = glob.glob("annotations/*.txt")
annotations = []
idx = 1
for annotation in allAnnotations:
    fp = open(annotation, 'r')
    for line in fp:
        newDict = {}
        newDict['id'] = idx
        newDict['image_id'] = imageId[annotation.split('/')[1].split('.')[0]]
        dat = line.split(',')
        newDict['category_id'] = int(dat[5]) + 1
        newDict['bbox'] = [int(dat[0]), int(dat[1]), int(dat[2]), int(dat[3])]
        newDict['area'] = float(dat[2]) * float(dat[3])
        newDict['iscrowd'] = 0
        idx += 1
        annotations.append(newDict)

data['images'] = images
data['categories'] = categoriesData['categories']
data['annotations'] = annotations

print("Writing the Data to file...")

outfile = 'instances.json'
outdata = json.dumps(data, indent=4)
with open(outfile, 'w') as outJson:
    outJson.write(outdata)

print("Done")
