import boto3
import botocore
from fastapi import UploadFile
from .config import settings

def upload_faiss_to_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        endpoint_url=f"https://{settings.S3_ENDPOINT}"
    )
    s3.upload_file(settings.VECTOR_DB_PATH, settings.S3_FAISS_BUCKET, "faiss_index")
    s3.upload_file(settings.VECTOR_DB_PATH + "_meta.pkl", settings.S3_FAISS_BUCKET, "faiss_index_meta.pkl")

def download_faiss_from_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        endpoint_url=f"https://{settings.S3_ENDPOINT}"
    )

    try:
        s3.head_object(Bucket=settings.S3_FAISS_BUCKET, Key="faiss_index")
        s3.download_file(settings.S3_FAISS_BUCKET, "faiss_index", settings.VECTOR_DB_PATH)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print("No FAISS index found in S3. Starting fresh.")
        else:
            raise

    try:
        s3.head_object(Bucket=settings.S3_FAISS_BUCKET, Key="faiss_index_meta.pkl")
        s3.download_file(settings.S3_FAISS_BUCKET, "faiss_index_meta.pkl", settings.VECTOR_DB_PATH + "_meta.pkl")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print("No FAISS metadata found in S3. Starting fresh.")
        else:
            raise

def upload_file_to_docs_s3(file: UploadFile):
    import io
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        endpoint_url=f"https://{settings.S3_ENDPOINT}"
    )

    file.file.seek(0)
    data = file.file.read()
    file_size = len(data)
    if file_size == 0:
        raise ValueError(f"File {file.filename} is empty")

    s3.put_object(
        Bucket=settings.S3_DOCS_BUCKET,
        Key=file.filename,
        Body=io.BytesIO(data),
    )

def clear_faiss_from_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        endpoint_url=f"https://{settings.S3_ENDPOINT}"
    )

    keys = ["faiss_index", "faiss_index_meta.pkl"]

    for key in keys:
        try:
            s3.delete_object(Bucket=settings.S3_FAISS_BUCKET, Key=key)
            print(f"Deleted {key} from {settings.S3_FAISS_BUCKET}")
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                print(f"{key} not found in {settings.S3_FAISS_BUCKET}")
            else:
                raise

def clear_docs_from_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        endpoint_url=f"https://{settings.S3_ENDPOINT}"
    )

    objects = s3.list_objects_v2(Bucket=settings.S3_DOCS_BUCKET).get("Contents", [])
    if not objects:
        print(f"No documents found in {settings.S3_DOCS_BUCKET}")
        return

    for obj in objects:
        key = obj["Key"]
        s3.delete_object(Bucket=settings.S3_DOCS_BUCKET, Key=key)
        print(f"Deleted {key} from {settings.S3_DOCS_BUCKET}")

def clear_all_from_s3():
    clear_docs_from_s3()
    clear_faiss_from_s3()
    print("All documents and FAISS index cleared from S3.")


def list_docs_in_s3():
    """
    List all documents currently stored in the docs S3 bucket.
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        endpoint_url=f"https://{settings.S3_ENDPOINT}"
    )

    objects = s3.list_objects_v2(Bucket=settings.S3_DOCS_BUCKET).get("Contents", [])
    if not objects:
        print(f"No documents found in {settings.S3_DOCS_BUCKET}")
        return []

    doc_keys = [obj["Key"] for obj in objects]
    print(f"Documents in {settings.S3_DOCS_BUCKET}: {doc_keys}")
    return doc_keys
