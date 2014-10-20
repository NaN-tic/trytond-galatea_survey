#!/usr/bin/env python
# This file is part of the galatea_survey module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval, Bool

__all__ = ['Survey']
__metaclass__ = PoolMeta


class Survey:
    __name__ = 'survey.survey'

    def get_survey_form(self, survey):
        # TODO
        return True

