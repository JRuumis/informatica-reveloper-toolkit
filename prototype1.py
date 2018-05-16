
# pmrep connect
# pmrep createFolder
# pmrep objectexport
# pmrep objectimport
# pmrep listobjects  <- can list folders
# pmrep updateseqgenvals <-- updates sequence values!
# pmrep VALIDATION
# pmrep backup and restore

# TODOs:
# 1) test PMCMD access, test system variables, validate
# 2) establish infa connection
# 3) export folder
# 4) generate control file for import
# 5) get current folders in target
# 6) create folders that are missing (need source-target folder mappings - config file?)
# 5) import folder
# 6) analyse import output

import platform
from subprocess import call, Popen, PIPE, STDOUT, check_output  # Used to execute from the command line.
import os

def execute_command_line(cmd):
	if platform.system() == 'Linux':
		command_pipe = Popen("%s" % cmd, stdout=PIPE, stderr=PIPE, shell=True)
		command_return, command_err = command_pipe.communicate()
		return command_return + command_err
	else:
		return "ERROR: not working for Windows yet"

def check_command_exists(cmd):
	exec_result = execute_command_line(cmd)
	if exec_result.strip()[-17:] == 'command not found':
		return False
	else:
		return True



def is_environment_variable_defined(variable_name): return variable_name in os.environ

def get_environment_variable(variable_name):
	if is_environment_variable_defined(variable_name):
		return 'Environment variable %s has the value [%s]' % (variable_name, os.environ[variable_name])
	else:
		return 'ERROR: environment variable %s is not defined!' % variable_name




def validate_pmcmd():


	print get_environment_variable('INFA_HOME')
	print get_environment_variable('INFA_DOMAINS_FILE')
	print get_environment_variable('JANIS_VAR')
	print get_environment_variable('LD_LIBRARY_PATH')
	print get_environment_variable('PATH')

	print "checking pmrep..."
	print execute_command_line("pmrep -version")

	print check_command_exists("pmrep -version")
	print check_command_exists("pmrepx -version")


validate_pmcmd()