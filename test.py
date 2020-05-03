import time, sys
counter = 1
while True:
    counter += 1
    time.sleep(1)
    if counter == 5u:
        sys.stdout.write("ropox\n")
        sys.stdout.flush()
