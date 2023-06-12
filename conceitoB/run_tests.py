import os
import subprocess

tests_dir = "tests"
should_succeed_dir = os.path.join(tests_dir, "shouldSucceed")
should_fail_dir = os.path.join(tests_dir, "shouldFail")


def run_test(file_path):
    cmd = f"python3 main.py {file_path}"
    process = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return process.returncode, output.decode("utf-8"), error.decode("utf-8")


def run_tests():
    for dirpath, dirnames, filenames in os.walk(tests_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if dirpath == should_fail_dir:
                return_code, output, error = run_test(file_path)
                if return_code == 0:
                    print(f"Test failed: {file_path}")
                else:
                    print(f"Test passed (expected failure): {file_path}")
            else:
                return_code, output, error = run_test(file_path)
                if return_code == 0:
                    print(f"Test passed: {file_path}")
                else:
                    print(f"Test failed: {file_path}")


run_tests()
