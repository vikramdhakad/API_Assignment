from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from utils.resume_parser import extract_resume_data
from utils.translator import translate_text
from utils.currency_converter import convert_price, CONVERSION_RATES


app = Flask(__name__)
CORS(app)
SUPPORTED_LANGUAGES = {
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French"
}


@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    try:
        parsed_data = extract_resume_data(file)
        return jsonify(parsed_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET','POST'])
def translate_page():
    translation = ""
    original_text = ""
    selected_language = "hi"

    if request.method == "POST":
        original_text = request.form.get("text")
        selected_language = request.form.get("target_lang", "hi")

        if original_text and selected_language in SUPPORTED_LANGUAGES:
            translation = translate_text(original_text, selected_language)

    return render_template(
        "index.html",
        translated_text=translation,
        original_text=original_text,
        selected_language=selected_language,
        languages=SUPPORTED_LANGUAGES
    )


@app.route('/currency', methods=['GET', 'POST'])
def currency_converter_page():
    converted_price = None
    usd_amount = None
    selected_currency = "Indian Rupee"  # ✅ fixed

    if request.method == 'POST':
        try:
            usd_amount = float(request.form['usd_amount'])
            selected_currency = request.form['currency']
            result = convert_price(usd_amount, selected_currency)
            converted_price = result.get("converted_price") or result.get("error")
        except Exception as e:
            converted_price = f"Error: {str(e)}"

    return render_template(
    'index.html',
    currencies=CONVERSION_RATES.keys(),
    converted_price=converted_price,
    usd_amount=usd_amount,
    selected_currency=selected_currency,
    languages=SUPPORTED_LANGUAGES,                # ✅ ADD THIS
    selected_language="hi"                         # ✅ ADD THIS (or keep track of it)
)


@app.route('/price', methods=['GET'])
def pricing_api():
    # Accept either 'currency' or legacy 'country' param
    currency_param = request.args.get('currency') or request.args.get('country') or 'Indian Rupee'
    amount_str = request.args.get('amount', '100')
    try:
        usd_amount = float(amount_str)
    except ValueError:
        return jsonify({"error": f"Invalid amount '{amount_str}'"}), 400

    result = convert_price(usd_amount, currency_param)
    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)
