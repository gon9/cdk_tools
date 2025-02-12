#!/usr/bin/env python3
import os
import aws_cdk as cdk
from lib.gpu.gpu_stack import GPUStack
from lib.cpu.cpu_stack import CPUStack
from lib.webapp.webapp_stack import WebAppStack

app = cdk.App()

# デプロイ環境の設定（例：AWSアカウントとリージョンを指定）
env = cdk.Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION", "us-east-1")
)

# GPU インスタンス用スタックの作成
GPUStack(app, "GPUStack", env=env)

# CPU インスタンス用スタックの作成
CPUStack(app, "CPUStack", env=env)

# Web アプリ用スタックの作成
WebAppStack(app, "WebAppStack", env=env)

app.synth()
