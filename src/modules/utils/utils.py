import numpy as np


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
            np.cos(beta_in_rads) * np.cos(gamma_in_rads),
            -np.cos(beta_in_rads) * np.sin(gamma_in_rads),
            np.sin(beta_in_rads)
        ],
        [
            np.sin(alpha_in_rads) * np.sin(beta_in_rads) * np.cos(gamma_in_rads) +
            np.cos(alpha_in_rads) * np.sin(gamma_in_rads),
            np.cos(alpha_in_rads) * np.cos(gamma_in_rads) -
            np.sin(alpha_in_rads) * np.sin(beta_in_rads) *
            np.sin(gamma_in_rads),
            - np.sin(alpha_in_rads) * np.cos(beta_in_rads)

        ],
        [
            (-np.cos(alpha_in_rads) * np.sin(beta_in_rads)) *
            np.cos(gamma_in_rads) + np.sin(alpha_in_rads) *
            np.sin(gamma_in_rads),
            np.cos(alpha_in_rads) * np.sin(beta_in_rads) * np.sin(gamma_in_rads) +
            np.sin(alpha_in_rads) * np.cos(gamma_in_rads),
            np.cos(alpha_in_rads) * np.cos(beta_in_rads)

        ]
    ]


def rad2deg(rads: float) -> float:
    return rads * 180 / np.pi


def deg2rad(degree: float) -> float:
    return degree * np.pi / 180


def euclidean_distance(x: float, y: float) -> float:
    return np.sqrt(x ** 2 + y ** 2)


def sorting_vertices(vertices: np.ndarray):
    """
    Dado um polígono convexo você pode organizar os vertices
    pela fase entre o ponto médio do polígono com seus vértices
    """
    mean_x = np.mean(vertices[:, 0])
    mean_y = np.mean(vertices[:, 1])
    mean_point = np.array([mean_x, mean_y])

    def sort_by_angle(vertex: np.ndarray) -> float:
        vector = vertex - mean_point
        theta = np.arctan2(vector[1], vector[0])
        return theta if theta >= 0 else 2 * np.pi + theta

    return np.array(sorted(vertices, key=sort_by_angle))


def rotation_in_theta(theta_in_rads:float,array_2d:np.ndarray)->np.ndarray:

    rotation_matrix = [
        [np.cos(theta_in_rads),-np.sin(theta_in_rads)],
        [np.sin(theta_in_rads), np.cos(theta_in_rads)]
    ] 

    return np.dot(rotation_matrix,array_2d)    

