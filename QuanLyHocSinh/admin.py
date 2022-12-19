from flask import redirect,request
from sqlalchemy import Integer, ForeignKey

from QuanLyHocSinh.models import HocSinh, MonHoc, LopHoc, DiemSo, HocSinh_LopHoc, DiemCacMon, UserRole
from QuanLyHocSinh import db, app, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea



class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
         return current_user.is_authenticated and current_user.use_role == UserRole.ADMIN

class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
         return current_user.is_authenticated


class HocSinhView(AuthenticatedModelView):
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    can_view_details = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = {
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }

class DanhSachView(AuthenticatedModelView):
    column_searchable_list = ['name']
    column_filters = ['name']
    can_view_details = True
    column_exclude_list = ['User']


class StatsView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')



class SubjectView(AuthenticatedModelView):
    column_searchable_list = ['tenMH']
    column_filters = ['tenMH']
    can_view_details = True
    can_view_details = True
    can_export = True
    column_labels = {
        'tenMH' : 'Tên môn học',
        'id_ma_cac_mon':'Mã môn học'
    }
class ScoreView(AuthenticatedModelView):
    column_searchable_list = ['idHS']
    column_filters = ['idHS']
    can_view_details = True
    can_view_details = True
    can_export = True
    column_labels = {
        'IDMonHoc': 'Môn học',
        'ID_HS': 'Tên học sinh',
        'maDiemSo': 'Loại điểm',
        'giaTri': 'Giá trị',
    }
    column_editable_list = ['idDiemCacMon']
class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/admin')

class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        lop = request.args.get('lop')
        HocKi = request.args.get('hocki')
        #monhoc = request.args.get('monhoc'), hocki = request.args.get('hocki')
        stats = dao.thongke(lop =lop,hk=HocKi)
        lop = dao.load_LopHoc()
        monhoc = dao.load_MonHoc()
        hocki = dao.load_HocKy()
        return self.render('admin/index.html', stats=stats, monhoc=monhoc, hocki=hocki,lop = lop)

admin = Admin(app=app, name='Quản lý học sinh', template_mode='bootstrap4',index_view=MyAdminView())
admin.add_view(DanhSachView(HocSinh, db.session, name='Tiếp nhận học sinh'))
admin.add_view(SubjectView(MonHoc, db.session, name='Quản lý môn học'))
admin.add_view(ScoreView(DiemCacMon, db.session, name='Quản lý điểm'))
admin.add_view(LogoutView(name='Đăng xuất'))