台風の発生傾向が似た年探し
=========================

概要
------
台風の発生状況の似た年を出力する。

一方で、台風の発生状況の似た年は、収穫情報も似ているのかを出力する。


扱うトピック
-------------

- jubarecommenderの使い方
- 1つのプログラム内での複数クライアント、複数モデルの使い方


扱うデータ
-------------
- typhoon.csv
    気象庁 気象統計データ http://www.jma.go.jp/jma/menu/report.html
- harvest.csv
    農林水産省 統計情報 http://www.maff.go.jp/j/tokei/index.html

使い方
-------

::

    $ jubarecommender -p 9199 &
    $ jubarecommender -p 9299 &
    $ python typhoo.py


