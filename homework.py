"""Класс-модуль фитнес-трекера"""

from typing import Dict, ClassVar
from dataclasses import dataclass
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str  # имя класса тренировки;
    duration: float  # длительность тренировки в часах
    distance: float  # дист в км, которую преодолел пользователь
    speed: float  # средняя скорость, движения пользователя
    calories: float  # количество килокал, за время тренировки

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность:{self.duration: .3f} ч.; '
                   f'Дистанция:{self.distance: .3f} км; '
                   f'Ср. скорость:{self.speed: .3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.'
                   )
        return message


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int  # количество совершённых действий
    duration: float  # длительность тренировки
    weight: float  # вес спортсмена
    M_IN_KM: ClassVar[int] = 1000   # конст перевода знач из метр в км
    LEN_STEP: ClassVar[float] = 0.65

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        # расчет значение средней скорости движения во время тренировки.
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        # расчет преодоленной_дистанции_за_тренировку / время_тренировки
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Subclasses should implement this method!")
        # Логика подсчета калорий для каждого вида тренировки будет своя,
        # поэтому в базовом классе не нужно описывать поведение метода,
        # в его теле останется ключевое слово

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        # Определен в каждом дочерним классе индивидуально
        object_for_mes: InfoMessage = InfoMessage(type(self).__name__,
                                                  self.duration,
                                                  self.get_distance(),
                                                  self.get_mean_speed(),
                                                  self.get_spent_calories())

        return object_for_mes


@dataclass
class Running(Training):
    """Тренировка: бег."""
    MINUTE: ClassVar[int] = 60
    # в классе переопределен метод get_spent_calories"""
    COEF_CAL1: ClassVar[int] = 18  # Коэф для каллорий для бега
    COEF_CAL2: ClassVar[int] = 20  # Коэфициент для опреления каллорий для бега

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.COEF_CAL1 * self.get_mean_speed()
                    - self.COEF_CAL2) * self.weight / self.M_IN_KM
                    * (self.duration * self.MINUTE))
        # (18 * средняя_скорость - 20) * вес_спортсмена / M_IN_KM *
        # время_тренировки_в_минутах
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    # в классе переопределен метод get_spent_calories добавлен атрибут height
    COEF_CAL_WALK1: ClassVar[float] = 0.035  # Коэфициент для опр кал ходьба
    COEF_CAL_WALK2: ClassVar[float] = 0.029  # Коэфициент для опр кал ходьба
    MINUTE: ClassVar[int] = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.COEF_CAL_WALK1 * self.weight
                    + (self.get_mean_speed() ** 2 // self.height)
                    * self.COEF_CAL_WALK2 * self.weight) * (self.duration
                    * self.MINUTE))
    # (0.035 * вес + (средняя_скорость**2 // рост) * 0.029 * вес)
    # * время_тренировки_в_минутах
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float  # длина бассейна в метрах;
    count_pool: float  # сколько раз пользователь переплыл бассейн
    # в классе переопределены методы get_spent_calories() и get_mean_speed()
    # добавлены атрибуты length_pool count_pool
    COEF_CAL_SWM1: ClassVar[float] = 1.1  # Коэфи для опр калл плав
    COEF_CAL_SWM2: ClassVar[int] = 2  # Коэфи для опр калл плав
    LEN_STEP: ClassVar[float] = 1.38

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.get_mean_speed() + self.COEF_CAL_SWM1)
                    * self.COEF_CAL_SWM2 * self.weight)
        return calories

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = (self.length_pool * self.count_pool / self.M_IN_KM
                             / self.duration)
        # длина_бассейна * count_pool / M_IN_KM / время_тренировки
        return mean_speed


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: Dict = {'SWM': Swimming,
                           'RUN': Running,
                           'WLK': SportsWalking}
    create_tren: Training = training_dict[workout_type](*data)
    if create_tren is None:
        raise TypeError(f'Фун-я read_package не смогла создать объект трен-ки'
                        f'Получен следующий тип {workout_type}'
                        )
    return create_tren


def main(training: Training) -> str:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


# заранее подготовленные тестовые данные для проверки фитнес-трекера"""
if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
