# gemini-cli-webui
gemini-cliをGradioのUIから操作（非インタラクティブモードのみ）  
なお、Windowsでしか試してません。  
多分Windows以外じゃ動かない。  

## インストール
``` cli
# 適当なフォルダで
git clone https://github.com/siouni/gemini-cli-webui.git
cd gemini-cli-webui
# uvはなくてもOK
uv venv venv --python 3.11
venv\Scripts\activate
uv pip install -r requirements.txt
# node.jsのインストール（nodeenv利用）
nodeenv -p
# 一旦、コンソールを閉じて再度コンソールを起動（VScodeなら「ゴミ箱」（not ✘ アイコン）アイコンをクリック）
# gemini-cli-webui フォルダにいる前提
venv\Scripts\activate
npm install
# gemini cli を 一度インタラクティブモードで起動して初期設定を行う
# 終わったらCtrl+C（2回）で終了
npx gemini
python webui.py
```
  
**支援のお願い**  
貧乏なのでグラボが買えません。  
余裕のある方はもしよければ、下記サイトなどからご支援いただけると嬉しいです。  
  
[Amazon欲しいものリスト](https://www.amazon.jp/hz/wishlist/ls/2TDWT1E5JBT8S?ref_=wl_share)
※PCパーツはネタです。
  
[![OFUSE](https://github.com/user-attachments/assets/62ffa121-f975-4080-923a-7f55f3cf3759)](https://ofuse.me/siouni)  
OFUSEは投げ銭サイトです。  
  
[mond](https://mond.how/ja/siouni_unia)  
mondで匿名投稿・質問を受け付けています。  
質問などはこちらでも構いません。  
  
[prompton](https://prompton.io/siouni_unia)  
AIイラストの有償依頼を受け付けいています。  
無償プランもあるので、お試しならそちらでも。  
  
[patreon](https://patreon.com/siouni_unia)  
R18系のイラストをメンバーシップ向けに公開中。  