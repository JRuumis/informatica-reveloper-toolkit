
from informatica import system


def system_validation():

    print "Validating system fonfiguration for running PMCMD..."

    required_system_variables = [
        'INFA_HOME',
        'INFA_DOMAINS_FILE',
        'LD_LIBRARY_PATH',
        'PATH'
    ]

    system_variables_exist_list = [system.get_environment_variable(v) for v in required_system_variables]
    system_variables_exist = reduce( (lambda a,b: a and b), system_variables_exist_list )

    if not system_variables_exist: return False

    print "Validating the pmrep command..."
    if not system.check_command_exists("pmrep -version"):
        print "Command pmrep not found. Please run manually 'pmrep -version' to troubleshoot.\n"\
              "Make sure the required environment variables are set and with correct values.\n" \
              "Make sure the PATH variable is updated with the INFA_HOME bin path."
        return False
    else:
        print "Command pmrep successfully validated."



    return True




