from website import create_app
from flask import Flask, session, render_template, request
import sqlite3

app = create_app()

if __name__ == '__main__':
    app.run()