from Crashes import Crashes

import struct

class InvertedList:
    def __init__(self):
        self.index = {}

    def add_item(self, item_id, terms):
        for term in terms:
            if term not in self.index:
                self.index[term] = []
            self.index[term].append(item_id)

    def get_items(self, term):
        return self.index.get(term, [])

    def save_to_file(self, filepath):
        with open(filepath, 'wb') as f:
            for term, postings in self.index.items():
                term_bytes = term.encode('utf-8')
                f.write(struct.pack('I', len(term_bytes)))
                f.write(term_bytes)
                f.write(struct.pack('I', len(postings)))
                for posting in postings:
                    f.write(struct.pack('I', posting))

    @staticmethod
    def from_file(filepath):
        ilist = InvertedList()
        with open(filepath, 'rb') as f:
            while True:
                # read term length
                term_len = f.read(4)
                if not term_len:
                    break
                term_len = struct.unpack('I', term_len)[0]

                # read term
                term = f.read(term_len).decode('utf-8')

                # read number of postings
                num_postings = f.read(4)
                num_postings = struct.unpack('I', num_postings)[0]

                # read postings
                postings = []
                for i in range(num_postings):
                    posting = f.read(4)
                    posting = struct.unpack('I', posting)[0]
                    postings.append(posting)

                # add term to index
                ilist.index[term] = postings

        return ilist


