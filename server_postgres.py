# Structure: Twitter API sample string code
import requests
import os
import sys
import json
# To detect the language in text
# Reference: https://stackoverflow.com/questions/39142778/python-how-to-determine-the-language
import langid
import config
import datetime 
import argparse
import psycopg

bearer_token = config.BEARER_TOKEN

# Call the url
# Since we need the time, give endpoint as ?tweet.fields=created_at, based on Twitter API documentation

def create_url():
    return "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=created_at"

# Same as "def bearer_oauth" in the sample string code
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2SampledStreamPython"
    return r
    
def parse_timestamp(s):
    # Delete the unnecessary part of the date and time, change the colons to the bars
    date = s.split('T')[0]
    time = s.split('T')[1].split('.000Z')[0].replace("-", ":")
    timestamp = date + ":" + time
    return timestamp

def parse_json(json_response): 
    if langid.classify(json_response["text"])[0] == 'en':
        # Store time and text into two variables
        # We only want text in English, and thus we need a filter
        res_time = parse_timestamp(json_response["created_at"])
        res_text = json_response["text"].splitlines()
        res_text = ''.join(str(e) for e in res_text)
        res_id = json_response["id"]
        insert_query = (res_id, res_time, res_text)
        return insert_query

# Reset tweets table
def reset_tweets():
    connection = psycopg.connect(user="gb760", dbname = "final_project")
    cursor = connection.cursor()
    cursor.execute("""TRUNCATE tweets""")
    cursor.execute("""TRUNCATE tweets_backup""")
    connection.commit()
    if connection:
        cursor.close()
        connection.close()

# Insert values into tweets table
def insert_value(insert_query):
    connection = psycopg.connect(user="gb760", dbname = "final_project")
    cursor = connection.cursor()
                    
    query = """INSERT INTO tweets (tweet_id, time_stamp, tweet) VALUES (%s,%s,%s)"""
                    
    cursor.execute(query, insert_query)
    connection.commit()
                    
    if connection:
        cursor.close()
        connection.close()

# Insert values into tweets backup table
def insert_value_backup(insert_query):
    connection = psycopg.connect(user="gb760", dbname = "final_project")
    cursor = connection.cursor()
                    
    query = """INSERT INTO tweets_backup (tweet_id, time_stamp, tweet) VALUES (%s,%s,%s)"""
                    
    cursor.execute(query, insert_query)
    connection.commit()
                    
    if connection:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    
    url = create_url()
    
    #Parsing 
    parser = argparse.ArgumentParser(description='File/API.')
    parser.add_argument("--file", help="Generates a file of tweets.", default="")
    args = parser.parse_args()
    file = args.file
    
    if file == '': #### TWIITER API ####
        print ("Write tweets into table using Twitter API!")
        # Reset the table tweets
        reset_tweets()
        # The original code in "def connect_to_endpoints" in sample string code  
        while True:
            response = requests.request("GET", url, auth = bearer_oauth, stream = True)
            for response_line in response.iter_lines():
                if response_line:
                    json_response = json.loads(response_line)["data"]
                    insert_query = parse_json(json_response)
                    if insert_query: 
                        insert_value(insert_query)
                        insert_value_backup(insert_query)
                        
                if response.status_code != 200:
                    raise Exception(
                        "Request returned an error: {} {}".format(
                        response.status_code, response.text))
            timeout += 1
    else: #### JSON TWEETS ####
        print ("Write tweets into table using JSON Tweets")
        reset_tweets()
        with open(file) as json_file:
            time = 0
            json_datas = json.load(json_file)["data"]
            for json_response in json_datas:
                insert_query = parse_json(json_response)  
                if insert_query: 
                    insert_value(insert_query)
        print ("Writing Successfully!")
