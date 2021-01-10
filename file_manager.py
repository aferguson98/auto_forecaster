import os

import boto3
import iris
import json
import urllib.request


class AWSEarthDownloader:
    def __init__(self):
        self.sqs = boto3.client(
            'sqs', region_name='eu-west-2',
            aws_access_key_id="AKIAJCYPPH7NDJP6DI3A",
            aws_secret_access_key="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")
        self.to_download = []

    def retrieve_messages(self):
        while True:
            messages = self.sqs.receive_message(QueueUrl='https://sqs.eu-west-2'
                                                         '.amazonaws.com'
                                                         '/623240509878'
                                                         '/mo_hi_res_det_ukvx',
                                                MaxNumberOfMessages=10)
            try:
                messages = messages['Messages']
            except KeyError:
                return
            for message in messages:
                notification = json.loads(message['Body'])
                print(json.loads(notification['Message']))
                self.to_download.append(json.loads(notification['Message']))
            deletion = self.sqs.delete_message_batch(
                QueueUrl=('https://sqs.eu-west-2.amazonaws.com/623240509878'
                          '/mo_hi_res_det_ukvx'),
                Entries=([{'Id': message['MessageId'],
                           'ReceiptHandle': message['ReceiptHandle']}
                          for message in messages])
            )

    def download_data(self):
        for sns_message in self.to_download:
            url = ("https://s3.eu-west-2.amazonaws.com/" +
                   sns_message['bucket'] + "/" + sns_message['key'])
            ref_time = sns_message['forecast_reference_time']
            ref_time = ref_time.replace("-", "").replace(":", "")
            if not os.path.exists("data/" + ref_time):
                os.makedirs("data/" + ref_time)
            urllib.request.urlretrieve(url, "data/" + ref_time + "/" +
                                       sns_message['name'] + "_" +
                                       sns_message['key'])


if __name__ == '__main__':
    downloader = AWSEarthDownloader()
    downloader.retrieve_messages()
    downloader.download_data()
