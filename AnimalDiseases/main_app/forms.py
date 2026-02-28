from django import forms
from AnimalDiseases.settings import BASE_DIR
import pickle



class AnimalTypeForm(forms.Form):
    """
        Animal type form.
        __init__(*args, **kwargs) is overridden such that it dynamically loads the data for a field when form is instantiated.
        For more information about creating forms and working with them check Django documentation.
    """

    animal_type = forms.ChoiceField(label='Choose animal type:', choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open(str(BASE_DIR.parent) + '/Animal_data/animals_by_number.pkl', 'rb') as file:
            self.animals_by_number = pickle.load(file)

        choices = [(n, a) for a, n in self.animals_by_number.items()]
        self.fields['animal_type'].choices = choices




class SymptomsForm(forms.Form):
    """
        Symptoms form.
        __init__(animal_type, *args, **kwargs) is overridden such that it dynamically loads the data for a field when form is instantiated.
        Method __init__() takes a required parameter 'animal_type' for dynamically loading corresponding data to an animal type.
        For more information about creating forms and working with them check Django documentation.
    """

    breed = forms.ChoiceField(label='Breed', choices=[])
    appetite = forms.ChoiceField(label='Loss of appetite', choices=((0, 'No'), (1, 'Yes')))
    vomiting = forms.ChoiceField(label='Vomiting', choices=((0, 'No'), (1, 'Yes')))
    diarrhea = forms.ChoiceField(label='Diarrhea', choices=((0, 'No'), (1, 'Yes')))
    coughing = forms.ChoiceField(label='Coughing', choices=((0, 'No'), (1, 'Yes')))
    breathing = forms.ChoiceField(label='Labored breathing', choices=((0, 'No'), (1, 'Yes')))
    lameness = forms.ChoiceField(label='Lameness', choices=((0, 'No'), (1, 'Yes')))
    skin = forms.ChoiceField(label='Skin lesions', choices=((0, 'No'), (1, 'Yes')))
    nose = forms.ChoiceField(label='Nasal discharge', choices=((0, 'No'), (1, 'Yes')))
    eyes = forms.ChoiceField(label='Eyes discharge', choices=((0, 'No'), (1, 'Yes')))
    fever = forms.ChoiceField(label='Fever', choices=((0, 'No'), (1, 'Yes')))
    sneezing = forms.ChoiceField(label='Sneezing', choices=((0, 'No'), (1, 'Yes')))
    lethargy = forms.ChoiceField(label='Lethargy', choices=((0, 'No'), (1, 'Yes')))
    w_reduce = forms.ChoiceField(
        label='Wool reduce',
        choices=((0, 'No'), (1, 'Yes')),
        help_text='(Symptom usually appropriate for sheeps, rabbits, etc. If your pet is not one of this just set to "No")'
        )
    swelling = forms.ChoiceField(label='Swelling', choices=((0, 'No'), (1, 'Yes')))
    weight_loss = forms.ChoiceField(label='Weight loss', choices=((0, 'No'), (1, 'Yes')))
    dehydration = forms.ChoiceField(label='Dehydration', choices=((0, 'No'), (1, 'Yes')))
    m_reduce = forms.ChoiceField(
        label='Milk reduce',
        choices=((0, 'No'), (1, 'Yes')),
        help_text='(Symptom usually appropriate for cows, goats, sheeps, etc. If your pet is not one of this just set to "No")',
    )
    heart = forms.IntegerField(label='Heart rate', min_value=50, max_value=200, required=False)

    def __init__(self, animal_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open(str(BASE_DIR.parent) + '/Animal_data/breeds.pkl', 'rb') as a:
            breeds = pickle.load(a)

        self.fields['breed'].choices = breeds[animal_type]
