# -*- coding: utf-8 -*-

from openerp import fields, models, api
from openerp.tools.translate import _
from odoo.exceptions import ValidationError


class DocumentDocument(models.Model):
    _name = "document.document"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char(string="Name")
    document = fields.Binary("Document", attachment=True)
    directory_id = fields.Many2one('document.directory', string='Directory')
    description = fields.Html(string='Description')
    tag_ids = fields.Many2many('document.tag', 'document_tag_rel', 'document_id', 'tag_id', 
        string='Tags', help="Classify and analyze your Document")


class DocumentDirectory(models.Model):
    _name = "document.directory"


    @api.multi
    def _get_document_count(self):
        res = {}
        DocumentObj = self.env['document.document']
        for dir in self:
            dir.document_count = len(dir.document_ids) or 0

    name = fields.Char()
    parent_id = fields.Many2one('document.directory',string='Parent Directory', select=True)
    user_ids = fields.Many2many('res.users', 'document_user_rel', 'user_id', 'doc_id', string="Users")
    document_count = fields.Integer(compute='_get_document_count', string="Number of documents attached")
    description = fields.Html(string='Description')
    document_ids = fields.One2many(comodel_name='document.document', inverse_name='directory_id', string='Documents')
    tag_ids = fields.Many2many('document.tag', 'directory_tag_rel', 'directory_id', 'tag_id', 
        string='Tags', help="Classify and analyze your Document")
    department_id = fields.Many2one('hr.department', string='Department')

    @api.multi
    def name_get(self):
        def get_names(directory):
            """ Return the list [cat.name, cat.parent_id.name, ...] """
            res = []
            while directory:
                res.append(directory.name)
                directory = directory.parent_id
            return res
        return [(directory.id, " / ".join(reversed(get_names(directory)))) for directory in self]

    @api.constrains('parent_id')
    def _check_directory_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('Error ! You cannot create recursive Directory.'))
        return True


class Tag(models.Model):

    _name = "document.tag"
    _description = "Document Tags"

    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
