#!/usr/bin/env python
# This file is part of the galatea_survey module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, Bool
from .tools import slugify
from collections import OrderedDict

__all__ = ['Survey', 'SurveyField', 'SurveyGalateaWebSite']
__metaclass__ = PoolMeta

SURVEY_EXCLUDE_FIELDS = ['many2one']

class Survey:
    __name__ = 'survey.survey'
    esale = fields.Boolean('eSale',
        help='Available survey in eSale plattforms.')
    slug = fields.Char('Slug', translate=True,
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
    login = fields.Boolean('Login',
        states={
            'invisible': ~Bool(Eval('esale')),
        }, depends=['esale'],
        help='Login Users')
    manager = fields.Boolean('Manager',
        states={
            'invisible': ~Bool(Eval('esale')),
        }, depends=['esale'],
        help='Manager Users')
    css = fields.Char('CSS', translate=True,
        states={
            'invisible': ~Bool(Eval('esale')),
        }, depends=['esale'],
        help='CSS style.')
    esale_description = fields.Text("Description", translate=True,
        states={
            'invisible': ~Bool(Eval('esale')),
        }, depends=['esale'])
    esale_notes = fields.Text("Notes", translate=True,
        states={
            'invisible': ~Bool(Eval('esale')),
        }, depends=['esale'])
    esale_response = fields.Text("Response", translate=True,
        states={
            'invisible': ~Bool(Eval('esale')),
        }, depends=['esale'])

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

    def galatea_survey_form(self):
        '''Return a dict with form fields grouped by steps'''
        # TODO: create order by steps and fields.
        # Current: order fields is with sequence field (all fields).
        # Not use order with steps.
        survey_form = {}

        steps = []
        for f in self.fields_:
            if not f.step in steps:
                steps.append(f.step)

        before_step = None
        for f in self.fields_:
            if f.type_ in SURVEY_EXCLUDE_FIELDS:
                continue
            current_step = f.step.code
            if before_step != current_step:
                fields = []
                survey_form[f.step.code] = OrderedDict()
                survey_form[f.step.code]['code'] = f.step.code
                survey_form[f.step.code]['name'] = f.step.name
                survey_form[f.step.code]['sequence'] = f.step.sequence or 1

            fields.append({
                'name': f.name,
                'label': f.string,
                'type_': f.type_,
                'required': f.required,
                'textarea': f.textarea,
                'email': f.email,
                'password': f.password,
                'url': f.url,
                'help': f.help_,
                'selection': f.selection,
                'default_value': f.default_value,
                'css': f.css,
                })

            survey_form[f.step.code]['fields'] = fields
            before_step = current_step
        return dict(OrderedDict(
            sorted(survey_form.items(), key=lambda t: t[1]['sequence'])
            ))


class SurveyField:
    __name__ = 'survey.field'
    css = fields.Char('CSS',
        help='CSS style.')


class SurveyGalateaWebSite(ModelSQL):
    'Survey - Galatea Website'
    __name__ = 'survey.survey-galatea.website'
    _table = 'survey_survey_galatea_website'
    survey = fields.Many2One('survey.survey', 'Survey', ondelete='CASCADE',
            select=True, required=True)
    website = fields.Many2One('galatea.website', 'Website', ondelete='RESTRICT',
            select=True, required=True)
