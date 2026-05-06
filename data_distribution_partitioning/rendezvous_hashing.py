import hashlib


class RendezvousHashing:
    def __init__(self, servers=None):
        self.servers = []
        for server_id in servers or []:
            self.add_server(server_id)

    def add_server(self, server_id):
        if server_id not in self.servers:
            self.servers.append(server_id)
            return True
        return False

    def remove_server(self, server_id):
        if server_id in self.servers:
            self.servers.remove(server_id)
            return True
        return False

    def get_server(self, key):
        """Finds the server with the highest score for a given key."""
        if not self.servers:
            return None

        highest_score = -1
        champion_server = None

        for server in self.servers:
            score = self.get_score(key, server)
            if score > highest_score:
                highest_score = score
                champion_server = server
        return champion_server

    def get_score(self, key, server):
        combined_string = f"{key}:{server}"
        return int(hashlib.sha256(combined_string.encode()).hexdigest(), 16)


if __name__ == "__main__":
    # 1. Initialize with 3 servers
    cluster = RendezvousHashing(["Server_A", "Server_B", "Server_C"])

    # 2. Map a session key
    session_key = "sess_98765"
    target = cluster.get_server(session_key)
    print(f"Initial mapping: '{session_key}' goes to -> {target}")

    # 3. Simulate Server_B crashing
    print("\n--- Server_B crashed ---")
    cluster.remove_server("Server_B")

    # 4. Map the key again
    new_target = cluster.get_server(session_key)
    print(f"Failover mapping: '{session_key}' now goes to -> {new_target}")
