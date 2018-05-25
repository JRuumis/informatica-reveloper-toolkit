from common import config
from version_control import git_control
from informatica import pmrep
import sys

from argparse import ArgumentParser


parser = ArgumentParser(description="Rittman Mead Informatica Migration Script")
parser.add_argument('migration_mode', choices=['export','import'], help="Informatica migration mode.")
parser.add_argument('-c', '--config_json', action="store", default='config.json', help="Config JSON file to be used. Default: 'config.json'")
parser.add_argument('-v', '--verbose', action="store", default=False, help="Instruction to run migration in verbose mode - giving much more information about the migration process.")
parser.add_argument('-g', '--use_git', action="store_true", default=True, help="Use version control.")

args = parser.parse_args()

try:
    # Parse config parameters
    param_migration_mode = args.migration_mode
    param_config_json = args.config_json
    param_verbose = args.verbose
    param_use_git = args.use_git

except Exception as err:
    print '\n\nException caught:\n\n%s ' % err
    print '\n\tError: Failed to get command line arguments. Exiting.'
    sys.exit(1)

config = config.get_from_json(config_json=param_config_json)
git = git_control.Git(config, verbose=param_verbose)
infa = pmrep.Pmrep(config, git_control=git, verbose=param_verbose)

if param_migration_mode == 'export':
    export_outcome = infa.do_export(use_git=param_use_git)
elif param_migration_mode == 'import':
    import_outcome = infa.do_import(use_git=param_use_git)

