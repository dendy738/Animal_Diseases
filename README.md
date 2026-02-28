Web application "Animal Diseases"

Application is intended for disease prediction of your pet or farm animals.
During application development animals data with animal parameters and all possible symptoms for each disease were explore.
For disease prediction were used ML algorithms with a partial algorithm transformation of own development.

Animal list for which disease can be predicted is following:
 - Dog;
 - Cat;
 - Cow;
 - Pig;
 - Rabbit;
 - Goat;
 - Sheep;
 - Horse;

Also, you can look at general disease statistic for each animal dependent on animal feature and your own statistic of activity.

In order to deploy the application you need:
 - install whole package from GitHub to your local machine;

 - activate venv in the root:
    Windows command:
    [ ./final/Scripts/Activate.ps1 ] - for PowerShell
    [ ./final/Scripts/activate.bat ] - for cmd

 - install all necessary libraries:
    [ python -m pip install -r requirements.txt ]

 - in the file 'settings.py' which is located in 'Final_project/AnimalDiseases/AnimalDiseases/settings.py' set a connection
to your own DB via the variable 'DATABASES' by set up options;

 - run the command [ python manage.py runserver ] in your shell. By default, Django running all projects across port 8000.
If port is not accessed - [ python manage.py runserver <available_port_number> ];

 - open your browser and enter 'http://127.0.0.1:<your_port_number>' 

 - Enjoy it!
