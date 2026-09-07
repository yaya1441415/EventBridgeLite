from aws_cdk import (
    Duration,
    aws_lambda as lambda_,
    aws_lambda_event_sources as sources,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_sqs as sqs,
    aws_dynamodb as ddb,
)
from constructs import Construct

#reusable ConsumerPipeline construct that creates an SQS queue with DLQ
#
class ConsumerPipeline(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        topic: sns.Topic,
        source: str,
        event_types: list[str] | None = None,
        table:ddb.Table
    ) -> None:
        super().__init__(scope, construct_id)
        self.dlq = sqs.Queue(self, "Dlq")

        self.queue = sqs.Queue(
            self, 
            "Queue",
            visibility_timeout=Duration.seconds(60),
            dead_letter_queue=sqs.DeadLetterQueue(max_receive_count=3, queue=self.dlq),
        )

        filter_policy = None
        if event_types is not None:
            filter_policy = {
                "event_type": sns.SubscriptionFilter.string_filter(allowlist=event_types)
            }

        topic.add_subscription(
            subs.SqsSubscription(self.queue, filter_policy=filter_policy)
        )

        self.function = lambda_.Function(
            self,
            "Fn",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="handlers.lambda_handler.handler",
            code=lambda_.Code.from_asset(source),
            timeout=Duration.seconds(10),
        )

        self.function.add_environment("DEDUPE_TABLE", table.table_name)
        self.function.add_environment("CONSUMER_NAME", construct_id)
        table.grant_read_write_data(self.function)

        self.function.add_event_source(
            sources.SqsEventSource(self.queue, batch_size=5)
        )