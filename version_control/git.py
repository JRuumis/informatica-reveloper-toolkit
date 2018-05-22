import re
import os

# TODO: DONE - finish translating
# TODO: verbose flag !!!!!!!!!!!!!!
# TODO: command to return an object!!!
# TODO: all command responses to be collected
# TODO: sort out merge
# TODO: add comments

from informatica import system

class Git:
    def __init__(self, config, validate=True, verbose=False):
        try:
            self.git_remote_url = config.content['git']['remote_url']
            self.git_root_folder = os.path.normpath( config.content['git']['repository_root_folder'] )
            self.git_informatica_sub = config.content['git']['informatica_subfolder'].strip('/').strip('\\').strip('\\\\')
            self.git_informatica_root_folder = os.path.normpath( os.path.join(self.git_root_folder, self.git_informatica_sub) )
            self.git_default_branch = config.content['git']['default_branch']
            self.verbose = verbose

        except Exception as err:
            print 'ERROR: Failed to read all required parameters from config.json for git access.'
            print 'Check the json file format, e.g. are there any missing commas or closing quotes, brackets?'
            print 'Use the config.json.template file in this folder as your reference.\n'
            if verbose:
                print 'Exception:\n%s\n' % str(err)
            exit(1)

        if validate:
            result = self.validate_environment()
            if not result:
                exit(1)


    def validate_environment(self):
        # --- git access validation ---
        # check git command access
        print 'Validating git access...'
        git_version_check_command = "git --version"

        git_exists = system.check_command_exists(git_version_check_command, self.verbose)
        if git_exists:
            print 'git command available, successfully validated.\n'
        else:
            print "ERROR: Command git not found. Please run manually 'git --version' to troubleshoot.\n" \
                  "Make sure git is installed and accessible to the user running this application.\n" \
                  "Make sure the PATH variable is updated with the GIT bin path."
            return False

        # check git version
        git_version = self.get_git_version()

        try:
            results_search = "git version (\d*).(\d*).(\d*)"
            res = re.search(results_search, git_version)

            if int(res.group(1)) < 2:
                print 'WARNING: your git version is old. It is recommended to have git version 2.13.x or newer.\n' \
                      'The version you are using is %s.%s.%s.\n' \
                      'Some required functionality may not work with your version.\n' % (res.group(1), res.group(2), res.group(3))
        except Exception as err:
            print 'ERROR: could not parse git version from response. Expected: "git version <integer>.<integer>.<integer>"'
            print 'Received response: %s' % git_version
            print 'Exception:\n%s\n' % str(err)
            return False


        # -- git repository folder check --
        print 'Validating git repository folders...'

        # check repo root
        if os.path.isdir(self.git_root_folder):
            print 'Folder git.repository_roof_folder: %s exists' % self.git_root_folder
        else:
            print 'ERROR: folder %s does not exist or is not accessible.' % self.git_root_folder
            return False

        # check informatica subfolder
        if os.path.isdir(self.git_informatica_root_folder):
            print 'Folder git.informatica_subfolder under git.repository_root_folder: %s exists' % self.git_informatica_root_folder
        else:
            print 'ERROR: folder %s does not exist or is not accessible.' % self.git_informatica_root_folder
            print 'Make sure the git.informatica_subfolder value in json is a sub-path and not absolute path.'
            return False

        print 'Git repository folders successfully validated.\n'


        # -- git repository check --
        # check if folder is a repo
        print 'Validating git repository under git repository root folder...'

        inside_work_tree = self.execute_command('rev-parse --is-inside-work-tree')
        if not inside_work_tree == 'true':
            print 'ERROR: The git.repository_root_folder %s is found to be neither a git repository root ' \
                  'nor a repository subfolder.' % self.git_root_folder
            print 'Perform `git clone <URL>` to establish a git repository in this folder.'
            return False

        repo_root_for_folder = self.execute_command('rev-parse --show-toplevel')
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

        print 'Git repository folders successfully validated.\n'


        # -- git additional checks --
        print 'Performing additional git checks...\n'
        print 'Branches (local and remote, current branch indicated with a *):\n%s\n' % self.get_all_branches()
        print 'Checking remote repository access: %s...' % self.git_remote_url
        remote_response = self.validate_remote_repository()
        if 'remote error' in remote_response:
            print 'ERROR: Cannot access the remote repository.'
            print 'Message returned from git:\n' \
                  '------------------------------------------------\n' \
                  '%s\n' \
                  '------------------------------------------------\n' % remote_response
            return False
        else:
            print 'Git remote access successfully validated.\n'

        print 'All git validations done.\n'

        return True


    def execute_command(self, git_command):
        """
        Executes a Git command and reports an error if one is detected.

        E.g.
        >>> self.execute_command('pull')
        """
        current_dir = os.getcwd()
        os.chdir(self.git_root_folder)
        full_command = 'git %s' % git_command

        if self.verbose:
            print 'git command to be executed: %s' % full_command

        output = system.execute_command_line(full_command).strip()
        if self.verbose:
            print 'git output:\n------------------------------\n%s\n------------------------------\n' % output

        os.chdir(current_dir)
        return output

    def get_git_version(self):
        return self.execute_command('--version')

    def get_all_branches(self):
        return self.execute_command('branch -a')

    def get_current_branch(self):
        return self.execute_command('branch')

    def validate_remote_repository(self):
        return self.execute_command('ls-remote %s' % self.git_remote_url)

    def checkout(self, branch):
        """Checks out a Git branch."""
        return self.execute_command('checkout %s' % branch)

    def pull(self):
        """Pulls latest changes from the tracked remote Git repository."""
        fetch_result =  self.execute_command('fetch %s' % self.git_remote_url)
        pull_result =   self.execute_command('pull')
        return fetch_result + pull_result

    def pull_branch(self,branch):
        """Pulls latest changes from the tracked remote Git repository."""
        fetch_result =  self.execute_command('fetch %s' % self.git_remote_url)
        pull_result =   self.execute_command('pull %s %s' % (self.git_remote_url, branch) )
        return fetch_result + pull_result

    def create_branch(self, new_branch, base_branch):
        """Creates a new branch from an existing branch (`base`)."""
        checkout_base_result =          self.checkout(base_branch)
        pull_result =                   self.pull()
        checkout_new_branch_result =    self.execute_command('checkout -b %s %s' % (new_branch, base_branch) )
        return checkout_base_result + pull_result + checkout_new_branch_result

    def delete_branch(self, branch):
        """Delete a Git branch."""
        return self.execute_command('branch -d %s' % branch)

    """
    def merge(self, trunk, branch, no_fast_forward=False):
        ##### Merges a Git branch to a trunk.
        checkout_result = self.checkout(trunk)

        # TODO: checkout_result is not a list !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Error if there is a problem checking out
        if checkout_result[1] and ('Already on \'%s\'' % trunk) not in checkout_result[1] and 'Switched to branch \'%s\'' % trunk not in checkout_result[1]:
            return checkout_result

        pull_result = self.pull()
        if pull_result[1]:
            if re.search('no tracking information', pull_result[1]):  # Check if pull failed because there is no remote
                if trunk in [self.git_default_branch # master and development
                             ]:  # If trunk is not one of the main trunks we should exit
                    return pull_result
            elif 'The use of this system is restricted to authorized persons only' in pull_result[1]:
                pass  # Skip error
            else:  # Return an error
                return pull_result

        print('Merging %s into %s...' % (branch, trunk))
        if no_fast_forward:
            merge_result = cmd(['merge', '--no-ff', branch])
        else:
            merge_result = cmd(['merge', branch])

        return merge_result
    """

    def push(self, branch):
        """Pushes a branch to a remote repository."""
        return self.execute_command('push %s %s' % (self.git_remote_url, branch) )

    def commit_all(self, commit_message):
        """Commits all changes."""
        add_result =        self.execute_command('add --all')  # Stage changes
        commit_result =    self.execute_command( 'commit -a -m "%s"' % commit_message.replace('"', '\'') )
        return add_result + commit_result

    def tag(self, tag_name, branch, tag_message=""):
        """Tag commit on a specific branch, optionally using a message."""
        if self.verbose:
            print('Tagging %s with %s...' % (branch, tag_name))
        checkout_result =   self.checkout(branch)
        tag_result =        self.execute_command( 'tag -a %s -m %s' % (tag_name, tag_message) )
        return checkout_result + tag_result
