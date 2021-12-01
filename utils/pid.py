class PID:
    __k_p: float
    __k_i: float
    __k_d: float
    __set_point: float
    __last_error: float
    __integral_value: float

    def __init__(self, k_p: float, k_i: float, k_d: float, windup_guard: float = 5, set_point: float = 0.0):
        self.__k_p = k_p
        self.__k_d = k_d
        self.__k_i = k_i
        self.__last_error = 0
        self.__integral_value = 0
        self.__windup_guard = windup_guard
        self.__set_point = set_point

    def step(self, feedback_value: float) -> float:
        error = feedback_value - self.__set_point
        """ Como não foi sincronizado o tempo da simulação
            com o tempo da aplicação vulgo controlador, então
            foi decido que o dt, ou variação do tempo seria
            igual a 1
            ou seja erro/dt = erro
         """
        p = error

        self.__integral_value += error

        if self.__integral_value >= self.__windup_guard:
            self.__integral_value = self.__windup_guard
        elif self.__integral_value <= -self.__windup_guard:
            self.__integral_value = -self.__windup_guard

        d = error - self.__last_error

        self.__last_error = error

        return self.__k_p * p + self.__k_d * d + self.__k_i * self.__integral_value

    def clear(self):
        self.__last_error = 0
        self.__integral_value = 0
