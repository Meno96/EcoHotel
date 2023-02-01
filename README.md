<h1 align="center">
    Pomelia EcoHotel
</h1>

This repo shows how to create a blockchain-based tracking system of consumption and energy produced by photovoltaic panels via a web application.

This system shall receive, at a specified endpoint, POST requests in JSON in the following format: 

    {
        ‘produced_energy_in_watt’: 121293434,
        ‘consumed_energy_in_watt’: 239293
    }
    
These requests will then be displayed in table form in the web application and a transaction will be made on Ethereum Goerli containing the two values.

<hr/>

## 🛠️&nbsp; How to run
- Clone the repo
- Create and activate virtual enviroment
- Install requirements: --> 
    ```
    pip install -r requirements.txt
    ```
- Make database migrations: --> 
    ```
    python manage.py makemigrations
    ``` 
    ```
    python manage.py migrate
    ```
- Run server: --> 
    ```
    python manage.py runserver
    ```
- Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser
- Log in with the following credentials to access all features: 

    Username: `admin`
    
    password: `admin`

## 🗎&nbsp; Requirements
- Main page, accessible only by logged in users, where to show the table containing the values in question and the hash of the transaction.

- A page, to which only administrators can access, where it is possible to see the total consumed and produced.

- A logging system to memorize the last IP that accessed the platform for a certain administrator user, in order to show a warning message when this is different from      the previous one.

## 🚀&nbsp; How it's suppose to work?
Once logged in with the admin user you are on this page:

<p align="center">
    <img width="80%" src="./assets/GitHubImages/screen1.png" alt="Homepage">
</p>

### Produced And Consumed Energy Table
If we enter the first link we can see the table with the relative data of energy produced and energy consumed:

<p align="center">
    <img width="80%" src="./assets/GitHubImages/screen2.png" alt="Homepage">
</p>

This data is extracted from an SQL database which is populated when a transaction is sent to the Goerli blockchain.

By clicking on the hash of the transaction, you are redirected to Goerli's Etherscan where you can see all the details of the transaction.


