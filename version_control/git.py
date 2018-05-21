"""
Module for interacting with Git repositories.
"""

import re
from subprocess import Popen, PIPE  # Used to execute from the command line.

import rm_sys

# Git Functions
# ==============================================================================


def cmd(command):
	"""
	Executes a Git command and reports an error if one is detected.

	E.g.

	>>> rm_sys.git.cmd(['pull'])
	"""

	command = [rm_sys.GIT_EXE, '-C', rm_sys.GIT_REPO] + command
	output = Popen(command, stdout=PIPE, stderr=PIPE).communicate()
	if output[1]:
		print(output[1])
	return output


def checkout(brnch):
	"""Checks out a Git branch."""

	print('Checking out %s...' % brnch)
	return cmd(['checkout', brnch])


def pull():
	"""Pulls latest changes from the tracked remote Git repository."""
	cmd(['fetch'])
	return cmd(['pull'])


def branch(brnch, base):
	"""Creates a new branch from an existing branch (`base`)."""
	checkout(base)
	pull()
	return cmd(['checkout', '-b', brnch, base])


def delete_branch(brnch):
	"""Delete a Git branch."""
	return cmd(['branch', '-d', brnch])


def merge(trunk, brnch, no_ff=False):
	"""Merges a Git branch to a trunk."""
	out = checkout(trunk)

	# Error if there is a problem checking out
	if out[1] and 'Already on \'%s\'' % trunk not in out[1] and 'Switched to branch \'%s\'' % trunk not in out[1]:
		return out

	out = pull()
	if out[1]:
		if re.search('no tracking information', out[1]):  # Check if pull failed because there is no remote
			if trunk in [rm_sys.GIT_DEVELOP,
			             rm_sys.GIT_MASTER]:  # If trunk is not one of the main trunks we should exit
				return out
		elif 'The use of this system is restricted to authorized persons only' in out[1]:
			pass  # Skip error
		else:  # Return an error
			return out

	print('Merging %s into %s...' % (brnch, trunk))
	if no_ff:
		out = cmd(['merge', '--no-ff', brnch])
	else:
		out = cmd(['merge', brnch])
	return out


def push(remote, brnch):
	"""Pushes a branch to a remote repository."""
	print('Pushing %s to %s...' % (brnch, remote))
	return cmd(['push', remote, brnch])


def commit_all(msg):
	"""Commits all changes."""
	cmd(['add', '--all'])  # Stage changes
	return cmd(['commit', '-a', '-m', msg])


def tag(tag_name, brnch, msg=""):
	"""Tag commit on a specific branch, optionally using a message."""
	print('Tagging %s with %s...' % (brnch, tag_name))
	checkout(brnch)
	cmd(['tag', '-a', tag_name, '-m', msg])

# End of Git Functions
# ==============================================================================
