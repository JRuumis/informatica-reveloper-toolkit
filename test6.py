from common import config
from version_control import git_control
from informatica import pmrep


# todo: DONE - import output to log - DONE
# todo: DONE - export to log - DONE
# todo: DONE - folder to migrate - auto - DONE
# todo: DONE - infa test exports folder - also in config - DONE
# todo: DONE git
# todo: DONE infa validation - to informatica class
# todo: DONE - git validation - to git class

# todo: code ---> to rm git !!!!!!!!!!!!!
# todo: calling from command line
    # todo: DONE export (git)
    # todo: DONE import, (git)
    # todo: DONE duplicate folder with different name
    # todo: DONE create folder
    # todo: delete folder

# todo: REFACTOR (4 - 12h)
# TODO: delete archive ONLY if 0 errors returned in summary!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# TODO: make infa and git work together - should be quick and easy now (fingers crossed)
# TODO: create front-end interface - one_python_control_module.py --that-accepts-different-commands-as-keys --to-tell-it-what-to-do <--- implementation + testing should be no more than 1-2h
# TODO: refactor
# TODO: create documentation, discuss with Experian
# TODO: refactor more and code review with Mark Cann, Mark Reedman
# TODO: deploy on environments
# TODO: acceptance testing with Experian



config = config.get_from_json()
git = git_control.Git(config, verbose=False)

current_branch = git.get_current_branch()
print '===== TESTING: currently in branch: %s =====\n\n\n' % current_branch

infa = pmrep.Pmrep(config, git)

export_outcome = infa.do_export()
import_outcome = infa.do_import()

