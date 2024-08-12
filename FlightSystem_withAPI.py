import requests
import random
import time
from collections import defaultdict, namedtuple
import heapq


Flight = namedtuple('Flight', 'OACode DACode passengers seats distance Dcity OCity flightnumer seats_reserved')
Booking = namedtuple('Booking', 'booked_under booking_id num_seats distance cost flightsTaken password bookingTimeAndDate probability_of_delay')

class FlightSystem:
    def __init__(self):
        self.flightMap = {}
        self.flightGraph = defaultdict(list)
        self.flight = []
        self.bookings = []
        self.installed = False

    def check_key(self, key):
        return key in self.flightMap

    def checkCityExists(self, city):
        return self.check_key(city)

    def notInstalledError(self):
        print("Critical Error: Flight Data Not Installed")

    def trimalpha(self, s):
        return ''.join(filter(str.isalpha, s))

    def fetchFlightDataFromAPI(self):
        api_key = "YOUR_API_KEY"  # Replace with your actual API key
        url = f"https://aviation-edge.com/v2/public/flights?key={api_key}&arr_iata=JFK&dep_iata=LAX"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError if the status code is 4xx, 5xx
            
            data = response.json()
            
            # Print the data to inspect its structure
            print("API Response Data:", data)
            
            ind = 1  # Starting index for new cities
            
            # Assuming the data is a list of flight dictionaries
            if isinstance(data, list):
                for flight_data in data:
                    if not isinstance(flight_data, dict):
                        print("Unexpected data format:", flight_data)
                        continue
                    
                    # Print flight_data to debug
                    print("Processing flight data:", flight_data)
                    
                    try:
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

                    except KeyError as e:
                        print(f"Missing expected key: {e}")
                        continue

                print("Flight data successfully fetched and processed.")

            else:
                print("Unexpected API response format.")

        except requests.RequestException as e:
            print(f"An error occurred: {e}")

    def buildGraph(self):
        for flight in self.flight:
            originIndex = self.flightMap[flight.OCity]
            destinationIndex = self.flightMap[flight.Dcity]
            probability = random.uniform(0, 1)  # Example: Random probability of delay
            self.flightGraph[originIndex].append((flight.distance, destinationIndex, flight.flightnumer, probability))

    def calculateCost(self, distance):
        baseFare = 50
        totalFare = (distance + 1) // 2 + baseFare
        return totalFare

    def install(self):
        if self.installed:
            print("Flight Data Already Installed")
            return
        self.installed = True
        print("Installing Flight Data....")
        self.fetchFlightDataFromAPI()
        self.buildGraph()
        print("Flight Data Successfully Installed!")

    def Dijkstra(self, source, destination):
        pq = []
        dist = [float('inf')] * (len(self.flightMap) + 1)
        vis = [False] * (len(self.flightMap) + 1)
        parent = [-1] * (len(self.flightMap) + 1)
        path = [-1] * (len(self.flightMap) + 1)
        dist[source] = 0
        heapq.heappush(pq, (0, source))

        while pq:
            currw, currv = heapq.heappop(pq)
            if vis[currv]:
                continue
            vis[currv] = True

            for nextw, nextv, nextfin, _ in self.flightGraph[currv]:
                if vis[nextv]:
                    continue

                newWeight = currw + nextw
                if newWeight < dist[nextv]:
                    dist[nextv] = newWeight
                    parent[nextv] = currv
                    path[nextv] = nextfin
                    heapq.heappush(pq, (newWeight, nextv))

        pathTaken = []
        if dist[destination] == float('inf'):
            return pathTaken

        i = destination
        while i != source:
            pathTaken.append(path[i])
            i = parent[i]
        pathTaken.reverse()
        return pathTaken

    def reserveSeats(self):
        if not self.installed:
            self.notInstalledError()
            return
        
        originCity = input("Enter Origin City: ").strip().upper()
        if not self.checkCityExists(originCity):
            print("Entered City doesn't exist!!")
            if input("Enter 1 to retry booking or any other key to Exit: ") == "1":
                return self.reserveSeats()
            return

        destinationCity = input("Enter Destination City: ").strip().upper()
        if not self.checkCityExists(destinationCity):
            print("Entered Destination City doesn't exist!!")
            if input("Enter 1 to retry booking or any other key to Exit: ") == "1":
                return self.reserveSeats()
            return

        path = self.Dijkstra(self.flightMap[originCity], self.flightMap[destinationCity])
        if not path:
            print(f"Sorry there is no flight connecting {originCity} and {destinationCity}")
            if input("Enter 1 to retry booking seats or any other key to Exit: ") == "1":
                return self.reserveSeats()
            return

        print(f"You will have to take {len(path)} flight(s) to reach your destination:")

        totalDistance = 0
        for i in path:
            print(f"From {self.flight[i].OCity} to {self.flight[i].Dcity}")
            totalDistance += self.flight[i].distance
            print("then")

        print("You will reach your destination")
        costFlight = self.calculateCost(totalDistance)
        print(f"The total sum you will have to pay is {costFlight} $")
        print(f"You will have travelled {totalDistance} miles")

        reqseats = int(input("Enter number of Required Seats: "))
        counter = 0

        for i in path:
            if reqseats > self.flight[i].seats - self.flight[i].seats_reserved:
                print(f"Sorry The Flight {self.flight[i].OCity} to {self.flight[i].Dcity} has Only {self.flight[i].seats - self.flight[i].seats_reserved} seats available")
                counter = 1

        if counter:
            if input("Enter 1 to retry or any other key to Exit: ") == "1":
                return self.reserveSeats()
            return

        for i in path:
            self.flight[i] = self.flight[i]._replace(seats_reserved=self.flight[i].seats_reserved + reqseats)

        pword = ''.join(random.choices('0123456789!@#$%^&*abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=8))
        book = Booking(
            booked_under=input("Enter Booking Name: "),
            booking_id=len(self.bookings),
            num_seats=reqseats,
            distance=totalDistance,
            cost=costFlight,
            flightsTaken=path,
            password=pword,
            bookingTimeAndDate=time.ctime()
        )

        self.bookings.append(book)
        print(f"Booking Successful!!")
        print(f"Your booking id is: {book.booking_id}")
        print(f"Your password is: {pword}")
        print("Please remember these for future reference")

    def authenticate(self):
        bookid = int(input("Enter your booking id: "))
        passwd = input("Enter your password: ")

        if bookid >= len(self.bookings):
            print("Your Booking ID is incorrect!!")
            return -1

        if passwd != self.bookings[bookid].password:
            print("Your Password is incorrect!!")
            return -1

        print("Successfully Logged in!!!!")
        return bookid

    def cancellation(self):
        authKey = self.authenticate()
        if authKey != -1:
            if input("Press 1 to confirm your cancellation: ") == "1":
                print(f"Your ticket has been cancelled and your money {self.bookings[authKey].cost - 100} has been added to your account after deducting cancellation amount")
                for i in self.bookings[authKey].flightsTaken:
                    self.flight[i] = self.flight[i]._replace(seats_reserved=self.flight[i].seats_reserved - self.bookings[authKey].num_seats)

    def showBooking(self):
        if not self.installed:
            self.notInstalledError()
            return

        authKey = self.authenticate()
        if authKey != -1:
            booking = self.bookings[authKey]
            print(f"Your Booking Id is: {authKey}")
            print(f"Your journey is booked under the name: {booking.booked_under}")
            print(f"The number of seats you have reserved are: {booking.num_seats}")
            print(f"The number of flights you will be taking is {len(booking.flightsTaken)} namely:")
            for i in booking.flightsTaken:
                print(f"From {self.flight[i].OCity} to {self.flight[i].Dcity}")
                print("then")
            print("You will reach your destination")
            print(f"Your Journey will be of {booking.distance} miles")
            print(f"The total money you have paid is {booking.cost} USD")

if __name__ == "__main__":
    fs = FlightSystem()
    fs.install()  # This will fetch data from the API and build the graph
    while True:
        print("\nOptions:")
        print("1. Reserve Seats")
        print("2. Cancel Booking")
        print("3. Show Booking")
        print("4. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            fs.reserveSeats()
        elif choice == "2":
            fs.cancellation()
        elif choice == "3":
            fs.showBooking()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")
