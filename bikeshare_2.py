import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['all','january','february','march','april','may','june']
days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    month = None
    day = None
    city = None
    while city not in (CITY_DATA.keys()):
        city = input('Please choose a city from "chicago","new york city","washington": ').lower()

    # get user input for month (all, january, february, ... , june)
    while month not in months:
        try:
            month = input('\nPlease enter a month to filter by between january and june or enter "all" to not filter by month: ').lower()
        except:
            print('Please enter a valid input')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in days:
        try:
            day = input('\nPlease enter a day to filter by or enter "all" to skip filtering by days: ').lower()
        except:
            print('Please enter a valid input')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    if month != 'all':
        df = df[df['month'] == months.index(month)]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month is: ',months[df['month'].mode()[0]])

    # display the most common day of week
    print('Most common day of the week is: ',days[df['day_of_week'].mode()[0]])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('Most common hour is: ', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common start station is: ',df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most common end station is: ',df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('Most frequent combination of start and end station trips is:\n',
    df.groupby(['Start Station', 'End Station']).size().nlargest(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time is: ',df['Trip Duration'].sum())

    # display mean travel time
    print('Mean Travel Time is:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types:\n',df['User Type'].value_counts())

    # Display counts of gender
    if city != 'washington':
        print('Counts of gender:\n',df['Gender'].value_counts())
    # Display earliest, most recent, and most common year of birth
        print('Earliest year of birth is: ', int(df['Birth Year'].min()))
        print('Most recent year of birth is: ', int(df['Birth Year'].max()))
        print('Most common year of birth is: ', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def show_raw_data(city):
    df = pd.read_csv(CITY_DATA[city])
    user_input = 'yes'
    start_index = 0
    increment = 6
    while user_input == 'yes':
        print(df.iloc[start_index:start_index+increment, 0:])
        user_input = input('Would you like to see aditional rows from raw data?(yes/no): ').lower()
        if user_input != 'yes':
            break
        start_index+=increment


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if not df.empty:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df,city)
            show_raw_data(city)
        else:
            print('Empty data frame for selected city/month/day combination.')
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
