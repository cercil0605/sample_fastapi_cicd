import os
from google.cloud import firestore
from dotenv import load_dotenv

# envに基づいてfirestoreと通信
_db = None
load_dotenv()


def get_db() -> firestore.Client:
    global _db
    if _db is None:
        if os.getenv("FIRESTORE_EMULATOR_HOST"):
            # エミュレータに接続
            _db = firestore.Client()
        else:
            # 実際のFirestoreに接続
            _db = firestore.Client(project=os.getenv("FIRESTORE_PROJECT_ID"))
    return _db
