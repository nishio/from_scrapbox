import re


def get_api_url(url_or_title, default_project="nishio"):
    """
    Given API URL, Page URL, Page Title or External Link, return API URL.

    >>> get_api_url("https://scrapbox.io/nishio/example")
    'https://scrapbox.io/api/pages/nishio/example'

    >>> get_api_url("https://scrapbox.io/api/pages/nishio/example")
    'https://scrapbox.io/api/pages/nishio/example'

    >>> get_api_url("example")
    'https://scrapbox.io/api/pages/nishio/example'

    >>> get_api_url("foobar/example")
    'https://scrapbox.io/api/pages/foobar/example'

    """
    import re

    if "api/pages/" in url_or_title:
        return url_or_title

    # Check if the input is a full URL (starts with "http:// or https://")
    if url_or_title.startswith("http://") or url_or_title.startswith("https://"):
        return re.sub(
            r"(https://scrapbox\.io)/([^/]+)/([^/]+)",
            r"\1/api/pages/\2/\3",
            url_or_title,
        )

    # If the input is a simple title or a partial URL, construct the full API URL
    if "/" in url_or_title:
        # It's a partial URL
        project, title = url_or_title.split("/", 1)
    else:
        # It's just a title
        project = default_project
        title = url_or_title

    return f"https://scrapbox.io/api/pages/{project}/{title}"
    return api_url


if __name__ == "__main__":
    import doctest

    doctest.testmod()
