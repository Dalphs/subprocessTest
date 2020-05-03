import subprocess, sys, time

def run():

    #setting up the popen subprocess, cwd goes to another location before running the training command
    process = subprocess.Popen(('./sopare.py -l '), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd="../sopare")
    
    while True:
        
        nextline = process.stdout.readline()

        if process.poll() is not None:
            break
        #decoding from bytes to string
        currentline = nextline.decode()
        #printing everything, not important but good for debugging
        print(currentline)
        #This is where our if/elif statements will control the GPIO pins when a specific word is recognized
        if("ropox" in currentline):
            sys.stdout.write("virker\n")
            sys.stdout.flush()

    process.wait()
    output = process.communicate()[0]
    exitCode = process.returncode

    if(exitCode == 0):
        return output
    else:
        raise Exception("Failure, something went wrong")
    print("done")