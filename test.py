import json

# recipient_pubkey:str,
#  amount:float, trxfee_amount:float,
#  trx_type:str = 'trx'
recipient_pubkey = "44546935152001363966336994115318905757253929535165058542390512753259362015709135447938822489762922897816314900802678280645195532490278730400211890505496161187330191639699053578875682877202312631626270135977532590297627311050878465544615999041238522547192514820047278595941435394281023621479436374614442433893,65537"
amount = 5
trxfee_amount = 0.001
trx_type = 'trx'
import wallet_cli

wallet = wallet_cli.wallet()
transaction = wallet.create_transaction(
    recipient_pubkey= recipient_pubkey,
    amount= amount,
    trxfee_amount=trxfee_amount,
    trx_type= trx_type
)

print(json.dumps(transaction, indent=4))