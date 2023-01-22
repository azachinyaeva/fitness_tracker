from typing import ClassVar


class InfoMessage:
    """ Информационное сообщение о тренировке """

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message: str = (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    M_IN_KM: ClassVar[int] = 1000  # метров в одном км
    LEN_STEP: ClassVar[float] = 0.65  # метров в одном шаге

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """ значение дистанции, преодолённой за тренировку """
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """  значение средней скорости движения во время тренировки """
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """  возвращает число потраченных калорий """
        raise NotImplementedError(f'Переопределите метод класса {type(self).__name__} ')

    def show_training_info(self) -> InfoMessage:
        """ Информационное сообщение о тренировке """
        message: InfoMessage = InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        return message


class Running(Training):
    """ Бег """
    MIN_IN_HOUR: ClassVar[int] = 60  # минут в часе
    CALORIES_COEFF_1: ClassVar[int] = 18  # коэффициент калорий 1
    CALORIES_COEFF_2: ClassVar[int] = 20  # коэффициент калорий 2

    def get_spent_calories(self) -> float:
        """  кол-во затраченных при беге калорий """
        spent_calories: float = ((self.CALORIES_COEFF_1 * self.get_mean_speed()
                           - self.CALORIES_COEFF_2) * self.weight / self.M_IN_KM
                          * (self.duration * self.MIN_IN_HOUR))
        return spent_calories


class SportsWalking(Training):
    """ Спортивная ходьба """
    MIN_IN_HOUR: ClassVar[int] = 60  # минут в часе
    W_CALORIES_COEFF_1: ClassVar[float] = 0.035  # коэффициент калорий 1
    W_CALORIES_COEFF_2: ClassVar[float] = 0.029  # коэффициент калорий 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height  # рост

    def get_spent_calories(self) -> float:
        """ кол-во затраченных при ходьбе калорий """
        spent_calories: float = ((self.W_CALORIES_COEFF_1 * self.weight +
                           (self.get_mean_speed() ** 2 // self.height) * self.W_CALORIES_COEFF_2
                           * self.weight) * (self.duration * self.MIN_IN_HOUR))
        return spent_calories


class Swimming(Training):
    """ Плавание """
    M_IN_KM: ClassVar[int] = 1000  # метров в одном км
    S_CALORIES_COEFF_1: ClassVar[float] = 1.1  # коэффициент калорий 1
    S_CALORIES_COEFF_2: ClassVar[int] = 2  # коэффициент калорий 2
    LEN_STEP: ClassVar[float] = 1.38  # метров в одном гребке

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # длина бассейна в метрах
        self.count_pool = count_pool  # число преодолений бассейна

    def get_mean_speed(self) -> float:
        """ средняя скорость движения """
        mean_speed: float = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """ кол-во затраченных при плавании калорий """
        spent_calories: float = ((self.get_mean_speed() + self.S_CALORIES_COEFF_1)
                          * self.S_CALORIES_COEFF_2 * self.weight)
        return spent_calories


def read_package(workout_type: str,
                 data: list) -> Training:
    """ Прочитать данные, полученные от датчиков """
    training: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        result: Training = training[workout_type](*data)
    except KeyError:
        raise Exception('Неправильный тип тренировки')
    return result


def main(training: Training) -> None:
    """ Главная функция """
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
