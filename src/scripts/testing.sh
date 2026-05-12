
cd "$(dirname "$0")/.." || exit
source env/bin/activate
python3 -m pytest tests/ -v