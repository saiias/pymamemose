=======================================
pymamemose:reStructuredText memo server
=======================================

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

.. sourcecode::
    pip install -e 'git+git://github.com/saiias/pymamemose.git'
