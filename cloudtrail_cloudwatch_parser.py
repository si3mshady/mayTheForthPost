import boto3, subprocess, datetime, json


logs = boto3.client('logs', region_name='us-east-2')
LOG_GROUP = "sampleTrail"
FILTER_STRING  = "message"
QUERY = f'fields @message|filter @message like \"{FILTER_STRING}\"'

#tuples
(START_SECONDS,END_SECONDS) = 0,59
(START_MINS, END_MINS) = 0, 0
(START_HOUR, END_HOUR) = 4,5   #local time
DELTA = 0  #days ago



def get_alpha_time(s,m,h,delta=DELTA)-> datetime:
    start_point =  datetime.datetime.today()-datetime.timedelta(days=delta)
    start_point = start_point.replace(second=s,minute=m,hour=h)
    return start_point

def get_omega_time(day,s=END_SECONDS,m=END_MINS,h=END_HOUR)-> datetime:
    return day.replace(second=s,minute=m,hour=h)

#keyword arguments
kwargs_alpha = {"s":START_SECONDS,"m":START_MINS, "h":START_HOUR, "delta": DELTA}

kwargs_omega = {"day":get_alpha_time(**kwargs_alpha),"s": END_SECONDS,"m":END_MINS, "h":END_HOUR}

kwargs_cloudwatch = {"logGroupName": LOG_GROUP, "startTime": int(get_alpha_time(**kwargs_alpha).timestamp()),
"endTime":int(get_omega_time(**kwargs_omega).timestamp()), "limit":10, "queryString": QUERY }


def init_query() -> dict:
    print("start",kwargs_cloudwatch.get('startTime'))
    print("end", kwargs_cloudwatch.get('endTime'))
    print(kwargs_cloudwatch.get('queryString'))

    return  logs.start_query(**kwargs_cloudwatch)['queryId']


def get_query_results(id):
    return  logs.get_query_results(queryId=id)


def process_logs():
    query_id = init_query()
    result = get_query_results(query_id)

    while result.get('status') != 'Complete':
        result = get_query_results(query_id)
    return result.get('results')



if __name__ == "__main__":
    res = process_logs()
    comprehension = [json.loads(eventName[0]['value']).get('eventName') for eventName in res]
    print(comprehension)



#Elliott Arnold  - boto3/python course  #mayTheForthBeWithYou  5-4-22  7-11
