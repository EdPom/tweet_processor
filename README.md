# tweet_processor
## Overview
This is a toy project that
  1. tracks specific terms on twitter,
  2. stream the tweets to SQL server,
  3. query on the stored tweets,
  4. then present the result of queries on webpage.

This project is meant as a way to learn how to use
  * Twitter API
  * AWS Kinesis
  * AWS Redshift

## Dependency
AWS EC2 setup:
  * Python 3
  * Kinesis agent
  * gcc
  * memcached

Python scripting:
  * psycopg2
  * memcache
  * tweepy

Twitter / tweet tracking:
  * Twitter bot keys & tokens

Other AWS services:
  * Redshift
  * S3
  * Kinesis

## Components
**tweet_basketball.py** and **tweet_baseball.py**:
  * Connect to Tweeter API using bot tokens.
  * Track tweet streams with specific terms (`basketball` and `baseball` for each script).
  * Extract `created_at` and `id_str` field from each tweet record.
  * Store the tweet record to `/tmp/<term>.log`

**Kinesis Firehose**:
  * Agent on stream source side is configured by `/etc/aws-kinesis/agent.json`.
  * Configure Kinesis agent to monitor the two `/tmp/<term>.log` files.
  * Send new records to the corresponding delivery streams.
  * Each delivery stream is then configured to
    * Store the records to **S3** first.
    * Then use `COPY` command to copy the records to **Redshift**.

**Redshift**:
  * A Redshift cluster / database is preconfigured with 2 tables for each stream.

**count_tweets.py**:
  * Query the database for "number of all tweets that are at most 10 minutes older than the newest tweet", for each table.
  * Store the result to memcache.

**simple_http.py**:
  * Simple HTTP server to serve `index.html` for presenting the result.
  * `index.html` requests `status.json` for an update.

