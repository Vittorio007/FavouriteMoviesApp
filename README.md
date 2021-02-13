# FavouriteMoviesApp

### About Application  

Application where you can open account and create a list of your favourite movies, serials and games.  
All you can search by search engine which takes data from API site http://www.omdbapi.com/.  
You can also see more interesting details of every movie or delete movie from the favourite list.  
Of course when you want to, you can delete your account from data base.

### How to open it by Docker

If you want to open it by Docker you need to have Docker installed at your PC.

At https://www.docker.com/get-started you have all information how to install Docker. 

Then, if you have Docker installed:

If you want to only check my app once you can use my key password (go to 3 point). 
If you want to use more times, please create your own password.

1. First you have to go to site http://www.omdbapi.com/ and create a free account to take apikey which will be 
   sent to your mail.
2. Next is to go to main directory and put password in "Dockerfile" <code>ENV APIKEY='<your_password>'</code>
3. Finally, open terminal in directory where you saved this project:
   
   3.1 Go to directory '/docker_base'. Create Docker Base Image by writing <code>docker build -t docker_base_image .</code>
      - This image contains all base dependencies of project. Thanks to that there will be no need install all requirements after change something in main app file. 
   
   3.2 Go to main directory of project. Create Docker App Image by writing <code>docker build -t <your_name_of_app_image> .</code>
   
   3.3 Run project/create app container <code>docker run -p 5000:5000 <your_name_of_app_image></code>   

HAVE FUN !

