# import azure blob storange
from azure.storage import BlobService
from azure import WindowsAzureMissingResourceError
import glob
import os
import engaged.data.azure_connect as AC

ACCOUNT_NAME = 'sounds'
ACCOUNT_KEY  = AC.getAccountKey() # primary access key
HOST_BASE    = '.blob.core.windows.net'

blob_service = BlobService(account_name=ACCOUNT_NAME,
                           account_key=ACCOUNT_KEY,
                           host_base=HOST_BASE)

CONTAINER = 'bat-detective' # or whatever else you like

created = blob_service.create_container(CONTAINER, x_ms_blob_public_access='container')
print "Created" if created else "Not created (probably already existing)"

audio_dir = '../../data/wav/'
SOUND_FILES = glob.glob(audio_dir + '*.wav')

for f in SOUND_FILES:
    print "uploading", os.path.basename(f)
    blob_service.put_block_blob_from_path(
        CONTAINER,                          # container
        os.path.basename(f),                # blob
        f,                                  # path
        x_ms_blob_content_type='audio/wav'
    )


blobs = blob_service.list_blobs(CONTAINER)

for blob in blobs:
    print(blob.name)