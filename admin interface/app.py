from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_restful import Resource, Api, abort, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "#$%#$%^%^BFGBFGBSFGNSGJTNADFHH@#%$%#T#FFWF$^F@$F#$FW"
app.config["PERMANET_SESSION_LIFETIME"] = timedelta(hours=10)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///votes.sqlite3'
api = Api(app)

db = SQLAlchemy(app)


class Votes(db.Model):
	_id = db.Column("id", db.Integer, primary_key=True)
	partie_id = db.Column("partieid", db.Integer, nullable=False)
	partie = db.Column("partie", db.String(50), nullable=False)
	votes = db.Column("votes", db.Integer, nullable=False)

	def __init__(self, partie_id, partie, votes):
		self.partie_id = partie_id
		self.partie = partie
		self.votes = votes

class admin(db.Model):
	_id = db.Column("id", db.Integer, primary_key=True)
	username = db.Column("username", db.String(100), nullable=False)
	password = db.Column("password", db.String(100), nullable=False)

	def __init__(self, username, password):
		self.username = username
		self.password = password


video_put_args = reqparse.RequestParser()
video_put_args.add_argument("vote", type=int, help="ERROR")

resource_fields = {
	"id": fields.Integer,
	"partie_id": fields.Integer,
	"partie": fields.String,
	"votes": fields.Integer
}


class MyApi(Resource):
	@marshal_with(resource_fields)
	def patch(self, vote):
		args = video_put_args.parse_args()
		result = Votes.query.filter_by(partie_id=vote).first()
		if not result:
			abort(409, message="Invalid Vote Id")

		if args["vote"] == 1:
			result.votes = int(result.votes) + 1
		elif args["vote"] == 2:
			result.votes = int(result.votes) + 1
		elif args["vote"] == 3:
			result.votes = int(result.votes) + 1

		db.session.commit()

		return result


api.add_resource(MyApi, "/recvapi/<int:vote>")

@app.route("/")
def index():
	if "admin" in session:
		bjp=Votes.query.filter_by(partie="bjp").first()
		cong=Votes.query.filter_by(partie="cong").first()
		harish=Votes.query.filter_by(partie="harish").first()
		return render_template("index.html",
			bjp=bjp,
			cong=cong,
			harish=harish,
			total = int(bjp.votes) + int(cong.votes) + int(harish.votes)
		)
	else:
		return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		found_admin = admin.query.filter_by(username=username).first()
		if found_admin:
			if found_admin.password == password:
				session.permanent = True
				session["admin"] = username
				return redirect(url_for("index",
						bjp=Votes.query.filter_by(partie="bjp"),
						cong=Votes.query.filter_by(partie="cong"),
						harish=Votes.query.filter_by(partie="harish")
					))
			else:
				flash("Incorrect password")
				return redirect(url_for("login"))
		else:
			flash("username not found")
			return redirect(url_for("login"))
	
	return render_template("login.html")


if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)