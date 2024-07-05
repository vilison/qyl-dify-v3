
from flask_sqlalchemy.pagination import Pagination

from extensions.ext_database import db
from models.model import InstalledApp
from services.tag_service import TagService


class InstalledAppService:
    def get_paginate_installed_apps(self, tenant_id: str, args: dict) -> Pagination | None:
        """
        Get installed apps list with pagination
        :param tenant_id: tenant id
        :param args: request args
        :return:
        """
        filters = [
            InstalledApp.tenant_id == tenant_id
        ]

        if 'tag_ids' in args and args['tag_ids']:
            target_ids = TagService.get_target_ids_by_tag_ids('app',
                                                              tenant_id,
                                                              args['tag_ids'])
            if target_ids:
                filters.append(InstalledApp.app_id.in_(target_ids))
            else:
                return None

        installed_app_models = db.paginate(
            db.select(InstalledApp).where(*filters).order_by(InstalledApp.last_used_at.desc()),
            page=args['page'],
            per_page=args['limit'],
            error_out=False
        )

        return installed_app_models


