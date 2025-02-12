from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct

class CPUStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC の作成
        vpc = ec2.Vpc(self, "CPUVpc", max_azs=2)

        # 最新の Amazon Linux を利用
        machine_image = ec2.MachineImage.latest_amazon_linux()

        # CPU インスタンスの作成（例: t3.medium インスタンス）
        ec2.Instance(
            self,
            "CPUInstance",
            instance_type=ec2.InstanceType("t3.medium"),
            machine_image=machine_image,
            vpc=vpc,
        ) 