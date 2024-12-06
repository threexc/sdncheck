# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
#
# cli_parser: implementation of a sdncheck-specific parser
#
# Copyright (C) 2024 Trevor Gamblin <tgamblin@baylibre.com>
#
# SPDX-License-Identifier: GPL-2.0-only
#

import os
import argparse

default_testdir = os.path.abspath(os.path.dirname(__file__) + "/tests")

class SDNCheckParser(object):
    """Abstract the sdncheck argument parser"""

    @classmethod
    def get_cli_parser(cls):
        cli_parser = argparse.ArgumentParser()

        target_patch_group = cli_parser.add_mutually_exclusive_group(required=True)

        target_patch_group.add_argument(
            "--patch", metavar="PATCH", dest="patch_path", help="The patch to be tested"
        )

        target_patch_group.add_argument(
            "--directory",
            metavar="DIRECTORY",
            dest="patch_path",
            help="The directory containing patches to be tested",
        )

        cli_parser.add_argument(
            "--debug", "-d", action="store_true", help="Enable debug output"
        )

        cli_parser.add_argument(
            "--log-results",
            action="store_true",
            help='Enable logging to a file matching the target patch name with ".testresult" appended',
        )

        return cli_parser
