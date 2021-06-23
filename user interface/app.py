from flask import Flask, session, flash, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.secret_key = "WEWETWEFwef$%#$^RGG^Y$RGERGT#%^%^$%^465"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///voters.sqlite3'

db = SQLAlchemy(app)


class Voters(db.Model):
	_id = db.Column("id", db.Integer, primary_key=True)
	vid = db.Column("vid", db.Integer, nullable=False)
	name = db.Column("name", db.String(100), nullable=False)

	def __init__(self, vid, name):
		self.vid = vid
		self.name = name

class Voted(db.Model):
	_id = db.Column("id", db.Integer, primary_key=True)
	vvid = db.Column("vid", db.Integer, nullable=False)
	vname = db.Column("name", db.String(100), nullable=False)

	def __init__(self, vvid, vname):
		self.vvid = vvid
		self.vname = vname

def send_vote(vote_id):
	url = f"http://127.0.0.1:5000/recvapi/{vote_id}"

	data = {
		"vote": int(vote_id)
	}

	response = requests.patch(url, data)
	print(response.json)


@app.route("/", methods=["POST", "GET"])
def index():
	if request.method == "POST":
		vid = request.form["voter_id"]
		found_voter = Voters.query.filter_by(vid=vid).first()
		if found_voter:
			session["voter"] = found_voter.vid
			delete_voter = Voters.query.filter_by(vid=vid).delete()
			data = Voted(vid, found_voter.name)
			db.session.add(data)
			db.session.commit()
			return redirect(url_for("vote"))
		else:
			flash("Voter Id not found")
			return redirect(url_for("index"))

	return render_template("index.html")


@app.route("/vote", methods=["POST", "GET"])
def vote():
	if "voter" in session:
		if request.method == "POST":
			vote = request.form["vote"]
			if vote == "bjp":
				send_vote(1)
			elif vote == "cong":
				send_vote(2)
			elif vote == "harish":
				send_vote(3)

			session.pop("voter")
			return redirect(url_for("index"))
		return render_template("vote.html")
	else:
		return redirect(url_for("index"))


if __name__ == '__main__':
	db.create_all()
	app.run(port="5080",debug=True)