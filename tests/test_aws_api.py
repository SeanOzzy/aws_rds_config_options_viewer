"""
Basic unit tests for the AWS API calls in utils/aws_api.py
Run tests with:
python -m unittest tests/test_aws_api.py
"""

import unittest
from unittest.mock import patch, Mock
import utils.aws_api as aws_api

class TestAWSCalls(unittest.TestCase):

    @patch("utils.aws_api.boto3.client")
    @patch("utils.aws_api.os.environ.get", return_value="us-east-1")
    @patch("utils.aws_api.cache.get_from_cache", return_value=None)
    def test_get_supported_engines(self, mock_cache, mock_os_environ, mock_client):
        # Mock the API response
        mock_response = {
            'DBEngineVersions': [
                {'Engine': 'mysql'},
                {'Engine': 'postgres'}
            ]
        }
        
        # Mock the paginated response
        mock_paginator = Mock()
        mock_paginator.paginate.return_value = [mock_response]
        mock_client.return_value.get_paginator.return_value = mock_paginator

        engines = aws_api.get_supported_engines()
        self.assertEqual(engines, ["mysql", "postgres"])

    @patch("utils.aws_api.fetch_db_instance_classes_for_engine")
    @patch("utils.aws_api.os.environ.get", return_value="us-east-1")
    @patch("utils.aws_api.cache.get_from_cache", return_value=None)
    @patch("boto3.client")
    def test_get_supported_db_classes(self, mock_client, mock_cache, mock_os_environ, mock_fetch):
        # Mock the response for fetch_db_instance_classes_for_engine
        mock_fetch.return_value = {"db.t3.micro", "db.t4g.micro"}

        classes = aws_api.get_supported_db_classes(["mysql"])
        self.assertEqual(classes, ["db.t3.micro", "db.t4g.micro"])
