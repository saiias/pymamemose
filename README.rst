=======================================
pymamemose:reStructuredText memo server
=======================================

.. image :: https://travis-ci.org/saiias/pymamemose.png?branch=master

概要
=========
- Rudy製のメモツール"mamemose"のpython移植版
- 変更点としてMarkdownではくreStructuredTextでメモを記述する
- 基本的な概要はmamsemoseと同様  

未実装の機能
============

- シンタックスハイライト
- 数式の記述
- メモのタイトルを抽出
  
環境
====

- Python製
- 主にMac OS X 10.8のPython 2.7.2でテスト
- Windowsでの動作確認はしていない

インストール方法
================
::
   
    % pip install git+git://github.com/saiias/pymamemose.git

設定
====
ホームディレクトリに ``.pymamemose.json`` という設定ファイルを置くと、それを読み込みます。

設定項目
--------

- ``DOCUMENT_ROOT``:ドキュメントルート。デフォルトは ``$HOME/Dropbox/memo``

    
- ``ECENT_NUM``:「最近更新したファイル」を表示する数。デフォルトは ``10``

    
- ``PORT``:ポート番号。デフォルトは8000

- ``REST_PATTERN``:reStructuredTextドキュメント見なす拡張子。デフォルトは ``.rst``

- ``IGNORE_FILE``:無視するファイルのリストデフォルトは ``""``

設定例
------
$HOME/.pymamemose.json::

  {
    "DOCUMENT_ROOT" :"~/Dropbox/memo",
    "RECENT_NUM" : 5,
    "PORT" : 8000,
    "REST_PATTERN": ".(rst|txt)$",
    "IGNORE_FILE": "(DS_Store|Trashes)"
  }


使い方
======
設定ファイルをホームディレクトから読み込みます。
::
   
   % pymamemose &> /dev/null &
   

ライセンス
==========
修正BSDライセンス
