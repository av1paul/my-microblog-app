import os
from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))

    app.db = client.microblog

    @app.route('/', methods=['POST', 'GET'])
    def home():
        if request.method == 'POST':
            entry_content = request.form.get('content')
            entry_title = request.form.get('title')
            date = datetime.datetime.today().strftime('%d-%m-%Y')
            formatted_date = datetime.datetime.today().strftime('%d %B, %Y')
            app.db.entries.insert({
                'title': entry_title,
                'content': entry_content,
                'date': date,
                'formatted_date': formatted_date
            })
        entries_with_date = [
            (
                entry['title'],
                entry['content'],
                entry['formatted_date'],
                entry['date']
            )
            for entry in app.db.entries.find({})
        ]
        return render_template('home.html', entries=entries_with_date)

    return app
