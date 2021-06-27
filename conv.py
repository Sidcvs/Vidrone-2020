import json
import pprint
import cv2
import glob
import os
data = {}
'''
categoriesData = {}
with open('initialAnnotations.json') as inpJson:
    categoriesData = json.load(inpJson)
'''
imageId = {}

allImgs = glob.glob("VisDrone2019-DET-val/images/*.jpg")
images = []
idImg = 1
for img in allImgs:
    newDict = {}
    newDict['file_name'] = img.split('/')[-1]
    newDict['id'] = idImg
    imageId[img.split('/')[-1].split('.')[0]] = idImg
    myimg = cv2.imread(img)
    height, width, channels = myimg.shape
    newDict['height'] = height
    newDict['width'] = width
    images.append(newDict)
    idImg += 1

allAnnotations = glob.glob("VisDrone2019-DET-val/annotations/*.txt")
annotations = []
idx = 1
ctr = 1
for annotation in allAnnotations:
    fp = open(annotation, 'r')
    file_name = annotation.split('/')
    file_name = file_name[-1]
    data_list = []
    for line in fp:
        data_str = ""
        newDict = {}
        newDict['id'] = idx
        newDict['image_id'] = imageId[annotation.split('/')[-1].split('.')[0]]
        dat = line.split(',')
        # object class in category id
        newDict['category_id'] = int(dat[5]) 

        #newDict['bbox'] = [int(dat[0]), int(dat[1]), int(dat[2]), int(dat[3])]
        #newDict['area'] = float(dat[2]) * float(dat[3])
        #newDict['iscrowd'] = 0
        # addded truncation and occlusion
        newDict['truncation'] = int(dat[6])
        newDict['occlusion'] = int(dat[7])

        ## Add conditions for truncation and occlusion here 
        if newDict['occlusion'] == '2':
            continue

        # find center of image
        center = [int(dat[0]) + float(dat[2])/2 , int (dat[1]) + float(dat[3])/2] # center (in original dimensions)
        
        tot_height = 0 # total height of image
        tot_width = 0 #total width of image

        # get dimensions of image from image dictionary
        for image in images:
            if image['id'] == newDict['image_id']:
                tot_width = image['width']
                tot_height = image['height']
                break
        # get center coordinated (normalized with width and height)
        center_normalized = [center[0]/tot_width, center[0]/tot_height] 
        width_ht = [float(dat[2])/tot_width,float(dat[3])/tot_height]
        newDict['center'] = center_normalized
        newDict['width_ht'] = width_ht
        idx += 1
        data_str = str(newDict['category_id']) + ' ' + str(center_normalized[0]) + ' ' + str(center_normalized[1]) + ' ' + str(width_ht[0]) + ' ' + str(width_ht[1]) + '\n' 
    
        annotations.append(newDict)
        data_list.append(data_str)
    #print(annotation)
    outfile = 'VisDrone2019-DET-val/yolo_annotations/' + file_name
    with open(outfile,'w') as out:
        out.writelines(data_list)

data['images'] = images
#data['categories'] = categoriesData['categories']
data['annotations'] = annotations



'''
outfile = 'VisDrone2019-DET-val/yolo_annotations/0000001_02999_d_0000005.txt'
outdata = json.dumps(data, indent=4)
with open(outfile, 'w') as outJson:
    outJson.write(outdata)
'''
print("Done")