#!/usr/bin/python3

import sys
import os
import json

import torch
from torchvision import models, transforms as T

from PIL import Image
from flask import Flask, jsonify, request

sys.path.append('/app')

# Flask
debug = os.environ.get('FLASK_DEBUG', False)
app = Flask(__name__, static_url_path="/static", static_folder="static")
app.debug = debug
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Pytorch
os.environ['TORCH_HOME'] = '/app/torch_home/'
model = models.resnet18(pretrained=True)
model.eval()
normalize = T.Compose([T.Resize(256), T.CenterCrop(224), T.ToTensor(),
                       T.Normalize(mean=[0.485, 0.456, 0.406],
                                   std=[0.229, 0.224, 0.225])
                       ])

class_idx = json.load(open("misc/imagenet_class_index.json"))


@app.route('/test', strict_slashes=False)
def test():
    return f"Test! Torch version: {torch.__version__}"


@app.route('/upload_image', methods=['POST'])
def upload_image():
    r = {'result': 'No attached file'}

    if request.method == 'POST' and 'image' in request.files:
        try:
            topk = int(request.args.get('topk', 5))

            img = Image.open(request.files['image'])
            img_n = normalize(img)
            with torch.no_grad():
                preds = model(img_n[None, ...])[0]

            scores, idxs = preds.topk(topk)
            text = []
            for score, idx in zip(scores, idxs):
                text.append(f"{class_idx[str(idx.item())][1]}: " +
                            f"{score.item():.2f}")

            r['result'] = 'OK'
            r['text'] = ", ".join(text)

        except Exception as e:
            r['result'] = f"Exception {type(e)}: {str(e)}"

    return jsonify(r)


if __name__ == '__main__':
    app.run('0.0.0.0', debug=debug)

