import os.path

file = "Dockerfile"
cur_dir = os.getcwd()

runSnykList = ["RUN curl -O -s -L \"https://static.snyk.io/cli/latest/snyk-linux\"", "RUN mv snyk-linux /usr/local/bin/snyk", "RUN chmod +x /usr/local/bin/snyk", "RUN snyk config set api=da12766a-46b6-4186-8ba1-83eb1aae653c", "RUN snyk monitor --all-projects", "RUN snyk test --all-projects"]
value = str(runSnykList[4])


# Checks Dockerfile to see if Snyk Monitor is in the Dockerfile
def checkforsnyk(file, status):
    for line in file:
        if line.rstrip('\r\n') == status.rstrip('\r\n'):
            return True


print("Looking for Dockerfiles!")
# Search current and subdirectories for Dockerfiles
for dirpath, dirnames, files in os.walk(cur_dir):
    for name in files:
        if name == file:
            filename = os.path.join(dirpath, file)
            print("Found a Dockerfile in the following directory:", filename)
            print("Opening Dockerfile...")
            with open(filename, 'r+') as out:
                # Checking if Snyk is already in the Dockerfile
                if checkforsnyk(out, value):
                    print("Snyk is already in this Dockerfile")
                else:
                    print("Adding Snyk to Dockerfile")
                    for i in runSnykList:
                        out.write("%s\n" % i)