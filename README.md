es# ML Development Environment using AWS CDK (Python)

このプロジェクトは、AWS CDK (Python) を使用して、GPU を利用した機械学習開発環境を構築するサンプルスタックです。

## 特徴
- **新規VPC作成**: パブリックサブネットのみを含むシンプルな VPC を構築します。
- **セキュリティグループ**:
  - Mac からのアクセスについて、**セッションマネージャー** 経由の場合は SSH キーペア（ベアキー）は不要となります。
  - もし SSH 接続を利用する場合は、該当のキーペアによる認証が必要です。
  - HTTPアクセス（ポート80）は全体に対して許可
- **GPU対応EC2インスタンス**:
  - 軽量なGPUインスタンス（g4dn.xlarge）を1台起動
  - Deep Learning 用 AMI の指定方法として、SSM パラメータ経由と固定AMI ID（cdk.context.json 経由）の2通りをサポート
- **ストレージ**:
  - 50GB の EBS ボリュームをアタッチ（スタック削除時に自動削除される設定）

## 前提条件
- AWS CLI がインストール済みかつ設定済みであること
- AWS CDK がインストール済み (`npm install -g aws-cdk`)
- Python 3.7 以上
- 仮想環境の作成および依存パッケージのインストール（`poetry install`）
- AWS アカウントにおいて、EC2 や VPC などのリソースを作成する権限があること

※ セッションマネージャーを利用する場合、SSHキーペア（ベアキー）の設定は不要です。  
　SSH 接続を利用する場合は、必要に応じてキーペアやセキュリティグループの設定を行ってください。

## セットアップ手順

1. **リポジトリのクローン**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Python 仮想環境の作成と依存パッケージのインストール**
    ```bash
    pyenv install 3.10.x  # 使用したいPythonバージョンをインストール（例: 3.9.7など）
    pyenv local 3.10.x     # プロジェクトで使用するPythonバージョンを設定
    poetry install      # 依存パッケージをインストール
    ```

3. **CDK ブートストラップ**
    ```bash
    poetry run cdk bootstrap
    ```

4. **コードの設定**

    - **固定AMI ID を利用する場合**:
        - `cdk.context.json` にリージョン毎の AMI ID を記載してください。  
          例:
          ```json:cdk.context.json
          {
            "gpu_ami_configs": {
              "us-east-1": "ami-0abcdef1234567890",
              "ap-northeast-1": "ami-0fedcba9876543210"
            }
          }
          ```
    - **SSM パラメータ経由で AMI ID を利用する場合**:
        - **AWS 公式のパラメータを利用する場合**:
            - AWS Systems Manager Parameter Store に、AWS が公式に提供する Deep Learning 用 AMI のパラメータ（例: `/aws/service/deep-learning-ami/amazon-linux-2/latest`）がすでに登録されているため、追加の登録作業は不要です。
        - **カスタム AMI を利用する場合**:
            - 独自に用意した AMI ID を利用するならば、Parameter Store に例えば `/gpu/ami/deep-learning` などの名前でパラメータを登録し、そのパラメータ名を CDK コード内で使用してください（例: `MachineImage.from_ssm_parameter("/gpu/ami/deep-learning", os=...)`）。

5. **スタックのデプロイ**
    ```bash
    cdk deploy GPUStack  # スタック名を指定。 例えば GPUStack など
    ```
6. **インスタンスIDの確認**
    - インスタンスIDは、スタックデプロイ後に確認してください。
    ```bash
    cdk ls
    ```

7. **SSMを利用したアクセス**
    - セッションマネージャーを利用したアクセスの場合は、以下のコマンドでアクセスしてください。
    ```bash
    aws ssm start-session --target <インスタンスID>
    ```

8. **リソースの削除**
    開発終了後や不要になった場合は、以下のコマンドでリソースを削除してください。
    ```bash
    cdk destroy GPUStack  # スタック名を指定。 例えば GPUStack など
    ```

## SSMパラメータを利用する場合の追加設定

**Parameter Store へのパラメータ登録**:
   - AWS マネジメントコンソールまたは AWS CLI を利用して、例えば `/gpu/ami/deep-learning` という名前でパラメータを登録してください。
   - 値は、該当リージョンの Deep Learning 用 GPU AMI ID を設定します。

## ToDoリスト
- [ ] **設定の確認**:
  - 固定AMI ID利用時は、`cdk.context.json` の値を確認
  - SSMパラメータ経由の場合は、Parameter Store に正しい値が登録されているか確認
- [ ] **接続方法の選択**:
  - セッションマネージャーを利用する場合、SSH のためのキーペア設定は不要
  - SSH 接続を利用する場合は、`YOUR_KEY_PAIR_NAME` の設定が必要となります（別途セキュリティグループ等の設定も実施してください）。
- [ ] **アクセス元IP 更新**（SSH 利用時のみ）: Mac のグローバルIPなど、必要に応じた設定を行ってください。
- [ ] **デプロイテスト**: インスタンスが正常に起動し、セッションマネージャー経由または SSH 接続が可能か確認

## 注意点
- このスタックは開発目的用です。長期間利用する場合や本番環境での利用時は、セキュリティやコスト管理に十分注意してください。
- AWS CDK および各リソースの最新情報は、[AWS CDK の公式ドキュメント](https://docs.aws.amazon.com/cdk/latest/guide/home.html) をご参照ください。

## ライセンス
[MIT License](LICENSE)
