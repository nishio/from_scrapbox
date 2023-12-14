import os
import json
from utils.scrapbox import export_pages
import dotenv
import argparse

dotenv.load_dotenv()
dotenv.load_dotenv(".env_public")

# Getting environment variables
SID = os.getenv("SID")
PROJECT_NAME = os.getenv("PROJECT_NAME")
assert SID

parser = argparse.ArgumentParser(description="Export project data.")
parser.add_argument(
    "--project",
    type=str,
    default=PROJECT_NAME,
    help="The name of the project to export.",
)
parser.add_argument(
    "--meta",
    action="store_true",
    help="With metadata",
)
args = parser.parse_args()
PROJECT_NAME = args.project

outfile = f"{PROJECT_NAME}.json" if not args.meta else f"{PROJECT_NAME}_meta.json"

print(f'Exporting a json file from "/{PROJECT_NAME}"...')
result = export_pages(PROJECT_NAME, args.meta)
with open(outfile, "w") as file:
    json.dump(result, file, indent=2)

print(f'OK, wrote "{outfile}"')
