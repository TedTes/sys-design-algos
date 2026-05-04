import mmh3

class RendezvousHashing:
    def __init__(self, servers=None):
       self.servers = list(servers) if servers else []
    
    def add_server(self, server_id):
        if server not in self.servers:
            self.servers.append(server_id)
            return True
        return False
    
    def remove_server(self, server_id):    
        if server in self.servers:
            self.servers.remove(server_id)
            return True
        return False
    
    def get_server(self, key):
        """Finds the server with the highest score for a given key."""
        if not self.servers:
            return None
        highest_score = -1
        champipon_server = None

        for server in self.servers:
            score = self.get_score(key, server)
            if score > highest_score:
                highest_score = score
                champion_server = server
        return champion_server
    
    def get_score(self, key, server):
         combined_string = f"{key}-{server}"
         return mmh3.hash(combined_string)
      
    
   # 1. Initialize with 3 servers
cluster = RendezvousHash(["Server_A", "Server_B", "Server_C"])

# 2. Map a session key
session_key = "sess_98765"
target = cluster.get_server(session_key)
print(f"Initial mapping: '{session_key}' goes to -> {target}")

# 3. Simulate Server_B crashing (Assume Server_B was the original champion)
print("\n--- OH NO! Server_B crashed! ---")
cluster.remove_server("Server_B")

# 4. Map the key again
new_target = cluster.get_server(session_key)
print(f"Failover mapping: '{session_key}' now goes to -> {new_target}")