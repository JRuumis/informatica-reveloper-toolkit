import platform
from subprocess import Popen, PIPE
import os


def execute_command_line(cmd):
    command_pipe = Popen("%s" % cmd, stdout=PIPE, stderr=PIPE, shell=True)
    command_return, command_err = command_pipe.communicate()
    return command_return + command_err


def check_command_exists(cmd, verbose=False):
    exec_result = execute_command_line(cmd)
    if exec_result.strip()[-17:] == 'command not found' or \
            'is not recognized as an internal or external command' in exec_result:
        if verbose:
            print 'Error:\n%s\n' % exec_result
        return False
    else:
        return True


def is_environment_variable_defined(variable_name): return variable_name in os.environ


def get_environment_variable(variable_name, echo=False):
    if is_environment_variable_defined(variable_name):
        variable_value = os.environ[variable_name]
        if echo:
            print '\tEnvironment variable %s has the value [%s]' % (variable_name, variable_value)
        return variable_value
    else:
        print 'ERROR: environment variable %s is not defined!' % variable_name
        return False


def read_file(path_to_file):
    with open(path_to_file, 'r') as f: read_data = f.read()
    return read_data


def write_file(path_to_file, content, rewrite=True):
    if not rewrite and os.path.isfile(path_to_file):
        print "ERROR: File %s already exists!" % path_to_file
        return False

    with open(path_to_file, "w") as f: f.write(content)
    return True


def write_log(log_name, log_content, echo=True):
    log_folder = os.path.join('.', 'logs')

    if not os.path.isdir(log_folder):
        print 'ERROR: Cannot write log. Log folder %s does not exist.' % log_folder
        return False

    lof_file_path = os.path.join(log_folder, log_name)
    write_file(lof_file_path, log_content, rewrite=True)

    if echo: print 'Log file written: %s' % lof_file_path
    return True
