from aws_cdk import aws_ec2 as ec2
from constructs import Construct

def create_default_security_group(scope: Construct, vpc: ec2.IVpc, id: str = "DefaultSG", description: str = "Default security group") -> ec2.SecurityGroup:
    sg = ec2.SecurityGroup(
        scope,
        id,
        vpc=vpc,
        security_group_name=id,
        description=description,
        allow_all_outbound=True
    )

    # SSM を利用する場合、SSH (ポート22) のインバウンドルールは不要
    # もし SSH を有効にしたい場合は、以下のコメントを外してください。
    # sg.add_ingress_rule(
    #     ec2.Peer.any_ipv4(),
    #     ec2.Port.tcp(22),
    #     "Allow SSH access"
    # )
    return sg 