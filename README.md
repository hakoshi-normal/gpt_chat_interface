# gpt_chat_interface

rinnaの対話GPTモデルを利用したチャットインタフェース実装．
実装の都合上，計算サーバとインタフェース提供サーバを別端末としているため，物理サーバを1つ介する．

gpt_serverディレクトリ内ファイル群が計算サーバのプログラム，middle_server内ファイル群がインタフェース提供サーバのプログラムである．

以下のPythonライブラリ並びに依存ライブラリが必要となる．（requirements.txtに記載あり）

計算サーバ
- transformers
- accelerate
- sentencepiece

インタフェース提供サーバ
- paramiko
- fastapi
- uvicorn
- Jinja2
- python-multipart

 ![screenshot](https://raw.githubusercontent.com/hakoshi-normal/md_images/main/gpt_chat_interface_architecture_fig.jpg "fig")

参考
- インタラクティブなLINE風チャット小説@uji_keyaki(宇治 槻) Qiita
  https://qiita.com/uji_keyaki/items/87dd26c178ed8a18d267
- rinna/japanese-gpt-neox-3.6b-instruction-ppo Hugging Face
  https://huggingface.co/rinna/japanese-gpt-neox-3.6b-instruction-ppo
　他
