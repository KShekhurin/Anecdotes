from main import app


@app.route("/queue/", methods=["POST"])
def add_to_queue():
    pass


@app.route("/queue/", methods=["GET"])
def get_from_queue():
    pass


@app.route("/queue/submit/<id>/<int:is_submit>", methods=["POST"])
def submit_from_queue(id, is_submit):
    pass