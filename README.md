# 動物実験管理システム Yammane
Your advanced manager for merciful animals necessary for experiments  

動物実験を適正に実施し、また実験を行う側、管理する側、また審査する側の便宜を図り、動物実験管理システムのオープンソース開発を進めています。

<img src="static/logo.png" alt="Yammane" width="400">

## 検証中の実行環境
- Linux 3.10.0
- CentOS 7.9.2009
- Python 3.10.0
- Conda 23.1.0
- Flask 2.2.3
- uWSGI 2.0.21
- Nginx 1.22.1
- SQLAlchemy 2.0.4
- MariaDB 10.10.2

## 発表
### 動物実験管理システムのオープンソース開発
岡村 峻平*, 進導 美幸, 青砥 早希, 黒木 陽子, 岡村 浩司  
第70回日本実験動物学会総会 口頭発表IV O-38 (つくば国際会議場, 2023-05-24)

## 履歴
2023-04-06 GitHub リポジトリ 作成  
2023-05-24 第70回日本実験動物学会総会 発表  
2023-06-24 コミュニティ開発 開始予定  

## 英文概要
For animal experiments, each research institute must create a committee and regulations to supervise their experiment plans. They usually rely on expensive outsourced software to handle the amount and complexity of the pertinent information. Its maintenance cost is also a burden because updates are frequently required. Since attacks on medical information systems with ransomware or other malware have been increasing, there are concerns about employing such proprietary software. Here, researchers and administrative staff involving animal experiments have formed a team to develop our own management system with open-source software, namely, Linux, Apache, MariaDB, and Python. Because the system was designed as a web service based on the framework Flask and SQLAlchemy on the LAMP environment, it can be used in any client environment, including Linux and Windows, as well as smartphones, without the need to install any additional software. Its specification and documentation on installation and handling are also available, allowing users to operate and maintain it as an administrator. We continue to develop the system at the community level by releasing it to the public, especially in terms of security, as well as providing a support system for users, with the goal of making the system widely used in this country.
