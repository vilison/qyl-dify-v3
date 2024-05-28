import logging
from datetime import datetime, timedelta, timezone
from libs.helper import get_remote_ip
from models.racio.manager import *
from libs.password import compare_password
from libs.passport import PassportService
from services.errors.manager import (
    ManagerLoginError,
)

class ManagerService:


    @staticmethod
    def load_user(user_id: str) -> Manager:
        manager = Manager.query.filter_by(id=user_id).first()
        if not manager:
            return None

        if datetime.now(timezone.utc).replace(tzinfo=None) - manager.last_active_at > timedelta(minutes=10):
            manager.last_active_at = datetime.now(timezone.utc).replace(tzinfo=None)
            db.session.commit()

        return manager


    @staticmethod
    def authenticate(username: str, password: str) -> Manager:
        """authenticate account with username and password"""

        manager = Manager.query.filter_by(username=username).first()
        if not manager:
            raise ManagerLoginError('Invalid username or password.')

        if manager.password is None or not compare_password(password, manager.password, manager.password_salt):
            raise ManagerLoginError('Invalid username or password.')
        return manager

    @staticmethod
    def update_last_login(manager: Manager, request) -> None:
        """Update last login time and ip"""
        manager.last_login_at = datetime.now(timezone.utc).replace(tzinfo=None)
        manager.last_login_ip = get_remote_ip(request)
        db.session.add(manager)
        db.session.commit()
        logging.info(f'Account {manager.id} logged in successfully.')


    @staticmethod
    def get_account_jwt_token(manager):
        payload = {
            "user_id": manager.id,
            "exp": datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=30),
            "sub": 'API Passport',
        }

        token = PassportService().issue(payload)
        return token