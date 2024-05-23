import pytest

################################################
# mark_name = "data"
mark_name = "serv"
# mark_name = "work"

################################################
force_run_xfail = False
# force_run_xfail = True
force_run_xfail = "--runxfail" if force_run_xfail else ""

################################################
# report on xfail, xpassed
report_mode = "-rxX"
# report on xpassed
report_mode = "-rX"
# report on passed but with output
# report_mode = "-rP"

################################################
# TODO
a = "--collect-only"
# list all the test found

################################################
def main():
    cmd_list = [
        force_run_xfail,
        report_mode,
        a,
        "-vv",
        "-m",
        mark_name,
    ]
    cmd_list = [e for e in cmd_list if e]
    pytest.main(cmd_list)
    print("Previous cmd:", cmd_list, end="\n\n")
