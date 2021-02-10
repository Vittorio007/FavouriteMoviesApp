# FavouriteMoviesApp

### About Application  

Application where you can open account and create a list of your favourite movies, serials and games.  
All you can search by search engine which takes data from API site http://www.omdbapi.com/.  
You can also see more interesting details of every movie or delete movie from the favourite list.  
Of course when you want to, you can delete your account from data base.

### How to use it  
If you want to only check my app once you can use my key password (go to 3 point). 
If you want to use more times please create your own password.

1. First you have to go to site http://www.omdbapi.com/ and create a free account to take apikey which will be 
   sent to your mail.
2. Next is to go to main directory and put password in "Dockerfile" <code>ENV APIKEY='<your_password>'</code>
3. Finally, open terminal in directory where you saved this project:
   
   3.1 Create Docker container by writing <code>docker build -t <your_name_of_container> .</code>
   
   3.2 Run Project <code>docker run -p 5000:5000 <your_name_of_container></code>   

HAVE FUN !

