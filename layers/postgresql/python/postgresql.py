import json
import psycopg2 
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class PostgreSQL: 
    def __init__ (self):
        logger.info("------- PostgreSql Class Initialization")

        ssm = boto3.client('ssm', region_name='ca-central-1')
        p_dbserver = '/mri-phsa/dbserver'
        p_dbname = '/mri-phsa/dbname'
        p_dbuser = '/mri-phsa/dbuser'
        p_dbpwd = '/mri-phsa/dbpwd'
        # p_dbserver = '/mri-phsa/dbserver_ec2'
        # p_dbname = '/mri-phsa/dbname_ec2'
        # p_dbuser = '/mri-phsa/dbuser_ec2'
        # p_dbpwd = '/mri-phsa/dbpwd_ec2'
        params = ssm.get_parameters(
            Names=[
                p_dbserver, p_dbname, p_dbuser, p_dbpwd
            ],
            WithDecryption = True
        )
        logger.info("Finished Acquiring Params")
        if params['ResponseMetadata']['HTTPStatusCode'] != 200: 
            logger.info('ParameterStore Error: ', str(params['ResponseMetadata']['HTTPStatusCode']))
            sys.exit(1)

        for p in params['Parameters']: 
            if p['Name'] == p_dbserver:
                dbserver = p['Value']
            elif p['Name'] == p_dbname: 
                dbname = p['Value']
            elif p['Name'] == p_dbuser:
                dbuser = p['Value']
            elif p['Name'] == p_dbpwd:
                dbpwd = p['Value']
        logger.info("------- Connecting to PostgreSql")
        self.conn = psycopg2.connect(host=dbserver, dbname=dbname, user=dbuser, password=dbpwd)
        logger.info("------- PostgreSql Class Initialized")
    
    def closeConn(self):
        self.conn.close()


