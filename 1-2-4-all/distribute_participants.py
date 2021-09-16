import random
from pprint import pprint
from datetime import datetime, timedelta


PARTICIPANTS = [
    "Participant 1",
    "Participant n"
]


def yield_group_of_four(participants):
    participants = participants
    while participants:
        group = []
        while len(group) < 4:
            try:
                index_range = range(len(participants))
                random_index = random.choice(index_range)
                random_participant = participants.pop(random_index)
                group.append(random_participant)
            except IndexError:
                break
        yield group


if __name__ == '__main__':
    
    print('How should we proceed with IceBerg?')

    print('''
    reference: https://www.liberatingstructures.com/1-1-2-4-all/

    steps:
    - 1min self reflection
    - 2min Share and develop ideas in pairs
    - 4min Share and develop ideas in foursomes 
    ''')

    now = datetime.now()
    reflection = now + timedelta(minutes=1)
    pairs = reflection + timedelta(minutes=2)
    foursomes = pairs + timedelta(minutes=4)
    print(f'REFLECTION until: {reflection.hour}:{reflection.minute}')
    print(f'PAIRS until: {pairs.hour}:{pairs.minute}')
    print(f'FOURSOMES until: {foursomes.hour}:{foursomes.minute}')

    groups = yield_group_of_four(PARTICIPANTS)
    for i, group in enumerate(groups):
        print(f'GROUP {i + 1}:')
        pprint(group)
        print('')
