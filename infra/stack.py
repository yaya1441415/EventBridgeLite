from aws_cdk import Stack, CfnOutput, aws_sns as sns,  RemovalPolicy, aws_dynamodb as ddb
from constructs import Construct

from pipeline import ConsumerPipeline


class EventBridgeLiteStack(Stack):
    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        topic = sns.Topic(self, "EventsTopic", display_name="EventBridge Lite events")

        table = ddb.Table(
            self, 
            "DedupeTable",
            partition_key=ddb.Attribute(name="pk", type=ddb.AttributeType.STRING),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
            time_to_live_attribute="expires_at",
            removal_policy=RemovalPolicy.DESTROY,
        )
        for name, source, types in [
            ("Email", "services/consumer_email", ["user.signed_up"]),
            ("Sms", "services/consumer_sms", ["order.placed"]),
            ("Analytics", "services/consumer_analytics", None),
        ]:
            ConsumerPipeline(self, name, topic=topic, source=source, event_types=types, table=table )

        CfnOutput(self, "TopicArn", value=topic.topic_arn)