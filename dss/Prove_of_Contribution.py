import numpy as np
import matplotlib.pyplot as plt

# Define the number of users
num_users = 31

# Define the 30 minutes interval
T = 30

# Define weight coefficients
alpha = 1.0  # Weight for power generation
beta = 0.1   # Weight for power demand
gamma = 1.0  # Weight for storage contribution

# Initialize list to store validators (only one round now)
validators = []

print("Proof of Contribution to Grid - Blockchain Simulation")
print("-----------------------------------------------------")
print(f"Total Users: {num_users}")
print(f"Total Block Validations: 1\n")

# Function to perform a single block validation round
def perform_block_validation(round_num):
    # Randomly generate each user's power generation (G), demand (D), and storage contribution (S)
    G = np.random.uniform(0, 3, num_users)  # Generation (0 to 3 kW)
    D = np.random.uniform(0, 7, num_users)  # Demand (0 to 7 kW)
    S = np.random.uniform(0, 2, num_users)  # Storage contribution (0 to 2 kWh)

    # Set fixed values for users 6, 7, 8, 9, 10 (indices 5 to 9)
    fixed_users = [5, 6, 7, 8, 9]  # Zero-based indexing
    G[fixed_users] = 0.0
    D[fixed_users] = 3.0
    S[fixed_users] = 0.0

    # Calculate each user's Contribution Factor (CF) using the updated formula
    # Ensures any positive contribution gives a chance to be selected
    CF = alpha * G - beta * D + gamma * S  # Modified CF formula

    # Ensure CF is non-negative
    CF = np.maximum(CF, 0)

    # Calculate total Contribution Factor
    CF_total = np.sum(CF)

    # Calculate each user's probability to validate the block
    if CF_total > 0:
        P = CF / CF_total
    else:
        P = np.zeros(num_users)

    # Select the validator using weighted random choice
    validator = np.random.choice(range(num_users), p=P)
    validators.append(validator)

    # Print the results for this round
    print(f"Block {round_num}:")
    print("User\tGeneration (G)\tDemand (D)\tStorage (S)\tContribution Factor (CF)\tValidation Probability (P)")
    for i in range(num_users):
        fixed_flag = " (passive)" if i in fixed_users else ""
        print(f"{i+1}{fixed_flag}\t{G[i]:.2f} kW\t\t{D[i]:.2f} kW\t\t{S[i]:.2f} kWh\t\t{CF[i]:.4f}\t\t\t{P[i]:.2%}")
    print(f"\nUser {validator+1} is selected as the block validator and will receive an electricity price discount.\n")

    # Visualization
    fig, ax1 = plt.subplots(figsize=(14, 7))
    color = 'tab:blue'
    ax1.set_xlabel('User')
    ax1.set_ylabel('Contribution Factor (CF)', color=color)
    bars = ax1.bar(range(1, num_users+1), CF, color=color, alpha=0.6, label='Contribution Factor (CF)')
    ax1.tick_params(axis='y', labelcolor=color)

    # Adjust x-ticks for readability
    if num_users <= 20:
        plt.xticks(range(1, num_users+1))
    else:
        step = max(1, num_users // 10)
        plt.xticks(range(1, num_users+1, step))

    # Highlight the validator
    bars[validator].set_color('gold')

    # Highlight fixed users differently (e.g., hatch pattern)
    for idx in fixed_users:
        bars[idx].set_edgecolor('black')
        bars[idx].set_hatch('//')

    ax2 = ax1.twinx()  # Share x-axis
    color = 'tab:red'
    ax2.set_ylabel('Validation Probability (%)', color=color)
    ax2.plot(range(1, num_users+1), P*100, color=color, marker='o', label='Validation Probability (P)')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(0, 100)

    # Add legends
    fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)

    plt.title(f'Block {round_num}: Contribution Factors and Validation Probabilities')
    fig.tight_layout()
    plt.show()

# Perform a single block validation round
perform_block_validation(1)

print("Block validation completed.")
