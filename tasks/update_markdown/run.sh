# export from https://scrapbox.io/nishio to nishio.json
python -m tasks.export_json.main

# json to markdown
# Read /nishio.json and write to /obsidianPages/
deno run --allow-run --allow-read --allow-write tasks/json_to_markdown/mod.ts nishio.json nishio

# external_brain_in_markdown リポジトリの処理
echo "external_brain_in_markdown リポジトリを処理します..."

# リポジトリのクローン（存在しない場合）またはプル（存在する場合）
if [ -d "external_brain_in_markdown" ]; then
  echo "既存の external_brain_in_markdown リポジトリを更新します"
  cd external_brain_in_markdown
  git pull
  cd ..
else
  echo "external_brain_in_markdown リポジトリをクローンします"
  # GitHub Actions の場合は GITHUB_TOKEN を使用
  if [ -n "$GITHUB_TOKEN" ]; then
    git clone https://x-access-token:${GITHUB_TOKEN}@github.com/nishio/external_brain_in_markdown.git
  else
    git clone https://github.com/nishio/external_brain_in_markdown.git
  fi
fi

# pages ディレクトリが存在することを確認
mkdir -p external_brain_in_markdown/pages

# Markdown ファイルをコピー
echo "Markdown ファイルを external_brain_in_markdown/pages にコピーします"
cp -r obsidianPages/* external_brain_in_markdown/pages/

# 変更をコミットしてプッシュ
cd external_brain_in_markdown
git add pages/
git commit -m "Update Markdown files from Scrapbox export $(date '+%Y-%m-%d %H:%M:%S')"

# GitHub Actions の場合は GITHUB_TOKEN を使用
if [ -n "$GITHUB_TOKEN" ]; then
  git push https://x-access-token:${GITHUB_TOKEN}@github.com/nishio/external_brain_in_markdown.git
else
  git push
fi

cd ..
echo "Markdown ファイルの更新が完了しました"
