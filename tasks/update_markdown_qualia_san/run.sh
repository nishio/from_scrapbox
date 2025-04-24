set -e  # エラーが発生したらスクリプトを終了

PROJECT_NAME=qualia-san python -m tasks.export_json.main

deno run --allow-run --allow-read --allow-write tasks/json_to_markdown/mod.ts qualia-san.json qualia-san

echo "external_brain_in_markdown_qualia_san リポジトリを処理します..."

if [ -z "$GITHUB_TOKEN" ] && [ -z "$GITHUB_ACTIONS" ]; then
  echo "Git認証情報ヘルパーを設定します"
  git config --global credential.helper store
fi

if [ -d "external_brain_in_markdown_qualia_san" ]; then
  echo "既存の external_brain_in_markdown_qualia_san リポジトリを更新します"
  cd external_brain_in_markdown_qualia_san
  git pull
  cd ..
else
  echo "external_brain_in_markdown_qualia_san リポジトリをクローンします"
  if [ -n "$GITHUB_TOKEN" ]; then
    git clone https://x-access-token:${GITHUB_TOKEN}@github.com/nishio/external_brain_in_markdown_qualia_san.git
  else
    git clone https://github.com/nishio/external_brain_in_markdown_qualia_san.git
  fi
fi

mkdir -p external_brain_in_markdown_qualia_san/pages

echo "Markdown ファイルを external_brain_in_markdown_qualia_san/pages にコピーします"
cp -r quartzPages/* external_brain_in_markdown_qualia_san/pages/

cd external_brain_in_markdown_qualia_san
git add pages/ > /dev/null 2>&1
git commit --quiet --no-status -m "Update Qualia-san Markdown files from Scrapbox export $(date '+%Y-%m-%d %H:%M:%S')"

if [ -n "$GITHUB_TOKEN" ]; then
  git push https://x-access-token:${GITHUB_TOKEN}@github.com/nishio/external_brain_in_markdown_qualia_san.git
else
  git push
fi

cd ..
echo "Qualia-san版Markdown ファイルの更新が完了しました"
