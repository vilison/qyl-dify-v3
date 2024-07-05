from flask_restful import fields

from libs.helper import TimestampField

app_fields = {
    'id': fields.String,
    'name': fields.String,
    'mode': fields.String,
    'icon': fields.String,
    'icon_background': fields.String
}

installed_app_fields = {
    'id': fields.String,
    'app': fields.Nested(app_fields),
    'app_owner_tenant_id': fields.String,
    'is_pinned': fields.Boolean,
    'last_used_at': TimestampField,
    'editable': fields.Boolean,
    'uninstallable': fields.Boolean
}

installed_app_list_fields = {
    'installed_apps': fields.List(fields.Nested(installed_app_fields))
}

tag_fields = {
    'id': fields.String,
    'name': fields.String,
    'type': fields.String
}

app_with_tags_fields = {
    'id': fields.String,
    'name': fields.String,
    'description': fields.String,
    'mode': fields.String,
    'icon': fields.String,
    'icon_background': fields.String,
    'created_at': TimestampField,
    'tags': fields.List(fields.Nested(tag_fields))
}

installed_app_partial_fields = {
    'id': fields.String,
    'app': fields.Nested(app_with_tags_fields),
    'app_owner_tenant_id': fields.String,
    'is_pinned': fields.Boolean,
    'last_used_at': TimestampField,
    # 'editable': fields.Boolean,
    'uninstallable': fields.Boolean
}

installed_app_pagination_fields = {
    'page': fields.Integer,
    'limit': fields.Integer(attribute='per_page'),
    'total': fields.Integer,
    'has_more': fields.Boolean(attribute='has_next'),
    'data': fields.List(fields.Nested(installed_app_partial_fields), attribute='items')
}