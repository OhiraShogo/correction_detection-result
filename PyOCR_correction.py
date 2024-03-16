from PIL import Image
import pyocr
import re
import statistics
import cv2
import numpy as np
import Levenshtein
import os

sym0 = 'lent'
sym1 = 'modere'
sym2 = 'pressez'
sym3 = 'rall'
sym4 = 'tres'
sym5 = 'cresc'
sym6 = 'moins'
list = [sym0,sym1,sym2,sym3,sym4,sym5,sym6]

def keep_only_alphabets(input_str): #文字列からアルファベット以外を除去するための関数
    return re.sub(r'[^a-zA-Z]', '', input_str)

def levenshtein_similarity(str1, str2): #レーベンシュタイン距離を用いた類似度αを計算するための関数
    distance = Levenshtein.distance(str1, str2)
    max_length = max(len(str1), len(str2))
    similarity = 1 - (distance / max_length)
    return similarity

def com(bbox,conf,label,dir,st): #PyOCRを用いた修正のための関数
  image = img.crop((bbox[0], bbox[1], bbox[2], bbox[3]))
  txt1 = tool.image_to_string(image, lang='eng', builder=pyocr.builders.TextBuilder(tesseract_layout=8)) #PyOCRでバウンディングボックス内を読み取る
  txt1 = txt1.lower() #小文字に変換
  txt1 = txt1.replace(' ','') #空白を除去
  txt1 = txt1.replace('é','e') #éをeに変換
  txt1 = keep_only_alphabets(txt1) #アルファベット以外を除去
  p = 0
  length = len(txt1)
  pos = [0]*len(list) #各クラスの類似度Θを入れるためのリスト
  n = 0
  filtered_result_path = dir + "/" + st
  for sub in list:
    pos[n] = levenshtein_similarity(txt1, sub) #レーベンシュタイン距離を計算
    if  len(txt1) != 0 and txt1[0] == sub[0]  :
      pos[n] += 0.1 #頭文字が一致していた場合0.1を加算
    n+=1
  pos[label] += conf*0.8 #YOLOv5の信頼度に0.8をかけた値を加算
  max_number = max(pos) #Θが最も高いクラスを探す
  index = pos.index(max_number) #Θが最も高いクラスを探す
  if pos[index] < 0.4: #Θが0.4を下回った場合に検出を無効
    print(name)
    print('detection:'+txt1)
    print(list[label])
    print('none')
    print(pos)
  else:
    if label != index: #Θが最も高いクラスが検出結果のクラスと異なった場合修正過程を出力
      print(name)
      print('detection:'+txt1)
      print(list[label])
      print('re:')
      print(list[index])
      print(pos)
    with open(filtered_result_path, "a") as f:
      f.write(f"{index} {conf} {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n") #修正後の結果を書き出す


tools = pyocr.get_available_tools()
tool = tools[0]
l_path = "#YOLOv5の検出結果が入ったディレクトリのパス" 
p_path = "#上記の検出対象となった楽譜画像が入ったディレクトリパス" 
lfiles = sorted(os.listdir(l_path))
pfiles = sorted(os.listdir(p_path))
result_path = "#修正後の結果を格納するディレクトリパス" 
os.makedirs(result_path, exist_ok=True)
for file1, file2 in zip(lfiles, pfiles):
    path1 = os.path.join(l_path, file1)
    path2 = os.path.join(p_path, file2)
    img = Image.open(path2)
    name = os.path.basename(path1)
    with open(path1, "r") as f:
      lines = f.readlines()
      for line in lines:
        parts = line.strip().split(" ")
        if len(parts) == 6:
            label, confidence, x_left, y_top, x_right, y_bottom = parts
            confidence = float(confidence)
            label = int(label)
            bbox = (int(x_left), int(y_top), int(x_right), int(y_bottom))
            com(bbox,confidence,label,result_path,name) #PyOCRを用いた修正のための関数を呼び出す
