import subprocess

import dotbot


class Ghq(dotbot.Plugin):
    """
    Clones remote git repositories using 'ghq get'
    """
    _supported_directives = ['ghq']

    # Dotbot methods

    def can_handle(self, directive):
        return directive in self._supported_directives

    def handle(self, directive, data):
        try:
            self._get(data)
            return True
        except ValueError as e:
            self._log.error(e)
            return False

    # Utility

    @property
    def cwd(self):
        return self._context.base_directory()

    # Inner methods

    def _get(self, data):
        for repo in data:
            self._run(
                "ghq get {}".format(repo),
                "Cloning {}".format(repo),
                "Failed to clone {}".format(repo),
            )

    def _run(self, command, message=None, error_message=None):
        if message is not None:
            self._log.lowinfo(message)

        result = subprocess.call(command, cwd=self.cwd, shell=True)

        if result != 0:
            if error_message is None:
                error_message = 'Command failed: {}'.format(command)

            raise ValueError(error_message)
