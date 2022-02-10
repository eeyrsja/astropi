from PIL import Image
from numpy import array

for i in range(163,164):
    piccy = Image.open(f"/home/pi/free_data/zz_astropi_1_photo_{i}.jpg")

    piccy2 = piccy.rotate(180)
    piccy2.show()

    crop = 400

    left = 0 + crop
    top = 0 + crop
    bottom = 1944 - crop
    right = 2592 - crop

    piccy3 = piccy2.crop((left, top, right, bottom))

    piccy4 = piccy3.convert('L')
    piccy4.show()
    piccy4 = array(piccy4)/255

    piccy5 = piccy4 > 0.45
    white_pixels = piccy5.sum()
    total_pixels = piccy5.size
    percentage_cloud = 100 * (white_pixels / total_pixels)
    print(f"photo_{i}:  {percentage_cloud:0.2f}")

    Image.fromarray(piccy5*255).show()
