import struct 
class Crashes:
    def __init__(self, id, date, time, location, operator, flight, route, model, aboard, fatalities):
        self.id = id
        self.date = date if date != "" else "00/00/1990"
        self.time = time if time != "" else "00:00"
        self.location = location if location != "" else "Unknown"
        self.operator = operator if operator != "" else "Unknown"
        self.flight = flight if flight != "" else "Unknown"
        self.route = route if route != "" else "Unknown"
        self.model = model if model != "" else "Unknown"
        self.aboard = int(aboard) if (type(aboard) is str and aboard.isdigit()) or (type(aboard) is int) else -1
        self.fatalities = int(fatalities) if (type(fatalities) is str and fatalities.isdigit()) or (type(fatalities) is int) else -1
    
    # Return the object as a String
    def __str__(self):
        return f"ID: {self.id}\nDate: {self.date}\nTime: {self.time}\nLocation: {self.location}\nOperator: {self.operator}\nFlight: {self.flight}\nRoute: {self.route}\nModel: {self.model}\nAboard: {self.aboard}\nFatalities: {self.fatalities}"
    
    # Return the object as a String same as __str__ but with a different format
    def __repr__(self):
        return f"{self.id}, {self.date}, {self.time}, {self.location}, {self.operator}, {self.flight}, {self.route}, {self.model}, {self.aboard}, {self.fatalities}\n"
    
    # Return the object as a Dictionary    
    def __dict__(self):
        return {'id': self.id, 'date': self.date, 'time': self.time, 'location': self.location, 'operator': self.operator, 'flight': self.flight, 'route': self.route, 'model': self.model, 'aboard': self.aboard, 'fatalities': self.fatalities}
    
        
        
    # Return the size of the object
    def get_size(self):
        return struct.calcsize('?') + struct.calcsize('i') + struct.calcsize('i') + len(self.date.encode('utf-8')) + struct.calcsize('i') + len(self.time.encode('utf-8')) + struct.calcsize('i') + len(self.location.encode('utf-8')) + struct.calcsize('i') + len(self.operator.encode('utf-8')) + struct.calcsize('i') + len(self.flight.encode('utf-8')) + struct.calcsize('i') + len(self.route.encode('utf-8')) + struct.calcsize('i') + len(self.model.encode('utf-8')) + struct.calcsize('i') + struct.calcsize('i')
    
    def get_year(self):
        try:
            return int(self.date[-4:])
        except:
            return -1
        
def save_crashes_to_file(crashes, file_path):
    with open(file_path, 'wb') as f:
        for c in crashes:
            f.write(struct.pack('?', True))
            f.write(struct.pack('i', c.id))
            f.write(struct.pack('i', len(c.date.encode('utf-8'))))
            f.write(c.date.encode())
            f.write(struct.pack('i', len(c.time.encode('utf-8'))))
            f.write(c.time.encode())
            f.write(struct.pack('i', len(c.location.encode('utf-8'))))
            f.write(c.location.encode())
            f.write(struct.pack('i', len(c.operator.encode('utf-8'))))
            f.write(c.operator.encode())
            f.write(struct.pack('i', len(c.flight.encode('utf-8'))))
            f.write(c.flight.encode())
            f.write(struct.pack('i', len(c.route.encode('utf-8'))))
            f.write(c.route.encode())
            f.write(struct.pack('i', len(c.model.encode('utf-8'))))
            f.write(c.model.encode())
            f.write(struct.pack('i', c.aboard))
            f.write(struct.pack('i', c.fatalities))
            

def load_crashes_from_file(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
        crashes = []
        i = 0
        try:
            while i < len(content):
                valid = struct.unpack('?', content[i:i+1])[0]
                i += 1
                id = struct.unpack('i', content[i:i+4])[0]
                i += 4
                date_len = struct.unpack('i', content[i:i+4])[0]
                i += 4
                date = content[i:i+date_len].decode(errors='ignore')
                i += date_len
                time_len = struct.unpack('i', content[i:i+4])[0]
                i += 4
                time = content[i:i+time_len].decode(errors='ignore')
                i += time_len
                location_len = struct.unpack('i', content[i:i+4])[0]
                i += 4
                location = content[i:i+location_len].decode(errors='ignore')
                i += location_len
                operator_len = struct.unpack('i', content[i:i+4])[0]
                i += 4
                operator = content[i:i+operator_len].decode(errors='ignore')
                i += operator_len
                flight_len = struct.unpack('i', content[i:i+4])[0]
                i += 4
                flight = content[i:i+flight_len].decode(errors='ignore')
                i += flight_len
                route_len = struct.unpack('i', content[i:i+4])[0]
                i += 4
                route = content[i:i+route_len].decode(errors='ignore')
                i += route_len
                model_len = struct.unpack('i', content[i:i+4])[0]
                i += 4
                model = content[i:i+model_len].decode(errors='ignore')
                i += model_len
                aboard = struct.unpack('i', content[i:i+4])[0]
                i += 4
                fatalities = struct.unpack('i', content[i:i+4])[0]
                i += 4
                
                c = Crashes(id, date, time, location, operator, flight, route, model, aboard, fatalities)
                if valid:
                    crashes.append(c)
        except:
            pass
        
    return crashes
        
def create_crash(file_path, new_crash):
    crashes = load_crashes_from_file(file_path)
    crashes.append(new_crash)
    save_crashes_to_file(crashes, file_path)

def read_crash(file_path, id):
    crashes = load_crashes_from_file(file_path)
    for c in crashes:
        if c.id == id:
            return c
    return None


def update_crash(file_path, id, new_crash):
    crashes = load_crashes_from_file(file_path)
    for c in crashes:
        if c.id == id:
            c.date = new_crash.date
            c.time = new_crash.time
            c.location = new_crash.location
            c.operator = new_crash.operator
            c.flight = new_crash.flight
            c.route = new_crash.route
            c.model = new_crash.model
            c.aboard = new_crash.aboard
            c.fatalities = new_crash.fatalities
            save_crashes_to_file(crashes, file_path)
            return

def delete_crash(file_path, id):
    crashes = load_crashes_from_file(file_path)
    for c in crashes:
        if c.id == id:
            crashes.remove(c)
            save_crashes_to_file(crashes, file_path)
            return