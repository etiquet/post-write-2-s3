from flask import Flask, request, jsonify, Blueprint
import boto3
import os
from datetime import datetime
import mimetypes, logging , gzip , io

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AWS S3 Configuration
S3_BUCKET = os.getenv("S3_BUCKET")
S3_ACCESS_KEY_ID = os.getenv("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")
S3_REGION = os.getenv("S3_REGION")
S3_URL = os.getenv("S3_URL")
S3_FOLDER = os.getenv("S3_FOLDER", "odfclient")

s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY,
    region_name=S3_REGION,
    endpoint_url=S3_URL
)

#Kubernetes Health Check
health_check_bp = Blueprint('health_check', __name__)

@health_check_bp.route('/health')
def health_check():
    # Check database connectivity, pings, roundtrip request timings, etc
    # Return a JSON response with a status code of 200 if the application is healthy
    # Return a status code of 500 along with an error message if there are any issues
    return jsonify({'status': 'ok'}), 200

app.register_blueprint(health_check_bp)

def decompress_gzip(data):
    with gzip.GzipFile(fileobj=io.BytesIO(data), mode='rb') as f:
        return f.read()

@app.route('/ODFClient', methods=['POST'])
def upload_content():
    logger.info("ODFClient upload called")

    if not request.data:
        return jsonify({'error': 'No content in the request'}), 400
    
    content = request.data
    content_type = request.headers.get('Content-Type')
    content_encoding = request.headers.get('Content-Encoding')
    extension = mimetypes.guess_extension(content_type)
    
    headers = dict(request.headers)
    logger.info("Received request with headers: %s", headers)

    if content_encoding == 'gzip':
        try:
            logger.info("Got some zipped type / content ")
            content = decompress_gzip(content)
            logger.info("Unzipped ")
            extension = '.xml'  # Assuming the decompressed content is a text file
        except Exception as e:
            return jsonify({'error': f'Failed to decompress gzip content: {str(e)}'}), 400
    elif content_type == 'application/xml; charset=UTF-8':
        extension = '.xml'
    else:
        extension = mimetypes.guess_extension(content_type)
    
    if not extension:
        logger.info("Could not define extension with this mime : %s force to >> .rawbody" , content_type)
        extension = '.rawbody'
  
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"{S3_FOLDER}/{current_time}_odf{extension}"

    try:
        logger.info("Send content to bucket :" , file_name)
        s3.put_object(Bucket=S3_BUCKET, Key=file_name, Body=content, ContentType=content_type)
        return jsonify({'message': 'Content uploaded successfully', 'file_name': file_name}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
