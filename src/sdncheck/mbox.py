#! /usr/bin/env python3

# mbox.py
#
# Classes for representing mboxes, parsed patches and patch series, and
# the repositories they target
#
# Copyright (C) Trevor Gamblin <tgamblin@baylibre.com>
#
# SPDX-License-Identifier: GPL-2.0-only
#

import email
import os
import re

from dataclasses import dataclass

# From: https://stackoverflow.com/questions/59681461/read-a-big-mbox-file-with-python
class MboxReader:
    def __init__(self, filepath):
        self.handle = open(filepath, "rb")
        assert self.handle.readline().startswith(b"From ")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.handle.close()

    def __iter__(self):
        return iter(self.__next__())

    def __next__(self):
        lines = []
        while True:
            line = self.handle.readline()
            if line == b"" or line.startswith(b"From "):
                yield email.message_from_bytes(b"".join(lines))
                if line == b"":
                    break
                lines = []
                continue
            lines.append(line)


class Patch:
    def __init__(self, data):
        self.author = data["From"]
        self.to = data["To"]
        self.cc = data["Cc"]
        self.subject = data["Subject"]
        self.split_body = re.split("---", data.get_payload(), maxsplit=1)
        self.commit_message = self.split_body[0]
        self.diff = self.split_body[1]
        # get the shortlog, but make sure to exclude bracketed prefixes
        # before the colon, and remove extra whitespace/newlines
        self.shortlog = self.subject[self.subject.find(']', 0,
            self.subject.find(':')) + 1:].replace('\n', '').strip()

class PatchSeries:
    def __init__(self, filepath):
        with MboxReader(filepath) as mbox:
            # Keep raw copies of messages in a list
            self.messages = [message for message in mbox]
            # Get a copy of each message's core patch contents
            self.patchdata = [Patch(message) for message in
                              self.messages]

        assert self.patchdata
        self.patch_count = len(self.patchdata)
        self.path = filepath

        @property
        def path(self):
            return self.path
