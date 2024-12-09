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

def get_matches(matchfile):
    # get all valid email addresses in the match list, and ignore everything
    # else
    with open(matchfile) as match_list:
        filedata = match_list.read()

        # search for all occurrences, but use finditer() so that the matches
        # remain intact
        return [x.group() for x in re.finditer(email_pattern, filedata)]

def run():
    cli_parser = SDNCheckParser.get_cli_parser()
    args = cli_parser.parse_args()
    series = PatchSeries(args.patch_path)
    matches = None
    domains = None
    results = []
    
    #matches = get_matches(args.match_list)
    # get all valid email addresses in the match list, and ignore everything
    # else
    with open(args.match_list) as match_list:
        filedata = match_list.read()

        # search for all occurrences, but use finditer() so that the matches
        # remain intact
        matches = [x.group() for x in re.finditer(email_pattern, filedata)]

    if not matches:
        print(f"No valid email addresses or domains to match against in {args.match_list}")
    if args.debug:
        print(f"[DEBUG] Found the following email addresses in the match list: ")
        print()
        for match in matches:
            print(f"- {match}")
        print()

    # now get the respective domains to check against the actual patch(es)
    domains = [address.split("@", 1)[1] for address in matches]
    if args.debug:
        print(f"[DEBUG] Checking against the following domains: ")
        print()
        for domain in domains:
            print(domain)

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

        if not author_result and not to_result and not cc_result:
            print(f"No bad addresses found in '{patch.subject}'.")
        else:
            results.append(SDNMatch(patch.subject, author_result, to_result,
                                    cc_result))

    print(results)
    for result in results:
        pass
