import matplotlib.pyplot as plt
import math

def draw_comparison(design_points, actual_points):
    if len(design_points) != 4 or len(actual_points) != 4:
        raise ValueError("Должно быть по 4 точки для каждого прямоугольника")

    # Вычисляем разницы между координатами
    def calculate_diffs(design, actual):
        return [(a[0]-d[0], a[1]-d[1]) for d, a in zip(design, actual)]

    diffs = calculate_diffs(design_points, actual_points)

    # Функция для подготовки координат
    def prepare_rectangle(points):
        ordered = [points[0], points[2], points[3], points[1], points[0]]
        return [p[0] for p in ordered], [p[1] for p in ordered]

    def calculate_rotation_angle(design, actual):
        design_vector = (design[1][0] - design[0][0], design[1][1] - design[0][1])
        actual_vector = (actual[1][0] - actual[0][0], actual[1][1] - actual[0][1])

        design_angle = math.atan2(design_vector[1], design_vector[0])
        actual_angle = math.atan2(actual_vector[1], actual_vector[0])

        # Угол поворота в градусах
        rotation_angle = math.degrees(actual_angle - design_angle)

        # Нормализация угла в диапазоне от -180° до +180°
        rotation_angle = (rotation_angle + 360) % 360
        if rotation_angle > 180:
            rotation_angle -= 360
        return rotation_angle

    rotation_angle = calculate_rotation_angle(design_points, actual_points)

    # Создаем график с дополнительным пространством для текста
    fig = plt.figure(figsize=(12, 10))
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 1])
    ax = fig.add_subplot(gs[0])
    text_ax = fig.add_subplot(gs[1])

    # Отключаем оси для текстовой области
    text_ax.axis('off')

    # Рисуем прямоугольники
    for points, style, color, label in [
        (design_points, 'b--', 'blue', 'Проектная форма (A4)'),
        (actual_points, 'r-', 'red', 'Фактическое положение')
    ]:
        x, y = prepare_rectangle(points)
        ax.plot(x, y, style, label=label, linewidth=2)
        ax.scatter(x[:-1], y[:-1], color=color, s=80, edgecolors='k', zorder=3)

    # Настройка графической части
    ax.set_title("Сравнение проектной и фактической позиции\n(формат A4: 210 × 297 мм)", fontsize=14)
    ax.set_xlabel("X-координата (мм)", fontsize=12)
    ax.set_ylabel("Y-координата (мм)", fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.legend(loc='best')
    ax.set_aspect('equal', adjustable='datalim')
    ax.autoscale(enable=True)

    # Формируем текст с фактическими углами и координатами
    output_text = "Рабочие точки по проекту:\n"
    for point in actual_points:
        output_text += f"({point[0]:.3f}, {point[1]:.3f}) мм\n"

    output_text += "\nФактические углы:\n\n"
    labels = ['Левый нижний угол', 'Правый нижний угол', 
             'Левый верхний угол', 'Правый верхний угол']
    
    for label, (dx, dy), d_point, a_point in zip(labels, diffs, design_points, actual_points):
        output_text += (
            f"{label}:\n"
            f"Факт:   ({a_point[0]:.3f}, {a_point[1]:.3f}) мм\n"
            f"ΔX = {dx:+.3f} мм | ΔY = {dy:+.3f} мм\n\n"
        )

    output_text += f"Угол поворота фактической фигуры: {rotation_angle:.3f}°\n"

    # Добавляем текстовый блок
    text_ax.text(0, 0.5, output_text, 
                fontfamily='monospace', 
                fontsize=10, 
                verticalalignment='center',
                bbox={'facecolor': '#f0f0f0', 'pad': 10})

    plt.tight_layout()
    plt.show()

# Данные для примера
design_points = [
    (0, 0),    # Левый нижний
    (210, 0),  # Правый нижний
    (0, 297),  # Левый верхний
    (210, 297) # Правый верхний
]

actual_points = [
    (30.500, 45.114),
    (258.921, 20.000),
    (65.518, 368.167),
    (294.440, 343.553)
]

draw_comparison(design_points, actual_points)
