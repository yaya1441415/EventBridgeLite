from aws_cdk import App
from stack import EventBridgeLiteStack

app = App()
EventBridgeLiteStack(app, "EventBridgeLiteStack")
app.synth()
