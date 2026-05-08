try:
    from .consistent_hashing_ring import ConsistentHashRing
    from .rendezvous_hashing import RendezvousHashing
except ImportError:
    from consistent_hashing_ring import ConsistentHashRing
    from rendezvous_hashing import RendezvousHashing


def count_moved(before, after):
    return sum(before[key] != after[key] for key in before)


def print_summary(name, before, after):
    moved = count_moved(before, after)
    print(f"{name}: moved {moved}/{len(before)} keys")
    for key in sorted(before)[:8]:
        marker = "changed" if before[key] != after[key] else "same"
        print(f"  {key}: {before[key]} -> {after[key]} ({marker})")


def demo_consistent_hashing(keys):
    ring = ConsistentHashRing(vnodes=100)
    for server in ["Server_A", "Server_B", "Server_C"]:
        ring.add_server(server)

    before = ring.get_assignments(keys)
    ring.add_server("Server_D")
    after = ring.get_assignments(keys)

    print_summary("Consistent hashing after adding Server_D", before, after)
    print(f"  distribution: {dict(ring.get_distribution(keys))}")


def demo_rendezvous_hashing(keys):
    cluster = RendezvousHashing(["Server_A", "Server_B", "Server_C"])

    before = cluster.get_assignments(keys)
    cluster.add_server("Server_D")
    after = cluster.get_assignments(keys)

    print_summary("Rendezvous hashing after adding Server_D", before, after)
    print(f"  distribution: {dict(cluster.get_distribution(keys))}")


if __name__ == "__main__":
    keys = [f"user:{i}" for i in range(30)]

    demo_consistent_hashing(keys)
    print()
    demo_rendezvous_hashing(keys)
