""" CONTROLLER FILE"""
import logging
from http import HTTPStatus
import sys
import subprocess
from .models import AWSAccount
from ..db import db

from flask import request


from ..utils import json_response, error_response
from .exceptions import AccountNameAlreadyExists, AccountDoesNotExists,  \
    AccountIdMissing, WrongCredentials, KeyAlreadyExists, NoFileFoundException
from .service import OnBoardService

# Creating Logger object
logger = logging.getLogger("on_board")
logger.addHandler(logging.StreamHandler(sys.stdout))


def add_account():
    """Add AWS Account credentials"""

    try:
        data = request.json
        aws_access_key = data["aws_access_key"]
        aws_secret_key = data["aws_secret_key"]
        account_name = data["account_name"]

        # Check if account name already exists
        logger.info("Checking if Account Already Exists")
        if AWSAccount.query.filter(AWSAccount.account_name == account_name).first() is not None:
            raise AccountNameAlreadyExists()

        # Check credentials and permission required
        logger.info("Checking if Invalid Credentials")
        credentials = OnBoardService.invalid_credentials(
            aws_access_key, aws_secret_key)
        if credentials:
            raise WrongCredentials(message=credentials)

        # Encode the KEYS
        logger.info("Encoding into base64 string")
        aws_access_key = OnBoardService.encode_to_base64(aws_access_key)
        aws_secret_key = OnBoardService.encode_to_base64(aws_secret_key)

        logger.info("Adding the Account to Database")
        account_obj = AWSAccount(
            account_name=account_name,
            access_key=aws_access_key,
            secret_key=aws_secret_key
        )
        db.session.add(account_obj)
        db.session.commit()
        logger.info(
            f"Created Account Successfully with 'id': {str(account_obj.id)}")
        return json_response({"id": str(account_obj.id)})

    except AccountNameAlreadyExists:
        logger.info("Account Name Already Exist")
        return error_response(f"Account with name {account_name} already exists", HTTPStatus.BAD_REQUEST)
    except WrongCredentials as wc_error:
        logger.info(wc.message)
        return error_response(wc_error.message, HTTPStatus.BAD_REQUEST)


def upload_key_pair():
    """Upload key for the Account"""
    try:
        logger.info("Validating Params")
        if 'file' not in request.files or request.files['file'].filename == '':
            raise NoFileFoundException()
        if 'account_id' not in request.args:
            return AccountIdMissing()
        file = request.files['file']

        account_id = request.args.get('account_id')
        pem_file_path = f'./private/keys_pairs/{file.filename}'

        logger.info("Uploading Key to the Specified Location")
        account = AWSAccount.query.get(account_id)
        if account is not None:
            if not account.key_name:
                file.save(pem_file_path)
                result = subprocess.run(f"ls", cwd="./private/keys_pairs/")
                if result.returncode == 0:
                    account.key_name = file.filename
                    db.session.add(account)
                    db.session.commit()
                    return json_response('File uploaded successfully')
                else:
                    return json_response('File uploaded successfully')
            else:
                raise KeyAlreadyExists()
        else:
            raise AccountDoesNotExists()

    except AccountDoesNotExists:
        error = f"Account Does not Exist with ID '{account_id}' "
        logger.error(error)
        return error_response(error, HTTPStatus.NOT_FOUND)
    except KeyAlreadyExists:
        error = f"Key Already Exists with name '{account.key_name}' "
        logger.error(error)
        return error_response(error, HTTPStatus.ALREADY_REPORTED)
    except AccountNameAlreadyExists:
        error = f"Account Name '{account.account_name}' Already Exists. Please try with other Account Name"
        logger.error(error)
        return error_response(error, HTTPStatus.ALREADY_REPORTED)
    except NoFileFoundException:
        error = "Please provide file to upload"
        logger.error(error)
        return error_response(error, HTTPStatus.BAD_REQUEST)
    except AccountIdMissing:
        error = "Please provide Account ID"
        logger.error(error)
        return error_response(error, HTTPStatus.BAD_REQUEST)
