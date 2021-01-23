from flask import Flask, render_template
from mysql import connector
from flask import request, redirect, url_for

db = connector.connect(
    host     ="localhost",
    user     ="root",
    passwd   ="",
    database ="0414_uasweb"
)
if db.is_connected():
    print("Berhasil Terhubung ke Database")

app = Flask(__name__)
@app.route("/")
def home():
	cur = db.cursor()
	cur.execute("select * from base_uas")
	res = cur.fetchall()
	print(res)
	cur.close()
	return render_template("index.html", data=res)
@app.route('/admin/')
def halaman_awal():
    cur = db.cursor()
    cur.execute("select * from base_uas")
    res = cur.fetchall()
    cur.close()
    return render_template('admin.html', hasil=res)
	
@app.route('/ubah/<id>/', methods=['GET'])
def ubahdata(id):
    cur = db.cursor()
    cur.execute('select * from base_uas where id=%s', (id,))
    res = cur.fetchall()
    cur.close()
    return render_template('edit.html', hasil=res)

@app.route('/ubah/', methods=['POST'])
def ubah():
    idasli = request.form['idasli']
    id = request.form['id']
    data = request.form['data']
    image = request.form['image']
    cur = db.cursor()
    sql = "UPDATE base_uas SET id=%s, data=%s, image=%s WHERE id=%s"
    value = (id, data, image, idasli)
    cur.execute(sql, value)
    db.commit()
    return redirect(url_for('home'))
		
@app.errorhandler(404)
def page(e):
	return render_template('eror.html')
	

if __name__ == '__main__':
	app.run(debug=True)
	
