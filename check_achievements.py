"""Print the achievements GitHub displays on a public user profile."""

import argparse
from html.parser import HTMLParser
import re
import sys
from urllib.error import URLError
from urllib.request import Request, urlopen


class BadgeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.badges = set()

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            label = dict(attrs).get("alt") or ""
            if label.startswith("Achievement: "):
                self.badges.add(label.removeprefix("Achievement: ").strip())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("username", help="GitHub profile to check")
    username = parser.parse_args().username
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,38}", username):
        parser.error("Enter a GitHub username, without a URL or @ sign.")
    request = Request(
        f"https://github.com/{username}?tab=achievements",
        headers={"User-Agent": "github-achievement-check/1.0"},
    )
    try:
        with urlopen(request, timeout=15) as response:
            html = response.read().decode("utf-8")
    except (URLError, TimeoutError) as error:
        print(f"Could not read the profile for {username}: {error}", file=sys.stderr)
        return 1
    profile = BadgeParser()
    profile.feed(html)
    for badge in sorted(profile.badges):
        print(badge)
    if not profile.badges:
        print("No public achievement badges found on the page.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
