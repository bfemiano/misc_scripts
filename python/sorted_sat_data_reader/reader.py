from argparse import ArgumentError
import glob

class SatReading():

    def __init__(self, record: str):
        [sid, g_lat, g_lon, reading, ts] = record.strip("\n").split("|")
        self.record = record
        self.sid = sid
        self.g_lat = g_lat
        self.g_lon = g_lon
        self.reading = reading
        self.ts = ts

    def is_lte(self, other) -> bool:
        if not isinstance(other, SatReading):
            raise ArgumentError
        if other.ts > self.ts:
            return True
        return False

    def __str__(self) -> str:
        return self.record

def get_next(gen) -> SatReading:
    try: 
        return next(gen)
    except StopIteration:
        return None

def create_file_reader_map() -> dict:
    readers = {}
    for i, f in enumerate(glob.glob("datfiles/*.dat")):
        def _read(f):
            for line in open(f):
                yield SatReading(line)
        readers[i] = _read(f)
    return readers

def has_more_records(top_item_per_reader: dict):
    return not all(i == None for i in top_item_per_reader.values())

def merge_single_file(readers: dict):
    top_item_per_reader = {i: get_next(readers[i]) for i in readers}
    with open("merged_sat.out", "w") as o_file:
        while(has_more_records(top_item_per_reader)):
            cur_min = None
            cur_min_index = None
            for i, sat_recording in top_item_per_reader.items():
                if cur_min == None:
                    cur_min = sat_recording
                    cur_min_index = i
                elif sat_recording != None and sat_recording.is_lte(cur_min):
                    cur_min = sat_recording
                    cur_min_index = i
            top_item_per_reader[cur_min_index] = get_next(readers[cur_min_index])
            o_file.write(cur_min.record)

def main():
    readers = create_file_reader_map()
    merge_single_file(readers)
    
if __name__ == "__main__":
    main()