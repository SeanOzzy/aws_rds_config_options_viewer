"""
Define the RDS API endpoints
The endpoints are defined in a dictionary with the key being the name of the endpoint, 
and the value being a dictionary with the endpoint_url and region
The endpoint_url is the URL of the endpoint, and the region is the region that the endpoint is in
The endpoints are used by the RDS client to make requests to the API.
As new AWS regions are added you may need to update this file.
Docs - https://docs.aws.amazon.com/general/latest/gr/rds-service.html#rds_region
"""

RDS_ENDPOINTS = {
    "us-east-1": {
        "endpoint_url": "https://rds.us-east-1.amazonaws.com",
        "region": "us-east-1",
        },
    "us-east-2": {
        "endpoint_url": "https://rds.us-east-2.amazonaws.com",
        "region": "us-east-2",
        },
    "us-west-1": {
        "endpoint_url": "https://rds.us-west-1.amazonaws.com",
        "region": "us-west-1",
    },
    "us-west-2": {
        "endpoint_url": "https://rds.us-west-2.amazonaws.com",
        "region": "us-west-2",
    },
    "eu-west-1": {
        "endpoint_url": "https://rds.eu-west-1.amazonaws.com",
        "region": "eu-west-1",
    },
    "eu-west-2": {
        "endpoint_url": "https://rds.eu-west-2.amazonaws.com",
        "region": "eu-west-2",
    },
    "eu-central-1": {
        "endpoint_url": "https://rds.eu-central-1.amazonaws.com",
        "region": "eu-central-1",
    },
    "ap-southeast-1": {
        "endpoint_url": "https://rds.ap-southeast-1.amazonaws.com",
        "region": "ap-southeast-1",
    },
    "ap-southeast-2": {
        "endpoint_url": "https://rds.ap-southeast-2.amazonaws.com",
        "region": "ap-southeast-2",
    },
    "ap-northeast-1": {
        "endpoint_url": "https://rds.ap-northeast-1.amazonaws.com",
        "region": "ap-northeast-1",
    },
    "ap-northeast-2": {
        "endpoint_url": "https://rds.ap-northeast-2.amazonaws.com",
        "region": "ap-northeast-2",
    },
    "ap-south-1": {
        "endpoint_url": "https://rds.ap-south-1.amazonaws.com",
        "region": "ap-south-1",
    },
    "sa-east-1": {
        "endpoint_url": "https://rds.sa-east-1.amazonaws.com",
        "region": "sa-east-1",
    },
    "ca-central-1": {
        "endpoint_url": "https://rds.ca-central-1.amazonaws.com",
        "region": "ca-central-1",
    },
    "cn-north-1": {
        "endpoint_url": "https://rds.cn-north-1.amazonaws.com.cn",
        "region": "cn-north-1",
    },
    "cn-northwest-1": {
        "endpoint_url": "https://rds.cn-northwest-1.amazonaws.com.cn",
        "region": "cn-northwest-1",
    },
    "us-gov-west-1": {
        "endpoint_url": "https://rds.us-gov-west-1.amazonaws.com",
        "region": "us-gov-west-1",
    },
    "us-gov-east-1": {
        "endpoint_url": "https://rds.us-gov-east-1.amazonaws.com",
        "region": "us-gov-east-1",
    },
    "me-south-1": {
        "endpoint_url": "https://rds.me-south-1.amazonaws.com",
        "region": "me-south-1",
    },
    "eu-south-1": {
        "endpoint_url": "https://rds.eu-south-1.amazonaws.com",
        "region": "eu-south-1",
    },
    "eu-west-3": {
        "endpoint_url": "https://rds.eu-west-3.amazonaws.com",
        "region": "eu-west-3",
    },
    "eu-north-1": {
        "endpoint_url": "https://rds.eu-north-1.amazonaws.com",
        "region": "eu-north-1",
    },
    "ap-east-1": {
        "endpoint_url": "https://rds.ap-east-1.amazonaws.com",
        "region": "ap-east-1",
    },
    "ap-southeast-3": {
        "endpoint_url": "https://rds.ap-southeast-3.amazonaws.com",
        "region": "ap-southeast-3",
    },
    "ap-northeast-3": {
        "endpoint_url": "https://rds.ap-northeast-3.amazonaws.com",
        "region": "ap-northeast-3",
    },
    "af-south-1": {
        "endpoint_url": "https://rds.af-south-1.amazonaws.com",
        "region": "af-south-1",
    },
    "eu-south-2": {
        "endpoint_url": "https://rds.eu-south-2.amazonaws.com",
        "region": "eu-south-2",
    },
    "il-central-1": {
        "endpoint_url": "https://rds.il-central-1.amazonaws.com",
        "region": "il-central-1",
    },
    "me-central-1": {
        "endpoint_url": "https://rds.me-central-1.amazonaws.com",
        "region": "me-central-1",
    },
    "ap-southeast-4": {
        "endpoint_url": "https://rds.ap-southeast-4.amazonaws.com",
        "region": "ap-southeast-4",
    }
}