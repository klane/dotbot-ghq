import subprocess

import dotbot


class Ghq(dotbot.Plugin):
    """
    Clone remote git repositories using 'ghq get' and 'ghq import'
    """
    _supported_directives = ['ghq', 'ghqfile']

    # Dotbot methods

    def can_handle(self, directive):
        return directive in self._supported_directives

    def handle(self, directive, data):
        try:
            for entry in data:
                if directive == 'ghq':
                    self._get(entry)
                elif directive == 'ghqfile':
                    self._import(entry)
            return True
        except ValueError as e:
            self._log.error(e)
            return False

    # Utility

    @property
    def cwd(self):
        return self._context.base_directory()

    # Inner methods

    def _get(self, repo):
        self._run(
            "ghq get {}".format(repo),
            "Cloning {}".format(repo),
            "Failed to clone {}".format(repo),
        )

    def _import(self, filename):
        self._run(
            'ghq import < {}'.format(filename),
            'Importing {}'.format(filename),
            'Failed to import {}'.format(filename),
        )

    def _run(self, command, message=None, error_message=None):
        if message is not None:
            self._log.lowinfo(message)

        result = subprocess.call(command, cwd=self.cwd, shell=True)

        if result != 0:
            if error_message is None:
                error_message = 'Command failed: {}'.format(command)

            raise ValueError(error_message)
