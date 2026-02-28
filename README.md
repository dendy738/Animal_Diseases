Web application "Animal Diseases"

Application is intended for disease prediction of your pet or farm animals.
During application development animals data with animal parameters and all possible symptoms for each disease were explore.
For disease prediction were used ML algorithms with a partial algorithm transformation of own development.

Using three models for disease prediction:

First model - RandomForest:
    Evaluation:
    
        Accuracy: 0.9733333333333334
        
        Precision: 0.9755434782608695
        
        Recall: 0.9864777432712215
        
        F1 score: 0.9757475314540534
        
        ROC-AUC score: 0.9998847467352806

Second model - KNN:
    Evaluation:
    
        Accuracy: 0.98
        
        Precision: 0.9786588029707296
        
        Recall: 0.9793577981651376
        
        F1 score: 0.9764435789544433
        
        ROC-AUC score: 0.9954470027630216

Third model - DecisionTree:
    Evaluation:
    
        Accuracy: 0.838
        
        Precision: 0.8937613809514636
        
        Recall: 0.9055963988207547
        
        F1 score: 0.8813141338940813
        
        ROC-AUC score: 0.9989510328237392

Three models asynchronously do a prediction and then most popularity disease is selected.

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

Structure:
    Final_project/
    |-Animal_data/   # Folder with a files for loading in the project
        |-animals.pkl
        |-animals_by_number.pkl
        |-breeds.pkl
        |-diseases.pkl
    |-AnimalDiseases/  # Django project
        |-AnimalDiseases/
            |-Files which Django installed by default
            ...
        |-encoders/
            |-pass_encoder.py
        |-login/
            |-Files which Django installed by default
            ...
        |-main_app/
            |-Files which Django installed by default
            ...
        |-regst/
            |-Files which Django installed by default
            ...
        |-statistic/
            |-Files which Django installed by default
            ...
        |-user_statistic/
            |-Files which Django installed by default
            ...
        |-manage.py
    |-DataScience/  # DataScience exploration
        |-animal_data.ipynb
        |-cleaned_animal_disease_prediction.csv
        |-final_variant.ipynb
        |-second_variant_of_animals_data.ipynb
    |-Models/  # Folder with a models
        |-Final_Forest.pkl
        |-Final_KNN.pkl
        |-Final_Tree.pkl
    |-another_transformers.py  # Custom transformers for pipeline (actual)
    |-README.md  # Description of exploitation
    |-requirements.txt  # Dependences
    |-test.py  # Tests
    |-transf_mod.py  # Second version of custom transformers (not used)
    |-transformers.py  # First version of custom transformers (not used)

In order to deploy the application you need:
 - install whole package from GitHub to your local machine;

 - install all necessary libraries:
   
       python -m pip install -r requirements.txt 

 - in the file 'settings.py' which is located in 'Final_project/AnimalDiseases/AnimalDiseases/settings.py' set a connection
to your own DB via the variable 'DATABASES' by set up options or use SQLite3 by default. Also, set the variable 'DEBUG' to True for activating style;

 - run the command  in your shell.

        python manage.py runserver

   By default, Django running all projects across port 8000.
   If port is not accessed:

        python manage.py runserver <available_port_number>

 - open your browser and enter 'http://127.0.0.1:<your_port_number>' 

 - Enjoy it!
