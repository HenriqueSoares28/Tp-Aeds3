import pickle
import struct

from Crashes import Crashes

# Bucket size
BUCKET_SZ = 500

class Bucket:
    def __init__(self) -> None:
        self.map = []
        self.local_depth = 0

    def full(self) -> bool:
        return len(self.map) >= BUCKET_SZ

    def put(self, k, v) -> None:
        for i, (key, value) in enumerate(self.map):
            if key == k:
                del self.map[i]
                break
        self.map.append((k, v))

    def get(self, k):
        for key, value in self.map:
            if key == k:
                return value

    def get_local_high_bit(self):
      return 1 << self.local_depth

# Extendible hashing implementation
class ExtendibleHashing:
    def __init__(self) -> None:
        self.global_depth = 0
        self.directory = [Bucket()]

    # Get the bucket
    def get_bucket(self, k):
        h = hash(k)
        return self.directory[h & ((1 << self.global_depth) - 1)]

    def put(self, k, v) -> None:
        p = self.get_bucket(k)
        full = p.full()
        p.put(k, v)
        if full:
            if p.local_depth == self.global_depth:
                self.directory *= 2
                self.global_depth += 1

            p0 = Bucket()
            p1 = Bucket()
            p0.local_depth = p1.local_depth = p.local_depth + 1
            high_bit = p.get_local_high_bit()
            for k2, v2 in p.map:
                h = hash(k2)
                new_p = p1 if h & high_bit else p0
                new_p.put(k2, v2)

            for i in range(hash(k) & (high_bit - 1), len(self.directory), high_bit):
                self.directory[i] = p1 if i & high_bit else p0

    # List the hash directory
    def list_hash_directory(self):
        directory = self.directory
        hash_directory = []
        for i, bucket in enumerate(directory):
            bucket_map = bucket.map
            local_depth = bucket.local_depth
            hash_directory.append((i, bucket_map, local_depth))
        return hash_directory

    # get the value 
    def get(self, k):
        return self.get_bucket(k).get(k)
    
# read the hash table
def load_hash(dir):
    with open(dir, "rb") as file:
        return pickle.load(file)

# Save the hash table
def save_hash(hash_table, dir):
    with open(dir, "wb") as file:
        pickle.dump(hash_table, file)

# Read the hash file and return the value
def read_hash(file_path, hash_file_path, id):
    position = load_hash(hash_file_path).get(id)
    with open(file_path, 'rb') as f:
        content = f.read()
        i = position
        try:
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
                return(c)
            else:
                return None
        except:
            pass