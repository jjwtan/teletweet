echo 'starting db service...'

bash /home/pi/projects/twitter/scripts/start_db_service.sh

sleep 5

echo 'starting teletweet...'
bash /home/pi/projects/twitter/scripts/start_teletweet.sh

