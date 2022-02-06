import pymysql
import sys
from datetime import datetime, time
rds_host = "database-4.c8jazxaqybhk.us-east-1.rds.amazonaws.com"




logger = logging.getLogger()
logger.setLevel(logging.INFO)






def lambda_handler(event, context):

    try:
        conn = pymysql.connect(host=rds_host, user='admin', passwd='teste123', db='teste', connect_timeout=5)
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit()
    
    
    temperature = event.get('queryStringParameters')['temperature']
    time_now = datetime.now()
    day = time_now.day
    year = time_now.year
    month = time_now.month
    hour = time_now.hour
    minute = time_now.minute
    current_time = time.time()
    id = str(current_time)

    with conn.cursor() as cur:

        '''
        cur.execute("""
        create table Temperature (
        ID VARCHAR(100) NOT NULL,
        day int NOT NULL,
        month int NOT NULL,
        year int NOT NULL,
        hour int NOT NULL,
        minute int NOT NULL,
        temperature int NOT NULL,
        PRIMARY KEY (ID))""")''' 

        cur.execute('insert into Temperature (Id, day, month, year, hour, minute, temperature) values({},{},{},{},{},{},{})'.format(id,day, month, year, hour, minute, temperature))
        conn.commit()
        cur.execute("select * from Temperature")
        result = []
        for row in cur:
            result.append(list(row))
        logger.info(row)
        conn.commit()
        result = json.dumps(result, indent = 4)
        result = json.loads(result)
        return result
      
