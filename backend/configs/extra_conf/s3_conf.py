import os

AWS_QUERYSTRING_AUTH = False

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
# AWS_DEFAULT_ACL = None

# AWS_S3_URL_PROTOCOL = 'https'
# AWS_S3_USE_SSL = True
# AWS_S3_VERIFY = True
#
# AWS_AUTO_CREATE_BUCKET = True

# MEDIA_URL = 'https://%s/' % AWS_STORAGE_BUCKET_NAME

