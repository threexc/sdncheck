import re
from dataclasses import dataclass
from typing import List

from sdncheck.cli_parser import SDNCheckParser
from sdncheck.mbox import PatchSeries

email_pattern = re.compile("(?P<user>[A-Za-z0-9._%+-]+)@(?P<hostname>[A-Za-z0-9.-]+)\.(?P<domain>[A-Za-z]{2,})")

@dataclass
class SDNMatch:
    subject: str
    author_match: List[str]
    to_matches: List[str]
    cc_matches: List[str]

def get_domains_to_match(matchfile):
    # get all valid email addresses in the match list, and ignore everything
    # else
    with open(matchfile) as match_list:
        filedata = match_list.read()

        # search for all occurrences, but use finditer() so that the matches
        # remain intact
        emails = [x.group() for x in re.finditer(email_pattern, filedata)]

        if not emails:
            print(f"No valid email addresses or domains to match against in {args.match_list}")

        # now get the respective domains to check against the actual patch(es)
        domains = [address.split("@", 1)[1] for address in emails]

        return emails, domains

def check_domains_against_series(domains, series):
    results = []
    # check each patch in the target series for bad addresses
    for patch in series.patchdata:
        author = patch.author
        to_list = patch.to.split(",")
        cc_list = patch.cc.split(",")
        author_result = []
        to_result = []
        cc_result = []

        for domain in domains:
            if domain in author:
                author_result.append(author)

            for recipient in to_list:
                if domain in recipient:
                    to_result.append(recipient)

            for recipient in cc_list:
                if domain in recipient:
                    cc_result.append(recipient)

        if author_result or to_result or cc_result:
            results.append(SDNMatch(patch.subject, author_result, to_result,
                                    cc_result))
    return results

def run():
    cli_parser = SDNCheckParser.get_cli_parser()
    args = cli_parser.parse_args()
    series = PatchSeries(args.patch_path)
    matches, domains = get_domains_to_match(args.match_list)

    if args.debug:
        print(f"[DEBUG] Found the following email addresses in the match list: ")
        print()
        for match in matches:
            print(f"- {match}")
        print()

        print(f"[DEBUG] Checking against the following domains: ")
        print()
        for domain in domains:
            print(f"- {domain}")
        print()

    results = check_domains_against_series(domains, series)

    print(results)
    for result in results:
        pass
