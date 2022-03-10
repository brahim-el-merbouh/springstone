import os

from google.cloud import storage
from termcolor import colored
from springstone.params import BUCKET_NAME

def storage_upload(model_type,ticker, bucket=BUCKET_NAME, rm=False):
    client = storage.Client().bucket(bucket)

    storage_location = '{}/{}/{}/{}'.format(
        'models',
        'springstone',
        model_type,
        'model.joblib')
    blob = client.blob(storage_location)
    blob.upload_from_filename(f'model_{model_type}_{ticker}.joblib')
    print(colored("=> model_{}_{}.joblib uploaded to bucket {} inside {}".format(model_type,ticker, BUCKET_NAME, storage_location),
                  "green"))
    if rm:
        os.remove(f'model_{model_type}_{ticker}.joblib')
