# Just-rent

- Python 3.10
- MySQL 8.0
- Ubuntu 22.04.3 LTS

## Installation

更新並升級系統套件：

```bash
sudo apt update && sudo apt upgrade
```

創建虛擬環境

```bash
python3 -m venv .venv
```

啟動虛擬環境

```bash
source .venv/bin/activate
```

確認現在位置是否在虛擬環境中

```bash
which pip
```

安裝所有套件

```bash
pip install -r requirements.txt
```

執行資料庫遷移

```bash
flask db upgrade
```

啟動應用程式

```bash
flask run
```
