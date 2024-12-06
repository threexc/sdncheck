from sdncheck.cli_parser import SDNCheckParser
from sdncheck.mbox import PatchSeries
from sdncheck.tests.core import SDNCheckResults

def run():
    cli_parser = SDNCheckParser.get_cli_parser()
    args = cli_parser.parse_args()
    series = PatchSeries(args.patch_path)
    for testresult in results.mbox_signed_off_by_results:
        print(testresult)
    for testresult in results.mbox_shortlog_format_results:
        print(testresult)
    for testresult in results.mbox_commit_message_presence_results:
        print(testresult)
