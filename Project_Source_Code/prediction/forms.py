from django import forms


class PredictionForm(forms.Form):
    GENDER_CHOICES = [("female", "Female"), ("male", "Male")]
    ETHNICITY_CHOICES = [
        ("group A", "Group A"),
        ("group B", "Group B"),
        ("group C", "Group C"),
        ("group D", "Group D"),
        ("group E", "Group E"),
    ]
    EDUCATION_CHOICES = [
        ("some high school", "Some High School"),
        ("high school", "High School"),
        ("some college", "Some College"),
        ("associate's degree", "Associate's Degree"),
        ("bachelor's degree", "Bachelor's Degree"),
        ("master's degree", "Master's Degree"),
    ]
    LUNCH_CHOICES = [
        ("standard", "Standard"),
        ("free/reduced", "Free/Reduced"),
    ]
    COURSE_CHOICES = [
        ("none", "None"),
        ("completed", "Completed"),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Gender")
    ethnicity = forms.ChoiceField(choices=ETHNICITY_CHOICES, label="Race/Ethnicity")
    parental_education = forms.ChoiceField(
        choices=EDUCATION_CHOICES, label="Parental Level of Education")
    lunch = forms.ChoiceField(choices=LUNCH_CHOICES, label="Lunch Type")
    test_prep_course = forms.ChoiceField(
        choices=COURSE_CHOICES, label="Test Preparation Course")
    math_score = forms.IntegerField(
        min_value=0, max_value=100, label="Math Score", widget=forms.NumberInput())
    reading_score = forms.IntegerField(
        min_value=0, max_value=100, label="Reading Score", widget=forms.NumberInput())
    writing_score = forms.IntegerField(
        min_value=0, max_value=100, label="Writing Score", widget=forms.NumberInput())