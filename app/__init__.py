from flask import Flask, render_template, redirect, url_for, request, flash, session

app = Flask(__name__)
app.secret_key = 'development key'
from app import routes
