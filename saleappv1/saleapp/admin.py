from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from saleapp.models import Category, Product, UserRole
from saleapp import app, db
from flask_login import logout_user, current_user
from flask import redirect


class AuthenticateView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.ADMIN


class MyProductView(AuthenticateView):
    column_list = ['id', 'name', 'category_id']
    column_searchable_list = ['id', 'name']
    column_filters = ['id', 'name', 'price']
    column_editable_list = ['name']
    can_export = True
    column_labels = {
        'name': 'Tên sản phẩm',
        'category_id': 'Danh mục'
    }


class MyCategoryView(AuthenticateView):
    column_list = ['id', 'name', 'products']


class StatsView(AuthenticateView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class LogoutView(AuthenticateView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin = Admin(app, name='E-commerce Website', template_mode='bootstrap4')
admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
# admin.add_view(StatsView(name='Thống kê'))
# admin.add_view(LogoutView(name='Đăng xuất'))
