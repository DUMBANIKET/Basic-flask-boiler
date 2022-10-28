from flask import Flask,request, redirect,url_for,render_template
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True, nullable=False)    


@app.route("/")
def home():
	users = db.session.execute(db.select(User).order_by(User.username)).scalars()
	return render_template("list.html", users=users)

@app.route("/create", methods=["GET", "POST"])
def user_create():
	if request.method == "POST":
		user = User(
			username=request.form["username"],
		)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("home"))

	return render_template("create.html")


if __name__ == "__main__":
	with app.app_context():
		db.create_all()
		app.run(debug=True)