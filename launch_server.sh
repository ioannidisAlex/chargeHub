cd backend
source ./.venv/bin/activate
sudo python manage.py runsslserver 8765 --certificate /home/mikeg/TL_data/localhost.crt --key /home/mikeg/TL_data/localhost.key && deactivate && cd ..

