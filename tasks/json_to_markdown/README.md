# JSON to Markdown

Derived from https://github.com/blu3mo/ScrapboxToObsidian

## Usage

### Setup

I added `blu3mo/ScrapboxToObsidian` as git-submodule:
```bash
git submodule add https://github.com/blu3mo/ScrapboxToObsidian
```

You can do as follows:

Updating Submodules: If the submodule has new commits, you can update it by running `git submodule update --remote`

Cloning a Repository with Submodules: When cloning a repository with submodules, use `git clone --recurse-submodules [URL]` to ensure the submodules are also cloned.

### Run

`tasks/json_to_markdown/run.sh`

Read /nishio.json and write to /obsidianPages/...

