from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('user/index.html')
@app.route('/tentang')
def tentang():
    return render_template('user/tentang.html')

@app.route('/kontak')
def kontak():
    return render_template('user/kontak.html')


#  admin

@app.route('/admin/home')
def home():
    return render_template('admin/index.html')

@app.route('/admin/admin-kelola-barang')
def kelolabarang():
    return render_template('admin/barang.html')



if __name__ == '__main__':
    app.run(debug=True)
