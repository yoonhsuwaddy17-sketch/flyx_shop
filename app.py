import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "flyx_secret_key")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "flyx.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)
    brand = db.Column(db.String(80), default="FlyX")
    image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('orders', lazy=True))
    customer_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    size = db.Column(db.String(10), default='M')
    color = db.Column(db.String(50))
    quantity = db.Column(db.Integer, default=1)
    payment = db.Column(db.String(30), default='KPay')
    notes = db.Column(db.String(255))
    total_amount = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.before_first_request
def init_db():
    db.create_all()
    if Product.query.count() == 0:
        demo = Product(name="FlyX Classic Tee", price=10000, brand="FlyX", image=None)
        db.session.add(demo)
        db.session.commit()

@app.route("/")
def index():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("index.html", products=products)

@app.route("/order/<int:product_id>", methods=["GET","POST"])
def order(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == "POST":
        qty = int(request.form.get("quantity", 1))
        order = Order(
            product_id=product.id,
            customer_name=request.form["customer_name"],
            phone=request.form["phone"],
            address=request.form["address"],
            size=request.form.get("size","M"),
            color=request.form.get("color",""),
            quantity=qty,
            payment=request.form.get("payment","KPay"),
            notes=request.form.get("notes",""),
            total_amount=product.price * qty,
            status="Pending"
        )
        db.session.add(order)
        db.session.commit()
        flash("Order placed! Admin will confirm via phone/message.", "success")
        return redirect(url_for("index"))
    return render_template("order.html", product=product)

def is_admin():
    return session.get("admin") == True

@app.route("/admin", methods=["GET"])
def admin():
    authed = is_admin()
    products = Product.query.order_by(Product.created_at.desc()).all() if authed else []
    orders = Order.query.order_by(Order.created_at.desc()).all() if authed else []
    return render_template("admin.html", authed=authed, products=products, orders=orders)

@app.route("/admin/login", methods=["POST"])
def admin_login():
    pwd = request.form.get("password","")
    expected = os.environ.get("ADMIN_PASSWORD", "flyxadmin")
    if pwd == expected:
        session["admin"] = True
        flash("Admin logged in.", "success")
    else:
        flash("Wrong password.", "error")
    return redirect(url_for("admin"))

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    flash("Logged out.", "success")
    return redirect(url_for("admin"))

@app.route("/admin/product", methods=["POST"])
def admin_add_product():
    if not is_admin():
        return redirect(url_for("admin"))
    name = request.form["name"]
    price = int(request.form.get("price", 0))
    brand = request.form.get("brand","FlyX")
    img = request.files.get("image")
    filename = None
    if img and img.filename:
        filename = secure_filename(img.filename)
        img.save(os.path.join(UPLOAD_DIR, filename))
    p = Product(name=name, price=price, brand=brand, image=filename)
    db.session.add(p)
    db.session.commit()
    flash("Product saved.", "success")
    return redirect(url_for("admin"))

@app.route("/admin/order/<int:order_id>", methods=["POST"])
def admin_update_order(order_id):
    if not is_admin():
        return redirect(url_for("admin"))
    status = request.form.get("status","Pending")
    o = Order.query.get_or_404(order_id)
    o.status = status
    db.session.commit()
    flash("Order updated.", "success")
    return redirect(url_for("admin"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)