import base64
import boto3



class OnBoardService:

    @staticmethod
    def encode_to_base64(input_str):
        """"Encode the string in Base64 String"""
        return base64.b64encode(input_str.encode('utf-8'))

    @staticmethod
    def decode_from_base64(input_str):
        """Decode string from Base64 String"""
        return base64.decodebytes(input_str).decode()

    @staticmethod
    def invalid_credentials(aws_access_key, aws_secret_key):
        """
        Checks the Credentials of AWS ACcount Entered
        """
        try:
            # Create a session with the provided access key and secret key
            session = boto3.Session(
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key
            )

            # Creates Client
            iam_client = session.client('iam')

            #checks if user exists
            user_response = iam_client.get_user()
            user_name = user_response['User']['UserName']

            # list of roles required for the deployent
            roles_required = ["AmazonEC2FullAccess", "AmazonSSMFullAccess", "AmazonVPCFullAccess", "AmazonS3FullAccess"]

            # list of roles attached to IAM role
            attached_policies_response = iam_client.list_attached_user_policies(UserName=user_name)
            attached_policies = attached_policies_response['AttachedPolicies']
            roles_of_iam_user = []
            for policy in attached_policies:
                policy_name = policy['PolicyName']
                roles_of_iam_user.append(policy_name)

            if set(roles_required).issubset(roles_of_iam_user):
                return None
            else:
                return f"{set(roles_required)-set(roles_of_iam_user)} are the polices required but missing"


        except Exception as error:
            # If there was an error, the access key is invalid
            error = f"Access key verification failed: {str(error)}"
            return error
