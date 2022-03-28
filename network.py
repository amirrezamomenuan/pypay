from crypt import methods
import json

import requests
from flask import Flask

app = Flask(__name__)


@app.route("/initial-boot-data", methods = ["GET"])
def initial_boot_data():
    return "<p>Hello, World!</p>"


@app.route("/new-block", methods = ["POST"])
def new_block():
    return "<p>Hello, World!</p>"


@app.route("/new-transaction", methods = ["POST"])
def new_transaction():
    return "<p>Hello, World!</p>"


@app.route("/get-full-chain", methods = ['GET'])
def get_full_chain():
    return "<p>Hello, World!</p>"


@app.route("/get-mempool-transactions", methods = ['GET'])
def get_mempool_transactions():
    return "<p>Hello, World!</p>"