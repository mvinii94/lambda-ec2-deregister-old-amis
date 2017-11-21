import boto3
import logging
from datetime import datetime, timedelta


ec2 = boto3.client('ec2')

amis = ec2.describe_images(Filters=[ {'Name': 'tag:backup', 'Values': ['lambda-ec2-instance-backup']} ])

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ami_created_in={}

def lambda_handler(event, context):
    #PRINT THE PARAMETERS
    logger.info('Parameters received: {0}'.format(event))
    #GET THE DAYS PARAMETER TO USE AS RETENTION
    days = float(event['retention'])
    account_id = str(event['accountid'])
    #CALCULATE THE TIMESTAMP TO COMPARE TO CHECK IF THE AMI BACKUP IS OLD ENOUGH
    days_ago = datetime.now() - timedelta(days=int(days))
    logger.info('Timestamp with {0} day(s) ago to compare : {1}'.format(days,days_ago))
    #CREATE AMI_TAGS DICTIONARY
    ami_tags = {}
    #SEARCH AMI'S AND CHECK IF IT IS OLD ENOUGH IF IT IS, DELETES IT.s
    snapshots = ec2.describe_snapshots(MaxResults=1000,OwnerIds=[account_id])['Snapshots']
    for ami in amis['Images']:
        ami_tags.update( { ami['ImageId'] : tag['Value'] for tag in ami['Tags'] if tag['Key'] == 'CreationDate' } )
        #PRINT AMI_TAGS
        ami_created_in = ami_tags[ami['ImageId']]

        # CONVERT THE CREATION TIME TAG (STRING) TO DATETIME
        date_object = datetime.strptime(ami_created_in, "%Y-%m-%d %H:%M:%S.%f")
        logger.info('-----------------------------------------------------------')
        logger.info('AMI: ' + ami['ImageId'] + ' CREATED IN: ' + ami_created_in)

        if date_object < days_ago:
            logger.info('DEREGISTERING AMI: ' + ami['ImageId'])
            try:
                amiResponse = ec2.deregister_image(
                    DryRun=False,
                    ImageId=ami['ImageId'],
                )
                for snapshot in snapshots:
                    if snapshot['Description'].find(ami['ImageId']) > 0:
                        snap = ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                        logger.info('-----------------------------------------------------------')
                        logger.info("DELETING SNAPSHOT: " + snapshot['SnapshotId'])
                        logger.info('-----------------------------------------------------------')
            except:
                logger.info('Something went wrong, please check the logs for more information')
        else:
            logger.info("BACKUP NOT OLD ENOUGH.")
        logger.info('-----------------------------------------------------------')
