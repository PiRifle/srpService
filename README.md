# srpService

srpService is a microservice written in Flask Python that solves the Stable Roommates Problem. It provides a web server using Waitress, allowing users to submit their preferences and obtain matched outputs. This README provides an overview of the project and instructions on how to use and deploy it.

## Installation

To run srpService, follow these steps:

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/PiRifle/srpService.git
   ```

2. Navigate to the project directory:

   ```
   cd srpService
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

To use srpService, follow these instructions:

1. Start the web server by running the following command:

   ```
   python app.py
   ```

   The server will start and listen on port 6530.

2. Submit a POST request to the `/match` endpoint with the preferences JSON file. The `prefs` parameter should contain the preferences in the specified format:

   ```json
   {
       "a": ["b", "c"],
       "b": ["a", "c"],
       "c": ["b", "a"]
   }
   ```

   The server will respond with either "NO FILE" if the preferences file is missing or an output JSON with the matches and rejected participants:

   ```json
   {
       "matches": {
           "a": "b",
           "b": "a"
       },
       "rejected": ["c"]
   }
   ```

   Note that the matched output will only include the participants who have been successfully matched.

## Dockerization

The srpService package can be easily containerized using Docker. To create a Docker image and run the service in a container, follow these steps:

1. Ensure Docker is installed on your system.

2. Build the Docker image by running the following command:

   ```
   docker build -t srp-service .
   ```

   This will create a Docker image named `srp-service` based on the provided Dockerfile.

3. Run the Docker container using the following command:

   ```
   docker run -d -p 6530:6530 srp-service
   ```

   This will start the container and map port 6530 on the host machine to the container's port 6530.

4. You can now access srpService by submitting requests to `http://localhost:6530/match` as described in the "Usage" section.

## Contributing

If you wish to contribute to srpService, please follow the guidelines outlined in the CONTRIBUTING.md file.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the LICENSE file for more details.