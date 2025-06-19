
from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    download_link = ""
    if request.method == "POST":
        robots_content = request.form["robots_content"]
        test_url = request.form.get("test_url", "")

        if "disallow" in robots_content.lower():
            result += "✔️ Il file contiene direttive Disallow.\n"
        else:
            result += "❌ Nessuna direttiva Disallow trovata.\n"

        if "user-agent" not in robots_content.lower():
            result += "❌ Manca la direttiva User-agent.\n"
        else:
            result += "✔️ Direttiva User-agent presente.\n"

        if test_url:
            if "/admin" in test_url or "/login" in test_url:
                result += f"⚠️ Attenzione: L'URL '{test_url}' potrebbe necessitare di essere bloccato nel robots.txt.\n"
            else:
                result += f"🔍 L'URL '{test_url}' non sembra critico, ma verifica manualmente.\n"

        # Salvataggio file
        path = os.path.join("robots_download.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(robots_content)
        download_link = "/download"

    return render_template("index.html", result=result, download_link=download_link)

@app.route("/download")
def download_file():
    return send_file("robots_download.txt", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
