class Training:
    M_IN_KM = 1000  # метров в одном км
    LEN_STEP = 0.65  # метров в одном шаге

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float):
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self):
        """ значение дистанции, преодолённой за тренировку """
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self):
        """  значение средней скорости движения во время тренировки """
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self):
        """  возвращает число потраченных калорий """
        pass  # будет переопределён для каждого типа тренировки

    def show_training_info(self):
        """ Информационное сообщение о тренировке """
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """ Бег """
    MIN_IN_HOUR = 60  # минут в часе
    CALORIES_COEFF_1 = 18  # коэффициент калорий 1
    CALORIES_COEFF_2 = 20  # коэффициент калорий 2

    def get_spent_calories(self):
        """  кол-во затраченных при беге калорий """
        spent_calories = ((self.CALORIES_COEFF_1 * self.get_mean_speed()
                           - self.CALORIES_COEFF_2) * self.weight / self.M_IN_KM
                          * (self.duration * self.MIN_IN_HOUR))
        return spent_calories


class SportsWalking(Training):
    """ Спортивная ходьба """
    MIN_IN_HOUR = 60  # минут в часе
    W_CALORIES_COEFF_1 = 0.035  # коэффициент калорий 1
    W_CALORIES_COEFF_2 = 0.029  # коэффициент калорий 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height  # рост

    def get_spent_calories(self):
        """ кол-во затраченных при ходьбе калорий """
        spent_calories = ((self.W_CALORIES_COEFF_1 * self.weight +
                           (self.get_mean_speed() ** 2 // self.height) * self.W_CALORIES_COEFF_2
                           * self.weight) * (self.duration * self.MIN_IN_HOUR))
        return spent_calories


class Swimming(Training):
    """ Плавание """
    M_IN_KM = 1000  # метров в одном км
    S_CALORIES_COEFF_1 = 1.1  # коэффициент калорий 1
    S_CALORIES_COEFF_2 = 2  # коэффициент калорий 2
    LEN_STEP = 1.38  # метров в одном гребке

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # длина бассейна в метрах
        self.count_pool = count_pool  # число преодолений бассейна

    def get_mean_speed(self):
        """ средняя скорость движения """
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self):
        """ кол-во затраченных при плавании калорий """
        spent_calories = ((self.get_mean_speed() + self.S_CALORIES_COEFF_1)
                          * self.S_CALORIES_COEFF_2 * self.weight)
        return spent_calories


class InfoMessage:
    """ Информационное сообщение о тренировке """

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}',
                   f'Длительность: {self.duration:.3f} ч.',
                   f'Дистанция: {self.distance:.3f} км',
                   f'Средняя скорость: {self.speed:.3f} км/ч',
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message


def read_package(workout_type: str,
                 data: list):
    """ Прочитать данные, полученные от датчиков """
    training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training[workout_type](*data)


def main(training: Training):
    """ Главная функция """
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
