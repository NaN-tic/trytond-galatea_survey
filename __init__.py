#This file is part galatea_survey module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.pool import Pool
from .survey import *

def register():
    Pool.register(
        Survey,
        SurveyField,
        SurveyGalateaWebSite,
        module='galatea_survey', type_='model')
