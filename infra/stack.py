from aws_cdk import Stack, CfnOutput, aws_sns as sns
from constructs import Construct

from pipeline import ConsumerPipeline


class EventBridgeLiteStack(Stack):
    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        topic = sns.Topic(self, "EventsTopic", display_name="EventBridge Lite events")

        for name, source, types in [
            ("Email", "services/consumer_email", ["user.signed_up"]),
            ("Sms", "services/consumer_sms", ["order.placed"]),
            ("Analytics", "services/consumer_analytics", None),
        ]:
            ConsumerPipeline(self, name, topic=topic, source=source, event_types=types)

        CfnOutput(self, "TopicArn", value=topic.topic_arn)