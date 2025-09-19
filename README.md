# Sample API

これは、FastAPI、Google Cloud Firestoreを使用して構築され、Google Cloud BuildおよびCloud RunによるCI/CDパイプラインでデプロイされたユーザープロフィールAPIのサンプルプロジェクトです。
## 技術スタック

- **バックエンド**: FastAPI, Uvicorn, Pydantic
- **データベース**: Google Cloud Firestore
- **コンテナ化**: Docker, Docker Compose
- **CI/CD**: Google Cloud Build, Google Cloud Run
- **テスト**: Pytest, HTTPX

## ローカル開発

ローカルでアプリケーションを実行するには、Dockerがインストールされている必要があります。

1.  **Clone:**
    ```bash
    git clone <repository-url>
    cd sample_fastapi_cicd
    ```

2.  **Service**
    ```bash
    docker-compose up --build
    ```

    このコマンドは、アプリケーションのDockerイメージをビルドし、`app`および`firestore-emulator`サービスを開始します。

3.  **APIにアクセスします:**
    APIは `http://localhost:8080` で利用可能になります。
    -   **ヘルスチェック**: `http://localhost:8080/health`
    -   **APIドキュメント**: `http://localhost:8080/docs`

    Firestoreエミュレータは `localhost:8090` で実行されます。

## CI/CDパイプライン

このプロジェクトは、Google Cloud Buildを使用したCI/CDパイプラインで構成されています。mainブランチに変更がプッシュされると、CloudRunにデプロイされます。

## APIエンドポイント

利用可能なAPIエンドポイントは`/docs` のSwagger UIドキュメントにて確認してください。

-   `GET /health`: ヘルスチェックステータスを返します。
-   `/users` プレフィックスのユーザー関連エンドポイント。