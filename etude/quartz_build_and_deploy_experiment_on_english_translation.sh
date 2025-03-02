# 英訳JSONをQuartzで配信する実験

cp etude-github-actions/nishio/data_en_prev.json nishio.json

tasks/json_to_markdown/run.sh

cd quartz; npx quartz build

# cp -r quartz/public/* quartz_deploy/
rsync -av quartz/public/ quartz_deploy/