import subprocess, sys

def run(readable_results, data, rawbuf):
        if len(readable_results) > 0:
                sys.stdout.write(readable_results)
                sys.stdout.flush()
run(["ropox"], 1, 1)


