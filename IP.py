from PIL import Image  
img = Image.open('4.jpg')

Img = img.convert('L')
Img.save("4_1.jpg")

threshold = 110

table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
#img 0/1
photo = Img.point(table,'1')
photo.save("4_2.jpg")