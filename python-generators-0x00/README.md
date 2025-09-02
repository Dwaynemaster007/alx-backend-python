# Advanced Python: Generators, Decorators, and Asynchronous Programming

## Project: Python Generators

This project introduces advanced Python concepts by focusing on the use of generators to efficiently handle large datasets. It demonstrates how to seed a MySQL database and stream data from it in memory-efficient batches.

### Folder and File Structure

- `python-generators-0x00/`: The main project directory.
  - `seed.py`: A Python script to set up a MySQL database and insert data from a CSV file.
  - `0-stream_users.py`: A Python script containing a generator function that streams user data one row at a time.
  - `1-batch_processing.py`: A Python script with generator functions for fetching and processing data in memory-efficient batches.
  - `0-main.py`: A main script to demonstrate the `seed.py` functionality.
  - `1-main.py`: A main script to demonstrate the `0-stream_users.py` generator.
  - `2-main.py`: A main script to demonstrate the `1-batch_processing.py` functionality.
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
3.  **Run the batch processing script**:
    ```bash
    ./2-main.py
    ```

This will run the `batch_processing` generator in `1-batch_processing.py`, which fetches and processes users in batches of 50, and prints the filtered results.
