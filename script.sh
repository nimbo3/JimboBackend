read -p 'enter username: ' username
read -p 'enter server address: ' address
read -p 'enter server ssh port: ' port
echo connecting to server:
ssh $username@$address -p $port << EOF
  cd ~/website/
  source venv/bin/activate
  screen -X -S Joojle quit
  cd backend/
  git stash
  git pull origin master
  python3 manage.py makemigrations
  python3 manage.py migrate
  cd ../frontend
  git stash
  git pull origin master
  cd ..
  screen -dmS -S Joojle sudo docker-compose up
  logout
EOF