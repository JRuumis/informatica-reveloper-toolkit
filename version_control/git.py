
from informatica import system

class Git:
    //def __init__(self /*, config*/):

    def __init__(self):
        print 'asdf'


    def validate_environment(self):

        print 'Validating git access...'

        git_version_check_command = "git --version"

        git_exists = system.check_command_exists(git_version_check_command)
        if git_exists:
            print 'Git access OK'
        else:
            print "ERROR: Command git not found. Please run manually 'git --version' to troubleshoot.\n" \
                  "Make sure git is installed and accessible to the user running this application.\n" \
                  "Make sure the PATH variable is updated with the GIT bin path."
            return False

        git_version = system.execute_command_line(git_version_check_command)
        results_search = "git version (\d*).(\d*).(\d*)"
        res = re.search(results_search, git_version)

        if int(res.group(1)) < 2:
            print 'WARNING: your git version is old. It is recommended to have git version 2.13.x or newer. The version you are using is %s.%s.%s' % (res.group(1), res.group(2), res.group(3))






