from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum, DATE
from sqlalchemy.orm import relationship
from QuanLyHocSinh import db, app
from datetime import datetime
from flask_login import UserMixin
import enum

class UserRole(enum.Enum):
    ADMIN = 1
    USER = 2




class User (db.Model,UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    use_role = Column(Enum(UserRole), default=UserRole.USER)
    name = Column(String(50), nullable=False)
    date = Column(DATE, nullable = False)
    sex = Column(String(50),nullable = False)
    address = Column (String(50), nullable =False)
    email = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    #hocSinh = relationship('HocSinh', backref='User', uselist=False)


    def __str__(self):
        return self.name


class MonHoc (db.Model):
    __tablename__ = 'monhoc'
    IDMonHoc = Column(Integer, primary_key=True, autoincrement=True)
    tenMH = Column(String(50), nullable =False)
    # HS_MH = relationship('DiemSo', backref="monhoc", lazy=True)
    id_ma_cac_mon = relationship("DiemCacMon" , backref = "IDMonHoc", lazy = False)

    def __str__(self):
        return self.tenMH

class HocSinh (User):
    __tablename__ = 'hocsinh'
    ID_HS = Column(Integer, ForeignKey(User.id), primary_key=True, unique=True)
    # HS_MH = relationship('DiemSo', backref="hocsinh", lazy=True)
    #HS_LH = relationship('HocSinh_LopHoc', backref="hocsinh", lazy=True)
    id_diem_cac_mon = relationship("DiemCacMon", backref="ID_HS",lazy =True)

    def __str__(self):
        return self.name
class LopHoc(db.Model):
    __tablename__ = 'lophoc'
    maLop = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    tenLop = Column(String(50), nullable=False)
    LH_HS = relationship('HocSinh_LopHoc', backref="lophoc", lazy=True)

    def __str__(self):
        return self.tenLop

class HocKy (db.Model):
    __tablename__ = 'hocki'
    maHK= Column(Integer,primary_key=True, nullable=False,autoincrement=True)
    tenHK = Column(String(50), nullable =False)
    namHoc = Column(DATE, nullable =False)
    def __str__(self):
        return self.tenHK

class DiemSo (db.Model):
    __tablename__ = 'diemso'
    maDiemSo = Column(Integer, primary_key=True, autoincrement=True)
    loaiDiem = Column (Integer , nullable =False)
    maMH = Column(Integer, ForeignKey(MonHoc.IDMonHoc), nullable=False)
    ID_HocKi = Column(Integer,ForeignKey(HocKy.maHK), nullable = False)
    id_diem_cac_mon = relationship("DiemCacMon", backref ="maDiemSo",lazy = True)
    def __str__(self):
        if self.loaiDiem == 1:
            return "Diem Mieng"
        if self.loaiDiem == 2:
            return "Diem 15p"
        if self.loaiDiem == 3:
            return "Diem 45p"
        if self.loaiDiem == 4:
            return "Diem giua ki"
        if self.loaiDiem == 5:
            return "Diem cuoi ki"
        return "Loai ddiem khong ton tai"

class DiemCacMon(db.Model):
    __tablename__ ="diemcacmon"
    idDiemCacMon = Column(Integer, primary_key=True, autoincrement=True)
    idDiem = Column(Integer,ForeignKey(DiemSo.maDiemSo),nullable = False)
    idHS = Column(Integer,ForeignKey(HocSinh.ID_HS),nullable =False)
    idMon = Column(Integer,ForeignKey(MonHoc.IDMonHoc),nullable = False)
    giaTri = Column(Float, nullable=False)
class HocSinh_LopHoc(db.Model):
    __tablename__ = 'hocsinh_lophoc'
    maHS_LH = Column(Integer, primary_key=True, autoincrement=True)
    maLH = Column (Integer, ForeignKey(LopHoc.maLop), nullable = False)
    ID_HS = Column(Integer, ForeignKey(HocSinh.ID_HS), nullable=False)
    maHK = Column(Integer, ForeignKey(HocKy.maHK), nullable = False)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()
