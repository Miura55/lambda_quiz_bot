# パッチファイルがあれば削除する
if [ -e "lambda_patch.zip" ]; then
    rm lambda_patch.zip
    echo "Removed old lambda_patch.zip"
fi

# 必要なモジュールをインストール
cp lambda_function.py build/
cd build/
pip install -r ../requirements.txt -t .

# buildディレクトリ内のファイルをzipに圧縮して保存する
zip -r ../lambda_patch .
cd ..
