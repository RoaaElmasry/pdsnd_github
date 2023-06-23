import time
import pandas as pd

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input(
        "Please enter the city name:\n Chicago\n New york city\n washington\n "
    ).lower()
    # while loop to avoid any wrong input
    while city not in CITY_DATA.keys():
        print("Ivalid input, please enter a city from the list")

        city = input(
            "Please enter the city name:\n Chicago\n New york city\n washington\n "
        ).lower()

    # get user input for month (all, january, february, ... , june)
    month = input(
        "Please enter a month or all for not filtering by month:\njanuary\nfebruary\nmarch\napril\nmay\njune\nall\n"
    ).lower()
    month_list = ["january", "february", "march", "april", "may", "june", "all"]
    while month not in month_list:
        print(
            "Ivalid input, Please enter a month or all for not filtering by month: january\nfebruary\nmarch\napril\may\njune\all\n"
        )
        month = input(
            "Please enter a month or all for not filtering by month: january\nfebruary\nmarch\napril\nmay\njune\nall\n"
        ).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input(
        "Please enter the day as (Sat, Sun, Mon, Tue, Wed, Thur, Fri) or all for all days\n"
    ).lower()
    day_list = ["sat", "sun", "mon", "tue", "wed", "thur", "fri", "all"]

    while day not in day_list:
        print(
            "Invalid day, please enter the day as (Sat, Mon, Tue, Wed, Thur, Fri) or all for all days"
        )
        day = input(
            "Please enter the day as (Sat, Sun, Mon, Tue, Wed, Thur, Fri) or all for all days\n"
        ).lower()

    print("-" * 40)
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

    # to convert the start time to datetime use to_datetime

    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # to extract the month and the day from the start time use dt.month
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()

    month_list = ["january", "february", "march", "april", "may", "june", "all"]
    # filtering by month and checking not equall all months data
    if month != "all" and month in month_list:
        # converting month name to its order number
        month = month_list.index(month) + 1

        # to check if month equals the input month
        df = df[df["month"] == month]
    # filtering by the day
    day_list = ["sat", "sun", "mon", "tue", "wed", "thur", "fri", "all"]
    if day != "all" and day in day_list:
        df = df[df["day_of_week"].str.startswith(day.title())]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month

    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    common_month = df["month"].mode()[0]

    # display the most common day of week
    df["day_of_week"] = df["Start Time"].dt.day_name()
    common_day = df["day_of_week"].mode()[0]
    # display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    common_hour = df["hour"].mode()[0]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(
        "Most common month is {} \n Most common day is {},\n Most Frequent Start Hour is {} :".format(
            common_month, common_day, common_hour
        )
    )
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df["Start Station"].mode()[0]

    # display most commonly used end station
    common_end_station = df["End Station"].mode()[0]

    # display most frequent combination of start station and end station trip
    # this will make a new column(route) that combines start and end station together
    df["Route"] = df["Start Station"] + " " + df["End Station"]
    common_start_end_station = df["Route"].mode()[0]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(
        "common start station: {}\n common end station: {}\n common start/end station: {}\n".format(
            common_start_station, common_end_station, common_start_end_station
        )
    )
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    totaltravel_time = df["Trip Duration"].sum()
    # to convert seconds to hours:minutes:seconds
    total_travel = time.strftime("%H:%M:%S", time.gmtime(totaltravel_time))

    # display mean travel time
    meantravel_time = df["Trip Duration"].mean()
    # to convert seconds to hours:minutes:seconds
    mean_travel_time = time.strftime("%H:%M:%S", time.gmtime(meantravel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(
        "total time of travel is: {}\nmean time of travel is: {}".format(
            total_travel, mean_travel_time
        )
    )
    print("-" * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()
    print("\nThis took %s seconds." % (time.time() - start_time))
    # Display counts of user types
    # use to_frame() to make it appear better
    users_count = df["User Type"].value_counts().to_frame()
    print("user counts is ", users_count)

    # Display counts of gender
    # for washington (there are some missing data so we do if condition to avoid these gaps)
    try:
        users_gender_count = df["Gender"].value_counts().to_frame()
        print("user gender count are: ", users_gender_count)
        # Display earliest, most recent, and most common year of birth
        earliest_year_birth = df["Birth Year"].min()
        most_recent_year_birth = df["Birth Year"].max()
        most_common_year_birth = df["Birth Year"].mode()[0]

        print("\nEarliest birth year :  ", earliest_year_birth)
        print("\n Most recent year of bith :  ", most_recent_year_birth)
        print("\n Most common year of birth :  ", most_common_year_birth)

    except KeyError:
        print("gender typr is not valid in washington data")

    print("-" * 40)


def display_raw_data(city):
    print("\n Raw data is available to check... \n")
    # asking user to see raw data or not
    display_raw = input("May you want to see raw data? Enter yes or no: ")
    # while loop to specify the need of raw input or not
    while display_raw == "yes":
        try:
            for chunk in pd.read_csv(CITY_DATA[city], chunksize=5):
                print(chunk)
                display_raw = input("\nMay you want to see raw data? Enter yes or no: ")

                if display_raw != "yes":
                    print("Thank you")
                    break
            break

        except KeyboardInterrupt:
            print("Thank you.")


def main():
    while True:
        city, month, day = get_filters()
        print(city, month, day)
        df = load_data(city, month, day)
        print(df.head())
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
