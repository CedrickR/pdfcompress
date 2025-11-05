import os
import subprocess
import tempfile
from pathlib import Path

from flask import (Flask, flash, redirect, render_template, request, send_file,
                   url_for)
from werkzeug.utils import secure_filename

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf"}

QUALITY_PRESETS = {
    "low": "/screen",
    "medium": "/ebook",
    "high": "/prepress",
}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def compress_pdf(input_path: Path, output_path: Path, quality: str) -> None:
    quality_flag = QUALITY_PRESETS.get(quality, "/ebook")
    command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={quality_flag}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        str(input_path),
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError as exc:
        raise RuntimeError(
            "Ghostscript (gs) n'est pas disponible sur le serveur."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("La compression a échoué. Vérifiez que le fichier est valide.") from exc


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)
    app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024  # 32 MB
    app.secret_key = os.environ.get("SECRET_KEY", "change-me")

    @app.route("/")
    def index():
        return render_template("index.html", quality_presets=QUALITY_PRESETS)

    @app.post("/compress")
    def compress():
        if "pdf" not in request.files:
            flash("Aucun fichier reçu.", "danger")
            return redirect(url_for("index"))

        file = request.files["pdf"]
        if file.filename == "":
            flash("Aucun fichier sélectionné.", "warning")
            return redirect(url_for("index"))

        if not allowed_file(file.filename):
            flash("Le fichier doit être au format PDF.", "warning")
            return redirect(url_for("index"))

        filename = secure_filename(file.filename)
        quality = request.form.get("quality", "medium")

        with tempfile.NamedTemporaryFile(dir=UPLOAD_DIR, suffix=".pdf", delete=False) as original_tmp:
            file.save(original_tmp.name)

        compressed_tmp = tempfile.NamedTemporaryFile(dir=UPLOAD_DIR, suffix=".pdf", delete=False)
        compressed_tmp.close()

        try:
            compress_pdf(Path(original_tmp.name), Path(compressed_tmp.name), quality)
            return send_file(
                compressed_tmp.name,
                mimetype="application/pdf",
                as_attachment=True,
                download_name=f"compressed_{filename}",
            )
        except RuntimeError as err:
            flash(str(err), "danger")
            return redirect(url_for("index"))
        finally:
            for path in (original_tmp.name, compressed_tmp.name):
                try:
                    os.unlink(path)
                except FileNotFoundError:
                    pass

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
