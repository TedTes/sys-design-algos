python
import bisect
import hashlib


class ConsistentHashRing:

    def __init__(self, vnodes=200):
        self.vnodes = vnodes  # Number of points per physical server
        self.ring = []  # Sorted list of hashes: [hash1, hash2, ...]
        self.nodes = {}  # Map: {hash: physical_server_id}

    def add_server(self, server_id):
        """Adds a physical server by placing its virtual nodes on the ring."""
        for i in range(self.vnodes):
            # Create a unique string for each virtual node
            vnode_id = f"{server_id}#{i}"

            # Hash it to get a massive integer
            vnode_hash = int(
                hashlib.md5(vnode_id.encode()).hexdigest(), 16
            )  # Base 16 to base 10

            # Map the hash to the physical server
            self.nodes[vnode_hash] = server_id
            bisect.insort(self.ring, vnode_hash)  # Keeps self.ring sorted

    def get_server(self, key):
        """Finds the physical server for a given data key."""
        if not self.ring:
            return None

        # Hash the key
        key_hash = int(hashlib.md5(key.encode()).hexdigest(), 16)

        # Binary search for the first server hash >= key_hash
        idx = bisect.bisect_left(self.ring, key_hash)

        # Wrap around to the beginning if we reached the end
        if idx == len(self.ring):
            idx = 0

        # Look up the physical server mapped to that virtual hash
        target_vnode_hash = self.ring[idx]
        return self.nodes[target_vnode_hash]


# --- Usage ---
ring = ConsistentHashRing(vnodes=200)
ring.add_server("Server_A")
ring.add_server("Server_B")
ring.add_server("Server_C")

print(ring.get_server("sess_79879"))  # Returns the physical server ID