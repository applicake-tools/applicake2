#!/usr/bin/env python
import os

from applicake2.base.app import BasicApp
from applicake2.base.apputils.dirs import create_workdir
from applicake2.base.coreutils import Argument
from applicake2.base.apputils import templates
from applicake2.base.coreutils import Keys, KeyHelp


class TemplateApp(BasicApp):
    """
    A more advanced example for a BasicApp
    performing template reading, modifying and writing
    """

    def add_args(self):
        return [
            Argument("COMMENT", "value for comment variable"),
            Argument(Keys.WORKDIR, KeyHelp.WORKDIR)
        ]

    def run(self, log, info):
        info = create_workdir(log, info)

        info['TEMPLATEFILE'] = os.path.join(info[Keys.WORKDIR], "template_out.tpl")
        templates.read_mod_write(info, templates.get_tpl_of_class(self), info['TEMPLATEFILE'])
        log.debug("Templatefile sucessfully written. Contents are [%s]" % open(info['TEMPLATEFILE']).read())

        return info


if __name__ == "__main__":
    TemplateApp.main()