import numpy as np
from cython_modules.cython_parse import getLayerOutline
from multiprocessing import Pool


class ColorPolicy:
    def __init__(self):
        print("POLICY")
        self.data_structure = 'flattened_array'
        self._DATA_STRUCTURE_TYPES = ['flattened_array', 'interleaved_array',
                                      'tensor_array']

    def apply_normalization(self, color_array, xc, yc, zc):
        normalized_color_array = np.array([x/np.linalg.norm(x)
                        if x.any() else [0.0,0.0,0.0] for x in color_array])\
                            .reshape(xc*yc*zc, 3)
        return normalized_color_array

    def apply_dot_product(self, color_array, omf_header):
        print("STARTING POOL")
        layer_outline = getLayerOutline(omf_header)
        pool = Pool()
        color_results = [pool.apply_async(ColorPolicy.compose_arrow_interleaved_array,
                                          (color_iteration, layer_outline))
                         for color_iteration in color_array]
        new_color_matrix = []
        for result in color_results:
            interleaved = result.get(timeout=20)
            new_color_matrix.append(interleaved)
        return new_color_matrix

    @staticmethod
    def atomic_dot_product(color_vector, relative_vector_set):
        return [np.dot(color_vector, vector) for vector in relative_vector_set]

    @staticmethod
    def compose_arrow_interleaved_array(raw_vector_data, layer_outline):
        """
        this function would create the interleaved array for arrow objects i.e.
        start_vertex, stop_vertex, colorR, colorG, colorB
        :param raw_vector_data: is one iteration, matrix of colors
        :param layer_outline: is layer outline for color mask
        :return: interleaved array, array with vertices and colors interleaved
        """
        interleaved_array = []
        # get start_vertex array
        rel_set = [[1, 1, 0], [-1, 0, 1], [0, 1, 0]]
        for vector_begin, vector_tip in zip(layer_outline, raw_vector_data):
            if vector_tip.any():
                vector_tip /= np.linalg.norm(vector_tip)
                vector_begin /= np.linalg.norm(vector_begin)
                color_type = ColorPolicy.atomic_dot_product(vector_tip,
                                                relative_vector_set=rel_set)
            else:
                color_type = [0,0,0]
            interleaved_array.extend([*vector_begin, *vector_tip, *color_type])
        return interleaved_array
