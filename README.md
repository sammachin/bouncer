# Bouncer

![bouncer pic](https://raw.githubusercontent.com/sammachin/bouncer/master/callbouncer.jpg)

# Overview
Bouncer is a simple voice application built on Nexmo and AWS Chalice to frustrate spammers, once setup and with a number pointed to it any calls to that number will be forwarded back to the number that is calling them (based on the CallerID) This means the person calling you will get either:

* Thier own Voicemail
* An incomming call if they have call waiting
* Connected to their office reception if they send the main number as CLI

Either way they won't be bothering you and it will waste their time trying to work out whats going on!

For added enjoyment the calls are recorded and dumped in an S3 bucket, you'll then get an email with a link to the recording after each call.

# Setup
To set this up you will need:

- An AWS Account (you can run this on the Lambda free tier)
- Have the [AWS CLI tool](https://aws.amazon.com/cli/) and [Chalice Framework](http://chalice.readthedocs.io/en/latest/) installed and configured on your machine
- A Nexmo Account

Firstly clone this repo to your local machine.

## AWS
###S3
You will need to create an S3 bucket in your prefferred region, then set this bucket name and region in the `.chalice/config.json` file `environment_varibles`

###SES
You will also need to verify either a domain or the addresses you will use for email in SES for the same region.
You can choose to use the same address for both `EMAIL_TO` and `EMAIL_FROM` in the `config.json`

## Nexmo
Create a Nexmo Voice Application and save the private key to a local file named `private.key` in the project root, also make a note of the application ID. For now use dummy values for the answer and event urls.

Find and purchase a number in your country, then link this number to your application

Edit the `config.json` file and set your application ID.


# Deployment

Run `chalice deploy` from the project folder and your app will be deployed to Lambda, you will be prompted to accept the execution policy the first time.
Once the app has been deployed you will get a URL like `https://910e9mcan2.execute-api.us-east-1.amazonaws.com/api/`
Make a note of this.

Now go back to your nexmo application and edit the answerURL and eventURL values to be this amazonaws url with `/ncco` on the end for the answer and `/event` for the EventURL 