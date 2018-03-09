from urlconnection import soupify
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.set_option('expand_frame_repr', False)
pd.set_option('max_rows', 1500)


class Titanic:
    def __init__(self):
        self.first_class = []
        self.second_class = []
        self.third_class = []
        self.dictionary = {0: self.first_class, 1: self.second_class, 2: self.third_class}

    def fill_boat(self, url):
        soup = soupify(url)
        for class_dept, table in enumerate(soup.find_all('table', limit=3)):
            df = pd.read_html(str(table), header=0)[0]
            class_list = self.dictionary[class_dept]
            for row in df.iterrows():
                class_list.append(Passenger(row[1], class_dept))

    def __repr__(self):
        big_list = [self.first_class, self.second_class, self.third_class]
        return str(big_list)

    def analyze_survival_rate(self, x, y):
        x_axis = np.array([i.references[x] for class_dept in self.dictionary.values() for i in class_dept])
        y_axis = np.array([i.references[y] for class_dept in self.dictionary.values() for i in class_dept])
        colour = np.array(
            ['Blue' if i.references['Survived'] else 'Red' for class_dept in self.dictionary.values() for i in
             class_dept])
        plt.xlabel(x)
        plt.ylabel(y)
        plt.scatter(x_axis, y_axis, c=colour, s=5)
        plt.show()


class Passenger:
    male_prefix = {'Mr', 'Dr', 'Master', 'Sir', 'Colonel', 'Reverend', 'Father', 'Major', 'Captain', 'Don.'}
    female_prefix = {'Ms', 'Mrs', 'Miss', 'Mme.', 'Mlle'}

    def __init__(self, row, class_dept):
        self.last_name = row['Surname']
        self.first_name, self.sex = self.get_sex(row['First Names'])
        self.age = int(row['Age'][:-1]) if 'm' in row['Age'] else None if row['Age'].isalpha() else int(row['Age'])
        self.boarded_location = row['Boarded']
        self.survived = True if row['Survivor (S) or Victim (†)'] == 'S' else False
        self.class_dept = class_dept + 1
        self.references = {
            'Age': self.age,
            'Last Name': self.last_name[0],
            'First Name': self.first_name[0],
            'Location': self.boarded_location,
            'Survived': self.survived,
            'Sex': self.sex,
            'Class': self.class_dept
        }

    @staticmethod
    def get_sex(first_name):
        prefix, real_first_name = first_name.split()[0], ' '.join(first_name.split()[1:])
        prefix = prefix.replace('Â', '')
        if prefix in Passenger.male_prefix:
            return real_first_name, 'Male'
        elif prefix in Passenger.female_prefix:
            return real_first_name, 'Female'
        else:
            return first_name, 'Unknown'

    def __repr__(self):
        return f"Name:{self.first_name} {self.last_name}\n" \
               f"Sex: {self.sex}\n" \
               f"Age:{self.age}\n" \
               f"Boarded Location:{self.boarded_location}\n" \
               f"Survived:{'Yes' if self.survived else 'No'}\n"


titanic = Titanic()
titanic.fill_boat('http://www.titanicfacts.net/titanic-passenger-list.html')
# pprint.pprint(titanic)
titanic.analyze_survival_rate('Age', 'Class')
