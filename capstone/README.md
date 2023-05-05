#  CS50W Capstone project - Heresy Builder

Heresy Builder is a project for Harvard CS50W where the user can create army lists for the Games Workshop game Horus Heresy. I decided to go with this as it tied in with my personal hobby interests. It only contains a few unit entries for the game but more can be added should the user wish. It also lets the user calculate how much average damage each unit in their list will do on the table top. Due to the nature of the source material there are no apps that allow you to create a list and the information in this app is public. This app allows me as the user to input additional units as I see fit to create a list.

I tried to use everything I learnt in this course and previous CS50 courses, HTML, Bootstrap, JS, Python and Django. 

### Distinctiveness and Complexity

I believe this app to be quite different from the other course apps as it provides a different function. Its meant to help the user prepare and evaluate the choices they make before playing a game of Horus Heresy. Users can see the realistic damage output of a unit without having to do the math themseleves. It also helps as a in game reference so the user does not have to have printed lists or as an aid to make an in game choice. For complexity this app has a lot of interactions with app and user data to correctly calculate results and change the page without refreshing. 


## Templates folder

The website uses layout.html file as the base. Register/login/logout.html allow the user to create an account, sign in and out of the website and index.html describes the basic functions of the site.

Builder.html is split into two columns. Right side displays all the units currently implmented in the app split into the appropriate catagories. Users can click on the tabs to show or hide force organisation slots or each unit. The left side shows all units and equipment added to the army list and allows the user to change list name and finally submit. The list name is checked on change to make sure the user does not have two identical list names

Listview.html displays all user created lists ordered by how recent they are and on selection displays all units on the right side. 

Damagepage.html is where the user can check on the average damage from their units. The user has to first select one of their lists and a unit from it. Then they can select a target unit which is a list of all possible units currently implmeneted in the app. This will then show the average damage for every equiped weapon the unit has. This calculation is triggered if the user changes the list unit or target unit. 

## Static folder

Styles.css contains a small amount of CSS to animate the show/hiding of list tabs in the builder.thml

Script.js has a lot of functions to fetch data and change the html of the current page without reloading. On completion of this project I would have prefered this file was smaller now that I have a better understanding of the data type and format being passed around and standardizing how I used json. 

## Python

Views.py handles most of the work but I seperated the damage calculations into a calculations.py which uses the Fractions library as the game is played with 6-sided dice. 

## How to run

pip install Fraction
python manage.py makemigrations
python manage.py migrate
python manage.py runserver


