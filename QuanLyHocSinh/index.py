from flask_login import login_user, logout_user, current_user
from QuanLyHocSinh import app, dao, admin, login
from flask import render_template, request, redirect, session
from flask_session import Session




@app.route("/")
def Choose():
    return render_template("choose.html")

@app.route("/my/<int:id_hk>")
def index(id_hk):
    mon_hoc = dao.load_MonHoc()
    return render_template("index.html", mon_hoc=mon_hoc,id_hk = id_hk)

@app.route('/my/<id_hk>/logout')
def logout_my_user(id_hk):
    logout_user()
    return redirect('/my/'+id_hk+'/login')

@app.route("/diem/<int:id_hk>/<int:id_mon_hoc>")
def score(id_mon_hoc,id_hk):
    id_hs = current_user.id
    bangdiem = dao.load_bang_diem(id_mon_hoc, id_hk, id_hs=id_hs)
    bangdiemhocsinh=  dao.load_diem_cac_mon(current_user.id)
    return render_template("bangdiem.html", bangdiem=bangdiem, bangdiemhocsinh=bangdiemhocsinh, id_hk=id_hk)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)

@app.route('/my/<id_hk>/login', methods=['get', 'post'])
def login_my_user(id_hk):
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            n = request.args.get('next')
            return redirect(n if n else '/my/'+id_hk)
        else:

            err_msg = 'Username hoặc Password không chính xac !!'
    return render_template('login.html', err_msg=err_msg,id_hk = id_hk)


@app.route('/login-admin', methods=['post'])
def admin_login():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
        session["role"] = str(current_user.use_role)
    return redirect('/admin')


@app.route("/my/<id_hk>/tongket")
def TongKet(id_hk):
    load_mh = dao.load_MonHoc()
    id_hs = current_user.id
    listdiemtb = []
    for monhoc in load_mh:
        listdiemtb.append(dao.tinh_diem_tb(idhs=id_hs, idhk=id_hk, id_mh=monhoc.IDMonHoc))
    diem_tb_tat_ca_mon = round(sum(listdiemtb)/len(listdiemtb),2)
    xep_loai = dao.xep_loai(diem_tb_tat_ca_mon)
    return render_template("TongKet.html",
                           id_hk=id_hk,
                           load_mh=load_mh,
                           diemtbcacmon=listdiemtb,
                           dtbtc=diem_tb_tat_ca_mon,
                           xep_loai=xep_loai)


if __name__ == '__main__':
    app.run(debug=True)
