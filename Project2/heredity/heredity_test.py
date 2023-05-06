from heredity import *


def joint_probability_test():
    people = {
        'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
        'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
        'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
    }
    print(joint_probability(people, {"Harry"}, {"James"}, {"James"}))


joint_probability_test()
