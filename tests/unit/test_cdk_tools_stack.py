import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_tools.cdk_tools_stack import CdkToolsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_tools/cdk_tools_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkToolsStack(app, "cdk-tools")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
