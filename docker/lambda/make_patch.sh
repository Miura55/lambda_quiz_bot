# パッチファイルがあれば削除する
if [ -e lambda_patch.zip ]; then
    rm lambda_patch.zip
    echo "Removed old lambda_patch.zip"
fi

# buildディレクトリ内のファイルをzipに圧縮して保存する
zip -r lambda_patch build/
