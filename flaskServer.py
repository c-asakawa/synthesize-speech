from flask import Flask, Response, request, abort
# from flask_mail import Mail, Message
from argparse import ArgumentParser
from collections import namedtuple
from contextlib import closing
from io import BytesIO
from json import dumps as json_encode
import os
import os
import sys
from flask_cors import CORS

# boto3 for making requests to polly api
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError


# Create a client using the credentials and region defined in the adminuser
# section of the AWS credentials and configuration files
session = Session(profile_name="default")
polly = session.client("polly")

ResponseStatus = namedtuple("HTTPStatus",
                            ["code", "message"])
ResponseData = namedtuple("ResponseData",
                          ["status", "content_type", "data_stream"])

# Mapping the output format used in the client to the content type for the
# response
AUDIO_FORMATS = {"ogg_vorbis": "audio/ogg",
                 "mp3": "audio/mpeg",
                 "pcm": "audio/wave; codecs=1"}
CHUNK_SIZE = 1024
HTTP_STATUS = {"OK": ResponseStatus(code=200, message="OK"),
               "BAD_REQUEST": ResponseStatus(code=400, message="Bad request"),
               "NOT_FOUND": ResponseStatus(code=404, message="Not found"),
               "INTERNAL_SERVER_ERROR": ResponseStatus(code=500, message="Internal server error")}
PROTOCOL = "http"

app = Flask(__name__)  # init the flask application

CORS(app)  # enable cross-origin resource sharing on all routes

# app.config.update(dict(
#     DEBUG = True,
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = 587,
#     MAIL_USE_TLS = True,
#     MAIL_USE_SSL = False,
#     MAIL_USERNAME = os.environ["EMAIL_USERNAME"],
#     MAIL_PASSWORD = os.environ["EMAIL_PASSWORD"],
# ))
# mail = Mail(app)

@app.route("/")
def index():
    return 'hello world'
    # name = request.headers.get('name')
    # message = request.headers.get('message')
    # email = request.headers.get('email')
    # key = request.headers.get('key')

    # # make sure values are being passed through
    # if name is None or message is None or email is None:
    #     abort(400)
    #     return 'null header value(s)'

    # if key == os.environ["SECRET_KEY"]:

    #     msg = Message("subject line",
    #                   sender="test@asakawa.me",
    #                   recipients=["kylehtalus@gmail.com"])

    #     msg.body = "Message from: " + name + " <" + email + ">" + "\n\n" + message
    #     mail.send(msg)
    #     return 'message sent'
    # else:
    #     abort(401)
    #     return 'unauthorized'


@app.route("/getvoices")
def getVoices():
    params = {}
    voices = []
    while True:
        try:
            # Request list of available voices, if a continuation token
            # was returned by the previous call then use it to continue
            # listing
            response = polly.describe_voices(**params)
        except (BotoCoreError, ClientError) as err:
            # The service returned an error
            raise HTTPStatusError(HTTP_STATUS["INTERNAL_SERVER_ERROR"],
                                  str(err))

        # Collect all the voices
        voices.extend(response.get("Voices", []))

        # If a continuation token was returned continue, stop iterating
        # otherwise
        if "NextToken" in response:
            params = {"NextToken": response["NextToken"]}
        else:
            break

    json_data = json_encode(voices)
    bytes_data = bytes(json_data, "utf-8") if sys.version_info >= (3, 0) \
        else bytes(json_data)

    return bytes_data


@app.route("/synthesize")
def synthesize():
    outputFormat = 'ogg_vorbis'
    self.send_header('Content-type', content_type)
    self.send_header('Transfer-Encoding', 'chunked')
    self.send_header('Connection', 'close')


    resp = flask.Response("success")
    resp.headers['Content-type'] = 'audio/ogg'
    resp.headers['Transfer-Encoding'] = 'chunked'
    resp.headers['Connection'] = 'close'
    return resp

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text='hello world',
                                            VoiceId='Joanna',
                                            OutputFormat=outputFormat)
        print 'printing response...'
        print response

    except (BotoCoreError, ClientError) as err:
        # The service returned an error
        raise HTTPStatusError(HTTP_STATUS["INTERNAL_SERVER_ERROR"],
                              str(err))


    # return Response(content_type=AUDIO_FORMATS[outputFormat], data_stream=response.get("AudioStream"))
    return ResponseData(status=200,
                        content_type=AUDIO_FORMATS[outputFormat],
                        # Access the audio stream in the response
                        data_stream=response.get("AudioStream"))

