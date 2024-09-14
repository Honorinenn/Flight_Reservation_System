import requests
from collections import defaultdict, namedtuple

# Define the Flight namedtuple
Flight = namedtuple('Flight', 'OACode DACode passengers seats distance Dcity OCity flightnumer seats_reserved')

class FlightSystem:
    def __init__(self):
        self.flightMap = {}
        self.flightGraph = defaultdict(list)
        self.flight = []
        self.bookings = []
        self.installed = False

    # Function to fetch flight data from Aviation Edge API
    def fetchFlightDataFromAPI(self):
        api_key = "YOUR_API_KEY"  # Replace with your actual API key
        
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError if the status code is 4xx, 5xx
            
            data = response.json()
            
            # Process and integrate this data into the system
            ind = 1  # Starting index for new cities
            
            for flight_data in data:
                oac = flight_data['departure']['iata']
                dac = flight_data['arrival']['iata']
                pa = 0  # Placeholder, as API response does not include passengers
                sea = 0  # Placeholder, as API response does not include seats
                dist = 0  # Placeholder, as API response does not include distance
                dc = flight_data['arrival']['airport']
                oc = flight_data['departure']['airport']
                flight_number = flight_data['flight']['iata']
                seats_reserved = 0  # Placeholder
                
                # Create Flight namedtuple
                flight = Flight(oac, dac, pa, sea, dist, dc, oc, flight_number, seats_reserved)
                self.flight.append(flight)
                
                # Update flightMap with city codes
                if oc not in self.flightMap:
                    self.flightMap[oc] = ind
                    ind += 1
                
                if dc not in self.flightMap:
                    self.flightMap[dc] = ind
                    ind += 1

            print("Flight data successfully fetched and processed.")

        except requests.RequestException as e:
            print(f"An error occurred: {e}")

    # Other methods as defined in your original code...

# Usage
if __name__ == "__main__":
    fs = FlightSystem()
    fs.install()  # This will fetch data from the API and build the graph
    # Proceed with other operations
