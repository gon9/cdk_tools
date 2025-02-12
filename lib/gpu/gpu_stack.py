from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct
from lib.common import security_group

class GPUStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. 新規VPCの作成     
        vpc = ec2.Vpc(self, "GPUVpc",
                      max_azs=2,
                      nat_gateways=0,  # NAT Gatewayを作成しないことでコスト削減
                      subnet_configuration=[
                          ec2.SubnetConfiguration(
                              name="PublicSubnet",
                              subnet_type=ec2.SubnetType.PUBLIC,
                          )
                      ]
                     )

        # 2. SSM 用の IAM ロールの作成
        instance_role = iam.Role(
            self,  # このスタック（またはコンストラクト）を親として指定しています
            "InstanceSSMRole",  # この IAM ロールの論理ID（スタック内で一意の識別子）を定義
            # このロールが引き受けられる主体（サービス）を指定。ここでは EC2 インスタンスがこのロールを引き受けます
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            # EC2 インスタンスにSSM機能を利用させるための権限（マネージドポリシー）をアタッチしています。
            managed_policies=[
                # AWS が提供する SSM 用のマネージドポリシー「AmazonSSMManagedInstanceCore」をロールに追加
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
            ]
        )

        # 2．共通のセキュリティグループを作成（例）
        sg = security_group.create_default_security_group(self, vpc, id="GPUSecurityGroup")

        # 3. Deep Learning AMI の定義
        # Deep Learning AMI を直接指定
        machine_image = ec2.MachineImage.generic_linux(
            {
                "us-east-1": "ami-08ea187523fb45736", # Deep Learning Base OSS Nvidia Driver GPU AMI (Ubuntu 22.04) (x86)
                "ap-northeast-1": "ami-0ff7e0c3a0324f48d" # Deep Learning Base OSS Nvidia Driver GPU AMI (Amazon Linux 2) (x86)
            }
        )

        # 4. GPU インスタンスの作成
        ec2.Instance(
            self,
            "GPUInstance",
            instance_type=ec2.InstanceType("g4dn.xlarge"),
            machine_image=machine_image,
            vpc=vpc,
            security_group=sg,
            role=instance_role
        ) 
