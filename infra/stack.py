from aws_cdk import (
    Stack, 
    CfnOutput,
    aws_sns as sns,
    aws_sqs as sqs,
    aws_sns_subscriptions as subs,
    Duration,
    aws_lambda as lambda_,
    aws_lambda_event_sources as sources
)
from constructs import Construct # CDK's base construct class


#create an Sns Topic and an SQS queue,
#Subscribes the queue to th etopic (messages sent
#to topic go to queue)
#output the ARN and URL 
class EventBridgeLiteStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        topic = sns.Topic(self, "EventsTopic", display_name="EventBridge Lite events")
        dlq = sqs.Queue(self, "EmailDLQ")

        email_queue =  sqs.Queue(
                        self, "EmailQueue",
                        visibility_timeout=Duration.seconds(30),
                        dead_letter_queue=sqs.DeadLetterQueue(max_receive_count=3, queue=dlq),
                    )

        email_fn = lambda_.Function(
            self, "EmailConsumer",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="handlers.lambda_handler.handler",
            code=lambda_.Code.from_asset("services/consumer_email"),
            timeout=Duration.seconds(10),
        )

        email_fn.add_event_source(sources.SqsEventSource(email_queue, batch_size=5))
        #any message published to the topic goes automatically to the queue
        topic.add_subscription(subs.SqsSubscription(email_queue))

        CfnOutput(self, "TopicArn", value=topic.topic_arn)
        CfnOutput(self, "EmailQueueUrl", value=email_queue.queue_url)



        

