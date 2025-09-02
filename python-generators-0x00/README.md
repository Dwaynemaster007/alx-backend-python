# Advanced Python: Generators, Decorators, and Asynchronous Programming

## Project: Python Generators

This project introduces advanced Python concepts by focusing on the use of generators to efficiently handle large datasets. It demonstrates how to seed a MySQL database, stream data from it in memory-efficient batches and pages, and perform aggregations without loading all data into memory.

### Folder and File Structure

- `python-generators-0x00/`: The main project directory.
  - `seed.py`: A Python script to set up a MySQL database and insert data from a CSV file.
  - `0-stream_users.py`: A Python script containing a generator function that streams user data one row at a time.
  - `1-batch_processing.py`: A Python script with generator functions for fetching and processing data in memory-efficient batches.
  - `2-lazy_paginate.py`: A Python script containing a generator function that fetches data in lazily loaded pages.
  - `4-stream_ages.py`: A script that uses a generator to compute the average age of users without loading the entire dataset into memory.
  - `0-main.py`, `1-main.py`, `2-main.py`, `3-main.py`: Main scripts to demonstrate the functionalities.
  - `user_data.csv`: A sample CSV file containing user data.

### Database Setup and Configuration

The `seed.py` script connects to a MySQL server. You will need to ensure MySQL is installed and running, and configure the user and password in the script.

### How to Run

1.  **Install Dependencies**:
    ```bash
    pip install mysql-connector-python
    ```
2.  **Ensure Database is Populated**:
    Run `0-main.py` once to set up the database and insert data.
    ```bash
    ./0-main.py
    ```
3.  **Run the average age calculation script**:
    ```bash
    ./4-stream_ages.py
    ```

This will run the `calculate_average_age` function, which uses the `stream_user_ages` generator to compute and print the average age.
