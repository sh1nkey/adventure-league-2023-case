from collections import defaultdict

from timetable.models import Day, DAYS_OF_THE_WEEK_CHOICE, PAIR_NUMBER_CHOICE


def get_timetable(user_profile, if_even):
    days_with_subj_times = list(
        Day.objects
        .filter(week__group=user_profile.group, week__even_or_uneven=if_even)
        .prefetch_related('part_of_timetable')
        .values('day_of_the_week', 'part_of_timetable__subject__name', 'part_of_timetable__pair_number')
    )

    day_schedule = defaultdict(list)

    for entry in days_with_subj_times:
        day_of_the_week = DAYS_OF_THE_WEEK_CHOICE[entry['day_of_the_week'] - 1][1]
        subject_name = entry['part_of_timetable__subject__name']
        pair_number = PAIR_NUMBER_CHOICE[entry['part_of_timetable__pair_number'] - 1][1]

        day_schedule[day_of_the_week].append({'subject': subject_name, 'time': pair_number})

    result = []
    for day, subjects in day_schedule.items():
        result.append({
            "day_of_the_week": day,
            "subjects": subjects if subjects else None
        })
    return result