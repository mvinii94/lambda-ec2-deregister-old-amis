# Lambda EC2 Deregister Old AMIs

A serverless solution to deregister old AMIs created as backup using "lambda-ec2-instance-backup" which creates automated AMIs.

## Getting Started

This project contains two files:

CloudFormation SAM template (template.yaml)

Lambda Function (index.py)

The Lambda function will deregister Amazon Machine Images (AMI) from your AMIs which contains tag "backup" set as "lambda-ec2-instance-backup", as created by the serverless solution [lambda-ec2-instance-backup](https://github.com/mvinii94/lambda-ec2-instance-backup), each hour.

### Prerequisites

* **S3 Bucket** - *To upload the index.py file zipped.* 

* **AWS CLI Installed** - *To deploy the SAM CloudFormation template.* - [How to Install AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/installing.html)

### Deploying the lambda serverless application

* Clone this repository;

* Upload the lambda code zipped to an S3 Bucket of your preference in the desired region (should be the same where you are going to deploy the serverless solution);

* Run the following command providing the bucket name and the S3 key name toof your file:

```
aws cloudformation deploy --template-file template.yaml --stack-name lambda-ec2-deregister-old-amis --region us-east-1 --capabilities CAPABILITY_IAM --parameter-overrides Bucket=<MyBucketName> FileKey=lambda-ec2-deregister-old-amis.zip RetentionPeriod=0.1
```

## Authors

* **Marcus Ramos** - [GitHub](https://github.com/mvinii94/)
