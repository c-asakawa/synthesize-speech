## Synthesize Speech

This application reaches out to AWS's Polly API to synthesize text into speech. This application can be run locally
or can be hosted on a server. 

### Application Requirements
Web browser compliant with the HTML5 and EcmaScript5 standards (for example, Chrome 23.0 or higher, 
Firefox 21.0 or higher, Internet Explorer 9.0, or higher) Python version greater than 3.0

### Getting Started
1. Clone this repo `git clone https://github.com/c-asakawa/synthesize-speech.git`
2. Install AWS CLI https://docs.aws.amazon.com/cli/latest/userguide/installing.html
3. Create AWS Polly credentials https://docs.aws.amazon.com/polly/latest/dg/authentication-and-access-control.html
4. Update the aws credentials locally with the newly created credentials. These config files can be found at `~/.aws/` 
update `config` file to match your region. This file should look something like this.
``` 
[default]
output = mp3
region = us-west-2
```
Now update the `credentials` file. with the newly generated creditals made from step 3. This should look like the following
```
[default]
aws_access_key_id = ****
aws_secret_access_key = ****
region = us-west-2
```
5. Now we can finally run the python server. Run `python server.py`
6. Your done the app is now running locally, you can access this by opening up a web browser and navigate to
 `localhost:8000`
