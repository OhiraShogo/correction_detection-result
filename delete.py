import os
def calculate_iou(box1, box2):
    # バウンディングボックスの座標情報
    x1l, y1t, x1r, y1b = box1
    x2l, y2t, x2r, y2b = box2    # 重なっている領域の座標を計算
    x_left = max(x1l, x2l)
    y_top = max(y1t, y2t)
    x_right = min(x1r,x2r)
    y_bottom = min(y1b, y2b)
    if x_right <= x_left or y_bottom <= y_top:
        return 0.0    # 重なっている領域の面積を計算
    intersection_area = (x_right - x_left) * (y_bottom - y_top)    # 各バウンディングボックスの面積を計算
    area1 = (x1r - x1l)* (y1b - y1t)
    area2 = (x2r - x2l)* (y2b - y2t)    # IOUを計算
    iou = intersection_area / (area1 + area2 - intersection_area)
    return iou

l_path = "#YOLOv5の検出結果が入ったディレクトリのパス"
lfiles = sorted(os.listdir(l_path))
filtered_result_path  = "#修正後の結果を格納するディレクトリパス"
os.makedirs(filtered_result_path, exist_ok=True)
for file1 in lfiles:
  r_path = os.path.join(l_path, file1)
  name = os.path.basename(r_path)
  with open(r_path, "r") as f:
    lines = f.readlines() 
    filtered_results = {} #多重検出後の結果を保存するためのリスト
    i = 0
    for line in lines: #検出結果の各行を読み出し
      parts = line.strip().split(" ")
      if len(parts) == 6:
        label, confidence, x_center, y_center, width, height = parts
        confidence = float(confidence)
        label = int(label)
        bbox = (int(x_center), int(y_center), int(width), int(height))

        if not filtered_results:  #リストが空の場合、読み取り結果を保存
            filtered_results[0] =(label,bbox, confidence)
        else:
            up =0
            i = 0
            for data in filtered_results: #読みっとた行の信頼度をfiltered_resultsのすべての内容と比較
                abbox = filtered_results[data][1] #filtered_resultsのバウンディングボックスの座標を読み出す
                aconf = filtered_results[data][2] #filtered_resultsの信頼度を読み出す
                iou = calculate_iou(bbox,abbox) #現在読みとっている行の検出結果のバウンディングボックスとfiltered_resultsのバウンディングボックスのiouを計算
                if iou > 0.5: #iouが0.5を超えたか判断
                  if confidence > aconf: #現在読みとっている行の信頼度がfiltered_resultsの信頼度を超えているか判断
                    print('delete',filtered_results[data][0],r_path)
                    filtered_results[data] = (label,bbox, confidence) #信頼度が下回っていた結果が保存されていた場所に現在読みとっている行の検出結果を上書き
                    up = 1 #多重検出除去をしたとカウントする
                i += 1
            if up ==0: #多重検出除去をしていなければ読み取った結果をそのまま保存
                  filtered_results[i] = (label,bbox, confidence)
  with open(filtered_result_path + '/'+ name, "w") as f: #最終的な多重検出後の結果を書き出す
    for data in filtered_results:
        x_center, y_center, width, height = filtered_results[data][1]
        label = filtered_results[data][0]
        confidence = filtered_results[data][2]
        f.write(f"{label} {confidence} {x_center} {y_center} {width} {height}\n")
