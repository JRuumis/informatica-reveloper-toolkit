
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
        variable_value = os.environ[variable_name]
        print 'INFO: Environment variable %s has the value [%s]' % (variable_name, variable_value)
        return variable_value
    else:
        print 'ERROR: environment variable %s is not defined!' % variable_name
        return False