import gridfs
from IPython.display import Image
from IMDb_Bollywood_Celebrity import Scrape_info
from mongoengine import connect, Document, fields

connect(db='Bollywood_Celebs_Database', host="127.0.0.1", port=27017)


class dataB(Document):
    meta = {"collection": "Celebs"}
    celeb_name = fields.StringField(required=True)
    description = fields.StringField()
    upload_image = fields.FileField()


si = Scrape_info()

for i in range(len(si.Names) - 1):
    upload = dataB(celeb_name=si.Names[i], description=si.final_info[i])
    for j in range(len(si.image_save)-1):
        with open(si.image_save[j], 'rb') as ic:
            upload.upload_image.replace(ic, content_type='image/jpeg')
    upload.save()

# Retrieve images
for i in range(len(si.Names)-1):
    cb = dataB.objects(celeb_name=si.Names[i]).first()
    Image(cb.upload_image.read())
