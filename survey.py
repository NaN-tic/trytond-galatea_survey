#!/usr/bin/env python
# This file is part of the galatea_survey module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, Bool
from .tools import slugify

__all__ = ['Survey', 'SurveyGalateaWebSite']
__metaclass__ = PoolMeta


class Survey:
    __name__ = 'survey.survey'
    esale = fields.Boolean('eSale',
        help='Available survey in eSale plattforms.')
    slug = fields.Char('slug', translate=True,
        states={
            'required': Bool(Eval('esale')),
            'invisible': ~Bool(Eval('esale')),
        }, depends=['esale'],
        help='Cannonical uri.')
    websites = fields.Many2Many('survey.survey-galatea.website', 
        'survey', 'website', 'Websites',
        states={
            'invisible': ~Bool(Eval('esale')),
        }, depends=['esale'],
        help='Survey will be available in those websites')

    @staticmethod
    def default_websites():
        Website = Pool().get('galatea.website')
        return [p.id for p in Website.search([])]

    @classmethod
    def __setup__(cls):
        super(Survey, cls).__setup__()
        if 'name' not in cls.name.on_change:
            cls.name.on_change.add('name')
        if 'slug' not in cls.name.on_change:
            cls.name.on_change.add('slug')

    def on_change_name(self):
        res = {}
        if self.name and not self.slug:
            res['slug'] = slugify(self.name)
        return res

    def get_survey_form(self, survey):
        # TODO
        return True


class SurveyGalateaWebSite(ModelSQL):
    'Survey - Galatea Website'
    __name__ = 'survey.survey-galatea.website'
    _table = 'survey_survey_galatea_website'
    survey = fields.Many2One('survey.survey', 'Survey', ondelete='CASCADE',
            select=True, required=True)
    website = fields.Many2One('galatea.website', 'Website', ondelete='RESTRICT',
            select=True, required=True)
