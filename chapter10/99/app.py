import os
import flask
from flask import Flask, render_template, request
import subprocess
import re

app = Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.php')

def Translator(in_text):
    p = subprocess.run('echo '+ in_text +" | subword-nmt apply-bpe -c ../out_95/codes_95.ja | fairseq-interactive ../out_95/data-bin --path ../out_95/checkpoints/checkpoint_best.pt --beam 5 | grep '^H' | cut -f 3", text=True, stdout=subprocess.PIPE, shell=True)
    out_subw = p.stdout
    out = re.sub(r'(@@ )|(@@ ?$)', '', out_subw)
    return out

@app.route('/', methods=['POST'])
def result():
    if request.method == 'POST':
        in_text = list(request.form.to_dict().values())[0]
        out_text = Translator(in_text)
        return render_template("index.php", src_text=in_text, tgt_text=out_text)

if __name__ == "__main__":
    app.run(debug=True)