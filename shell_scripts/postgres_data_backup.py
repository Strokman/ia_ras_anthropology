import os
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime
path = '/home/basehabilis/ia_ras_anthropology/'
os.chdir(path)
filename = datetime.now().strftime('%Y-%m-%d-%H-%M') + '-pg-data' + '.zip'
with ZipFile(f'/home/basehabilis//basehabilis_dumps/{filename}', 'w', ZIP_DEFLATED) as archive:
    for dirname, subdirs, files in os.walk('postgres-data'):
        archive.write(dirname, arcname=dirname)
        for filename in files:
            archive.write(name := os.path.join(dirname, filename), arcname=name)
