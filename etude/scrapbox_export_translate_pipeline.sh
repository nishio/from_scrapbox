#!/bin/bash
# Scrapbox Export and Translation Pipeline
# このスクリプトはScrapboxプロジェクトのデータをエクスポート、クロール、翻訳する一連の処理を自動化します

# ステップ1: Scrapboxからプロジェクトデータをエクスポート（環境変数のPROJECT_NAMEを使用）
echo "ステップ1: Scrapboxからプロジェクトデータをエクスポート"
python -m tasks.export_json.main

# ステップ2: Scrapboxの「nishio」プロジェクトをクロール
echo "ステップ2: Scrapboxの「nishio」プロジェクトをクロール"
deno run --allow-read --allow-net --allow-write tasks/crawl_scrapbox/index.ts --project nishio

# ステップ3: クロールしたデータからすべてのリンクを抽出
echo "ステップ3: すべてのリンクを抽出"
python -m tasks.list_all_links.main

# ステップ4: 日本語を含むリンクを英語に翻訳
echo "ステップ4: リンクを英語に翻訳"
python -m tasks.translate.translate_links

# ステップ5: 翻訳後のタイトルに衝突がないかチェック
echo "ステップ5: タイトルの衝突をチェック"
python -m etude.link_collision_check

echo "処理が完了しました"