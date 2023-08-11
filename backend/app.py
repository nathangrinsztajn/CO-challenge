from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaderboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class LeaderboardEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    time = db.Column(db.Float, nullable=False)
    performance = db.Column(db.Float, nullable=False)
    function_code = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    new_entry = LeaderboardEntry(
        name=data['name'],
        time=data['time'],
        performance=data['performance'],
        function_code=data['function']
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'message': 'Successfully registered!'}), 200

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    entries = LeaderboardEntry.query.all()
    return jsonify([{
        'name': entry.name,
        'time': entry.time,
        'performance': entry.performance,
        'function': entry.function_code
    } for entry in entries]), 200

@app.route('/view_leaderboard', methods=['GET'])
def view_leaderboard():
    entries = LeaderboardEntry.query.all()
    return render_template('leaderboard.html', leaderboard=entries)

if __name__ == '__main__':
    # Create tables if they don't exist
    app.run()
