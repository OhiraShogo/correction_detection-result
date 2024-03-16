PyOCR_correction.p:yPyOCRを用いた誤検出修正プログラム

delete.py:多重検出の除去プログラム

dataset:本研究でのYOLOv5の検出結果と、その対象の楽譜画像

PyOCR_correction.pyの実行には、apt install tesseract-ocr libtesseract-dev、pip install pyocr、pip install python-Levenshteinを事前に実行してライブラリ等をインストールする必要がある。

PyOCR_correction.pyのプログラム内に書かれているように、l_path = "#YOLOv5の検出結果が入ったディレクトリのパス" 、p_path = "#上記の検出対象となった楽譜画像が入ったディレクトリパス" 、
result_path = "#修正後の結果を格納するディレクトリパス" を指定することで実行できる。

delete.pyの実行にはプログラム内に書かれているようにl_path = "#YOLOv5の検出結果が入ったディレクトリのパス"、filtered_result_path  = "#修正後の結果を格納するディレクトリパス"を
指定することで実行できる。

datasetには本研究でのYOLOv5の検出結果と、その対象の楽譜画像が入っている。上記プログラムにおいて、これらをディレクトリのパスに指定することで本研究のように実行が可能である。

また、本研究で用いられているYOLOv5の検出結果のフォーマットは通常とは異なってなっており、
[ラベル 信頼度　バウンディングボックスの楽譜画像における実際の左上のx座標　バウンディングボックスの楽譜画像における実際の左上のy座標 バウンディングボックスの楽譜画像における実際の右下のx座標 バウンディングボックスの楽譜画像における実際の右下のy座標]となっている。
