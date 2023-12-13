from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config
from flask_admin import Admin
from sqlalchemy import MetaData
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
import ssl
from wtforms import PasswordField
from wtforms.validators import DataRequired
from flask_admin import AdminIndexView
from flask_bcrypt import Bcrypt

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

# 사용자 정의한 Flask-Admin IndexView 클래스
class MyAdminIndexView(AdminIndexView):

    from src.models import User

    def is_accessible(self):
        # 인증 체크: 세션에 'user_id'가 있고 해당 사용자가 'admin'인 경우에만 접근 허용
        user_id = session.get('user_id')
        if user_id is not None:
            user = User.query.get(user_id)
            return user and user.username == 'admin'
        return False

    def index(self):
        return self.render('admin/index.html')

class UserAdmin(ModelView):
    # ... (이전 뷰 설정)

    def on_model_change(self, form, model, is_created):
        # 패스워드 필드에 값이 들어왔을 때만 암호화
        if 'password' in form:
            salt = generate_random_salt()
            model.password = generate_password_hash(form.password.data, salt=salt)
        else:
            del model.password  # 패스워드 필드가 비어 있으면 기존 값을 그대로 유지



def page_not_found(e):

    return render_template('404.html'), 404


def create_app():

    app = Flask(__name__)
    app.config.from_object(config)

    # Matplotlib 초기화는 메인 스레드에서만 수행
    if __name__ == '__main__':
        import matplotlib
        matplotlib.use('Agg')  # "Agg" 백엔드를 사용하여 GUI를 피함

    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    from src.models import User
    from src.models import Question as que

    admin = Admin(app, name='Crimeless', template_mode='bootstrap3')

    # 여기서 views/main_views를 임포트합니다.
    from views import main_views, question_views, answer_views, auth_views, graph_view
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(graph_view.bp)

    from src.filter import format_datetime

    app.jinja_env.filters['datetime'] = format_datetime

    admin.add_view(ModelView(User, db.session))

    # 오류 페이지
    app.register_error_handler(404, page_not_found)

    return app

if __name__ == '__main__':

    create_app().run(host='0.0.0.0', port=5028, debug=True)
