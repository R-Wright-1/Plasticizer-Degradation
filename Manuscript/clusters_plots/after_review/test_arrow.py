import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

ax = plt.subplot(111)

arrowstyle = mpatches.ArrowStyle.Simple(head_width=15,tail_width=8,head_length=5)
arrow = mpatches.FancyArrowPatch((0, 0), (1, 0), arrowstyle=arrowstyle)
ax.add_patch(arrow)

ax.set_ylim([-0.5, 0.5])
ax.set_xlim([-1, 2])