from flask import jsonify, request, current_app
from app import db
from app.api import bp
import boto3

# 上傳圖片 API 
@bp.route('/api/upload', methods=['POST'])
def upload_file():
    S3_BUCKET_NAME = current_app.config['S3_BUCKET_NAME']
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_name = f"Toyota2021Vios1.5經典/{file.filename}"

            # 上傳到 S3
            try:
                s3 = boto3.client('s3', aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'])
                s3.upload_fileobj(file, S3_BUCKET_NAME, file_name, 
                    ExtraArgs={'ContentType': 'image/jpeg'})
                
                url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file_name}"

                return jsonify({'url': url})
            
            except Exception as err:
                return jsonify({'error': str(err)}), 500
            
    return 'No file selected'