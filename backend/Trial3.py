import csv
import os
import random
import time
from collections import defaultdict, namedtuple
import heapq

# Define namedtuples for Flight and Booking
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
        raise Exception("Critical Error: Flight Data Not Installed")

    def trimalpha(self, s):
        return ''.join(filter(str.isalpha, s))

    def read_record(self):
        try:
            with open("out.csv", "r") as fp:
                reader = csv.reader(fp)
                next(reader)  # Skip header if there is one
                
                ind = 1
                for i, row in enumerate(reader):
                    if len(row) != 7:
                        continue  # Skip invalid rows
                    oac, dac, pa, sea, dist, dc, oc = row
                    oc = self.trimalpha(oc)
                    dc = self.trimalpha(dc)
                    
                    flight = Flight(oac, dac, int(pa), int(sea), int(dist), dc, oc, i, int(pa))
                    self.flight.append(flight)

                    if not self.check_key(oc):
                        self.flightMap[oc] = ind
                        ind += 1

                    if not self.check_key(dc):
                        self.flightMap[dc] = ind
                        ind += 1

        except FileNotFoundError:
            raise FileNotFoundError("File 'out.csv' not found!")

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
            return "Flight Data Already Installed"
        self.installed = True
        self.read_record()
        self.buildGraph()
        return "Flight Data Installed Successfully"

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

    def reserveSeats(self, originCity, destinationCity, reqseats, booked_under):
        if not self.installed:
            self.notInstalledError()

        if not self.checkCityExists(originCity):
            return "Entered City doesn't exist!!"

        if not self.checkCityExists(destinationCity):
            return "Entered Destination City doesn't exist!!"

        path = self.Dijkstra(self.flightMap[originCity], self.flightMap[destinationCity])
        if not path:
            return f"Sorry there is no flight connecting {originCity} and {destinationCity}"

        totalDistance = 0
        for i in path:
            totalDistance += self.flight[i].distance

        costFlight = self.calculateCost(totalDistance)

        counter = 0
        for i in path:
            if reqseats > self.flight[i].seats - self.flight[i].seats_reserved:
                return f"Sorry The Flight {self.flight[i].OCity} to {self.flight[i].Dcity} has Only {self.flight[i].seats - self.flight[i].seats_reserved} seats available"

        for i in path:
            self.flight[i] = self.flight[i]._replace(seats_reserved=self.flight[i].seats_reserved + reqseats)

        pword = ''.join(random.choices('0123456789!@#$%^&*abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=8))

        book = Booking(
            booked_under=booked_under,
            booking_id=len(self.bookings),
            num_seats=reqseats,
            distance=totalDistance,
            cost=costFlight,
            flightsTaken=path,
            password=pword,
            bookingTimeAndDate=time.ctime(),
            probability_of_delay=random.uniform(0, 1)
        )

        self.bookings.append(book)
        return {
            "message": "Booking Successful!!",
            "booking_id": book.booking_id,
            "password": pword
        }

    def authenticate(self, bookid, passwd):
        if bookid >= len(self.bookings):
            return -1

        if passwd != self.bookings[bookid].password:
            return -1

        return bookid

    def cancellation(self, bookid, passwd):
        authKey = self.authenticate(bookid, passwd)
        if authKey != -1:
            self.bookings[authKey].cost -= 100
            for i in self.bookings[authKey].flightsTaken:
                self.flight[i] = self.flight[i]._replace(seats_reserved=self.flight[i].seats_reserved - self.bookings[authKey].num_seats)
            return f"Your ticket has been cancelled and {self.bookings[authKey].cost} has been added to your account after deducting cancellation amount"
        return "Authentication failed"

    def showBooking(self, bookid, passwd):
        authKey = self.authenticate(bookid, passwd)
        if authKey != -1:
            booking = self.bookings[authKey]
            flight_details = []
            for i in booking.flightsTaken:
                flight_details.append({
                    "from": self.flight[i].OCity,
                    "to": self.flight[i].Dcity
                })
            return {
                "booking_id": authKey,
                "booked_under": booking.booked_under,
                "num_seats": booking.num_seats,
                "flights": flight_details,
                "distance": booking.distance,
                "cost": booking.cost
            }
        return "Authentication failed"
