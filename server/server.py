from flask import Flask, send_file, send_from_directory, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'apps'
ALLOWED_EXTENSIONS = {'py', 'ini', 'png', 'jpg', 'jpeg', 'gif'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['DOWNLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 限制


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 文件列表 API
@app.route('/apps')
def list_files():
    file_list = [
        {'id': '@1', 'label': 'code', 'children': [{'id': '10001', 'label': '请求百度'}, {'id': '10002', 'label': '请求google'}]},
        {'id': '@2', 'label': 'cmd', 'children': [{'id': '20001', 'label': 'ping命令'}, {'id': '20002', 'label': 'B'}]},
        {'id': '@3', 'label': 'exe', 'children': [{'id': '30001', 'label': 'C'}, {'id': '30002', 'label': 'D'}]},
    ]
    return jsonify(file_list)

# 文件列表 API
@app.route('/app/<string:app_id>')
def list_file(app_id):
    file_list = []
    for root, dirs, files in os.walk(os.path.join('apps', f'app_{app_id}')):
        print(root, dirs, files)
        for file in files:
            filepath = os.path.normpath(os.path.join(root, file)).replace(str(os.path.sep), str(os.path.altsep))
            file_list.append(filepath)
    return jsonify(file_list)


# 下载文件
@app.route('/download/<path:filepath>')
def download(filepath):
    dir_path = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    print(dir_path, filename, filepath)
    # 防止路径遍历攻击
    return send_file(
        filepath,
        as_attachment=True,
        download_name=filename  # Flask 2.0+ 使用 download_name
    )


if __name__ == '__main__':
    # 确保上传目录存在
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, port=5000)
