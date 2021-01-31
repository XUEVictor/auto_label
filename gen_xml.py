from xml.dom.minidom import Document
import os
import cv2

class xml:
    def __init__(self):
        pass
    def makexml(self,targe_file,Name,Type,Image,rect):
        
        Pheight,Pwidth,Pdepth=Image.shape
        cv2.imwrite('targe/' + targe_file +'/img/'+ Name + '.jpg',Image)

        xmlBuilder = Document()
        annotation = xmlBuilder.createElement("annotation")  # annotation標籤

        xmlBuilder.appendChild(annotation)
        folder = xmlBuilder.createElement("folder")#folder標籤
        folderContent = xmlBuilder.createTextNode(targe_file)#目標資料夾
        folder.appendChild(folderContent)
        annotation.appendChild(folder)

        filename = xmlBuilder.createElement("filename")#filename標籤
        filenameContent = xmlBuilder.createTextNode(Name+".jpg")
        filename.appendChild(filenameContent)
        annotation.appendChild(filename)

        Path = xmlBuilder.createElement("path")#path 標籤
        PathContent = xmlBuilder.createTextNode(os.path.abspath(os.path.dirname(__file__)))
        Path.appendChild(PathContent)
        annotation.appendChild(Path)

        source = xmlBuilder.createElement("source")  # source標籤
        database = xmlBuilder.createElement("database")  # database子標籤
        dbContent = xmlBuilder.createTextNode('Unknown')
        database.appendChild(dbContent)
        source.appendChild(database)
        annotation.appendChild(source)






        size = xmlBuilder.createElement("size")  # size標籤
        width = xmlBuilder.createElement("width")  # size子標籤width
        widthContent = xmlBuilder.createTextNode(str(Pwidth))
        width.appendChild(widthContent)
        size.appendChild(width)
        height = xmlBuilder.createElement("height")  # size子標籤height
        heightContent = xmlBuilder.createTextNode(str(Pheight))
        height.appendChild(heightContent)
        size.appendChild(height)
        depth = xmlBuilder.createElement("depth")  # size子標籤depth
        depthContent = xmlBuilder.createTextNode(str(Pdepth))
        depth.appendChild(depthContent)
        size.appendChild(depth)
        annotation.appendChild(size)

        segmented = xmlBuilder.createElement("segmented")#segmented 標籤
        segmentedContent = xmlBuilder.createTextNode(str(0))
        segmented.appendChild(segmentedContent)
        annotation.appendChild(segmented)






        object = xmlBuilder.createElement("object")
        picname = xmlBuilder.createElement("name")
        nameContent = xmlBuilder.createTextNode(Type)
        picname.appendChild(nameContent)
        object.appendChild(picname)
        pose = xmlBuilder.createElement("pose")
        poseContent = xmlBuilder.createTextNode("Unspecified")
        pose.appendChild(poseContent)
        object.appendChild(pose)
        truncated = xmlBuilder.createElement("truncated")
        truncatedContent = xmlBuilder.createTextNode("0")
        truncated.appendChild(truncatedContent)
        object.appendChild(truncated)
        difficult = xmlBuilder.createElement("difficult")
        difficultContent = xmlBuilder.createTextNode("0")
        difficult.appendChild(difficultContent)
        object.appendChild(difficult)
        bndbox = xmlBuilder.createElement("bndbox")
        xmin = xmlBuilder.createElement("xmin")
        mathData=int(rect[0])
        xminContent = xmlBuilder.createTextNode(str(mathData))
        xmin.appendChild(xminContent)
        bndbox.appendChild(xmin)
        ymin = xmlBuilder.createElement("ymin")
        mathData = int(rect[1])
        yminContent = xmlBuilder.createTextNode(str(mathData))
        ymin.appendChild(yminContent)
        bndbox.appendChild(ymin)
        xmax = xmlBuilder.createElement("xmax")
        mathData = int(rect[2])
        xmaxContent = xmlBuilder.createTextNode(str(mathData))
        xmax.appendChild(xmaxContent)
        bndbox.appendChild(xmax)
        ymax = xmlBuilder.createElement("ymax")
        mathData = int(rect[3])
        ymaxContent = xmlBuilder.createTextNode(str(mathData))
        ymax.appendChild(ymaxContent)
        bndbox.appendChild(ymax)
        object.appendChild(bndbox)

        annotation.appendChild(object)

        f = open('targe/' + targe_file +'/xml/'+ Name + ".xml", 'w')
        xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
        f.close()