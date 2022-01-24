import numpy as np
import matplotlib.pyplot as plt

segment_to_score = {
        0: 6,
        1: 13,
        2: 4,
        3: 18,
        4: 1,
        5: 20,
        6: 5,
        7: 12,
        8: 9,
        9: 14,
        10: 11,
        11: 8,
        12: 16,
        13: 7,
        14: 19,
        15: 3,
        16: 17,
        17: 2,
        18: 15,
        19: 10,
        20: 6,
        }

all_scores = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800, 4000, 6000, 12000, 18000, 24000, 30000, 36000, 42000, 48000, 54000, 60000, 66000, 72000, 78000, 84000, 90000, 96000, 102000, 108000, 114000, 120000, 25, 50]

colors_single_scores = {
        1: "white",
        2: "black",
        3: "black",
        4: "white",
        5: "white",
        6: "white",
        7: "black",
        8: "black",
        9: "white",
        10: "black",
        11: "white",
        12: "black",
        13: "black",
        14: "black",
        15: "white",
        16: "white",
        17: "white",
        18: "black",
        19: "white",
        20: "black",
        }

colors_multiplied_scores = {
        1: "green",
        2: "red",
        3: "red",
        4: "green",
        5: "green",
        6: "green",
        7: "red",
        8: "red",
        9: "green",
        10: "red",
        11: "green",
        12: "red",
        13: "red",
        14: "red",
        15: "green",
        16: "green",
        17: "green",
        18: "red",
        19: "green",
        20: "red",
        }

@np.vectorize
def calculate_angle(x, y):
    vector_length = np.sqrt(x**2 + y**2)
    if y >= 0:
        return np.degrees(np.arccos(x / vector_length))
    else:
        return 360 - np.degrees(np.arccos(x / vector_length))

@np.vectorize
def calculate_visualizing_scores(angle, distance):
    if distance > 1:
        return 0

    segment = np.floor((angle + 9) / 18)

    if distance >= 1-8/170:
        return segment_to_score[segment] * 200

    if distance <= 107/170 and distance > 107/170 - 8/170:
        return segment_to_score[segment] * 6000

    if distance <= 6.35/170:
        return 50

    if distance > 6.35/170 and distance <= 16/170:
        return 25

    return segment_to_score[segment]

@np.vectorize
def calculate_actual_scores(angle, distance):
    if distance > 1:
        return 0

    segment = np.floor((angle + 9) / 18)

    if distance >= 1-8/170:
        return segment_to_score[segment] * 2

    if distance <= 107/170 and distance > 107/170 - 8/170:
        return segment_to_score[segment] * 3

    if distance <= 6.35/170:
        return 50

    if distance > 6.35/170 and distance <= 16/170:
        return 25

    return segment_to_score[segment]

def get_color(score):
    if score == 25: return "green"
    if score == 50: return "red"
    if score <= 20: return colors_single_scores[score]
    if score <= 4000: return colors_multiplied_scores[int(score/200)]
    if score <= 120000: return colors_multiplied_scores[int(score/6000)]

def visualize_board(xx, yy, scores, point, radius, highest_score):
    fig, ax = plt.subplots()
    for score in all_scores:
        mask = scores == score
        ax.scatter(xx[mask], yy[mask], color=get_color(score), s=0.3)
    ax.set_aspect(1)
    ax.scatter(point[0], point[1])
    circle = plt.Circle ((point[0], point[1]), radius, alpha=0.3)
    ax.add_patch(circle)
    ax.annotate(f"avg: {highest_score:.2f}", (point[0], point[1]), (0.6, -1))
    plt.show()

def get_highest_scoring_area(xx, yy, scores, radius):

    highest_average_score = 0
    current_best_point = (None, None)
    scores_test = []

    for i, row in enumerate(scores):
        for j, score in enumerate(row):
            if score == 0:
                continue
            y = yy[i, j]
            x = xx[i, j]
            distances = np.sqrt((xx-x)**2 + (yy-y)**2)
            mask = distances <= radius
            scores_in_range = scores[mask].flatten()
            average_score = np.average(scores_in_range)
            if average_score > highest_average_score:
                current_best_point = (x, y)
                highest_average_score = average_score
                scores_test = scores_in_range

    return highest_average_score, current_best_point

def get_point_average(x, y, xx, yy, scores, radius):
    distances = np.sqrt((xx-x)**2 + (yy-y)**2)
    mask = distances <= radius
    scores_in_range = scores[mask].flatten()
    print(scores_in_range)
    average_score = np.average(scores_in_range)
    return average_score

def main():

    np.set_printoptions(threshold=np.inf)

    square_size = 1.3
    N = 350
    radius = 0.20

    x = np.linspace(-square_size, square_size, N)
    y = np.linspace(-square_size, square_size, N)

    xx, yy = np.meshgrid(x, y)

    distances = np.sqrt(xx**2 + yy**2)

    angles = calculate_angle(xx, yy)

    visualizing_scores = calculate_visualizing_scores(angles, distances)
    actual_scores = calculate_actual_scores(angles, distances)

    score, point = get_highest_scoring_area(xx, yy, actual_scores, radius)

    #visualize_board(xx, yy, visualizing_scores, point, radius, score)

    bull_score = get_point_average(0, 0, xx, yy, actual_scores, 0.1)
    visualize_board(xx, yy, visualizing_scores, (0, 0), 0.1, bull_score)

if __name__ == "__main__":
    main()
