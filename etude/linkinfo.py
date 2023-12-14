from utils.read_scrapbox_page import read_page

data = read_page("test")
links = set(data["links"])
print("links", links)
linksLc_to_links = {link.lower(): link for link in links}

links1hop = set(x["title"] for x in data["relatedPages"]["links1hop"])
print("links1hop", links1hop)

links2hop_link = set()
for x in data["relatedPages"]["links2hop"]:
    links2hop_link.update([linksLc_to_links[link] for link in x["linksLc"]])
print("links2hop_link", links2hop_link)


redlinks = links - links1hop - links2hop_link
backlinks = links1hop - links
forelinks = links1hop.intersection(links)
alllinks = links.union(links1hop.union(links2hop_link))

for link in alllinks:
    print(link)
    if link in forelinks:
        print("  is link to persistent page")
    if link in backlinks:
        print("  is backlink")
    if not link in redlinks:
        print("  is blue link")
    else:
        print("  is red link")

if 0:  # External link
    print(data["relatedPages"])
    projectLinks = set(data["projectLinks"])
    print("projectLinks", projectLinks)

    projectLinks1hop = set(data["relatedPages"]["projectLinks1hop"])
    print("projectLinks1hop", projectLinks1hop)

    print("projectBacklinks", projectLinks1hop - projectLinks)
