from sqlalchemy import func, engine

from QuanLyHocSinh.models import MonHoc, DiemSo, HocSinh, User, DiemCacMon,HocKy,LopHoc,HocSinh_LopHoc
from QuanLyHocSinh import db, login
import hashlib


def load_MonHoc():
    return MonHoc.query.all()


def load_bang_diem(id_mon_hoc=None, hocki=None, id_hs = None):
    return db.session.query(DiemSo.maDiemSo, DiemSo.loaiDiem, DiemSo.maMH, DiemSo.ID_HocKi, DiemCacMon.idDiem, DiemCacMon.idHS, DiemCacMon.giaTri)\
        .join(DiemCacMon, DiemCacMon.idDiem.__eq__(DiemSo.maDiemSo))\
        .filter(DiemSo.ID_HocKi.__eq__(hocki)).filter(DiemSo.maMH.__eq__(id_mon_hoc)).filter(DiemCacMon.idHS.__eq__(id_hs)).all()


def load_hoc_sinh():
    return HocSinh.query.all()


def load_diem_cac_mon(id_hs=None):
    query = DiemCacMon.query
    if id_hs:
        query = query.filter(DiemCacMon.idHS == id_hs)
    return query.all()


def tinh_diem_tb(idhs=None, idhk=None, id_mh=None):
    diem = load_bang_diem(id_mon_hoc=id_mh, hocki=idhk, id_hs=idhs)
    diemtb15p = 0
    diemtbmieng = 0
    diemtb45p = 0
    diemtbgiuaki = 0
    diemtbcuoiki = 0

    diemcuoiki = []
    diemgiuaki = []
    tongdiem15p = []
    tongdiem45p = []
    tongdiemmieng = []

    for d in diem:
        if d.loaiDiem == 1:
            tongdiemmieng.append(d.giaTri)
        elif d.loaiDiem == 2:
            tongdiem15p.append(d.giaTri)
        elif d.loaiDiem == 3:
            tongdiem45p.append(d.giaTri)
        elif d.loaiDiem == 4:
            diemgiuaki.append(d.giaTri)
        elif d.loaiDiem == 5:
            diemcuoiki.append(d.giaTri)
    diemtbmieng = sum(tongdiemmieng)/(len(tongdiemmieng) if len(tongdiemmieng) > 0 else 1)
    diemtb15p = sum(tongdiem15p)/(len(tongdiem15p) if len(tongdiem15p) > 0 else 1)
    diemtb45p = sum(tongdiem45p)/(len(tongdiem45p) if len(tongdiem45p) > 0 else 1)
    diemtbgiuaki = sum(diemgiuaki)/(len(diemgiuaki) if len(diemgiuaki) > 0 else 1)
    diemtbcuoiki = sum(diemcuoiki)/(len(diemcuoiki) if len(diemcuoiki) > 0 else 1)

    diem_tb_mon = (diemtbmieng + diemtb15p + diemtb45p * 2 + diemtbgiuaki * 2 + diemtbcuoiki * 3) / 9
    return round(diem_tb_mon, 2)

def diemtb(idhs = None, idhk = None):
    tat_ca_mon = load_MonHoc()
    diem_tb_list = []
    for monhoc in tat_ca_mon:
        diem_tb_list.append(tinh_diem_tb(idhs = idhs,idhk=idhk,id_mh=monhoc.IDMonHoc))
    count = 0
    a = []
    a.append(sum(diem_tb_list)/(len(diem_tb_list) if len(diem_tb_list) >=1 else 1))
    for  i in a:
        if i >= 5:
            count = count+1

    return count


def count ():
    query = db.session.query(func.count(HocSinh_LopHoc.maLH))
    for a in query:
        i = a[0]

    return i

def dem(siso=None):
    dem = 0
    for i in range(1, siso):
        if diemtb(i,1) == 1:
            dem = dem + 1
    return dem
def xep_loai(d):
    if d > 8:
        return 'Giỏi'
    if d > 6.5 and d < 8:
        return 'Khá'
    if d > 5 and d < 6.5:
        return 'Trung bình'
    return 'Yếu'

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()) and
                             User.password.__eq__(password)).first()
def load_MonHoc():
    return MonHoc.query.all()
def load_HocKy():
    return HocKy.query.all()

def load_LopHoc():
    return LopHoc.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

# def count_Dat():
#     query = db.session.query(HocSinh_LopHoc.ID_HS,HocSinh_LopHoc.maHK) \
#                             .filter(int(diemtb(idhs=HocSinh_LopHoc.ID_HS,idhk=HocSinh_LopHoc.maHK)) >= 5)
#     return query.all()
def TiLe():
    a = dem(count())
    b = count()
    c = a/b*100
    return round(c,2)

def thongke (hk = None, lop = None):
    query = db.session.query(LopHoc.tenLop,func.count(HocSinh_LopHoc.maLH),dem(count()),TiLe())\
                            .join(LopHoc,LopHoc.maLop.__eq__(HocSinh_LopHoc.maLH))\
                            .join(HocKy,HocKy.maHK.__eq__(HocSinh_LopHoc.maHK))
    query = query.group_by(LopHoc.maLop)

    if hk:
        query = query.filter(HocSinh_LopHoc.maHK == hk)
    if lop:
        query = query.filter(LopHoc.maLop == lop)
    return query.all()

if __name__ == '__main__':
    from QuanLyHocSinh import app
    with app.app_context():
        print(thongke())
        print(count())
        print(TiLe())