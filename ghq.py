import os
import subprocess

import dotbot


class GHQ(dotbot.Plugin):
    """
    Clone remote git repositories using 'ghq get'
    """

    _default_flags = ["--silent"]

    def __init__(self, context):
        super(GHQ, self).__init__(context)
        self._directives = {"ghq": self._get, "ghqfile": self._import}

    # Dotbot methods

    def can_handle(self, directive):
        return directive in self._directives

    def handle(self, directive, data):
        try:
            for entry in data:
                self._directives[directive](entry)
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
        repo, flags = self._parse(data, "repo")

        self._run(
            "ghq get {} {}".format(flags, repo),
            "Cloning {}".format(repo),
            "Failed to clone {}".format(repo),
        )

    def _import(self, data):
        filename, flags = self._parse(data, "file")

        if not os.path.isfile(filename):
            raise ValueError("Repo file not found: {}".format(filename))

        self._run(
            "ghq get {} < {}".format(flags, filename),
            "Importing {}".format(filename),
            "Failed to import {}".format(filename),
        )

    def _parse(self, data, key):
        if type(data) is dict:
            if key not in data:
                raise ValueError("Key '{}' not found in {}".format(key, data))

            if "flags" not in data:
                self._log.warning("Key 'flags' not found in {}".format(data))
                self._log.warning("Using default flags {}".format(self._default_flags))

            value = data[key]
            flags = data.get("flags", self._default_flags)
        else:
            value = data
            flags = self._default_flags

        return value, " ".join(flags)

    def _run(self, command, message=None, error_message=None):
        if message is not None:
            self._log.lowinfo(message)

        result = subprocess.call(command, cwd=self.cwd, shell=True)

        if result != 0:
            if error_message is None:
                error_message = "Command failed: {}".format(command)

            raise ValueError(error_message)
