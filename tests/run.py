import pytest

################################################
# mark_name = "data"
# mark_name = "serv"
mark_name = "work"

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
report_mode = "-rfEP"

################################################
# TODO
list_possible_tests = False
# list_possible_tests = True
list_possible_tests =  "--collect-only" if list_possible_tests else ""
# list all the test found

################################################
def main():
    cmd_list = [
        force_run_xfail,
        report_mode,
        list_possible_tests,
        "-vv",
        "-m",
        mark_name,
    ]
    cmd_list = [e for e in cmd_list if e]
    pytest.main(cmd_list)
    print("Previous cmd:", cmd_list, end="\n\n")
