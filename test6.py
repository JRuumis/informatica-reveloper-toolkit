from common import config
from version_control import git
from informatica import pmrep


# todo: DONE - import output to log - DONE
# todo: DONE - export to log - DONE
# todo: DONE - folder to migrate - auto - DONE
# todo: DONE - infa test exports folder - also in config - DONE

# todo: git
# todo: code ---> to rm git !!!!!!!!!!!!!
# todo: infa validation - to informatica class
# todo: DONE - git validation - to git class
# todo: calling from command line
    # todo: export (git)
    # todo: import, (git)
    # todo: duplicate folder with different name
    # todo: create folder
    # todo: delete folder
# todo: REFACTOR (4 - 12h)


config = config.get_from_json()

git = git.Git(config)

current_branch = git.get_current_branch()
print 'currently in branch: %s' % current_branch


infa = pmrep.Pmrep(config, git)

export_outcome = infa.do_export()
import_outcome = infa.do_import()

