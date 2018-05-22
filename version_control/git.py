import re
import os
from subprocess import Popen, PIPE

from informatica import system

class Git:
    #def __init__(self /*, config*/):

    def __init__(self, config, validate=True):

        #try:

        self.git_remote_url = config.content['git']['remote_url']
        self.git_root_folder = os.path.normpath( config.content['git']['repository_root_folder'] )
        self.git_informatica_sub = config.content['git']['informatica_subfolder'].strip('/').strip('\\').strip('\\\\')
        self.git_informatica_root_folder = os.path.normpath( os.path.join(self.git_root_folder, self.git_informatica_sub) )
        self.git_default_branch = config.content['git']['default_branch']

        #except Exception as err:
        #    print 'ERROR: Failed to read all required parameters from config.json for git access.'
        #    print 'Check the json file format, e.g. are there any missing commas or closing quotes, brackets?'
        #    exit(1)

        if validate:
            result = self.validate_environment()
            if not result: exit(1)


    def validate_environment(self):

        # git access validation
        print 'Validating git access...'
        git_version_check_command = "git --version"

        git_exists = system.check_command_exists(git_version_check_command)
        if git_exists:
            print 'Command git successfully validated.\n'
        else:
            print "ERROR: Command git not found. Please run manually 'git --version' to troubleshoot.\n" \
                  "Make sure git is installed and accessible to the user running this application.\n" \
                  "Make sure the PATH variable is updated with the GIT bin path."
            return False

        git_version = system.execute_command_line(git_version_check_command)
        results_search = "git version (\d*).(\d*).(\d*)"
        res = re.search(results_search, git_version)

        if int(res.group(1)) < 2:
            print 'WARNING: your git version is old. It is recommended to have git version 2.13.x or newer.\n' \
                  'The version you are using is %s.%s.%s.\n' \
                  'Some required functionality may not work with your version.\n' % (res.group(1), res.group(2), res.group(3))

        # git repository folder check
        print 'Validating git repository folders...'

        if os.path.isdir(self.git_root_folder):
            print 'Folder git.repository_roof_folder: %s exists' % self.git_root_folder
        else:
            print 'ERROR: folder %s does not exist or is not accessible.' % self.git_root_folder
            return False

        if os.path.isdir(self.git_informatica_root_folder):
            print 'Folder git.informatica_subfolder under git.repository_root_folder: %s exists' % self.git_informatica_root_folder
        else:
            print 'ERROR: folder %s does not exist or is not accessible.' % self.git_informatica_root_folder
            print 'Make sure the git.informatica_subfolder value in json is a sub-path and not absolute path.'
            return False

        print 'Git repository folders successfully validated.\n'

        # git repo check
        print 'Validating git repository under git repository root folder...'

        inside_work_tree = self.execute_command('rev-parse --is-inside-work-tree')
        if not inside_work_tree.strip() == 'true':
            print 'ERROR: The git.repository_root_folder %s is found to be neither a git repository root ' \
                  'nor a repository subfolder.' % self.git_root_folder
            print 'Perform `git clone <URL>` to establish a git repository in this folder.'
            return False

        repo_root_for_folder = self.execute_command('rev-parse --show-root')
        if repo_root_for_folder == self.git_root_folder:
            print 'The folder %s is a valid git repository root folder.' % self.git_root_folder
        else:
            print 'ERROR: The folder %s is a git repository subfolder, not root folder.' % self.git_root_folder
            print 'The repository root folder is: %s' % repo_root_for_folder
            print 'Is this is your informatica exports folder in your git repository, update the config.json file so that ' \
                  'git.repository_root_folder is the one above and add the relative path to your informatica exports folder in ' \
                  'git.informatica_subfolder.'
            print 'Example:\n\t"git": {\n\t\t"repository_root_folder": "/u01/migration/BI/",\n\t\t"informatica_subfolder": "informatica/archives"\n\t}\n'
            return False

        print 'Git repository folders successfully validated.'

        # git checks
        print 'Performing additional git checks...'

        print 'Branches (local and remote, current indicated with a *):\n%s\n' % self.all_branches()

        print 'Checking remote repository access: %s...' % self.git_remote_url
        remote_response = self.check_remote()
        if 'remote error' in remote_response:
            print 'ERROR: Cannot access the remote repository.'
            print 'Message returned from git:\n' \
                  '------------------------------------------------\n' \
                  '%s\n' \
                  '------------------------------------------------\n' % remote_response
            return False

        return True


    def execute_command(self, git_command, echo=False):
        """
        Executes a Git command and reports an error if one is detected.

        E.g.

        >>> rm_sys.git.execute_command(['pull'])
        """

        current_dir = os.getcwd()
        #print 'Now in: %s' % current_dir
        os.chdir(self.git_root_folder)
        #print 'Now in: %s' % os.getcwd()
        full_command = 'git %s' % git_command

        if echo:    print '\tGit command: %s' % full_command

        output = system.execute_command_line(full_command)
        #output = Popen(full_command, stdout=PIPE, stderr=PIPE).communicate()

        #if output[1]:   print 'git output: %s' % output[1]
        #if output[2]:   print 'git error: %s' % output[2]

        print 'DEBUGGGGGG git output:\n%s\n' % output

        os.chdir(current_dir)
        return output


    def all_branches(self):
        return self.execute_command('branch -a')

    def current_branch(self):
        return self.execute_command('branch')

    def check_remote(self):
        return self.execute_command('ls-remote %s' % self.git_remote_url)