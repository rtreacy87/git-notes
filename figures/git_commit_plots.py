import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

# Common settings
branch_y_positions = {'origin/main': 3, 'local/main': 2, 'testing': 1}
commit_colors = {'A': 'lightblue', 'B': 'lightgreen', 'C': 'lightsalmon', 
                 'D': 'plum', 'M': 'gold'}

# Function to draw a commit
def draw_commit(ax, x, y, label, color):
    circle = plt.Circle((x, y), 0.3, color=color, ec='black')
    ax.add_patch(circle)
    ax.text(x, y, label, ha='center', va='center', fontweight='bold')

# Function to draw a branch line
def draw_branch_line(ax, x_start, x_end, y):
    ax.plot([x_start, x_end], [y, y], 'k-', linewidth=2)

# Function to draw an arrow between commits
def draw_arrow(ax, x_start, y_start, x_end, y_end):
    arrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                           arrowstyle='->', color='red', linewidth=1.5,
                           connectionstyle='arc3,rad=0.3')
    ax.add_patch(arrow)

# Function to setup common elements for each plot
def setup_plot(title):
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.suptitle(title, fontsize=14)
    
    # Add branch labels
    for branch, y in branch_y_positions.items():
        ax.text(0.5, y, branch, ha='right', va='center', fontweight='bold')
    
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4)
    ax.axis('off')
    
    # Add legend
    for i, (commit, color) in enumerate(commit_colors.items()):
        circle = plt.Circle((i+0.7, 0.3), 0.2, color=color, ec='black')
        ax.add_patch(circle)
        ax.text(i+0.7, 0.3, commit, ha='center', va='center', fontweight='bold')
        ax.text(i+0.7, 0, f"Commit {commit}", ha='center', va='center')
    
    return fig, ax

# Plot 1: Initial state
fig1, ax1 = setup_plot('Step 1: Initial State')

# Draw branch lines
draw_branch_line(ax1, 1, 5, branch_y_positions['origin/main'])
draw_branch_line(ax1, 1, 2, branch_y_positions['local/main'])
draw_branch_line(ax1, 1, 3, branch_y_positions['testing'])

# Draw commits
draw_commit(ax1, 1, branch_y_positions['origin/main'], 'A', commit_colors['A'])
draw_commit(ax1, 2, branch_y_positions['origin/main'], 'B', commit_colors['B'])
draw_commit(ax1, 3, branch_y_positions['origin/main'], 'C', commit_colors['C'])
draw_commit(ax1, 1, branch_y_positions['local/main'], 'A', commit_colors['A'])
draw_commit(ax1, 1, branch_y_positions['testing'], 'A', commit_colors['A'])
draw_commit(ax1, 2, branch_y_positions['testing'], 'D', commit_colors['D'])

plt.tight_layout()
plt.savefig('git_workflow_step1.png', dpi=300, bbox_inches='tight')

# Plot 2: After git pull origin main
fig2, ax2 = setup_plot('Step 2: After git pull origin main')

# Draw branch lines
draw_branch_line(ax2, 1, 5, branch_y_positions['origin/main'])
draw_branch_line(ax2, 1, 4, branch_y_positions['local/main'])
draw_branch_line(ax2, 1, 3, branch_y_positions['testing'])

# Draw commits
draw_commit(ax2, 1, branch_y_positions['origin/main'], 'A', commit_colors['A'])
draw_commit(ax2, 2, branch_y_positions['origin/main'], 'B', commit_colors['B'])
draw_commit(ax2, 3, branch_y_positions['origin/main'], 'C', commit_colors['C'])
draw_commit(ax2, 1, branch_y_positions['local/main'], 'A', commit_colors['A'])
draw_commit(ax2, 2, branch_y_positions['local/main'], 'B', commit_colors['B'])
draw_commit(ax2, 3, branch_y_positions['local/main'], 'C', commit_colors['C'])
draw_commit(ax2, 1, branch_y_positions['testing'], 'A', commit_colors['A'])
draw_commit(ax2, 2, branch_y_positions['testing'], 'D', commit_colors['D'])

plt.tight_layout()
plt.savefig('git_workflow_step2.png', dpi=300, bbox_inches='tight')

# Plot 3: After git merge main
fig3, ax3 = setup_plot('Step 3: After git merge main')

# Draw branch lines
draw_branch_line(ax3, 1, 5, branch_y_positions['origin/main'])
draw_branch_line(ax3, 1, 4, branch_y_positions['local/main'])
draw_branch_line(ax3, 1, 5, branch_y_positions['testing'])

# Draw commits
draw_commit(ax3, 1, branch_y_positions['origin/main'], 'A', commit_colors['A'])
draw_commit(ax3, 2, branch_y_positions['origin/main'], 'B', commit_colors['B'])
draw_commit(ax3, 3, branch_y_positions['origin/main'], 'C', commit_colors['C'])
draw_commit(ax3, 1, branch_y_positions['local/main'], 'A', commit_colors['A'])
draw_commit(ax3, 2, branch_y_positions['local/main'], 'B', commit_colors['B'])
draw_commit(ax3, 3, branch_y_positions['local/main'], 'C', commit_colors['C'])
draw_commit(ax3, 1, branch_y_positions['testing'], 'A', commit_colors['A'])
draw_commit(ax3, 2, branch_y_positions['testing'], 'D', commit_colors['D'])
draw_commit(ax3, 4, branch_y_positions['testing'], 'M', commit_colors['M'])

# Draw merge arrows
draw_arrow(ax3, 3, branch_y_positions['local/main'], 4, branch_y_positions['testing'])
draw_arrow(ax3, 2, branch_y_positions['testing'], 4, branch_y_positions['testing'])

plt.tight_layout()
plt.savefig('git_workflow_step3.png', dpi=300, bbox_inches='tight')

print("Created three separate visualization images:")
print("1. git_workflow_step1.png - Initial state")
print("2. git_workflow_step2.png - After git pull origin main")
print("3. git_workflow_step3.png - After git merge main")

