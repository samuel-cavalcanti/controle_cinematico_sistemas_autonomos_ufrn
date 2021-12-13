import math


def euler_angles_to_rotation_matrix(angles: list[float]) -> list[list[float]]:
    '''
    |(cos(b)*cos(g))                                    (cos(b)*(-sin(g)))                                  sin(b)                                             |
    |sin(a))*sin(b)*cos(g) + cos(a)*sin(g)              cos(a)cos(g) - sin(a)sin(b)sin(g)                 -sin(a)*cos(b)                                |
    | (-cos(a)*sin(b) )*cos(g) + sin(a)*sin(g)    cos(a)*sin(b)*sin(g)+ sin(a)*cos(g)    cos(a)*cos(b)                                    |
    '''
    alpha_in_rads = angles[0]
    beta_in_rads = angles[1]
    gamma_in_rads = angles[2]

    return [
        [
            math.cos(beta_in_rads) * math.cos(gamma_in_rads),
            -math.cos(beta_in_rads) * math.sin(gamma_in_rads),
            math.sin(beta_in_rads)
        ],
        [
            math.sin(alpha_in_rads) * math.sin(beta_in_rads) * math.cos(gamma_in_rads) +
            math.cos(alpha_in_rads) * math.sin(gamma_in_rads),
            math.cos(alpha_in_rads) * math.cos(gamma_in_rads) -
            math.sin(alpha_in_rads) * math.sin(beta_in_rads) *
            math.sin(gamma_in_rads),
            - math.sin(alpha_in_rads) * math.cos(beta_in_rads)

        ],
        [
            (-math.cos(alpha_in_rads) * math.sin(beta_in_rads)) *
            math.cos(gamma_in_rads) + math.sin(alpha_in_rads) *
            math.sin(gamma_in_rads),
            math.cos(alpha_in_rads) * math.sin(beta_in_rads) * math.sin(gamma_in_rads) +
            math.sin(alpha_in_rads) * math.cos(gamma_in_rads),
            math.cos(alpha_in_rads) * math.cos(beta_in_rads)

        ]
    ]


def orientation_theta(angles: list[float]) -> float:
    alpha_in_rads = angles[0]
    beta_in_rads = angles[1]
    gamma_in_rads = angles[2]
    return 2 * math.acos(math.cos((alpha_in_rads + gamma_in_rads) / 2) * math.cos(beta_in_rads / 2))


def rad2deg(rads: float) -> float:
    return rads * 180 / math.pi


def deg2rad(degree: float) -> float:
    return degree * math.pi / 180


def euclidean_distance(x: float, y: float) -> float:
    return math.sqrt(x ** 2 + y ** 2)
