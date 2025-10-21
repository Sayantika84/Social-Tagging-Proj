import networkx as nx
import matplotlib.pyplot as plt
import random

def simulate_tagging_activity(dense_community_users, other_users, resources, tags, community_activity, other_activity):
    """Simulates tagging activity for both communities."""
    tagging_activity = []

    community_resource_pool = resources[:int(len(resources) * 0.3)]
    community_tag_pool = tags[:int(len(tags) * 0.5)]

    print("\nSimulating tagging for the dense community...")
    # Dense community users have higher activity and focus on a specific set of items
    for user in dense_community_users:
        for _ in range(community_activity):
            resource = random.choice(community_resource_pool)
            tag = random.choice(community_tag_pool)
            tagging_activity.append((user, resource, tag))

    print("Simulating tagging for other users...")
    # Other users have lower activity and tag from the general pool
    for user in other_users:
        for _ in range(other_activity):
            resource = random.choice(resources)
            tag = random.choice(tags)
            tagging_activity.append((user, resource, tag))

    return tagging_activity

def build_graph_from_activity(all_users, tagging_activity):
    """Builds a social graph based on shared tagging activity."""
    G = nx.Graph()
    G.add_nodes_from(all_users)

    tag_map = {}
    for user, resource, tag in tagging_activity:
        key = (resource, tag)
        if key not in tag_map:
            tag_map[key] = []
        tag_map[key].append(user)

    print("Building connections based on shared tags...")
    # Create weighted edges between users who used the same tag on the same resource
    for key, users_who_tagged in tag_map.items():
        unique_users = list(set(users_who_tagged))
        if len(unique_users) > 1:
            for i in range(len(unique_users)):
                for j in range(i + 1, len(unique_users)):
                    user1 = unique_users[i]
                    user2 = unique_users[j]
                    # Increase weight for each shared activity
                    if G.has_edge(user1, user2):
                        G[user1][user2]['weight'] += 1
                    else:
                        G.add_edge(user1, user2, weight=1)
    return G

def draw_graph(G, dense_community_users):
    """Visualizes the social network graph using matplotlib."""
    print("Preparing graph visualization...")
    total_users = G.number_of_nodes()
    
    pos = nx.spring_layout(G, k=0.15, iterations=50, weight='weight', seed=42)

    # Assign colors to nodes to distinguish the dense community
    node_colors = ['red' if node in dense_community_users else 'black' for node in G.nodes()]

    # Set edge widths based on their weight
    edge_weights = [G[u][v]['weight'] * 0.2 for u, v in G.edges()]

    plt.figure(figsize=(16, 14))

    nx.draw(G, pos,
            with_labels=False,
            node_size=80,
            node_color=node_colors,
            width=edge_weights,
            edge_color='gray')

    plt.title(f"Social Network Graph from Tagging Activity ({total_users} Users)", size=18)
    
    info_text = "The dense cluster (red nodes) forms from the community sharing similar tagging habits, distinct from other users (black nodes)."
    plt.figtext(0.5, 0.01, info_text, ha="center", fontsize=12, 
                bbox={"facecolor":"lightblue", "alpha":0.5, "pad":5})
    
    print("\n--- Social Graph Analysis ---")
    print(f"Total Users (Nodes): {G.number_of_nodes()}")
    print(f"Total Connections (Edges): {G.number_of_edges()}")
    
    plt.show()

def run_simulation_and_plot(num_community_users, num_other_users, num_resources, num_tags, community_activity, other_activity):
    """Sets up data, runs the simulation, and plots the resulting graph."""

    dense_community_users = [f"CommUser_{i}" for i in range(num_community_users)]
    other_users = [f"OtherUser_{i}" for i in range(num_other_users)]
    all_users = dense_community_users + other_users

    resources = [f"resource_{i}" for i in range(num_resources)]
    tags = [f"#tag_{i}" for i in range(num_tags)]
    
    tagging_activity = simulate_tagging_activity(dense_community_users, other_users, resources, tags, community_activity, other_activity)
    G = build_graph_from_activity(all_users, tagging_activity)
    
    if G.number_of_edges() > 0:
        draw_graph(G, dense_community_users)
    else:
        print("\nNo connections were formed based on the provided parameters. The graph is empty.")

def main():
    """Gets user input and runs the social network simulation."""
    print("--- Interactive Social Network Generator ---")
    print("This script generates a social graph based on simulated user tagging activity.")
    print("You can define the size of a core 'community' and a population of 'other' users.")
    
    choice = input("\nDo you want to use default settings? (yes/no): ").lower().strip()

    if choice in ['y', 'yes']:
        print("\nRunning with default settings...")
        run_simulation_and_plot(
            num_community_users=50,
            num_other_users=100,
            num_resources=50,
            num_tags=20,
            community_activity=20,
            other_activity=10
        )
    elif choice in ['n', 'no']:
        try:
            print("\nPlease provide custom settings:")
            num_community_users = int(input("Enter the number of users in the dense community (e.g., 50): "))
            num_other_users = int(input("Enter the number of other users (e.g., 100): "))
            num_resources = int(input("Enter the total number of resources (e.g., 50): "))
            num_tags = int(input("Enter the total number of tags (e.g., 20): "))
            community_activity = int(input("Enter activity level for community users (tags per user, e.g., 20): "))
            other_activity = int(input("Enter activity level for other users (tags per user, e.g., 10): "))
            
            print("\nRunning with custom settings...")
            run_simulation_and_plot(num_community_users, num_other_users, num_resources, num_tags, community_activity, other_activity)

        except ValueError:
            print("\nInvalid input. Please enter whole numbers only.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
    else:
        print("\nInvalid choice. Please enter 'yes' or 'no'.")


if __name__ == "__main__":
    main()

