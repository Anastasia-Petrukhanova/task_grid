import boto3
import json

def main():
    boto_session = boto3.Session(
        aws_access_key_id='', # your value
        aws_secret_access_key='') # your value
    sqs = boto_session.client(
        service_name='sqs',
        endpoint_url='https://message-queue.api.cloud.yandex.net',
        region_name='ru-central1')
    queue_url = '' # your value
    while True:
        print("Select action (print number): ")
        print("1) Send message")
        print("2) Recieve and delete message")
        print("3) Exit")
        action = input()
        if action == '1':
            while True:
                print("Delay: ")
                answer = input()
                if answer.isnumeric():
                    break
            print("Print message: ")
            message = input()
            response = sqs.send_message(
                QueueUrl=queue_url,
                DelaySeconds=int(answer),
                MessageBody=message
            )
            print("The message has been sent. Its id: " + response['MessageId'])
        elif action == '2':
            response = sqs.receive_message(
                QueueUrl=queue_url,
                AttributeNames=[
                    'SentTimestamp'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ],
                VisibilityTimeout=0,
                WaitTimeSeconds=10
            )
            if 'Messages' in response:
                message = response['Messages'][0]
                receipt_handle = message['ReceiptHandle']
                receipt_body = message['Body']
                print('Received Body: %s' % receipt_body)
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=receipt_handle
                )
                print('Received and deleted message: %s' % message)
            else:
                print("There are no messages in the queue")
        elif action == '3':
            break
        else:
            print("Invalid value")

if __name__ == '__main__':
    main()