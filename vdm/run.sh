sudo kill `sudo lsof -t -i:8000`
cd server
python HTTPListener.py
