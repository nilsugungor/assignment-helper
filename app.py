from flask import Flask, request, jsonify, render_template
from note_logic import save_user_note, get_all_notes  # Import necessary functions
from paraphraser import paraphrase_text  # Assuming paraphraser.py contains your paraphrase function

app = Flask(__name__)

# Route to serve the homepage
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")  # This will look inside the templates/ folder

@app.route("/add-note", methods=["POST"])
def add_note():
    if request.is_json:
        data = request.json
    else:
        data = request.form  # fallback for form-data

    note = save_user_note(
        user_id=data["user_id"],
        title=data.get("title", "Untitled"),
        content=data["content"]
    )
    return jsonify({"message": "Note saved", "note": note}), 200

# Route to view all saved notes
@app.route("/view-notes", methods=["GET"])
def view_notes():
    notes = get_all_notes()
    return jsonify(notes)

# Route to send selected notes to AI for paraphrasing
@app.route("/send-to-ai", methods=["POST"])
def send_to_ai():
    selected_notes_ids = request.json.get("selected_notes")
    notes = get_all_notes()

    # Get the selected notes
    selected_notes = [note for note in notes if note['id'] in selected_notes_ids]

    # Paraphrase the content of the selected notes
    for note in selected_notes:
        note['content'] = paraphrase_text(note['content'])  # Use paraphraser function here

    return jsonify({
        "message": "Notes sent to AI agent successfully!",
        "processed_notes": selected_notes
    })


if __name__ == "__main__":
    app.run(debug=True)
