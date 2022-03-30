import json

import requests
from flask import (
    Flask,
    jsonify,
    request,
    )
import block_core
import transaction_core


app = Flask(__name__)
from pypayd import deamon_node

@app.route("/initial-boot-data", methods = ["GET"])
def initial_boot_data():
    full_chain = deamon_node.full_chain
    mempool = deamon_node.mempool
    relative_nodes = deamon_node.relative_nodes

    return jsonify(
        {
            "full_chain" : full_chain,
            "mempool" : mempool,
            "relative_nodes" : relative_nodes
        }
    )
    # __________________ kind of done ____________________


@app.route("/new-block", methods = ["POST"])
def new_block():
    last_block = deamon_node.get_last_block()
    recieved_block = request.get_json()
    response_data = block_core.handle_new_block(block = recieved_block, last_block=last_block)
    #add block to chain
    return jsonify(
        {"message" : response_data[0], "status" : response_data[1]}
    )
    # __________________ kind of done ____________________


@app.route("/new-transaction", methods = ["POST"])
def new_transaction():
    recieved_transaction = request.get_json()
    print(recieved_transaction)
    response_data = transaction_core.validate_transaction(recieved_transaction)
    # add transaction to mempool
    return jsonify(
        {"message" : response_data[0], "status" : response_data[1]}
    )


@app.route("/get-full-chain", methods = ['GET'])
def get_full_chain():
    return "<p>Hello, World!</p>"


@app.route("/get-mempool-transactions", methods = ['GET'])
def get_mempool_transactions():
    return "<p>Hello, World!</p>"