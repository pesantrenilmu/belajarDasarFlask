from flask import Flask, render_template, request, redirect, flash, session
from flaskext.mysql import MySQL
app = Flask(__name__)
app.secret_key = 'rahasia'
db=MySQL(host="localhost", user="root", passwd="", db="dbtokoa")
db.init_app(app)

@app.route('/')
def index():
    return render_template('user/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM user where username=%s and password=%s",(username,password))
        data = cursor.fetchone()
        if data:
            session['user']=username
            return redirect('/admin/home')
        else:
            flash('Email atau password salah!', 'danger')
            return redirect('/login')

    return render_template('login.html')

@app.route('/tentang')
def tentang():
    return render_template('user/tentang.html')

@app.route('/kontak')
def kontak():
    return render_template('user/kontak.html')


#  admin

@app.route('/admin/home')
def home():
    if 'user' not in session:
        return redirect('/login')
    return render_template('admin/index.html')

@app.route('/admin/admin-kelola-barang')
def kelolabarang():
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM barang")
        data = cursor.fetchall()
    except Exception as e:
        flash(f"Gagal mengambil data: {e}", "danger")
    return render_template('admin/barang.html', hasil=data)


@app.route('/admin/form-tambah-barang', methods=['GET', 'POST'])
def formbarang():
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        stok = request.form['stok']
        kategori = request.form['kategori']
        deskripsi = request.form['deskripsi']
        try:
            cursor = db.get_db().cursor()
            sql = "INSERT INTO barang (nama, harga, stok, kategori, deskripsi) VALUES (%s, %s, %s, %s, %s)"
            val = (nama, harga, stok, kategori, deskripsi)
            print(val)
            cursor.execute(sql, val)
            db.get_db().commit()
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
        

        flash("Data barang berhasil ditambahkan!", "success")
        return redirect('/admin/admin-kelola-barang')
    return render_template('admin/formbarang.html')


@app.route('/admin/form-edit-barang/<id>', methods=['GET', 'POST'])
def formeditbarang(id):
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        stok = request.form['stok']
        kategori = request.form['kategori']
        deskripsi = request.form['deskripsi']
        try:
            cursor = db.get_db().cursor()
            sql = """
                UPDATE barang
                SET nama=%s, harga=%s, stok=%s, kategori=%s, deskripsi=%s
                WHERE id=%s
            """
            val = (nama, harga, stok, kategori, deskripsi,id)
            print(val)
            cursor.execute(sql, val)
            db.get_db().commit()
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
        

        flash("Data barang berhasil diupdate!", "success")
        return redirect('/admin/admin-kelola-barang')
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM barang where id=%s",(id))
        data = cursor.fetchone()
    except Exception as e:
        flash(f'Gagal mengambil data: {e}', 'danger')
        return redirect('/admin/admin-kelola-barang')
    return render_template('admin/formeditbarang.html', barang=data)


@app.route('/admin/hapus-barang/<int:id>', methods=['POST'])
def hapus_barang(id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("DELETE FROM barang WHERE id = %s", (id,))
        db.get_db().commit()
        flash("Barang berhasil dihapus.", "success")
    except Exception as e:
        flash(f"Gagal menghapus barang: {e}", "danger")
   

    return redirect('/admin/admin-kelola-barang')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')




@app.route('/admin/admin-kelola-pengguna')
def kelolapengguna():
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM barang")
        data = cursor.fetchall()
    except Exception as e:
        flash(f"Gagal mengambil data: {e}", "danger")
    return render_template('admin/pengguna.html', hasil=data)



@app.route('/admin/admin-kelola-user')
def kelolauser():
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM user")
        data = cursor.fetchall()
    except Exception as e:
        flash(f"Gagal mengambil data: {e}", "danger")
    return render_template('admin/user.html', hasil=data)


@app.route('/admin/form-tambah-user', methods=['GET', 'POST'])
def formuser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
        try:
            cursor = db.get_db().cursor()
            sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
            val = (username, password)
            print(val)
            cursor.execute(sql, val)
            db.get_db().commit()
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
        

        flash("Data user berhasil ditambahkan!", "success")
        return redirect('/admin/admin-kelola-user')
    return render_template('admin/formuser.html')

@app.route('/admin/form-edit-user/<id>', methods=['GET', 'POST'])
def formedituser(id):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
        try:
            cursor = db.get_db().cursor()
            sql = """
                UPDATE user
                SET username=%s, password=%s
                WHERE id=%s
            """
            val = (username, password,id)
            print(val)
            cursor.execute(sql, val)
            db.get_db().commit()
        except Exception as e:
            flash(f'Terjadi kesalahan saat menyimpan data: {e}', 'danger')
        

        flash("Data user berhasil diupdate!", "success")
        return redirect('/admin/admin-kelola-user')
    data=[]
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM user where id=%s",(id))
        data = cursor.fetchone()
    except Exception as e:
        flash(f'Gagal mengambil data: {e}', 'danger')
        return redirect('/admin/admin-kelola-user')
    return render_template('admin/formedituser.html', user=data)


if __name__ == '__main__':
    app.run(debug=True)
