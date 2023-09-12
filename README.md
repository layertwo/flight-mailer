# flight-mailer

## Overview

AWS Lambda function for reading RSS feeds and transforming them to an email. Filters entries based on last timeframe.

## Environment Variables

I use environment variables to store configuration values (I'm not going to store my configs and passwords here). Here are the environment variables you will need:

- EMAIL_HOST
- EMAIL_PORT
- EMAIL_USERNAME
- EMAIL_PASSWORD
- EMAIL_SENDER
- EMAIL_RECIPIENT
- INTERVAL_SEC

