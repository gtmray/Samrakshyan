List all images:
sudo docker images

Build image:
sudo docker build -t samrakshyan .

Remove all images:
sudo docker system prune -a --volumes

Run docker image:
<!-- sudo docker run -it --name sam -p 5000:5000 samrakshyan -->
<!-- sudo docker run -it --name sam -p 8000:8000 samrakshyan -->
<!-- sudo docker run -d -p 8000:80 samrakshyan -->
sudo docker run -p 8000:80 samrakshyan 

Check active containers:
sudo docker ps -a