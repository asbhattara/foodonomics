import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id="hfgwbgm9x273xh7r",
                                  public_key="33gmzdz9f8x2qcy3",
                                  private_key="c1679d39b04d8a3750d2ec45b4de35e8")

@app.route("/client_token", methods=["GET"])
def client_token():
	return braintree.ClientToken.generate()

@app.route("/checkout", methods=["POST"])
def create_purchase():
 	nonce = request.form["payment_method_nonce"]
	result = braintree.transaction.sale({
		"amount": "10.00",
		"payment_method_nonce": nonce
	})
