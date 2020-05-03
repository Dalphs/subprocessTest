import subprocess, sys

def execute(cmd):

    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, cwd="../")
    
    while True:
        nextline = process.stdout.readline()
        byteOutput = list(nextline)
        print(byteOutput)
        if process.poll() is not None:
            break
        currentline= nextline.decode()
        if currentline.__contains__("ls"):
            sys.stdout.write(currentline)
            sys.stdout.flush()

    process.wait()
    output = process.communicate()[0]
    exitCode = process.returncode
    print('done')

    if(exitCode == 0):
        return output
    else:
        raise Exception("Failure, something went wrong")
    

execute(["python", "test.py"])
