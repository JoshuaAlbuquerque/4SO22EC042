# Average Calculator Microservice

This project implements an Average Calculator microservice using Django. The service exposes a REST API that allows clients to request numbers based on qualified IDs and calculates the average of the stored numbers.

## Project Structure

- **src/**: Contains the main application files.
  - **manage.py**: Command-line utility for administrative tasks.
  - **db.sqlite3**: SQLite database file for storing data.
  - **requirements.txt**: Lists project dependencies.
  - **calculator/**: Main Django project directory.
  - **calcapis/**: Application directory for the Average Calculator API.
    - **models.py**: Defines data models for storing fetched numbers.
    - **views.py**: Contains view logic for handling API requests.
    - **urls.py**: URL routing for the API endpoints.
    - **tests.py**: Contains tests for the API functionality.

## Features

- **Qualified Number IDs**: Supports requests for numbers based on the following IDs:
  - `p`: Prime numbers
  - `f`: Fibonacci numbers
  - `e`: Even numbers
  - `r`: Random numbers

- **Window Size**: Configurable window size (default: 10) for storing unique numbers.

- **Average Calculation**: Calculates the average of stored numbers and returns it in the API response.

- **Error Handling**: Ignores responses that take longer than 500 ms or encounter errors.

## Usage

1. **Install Dependencies**: Run `pip install -r requirements.txt` to install the required packages.
2. **Run Migrations**: Execute `python manage.py migrate` to set up the database.
3. **Start the Server**: Use `python manage.py runserver` to start the development server.
4. **Access the API**: Send requests to the endpoint `numbers/{numberid}` to fetch numbers and calculate averages.

## API Endpoint

- **GET /numbers/{numberid}**: Fetch numbers based on the qualified ID and return the stored numbers before and after the latest API call, along with the average.

## Testing

- Use the `tests.py` file to write and run tests for the API functionality to ensure everything works as expected.

## License

This project is licensed under the MIT License.