# This file is part of the galatea_survey module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class GalateaSurveyTestCase(ModuleTestCase):
    'Test Galatea Survey module'
    module = 'galatea_survey'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        GalateaSurveyTestCase))
    return suite
