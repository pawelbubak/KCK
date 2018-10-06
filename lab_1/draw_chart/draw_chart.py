import matplotlib
import matplotlib.pyplot as plt

from lab_1.import_data import file_names


def draw_charts(data):
    config_font()
    f, (ax1, ax2) = plt.subplots(1, 2, sharey='all')
    f.set_size_inches(6.7, 4.8)

    data_tab = []
    label_tab = []
    # first chart
    for var in data:
        draw_first_chart(ax1, var.get('name'), var.get('data'))
        data_tab.append(var.get('last'))
        label_tab.append(switch(var.get('name')).get('name'))
    set_main_appearance(ax1)

    # second chart
    draw_second_chart(ax2, label_tab, data_tab)
    set_main_appearance(ax2)

    def convert_played_games_to_generation_number(ax):
        x1, x2 = ax.get_xlim()
        ax1b.set_xlim(played_games_to_generation_number(x1), played_games_to_generation_number(x2))
        ax1b.figure.canvas.draw()

    # first chart - second scale
    ax1b = ax1.twiny()
    set_second_x_label(ax1b)
    set_main_appearance(ax1b)

    ax1.callbacks.connect("xlim_changed", convert_played_games_to_generation_number)

    set_first_chart_appearance(ax1)
    set_second_chart_appearance(ax2)

    # save chart
    plt.savefig('myplot.pdf')
    plt.close()


def draw_first_chart(ax, name, data):
    config = switch(name)
    ax.plot(data.get('effort'), data.get('value'), label=config.get('name'),
            color=config.get('color'), marker=config.get('marker'),
            linewidth=1, markevery=25, markeredgecolor='#000000', markeredgewidth=0.5, markersize=4.5, alpha=0.8)
    ax.set_ylabel('Odsetek wygranych gier [%]')
    ax.set_xlabel('Rozegranych gier (x1000)')


def set_second_x_label(ax):
    ax.set_xlabel('Pokolenie')
    ax.xaxis.set_ticks(list(range(0, 201, 40)))
    ax.axis(xmin=0, xmax=200)
    ax.tick_params(axis="x", direction="in", top=True, width=0.5)


def draw_second_chart(ax, labels, data):
    box_plot = ax.boxplot(data, labels=labels, notch=True, patch_artist=True, showmeans=True)
    for box in box_plot['boxes']:
        box.set(color='blue', linewidth=0.9)
        box.set(facecolor='none')
    for whisker in box_plot['whiskers']:
        whisker.set(color='blue', linewidth=0.9, linestyle=(0, (5, 5)))
    for caps in box_plot['caps']:
        caps.set(color='black', linewidth=0.9)
    for medians in box_plot['medians']:
        medians.set(color='red', linewidth=0.9)
    for flier in box_plot['fliers']:
        flier.set(marker='+', markerfacecolor='blue', markeredgewidth=0.5, markersize=4.5, markeredgecolor='blue',
                  alpha=0.8)
    for means in box_plot['means']:
        means.set(marker='o', markerfacecolor='blue', markeredgewidth=0.5, markersize=4.5, markeredgecolor='black',
                  alpha=0.8)


def set_main_appearance(ax):
    for i in ['bottom', 'left', 'right', 'top']:
        ax.spines[i].set_linewidth(0.4)
    ax.axis(ymin=60, ymax=100)
    ax.grid(linestyle=(0, (3, 8)), linewidth=0.3, color='#707070')


def set_first_chart_appearance(ax):
    ax.axis(xmin=0, xmax=500)
    ax.legend(numpoints=2, edgecolor='#707070')
    ax.get_legend().get_frame().set_linewidth(0.55)
    ax.tick_params(axis="both", direction="in", right=True, top=True, width=0.5)


def set_second_chart_appearance(ax):
    ax.tick_params(axis="y", direction="in", left=False, right=True, width=0.5, labelright=True)
    ax.tick_params(axis="x", direction="in", top=True, width=0.5, labelrotation=20)


def switch(x):
    return {
        file_names[0]: {'color': 'blue', 'marker': 'o', 'name': '1-Evol-RS'},
        file_names[1]: {'color': 'green', 'marker': 'v', 'name': '1-Coev-RS'},
        file_names[2]: {'color': 'red', 'marker': 'D', 'name': '2-Coev-RS'},
        file_names[3]: {'color': 'black', 'marker': 's', 'name': '1-Coev'},
        file_names[4]: {'color': 'magenta', 'marker': 'd', 'name': '2-Coev'},
    }[x]


def config_font():
    matplotlib.rcParams['mathtext.fontset'] = 'stix'
    matplotlib.rcParams['font.family'] = 'STIXGeneral'
    matplotlib.rcParams['font.size'] = 9


def played_games_to_generation_number(value):
    return value / 2.5
