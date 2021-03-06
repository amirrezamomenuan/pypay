import json

from flask import (
    Flask,
    jsonify,
    request,
    )
import block_core
import transaction_core

CORRECT_STATUS_CODE = 200
INCORRECT_STATUS_CODE = 400

app = Flask(__name__)
import pypayd

@app.route("/initial-boot-data", methods = ["GET"])
def initial_boot_data():
    full_chain = pypayd.deamon_node.full_chain
    mempool = pypayd.deamon_node.mempool
    relative_nodes = pypayd.deamon_node.relative_nodes

    return jsonify(
        {
            "full_chain" : full_chain,
            "mempool" : mempool,
            "relative_nodes" : relative_nodes
        }
    )


@app.route("/new-transaction", methods = ["POST"])
def new_transaction():
    recieved_transaction = request.get_json()

    dictified_recieved_data = json.loads(recieved_transaction)
    response_data = transaction_core.validate_transaction(dictified_recieved_data)

    return jsonify(
        {"message" : response_data[0], "status" : response_data[1]}
    )


@app.route("/new-block", methods = ["POST"])
def new_block():
    last_block = pypayd.deamon_node.get_last_block()
    recieved_block = request.get_json()
    response_data = block_core.handle_new_block(block = recieved_block, last_block=last_block)
    if response_data[1] == CORRECT_STATUS_CODE:
        print(response_data[0])
    else:
        print("AN ERROR OCCURED: ",response_data[0])

    return jsonify(
        {"message" : response_data[0], "status" : response_data[1]}
    )


@app.route("/get-mempool-transactions", methods = ['GET'])
def get_mempool_transactions():
    ledger = pypayd.deamon_node.mempool
    print(ledger)
    return jsonify(
        {"message" : ledger, "status" : 200}
    )