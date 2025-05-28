import matplotlib.pyplot as plt

def plot_progress(progress):
    if not progress:
        print("No progress to plot.")
        return
    wpm_values, acc_values = zip(*progress)
    plt.figure(figsize=(10, 5))
    plt.plot(wpm_values, label='WPM')
    plt.plot(acc_values, label='Accuracy')
    plt.xlabel('Test Number')
    plt.ylabel('Value')
    plt.title('Typing Progress Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()
