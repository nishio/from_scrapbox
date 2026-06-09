# From Scrapbox

This is the code repository for exporting Scrapbox projects and converting the exported JSON into Markdown.

Generated Markdown is stored in separate data repositories. The daily scheduled workflows for the Japanese and English exports live in the data repositories so their activity follows the data they update.

## Data Repositories

- Japanese: [nishio](https://scrapbox.io/nishio/) to [nishio/external_brain_in_markdown](https://github.com/nishio/external_brain_in_markdown)
- English: [nishio-en](https://scrapbox.io/nishio-en/) to [nishio/external_brain_in_markdown_english](https://github.com/nishio/external_brain_in_markdown_english)
- Qualia-san: [qualia-san](https://scrapbox.io/qualia-san/) to [nishio/external_brain_in_markdown_qualia_san](https://github.com/nishio/external_brain_in_markdown_qualia_san)

## Repository Contents

- `tasks/export_json/`: exports Scrapbox project data with the Scrapbox export API
- `tasks/json_to_markdown/`: converts exported Scrapbox JSON into Markdown
- `tasks/update_markdown*/`: legacy orchestration scripts for updating data repositories
- `utils/`: shared Scrapbox and URL helpers

## Current Automation

The active scheduled workflows are in the data repositories:

- [external_brain_in_markdown/.github/workflows/update_markdown.yml](https://github.com/nishio/external_brain_in_markdown/blob/main/.github/workflows/update_markdown.yml)
- [external_brain_in_markdown_english/.github/workflows/update_markdown.yml](https://github.com/nishio/external_brain_in_markdown_english/blob/main/.github/workflows/update_markdown.yml)

Those workflows check out this repository as `_tools/from_scrapbox`, run the export and conversion code, then commit generated Markdown back to their own `pages/` directory.

For background, see [the author's Scrapbox page](https://scrapbox.io/nishio/From_Scrapbox) or [community notes](https://scrapbox.io/villagepump/nishio%2Ffrom_scrapbox).
