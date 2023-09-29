import os
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime
path = '/home/basehabilis/ia_ras_anthropology/'
os.chdir(path)
filename = datetime.now().strftime('%Y-%m-%d-%H-%M') + '-pg-data' + '.zip'

with ZipFile(f'/home/basehabilis/{filename}', 'w', ZIP_DEFLATED) as archive:
    archive.write('postgres-data')
