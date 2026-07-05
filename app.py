"""
AES-128 Encryption Web Application
Flask Backend
Author : Angga Yudha
"""

from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from aes.encrypt import AESEncrypt
from aes.decrypt import AESDecrypt

from aes.utils import (
    validate_key
)

# ======================================================
# FLASK CONFIG
# ======================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = "aes-128-project"

app.config["JSON_SORT_KEYS"] = False

# ======================================================
# HELPER
# ======================================================

def success(data):

    return jsonify({

        "success": True,

        "data": data

    })


def failed(message):

    return jsonify({

        "success": False,

        "message": str(message)

    })
    
    # ======================================================
# HOME
# ======================================================

@app.route("/")
def index():

    return render_template(

        "index.html"

    )
    
    # ======================================================
# ENCRYPT
# ======================================================

@app.route("/encrypt", methods=["POST"])
def encrypt():

    try:

        # ------------------------------------------
        # Ambil Data
        # ------------------------------------------

        data = request.get_json()

        plaintext = data.get(

            "plaintext",

            ""

        ).strip()

        key = data.get(

            "key",

            ""

        ).strip().upper()

        # ------------------------------------------
        # Validasi Input
        # ------------------------------------------

        if plaintext == "":

            return failed(

                "Plaintext tidak boleh kosong."

            )

        validate_key(

            key

        )

        # ------------------------------------------
        # Proses Enkripsi
        # ------------------------------------------

        aes = AESEncrypt(

            plaintext,

            key

        )

        result = aes.encrypt()

        # ------------------------------------------
        # Response
        # ------------------------------------------

        return success(

            result

        )

    except Exception as e:

        return failed(

            str(e)

        )
        
        # ======================================================
# DECRYPT
# ======================================================

@app.route("/decrypt", methods=["POST"])
def decrypt():

    try:

        # ------------------------------------------
        # Ambil Data
        # ------------------------------------------

        data = request.get_json()

        ciphertext = data.get(

            "ciphertext",

            ""

        ).strip().upper()

        key = data.get(

            "key",

            ""

        ).strip().upper()

        # ------------------------------------------
        # Validasi Input
        # ------------------------------------------

        if ciphertext == "":

            return failed(

                "Ciphertext tidak boleh kosong."

            )

        validate_key(

            key

        )

        # Ciphertext AES-128 = 16 byte = 32 digit hex
        if len(ciphertext) != 32:

            return failed(

                "Ciphertext harus terdiri dari 32 digit hexadecimal."

            )

        try:

            bytes.fromhex(ciphertext)

        except ValueError:

            return failed(

                "Ciphertext bukan hexadecimal yang valid."

            )

        # ------------------------------------------
        # Proses Dekripsi
        # ------------------------------------------

        aes = AESDecrypt(

            ciphertext,

            key

        )

        result = aes.decrypt()

        # ------------------------------------------
        # Response
        # ------------------------------------------

        return success(

            result

        )

    except Exception as e:

        return failed(

            str(e)

        )
        
        # ======================================================
# ERROR HANDLER
# ======================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({

        "success": False,

        "message": "Halaman tidak ditemukan."

    }), 404


@app.errorhandler(500)
def internal_error(error):

    return jsonify({

        "success": False,

        "message": "Terjadi kesalahan pada server."

    }), 500
    
    # ======================================================
# MAIN
# ======================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
        