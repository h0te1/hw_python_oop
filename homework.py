class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return print(f"""Тип тренировки: {self.training_type};
        Длительность: {self.duration} ч.;
        Дистанция: {round(self.distance, 3)} км;
        Ср.скорость: {round(self.speed, 3)} км/ч;
        Потрачено ккал: {round(self.calories, 3)}.""")


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: float = 1000

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        dist = self.get_distance()
        return dist / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = type(self).__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        mspeed = Running.get_mean_speed(self)  # средняя скорость
        cal = (18*mspeed - 20)  # для сокращения строки
        return cal * self.weight/Training.M_IN_KM * (self.duration * 60)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mspeed = self.get_mean_speed()  # средняя скорость
        local_bracket = (mspeed**2 // self.height)  # тоже соеращение строки
        bracket = (0.035 * self.weight + local_bracket * 0.029 * self.height)
        return bracket * self.duration


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> int:
        m_in_pool = self.length_pool * self.count_pool
        return m_in_pool / Training.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        spd = self.get_mean_speed()
        return (spd + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    code = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return code[workout_type](*data,)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    return info.get_message()


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
