class SDNCheckResult:
    def __init__(self, patch, testname, result, reason):
        self.patch = patch
        self.testname = testname
        self.result = result
        self.reason = reason
        self.pass_string = f"{self.result}: {self.testname} on {self.patch}"
        self.skip_or_fail_string = f"{self.result}: {self.testname} on {self.patch} ({self.reason})"

    def __str__(self):
        if self.result == "PASS":
            return self.pass_string
        else:
            return self.skip_or_fail_string

class SDNCheckResults:
    def __init__(self, series):
        self.series = series
        self.sdn_target_list_results = [test_sdn_target_list(patch) for patch in self.series.patchdata]
