# Advanced Python: Generators, Decorators, and Asynchronous Programming

## Project: Python Generators

This project introduces advanced Python concepts by focusing on the use of generators to efficiently handle large datasets. It demonstrates how to seed a MySQL database and stream data from it using generator functions, which is crucial for memory management in data-intensive applications.

### Folder and File Structure

- `python-generators-0x00/`: The main project directory.
  - `seed.py`: A Python script containing functions to connect to a MySQL database, create a database and table, and insert data from a CSV file.
  - `0-stream_users.py`: A Python script containing a generator function that streams user data from the database one row at a time.
  - `0-main.py`: The entry point for the program that demonstrates the use of the functions in `seed.py`.
  - `user_data.csv`: A sample CSV file containing user data.

### Database Setup and Configuration

The `seed.py` script connects to a MySQL server. You will need to ensure MySQL is installed and running, and configure the user and password in the script. The default script assumes a user `dwaynemaster` and the password stored in the `MYSQL_ROOT_PASSWORD` environment variable.

### How to Run

1.  **Install Dependencies**:
    ```bash
    pip install mysql-connector-python
    ```
2.  **Run the script**:
    ```bash
    ./1-main.py
    ```

This will run the `0-stream_users.py` generator and print the first 6 rows of data, showcasing the memory-efficient streaming.
