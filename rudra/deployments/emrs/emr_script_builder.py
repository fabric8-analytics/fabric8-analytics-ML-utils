"""EMR script builder implementation."""
from rudra.deployments.emrs.abstract_emr import AbstractEMR
from rudra.utils.validation import check_field_exists
from rudra.utils.helper import get_training_file_url, get_github_repo_info
from rudra import logger
from time import gmtime, strftime
import os
import json


class EMRScriptBuilder(AbstractEMR):
    """EMR Script implementation."""

    def __init__(self):
        """Initialize the EMRScriptBuilder instance."""
        self.current_time = strftime("%Y_%m_%d_%H_%M_%S", gmtime())

    def construct_job(self, input_dict):
        """Submit emr job."""
        required_fields = ['environment', 'data_version',
                           'bucket_name', 'github_repo']

        missing_fields = check_field_exists(input_dict, required_fields)

        if missing_fields:
            logger.error("Missing the parameters in input_dict",
                         extra=missing_fields)
            raise ValueError("Required fields are missing in the input {}"
                             .format(missing_fields))

        self.env = input_dict.get('environment')
        user, repo = get_github_repo_info(input_dict.get('github_repo'))
        self.training_file_url = get_training_file_url(user, repo)
        hyper_params = input_dict.get('hyper_params')
        self.aws_access_key = os.getenv("AWS_S3_ACCESS_KEY_ID") \
            or input_dict.get('aws_access_key')
        self.aws_secret_key = os.getenv("AWS_S3_SECRET_ACCESS_KEY")\
            or input_dict.get('aws_secret_key')
        self.bucket_name = input_dict.get('bucket_name')
        if hyper_params:
            try:
                self.hyper_params = json.dumps(input_dict.get('hyper_params'),
                                               separators=(',', ':'))
            except Exception as exc:
                logger.error("Invalid hyper params",
                             extra={"hyper_params": input_dict.get('hyper_params')})

        self.properties = {
            'AWS_S3_ACCESS_KEY_ID': self.aws_access_key,
            'AWS_S3_SECRET_ACCESS_KEY': self.aws_secret_key,
            'BUCKET_NAME': self.bucket_name
        }

    def run_job(self, input_dict):
        """Run the emr job."""
        raise NotImplementedError
