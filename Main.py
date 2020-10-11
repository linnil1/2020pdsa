import json
import subprocess
import sys
import time
import signal
import os


# IO setting
name = "restaurants"
file_input = f"{name}.json"
file_output = "/home/output/feedback"
DEBUG = True

# Set exec time
timeout_kill = 4
timeout_limit_python = 3.0
timeout_limit_java = 1.0

# Set exec command
exec_command = ["bash"]
# exec_command = ["su", "autolab"]
target_file_py   = f"{name}.sol.py"
target_file_java = f"{name}.sol.java"
target_exec_py   = f"{name}.judge.py"
target_exec_java = f"{name}.judge.java"
target_exec_java_main = "Judge"


def run_command(arg):
    return subprocess.Popen(arg,
                            cwd=os.getcwd(),
                            start_new_session=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)


def get_command_status(p, timeout=3.0):
    """
    Get the process status.

    It will be kill if it run excess timeout threshold

    Parameters
    ----------
    p: subprocess
    timeout: float

    Returns
    -------
    outs: encode str
    errs: encode str
    returncode: int
    Timeout: bool
    """
    try:
        # Run command
        outs, errs = p.communicate(timeout=timeout)
        print("Done")
        return outs, errs, p.returncode, False

    except subprocess.TimeoutExpired:
        # Kill it
        print("kill")
        p.terminate()
        p.kill()

        # Fully Kill
        # https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
        try:
            outs, errs = p.communicate(timeout=.1)
        except subprocess.TimeoutExpired:
            print("kill all")
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
            os.killpg(os.getpgid(p.pid), signal.SIGKILL)

        return b"", b"", p.returncode, True


def com_java():
    return run_command(["javac", "-cp", "algs4.jar:gson.jar",
                        "Judger.java", target_exec_java, target_file_java])


def run_py(casename):
    return run_command([*exec_command, "-c", f"python3 {target_exec_py} {casename}"])


def run_java(casename):
    return run_command([*exec_command, "-c", f"java -cp gson.jar:algs4.jar:. "
                                             f"{target_exec_java_main} {casename}"])


if __name__ == '__main__':
    if not DEBUG:
        open(file_output, 'w').close()
        f = open(file_output, 'a')
    else:
        f = sys.stdout
    cases = json.load(open(file_input))
    run_type = sys.argv[1]

    # compile java source
    if run_type == "java":
        timeout_limit = timeout_limit_java
        p = com_java()
        outs, errs, returncode, timeout = get_command_status(p)
        if DEBUG:
            print("DEBUG", str(outs), str(errs))
        if timeout:
            f.write("Compile timeout\n")
            sys.exit(0)
        if returncode != 0:
            f.write("Compile Error:\n")
            f.write(errs.decode('ascii'))
            sys.exit(0)
    else:
        timeout_limit = timeout_limit_python

    # run each score
    scores = {}
    for case in cases:
        casename = f"case{case['case']}"
        scores[casename] = 0
        json.dump([case], open(casename + ".in", "w"))
        os.chmod(casename + ".in", 0o707)
        open(casename + ".out", "w").close()
        os.chmod(casename + ".out", 0o707)

        # RUN
        if run_type == "python":
            p = run_py(casename + ".in")
        else:
            p = run_java(casename + ".in")
        outs, errs, returncode, timeout = get_command_status(p, timeout=timeout_kill)

        # Debug for outputs
        if DEBUG:
            print("DEBUG", outs, errs)
            f.write(outs.decode())
            f.write(errs.decode())

        # TLE
        f.write(f"{casename}:\t")
        if timeout:
            f.write(f"TLE\t(>{timeout_limit}s)\n")
            continue

        # RE
        if returncode != 0:
            f.write("RE\tReturn Code != 0\n")
            continue

        # RE for json format error
        try: 
            status = json.load(open(casename + ".out"))
            os.remove(casename + ".in")
            os.remove(casename + ".out")
        except Exception as e:
            f.write("RE\tYour program has runtime problem or Judger crash.\n")
            continue

        # calculate score
        isAC = all(i['status'] == "AC" for i in status)
        times = sum(float(i['time']) for i in status)
        if times >= timeout_limit * 1000:
            f.write(f"TLE\t(>{timeout_limit}s)\n")
        elif isAC:
            scores[casename] = case["score"]
            f.write("AC\n")

        f.write(f"Time: {times:.2f}ms\n")
        f.write(f"Score: {scores[casename]} / {case['score']}\n")
        # show status
        for j, st in enumerate(status):
            f.write(f"\tSample{j}:\t{st['status']}\t{st['time']:.1f} ms\n")

    # Write overall status
    f.write(json.dumps({'scores': scores}))
