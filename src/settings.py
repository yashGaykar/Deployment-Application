from dotenv import load_dotenv
import os

dotenv_path = '.env'
load_dotenv(dotenv_path)

AWS_SECRET_ACCESS_KEY=os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_KEY=os.environ.get("AWS_KEY")
IMAGE_ID=os.environ.get("IMAGE_ID")
INSTANCE_TYPE=os.environ.get("INSTANCE_TYPE")
INSTANCE_KEY=os.environ.get("INSTANCE_KEY")
SSM_ROLE_ARN=os.environ.get("SSM_ROLE_ARN")
AWS_REGION=os.environ.get("AWS_REGION")
INSTANCE_USER_NAME=os.environ.get("INSTANCE_USER_NAME")

BROKER_URL=os.environ.get("BROKER_URL")
BACKEND_URL=os.environ.get("BACKEND_URL")





