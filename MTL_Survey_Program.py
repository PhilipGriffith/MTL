import os
import numpy as np


class Utils:

    @staticmethod
    def convert2float(data):
        return float(data[1]), float(data[2]), float(data[3])

    @staticmethod
    def format_fname(fname, ftype):
        fname = os.path.splitext(fname)[0]
        fnew = '{}.{}'.format(fname, ftype)
        if os.path.exists(fnew):
            index = 1
            ftemplate = '{}({{}}).{}'.format(fname, ftype)
            fnew = ftemplate.format(index)
            while os.path.exists(fnew):
                index += 1
                fnew = ftemplate.format(index)
            return fnew
        else:
            return fnew


class Data:

    def __init__(self, points=None):
        self.points = []
        if points:
            self.add(points)

    def add(self, data):
        if os.path.isdir(data):
            for root, dirs, fs in os.walk(data):
                for f in fs:
                    ftype = self._valid_ftype(f)
                    if ftype:
                        fpath = os.path.join(root, f)
                        pnt = self._get_data(fpath, ftype)
                        self.points.extend(pnt)
                        print('{} added'.format(fpath))
        elif os.path.isfile(data):
            ftype = self._valid_ftype(data)
            if ftype:
                pnt = self._get_data(data, ftype)
                self.points.extend(pnt)
                print('{} added'.format(data))
        return

    def _get_data(self, fpath, ftype):

        data = []
        with open(fpath) as f:
            if ftype == '.pnt':
                for line in f:
                    pnt = self.get_data_topcon(line)
                    data.append(pnt)
            elif ftype == '.dxf':
                lines = f.readlines()
                data = self._get_data_dxf(lines)
            elif ftype == '.csv':
                for line in f:
                    pnt = self._get_data_nikon(line)
                    data.append(pnt)
        return data

    @staticmethod
    def _get_data_topcon(line):

        return line.rstrip().rstrip(',')

    def _get_data_dxf(self, lines):

        data = []
        for i, line in enumerate(lines):
            if i > 164:
                try:
                    line = line.strip()
                    if 'POINTNAMEBLOCK' in line:
                        pnt_line = self._get_coords(lines[i:i + 59])
                        if pnt_line[0] == 'ACDBENTITY':
                            pnt_line[0] = lines[i + 108].strip().upper()
                        line = ','.join(str(i) for i in pnt_line)
                        data.append(line)
                except ValueError:
                    pass
        return data

    @staticmethod
    def _get_data_nikon(line):

        data = line.rstrip().split(',')[1:]
        n = data[0]
        e = data[1]
        z = data[2]
        desc = data[3]
        return '{},{},{},{}'.format(desc, e, n, z)

    @staticmethod
    def _get_coords(lines):

        desc = lines[54].strip().upper()
        e = float(lines[2])
        n = float(lines[4])
        z = float(lines[6])
        return [desc, e, n, z]

    @staticmethod
    def _valid_ftype(f):
        valid_ftypes = ('.dxf', '.pnt', '.csv')
        ext = os.path.splitext(f)[1]
        return ext if ext in valid_ftypes else None


class DXF(Utils):

    def __init__(self, points):
        self.points = points
        self.start = "0\nSECTION\n2\nHEADER\n 9\n$ACADVER\n 1\nAC1009\n 9\n$EXTMIN\n 10\n" \
            "0.00000000\n 20\n0.00000000\n 30\n0.00000000\n 9\n$EXTMAX\n 10\n" \
            "0.00000000\n 20\n0.00000000\n 30\n0.00000000\n 9\n$LIMMIN\n 10\n" \
            "0.00000000\n 20\n0.00000000\n 9\n$LIMMAX\n 10\n12.00000000\n 20\n"\
            "9.00000000\n0\nENDSEC\n0\nSECTION\n2\nTABLES\n 0\nTABLE\n 2\nLAYER\n" \
            " 0\nLAYER\n 2\n0\n 70\n0\n 62\n7\n 6\nCONTINUOUS\n 0\nLAYER\n 2\n" \
            "Points\n 70\n0\n 62\n7\n 6\nCONTINUOUS\n0\nENDTAB\n0\nENDSEC\n0\n" \
            "SECTION\n 2\nBLOCKS\n 0\nBLOCK\n 8\n0\n 70\n2\n 3\nPOINTNAMEBLOCK\n" \
            " 2\nPOINTNAMEBLOCK\n 10\n0.00000000\n 20\n0.00000000\n 30\n0.00000000\n" \
            " 0\nPOINT\n 8\n0\n 10\n0.00000000\n 20\n0.00000000\n 30\n0.00000000\n" \
            " 0\nATTDEF\n 8\n0\n 40\n5.00000000\n 70\n0\n 3\nPOINT_NUMBER\n 2\n" \
            "POINT_NUMBER\n 1\n1\n 10\n0.00000000\n 20\n0.00000000\n 30\n0.00000000\n" \
            " 0\nATTDEF\n 8\n0\n 40\n0.01000000\n 70\n0\n 3\nELEVATION\n 2\n" \
            "ELEVATION\n 1\n\n 10\n0.00000000\n 20\n-0.02000000\n 30\n0.00000000\n" \
            " 0\nATTDEF\n 8\n0\n 40\n0.01000000\n 70\n0\n 3\nDESCRIPTION\n 2\n" \
            "DESCRIPTION\n 1\n\n 10\n0.00000000\n 20\n-0.04000000\n 30\n0.00000000\n" \
            "0\nENDBLK\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n"
        self.end = "0\nENDSEC\n0\nEOF\n"

    @staticmethod
    def _make_pointnameblock(num, code, x, y, z):

        x_offset = x + 0.005
        point_number_y = y + 0.015
        elevation_y = y - 0.005
        description_y = y - 0.025

        point_code = " 0\nINSERT\n 8\nPoints\n 66\n1\n 2\n" \
                     "POINTNAMEBLOCK\n 10\n" \
                     "{2:.4f}\n" \
                     " 20\n" \
                     "{3:.4f}\n" \
                     " 30\n" \
                     "{4:.4f}\n" \
                     " 0\nATTRIB\n 8\nPoints\n 40\n0.01000000\n" \
                     " 70\n0\n 2\n" \
                     "POINT_NUMBER\n 1\n" \
                     "{0}\n" \
                     " 10\n" \
                     "{5:.4f}\n" \
                     " 20\n" \
                     "{6:.4f}\n" \
                     " 30\n" \
                     "{4:.4f}\n" \
                     " 0\nATTRIB\n 8\nPoints\n 40\n0.01000000\n" \
                     " 70\n0\n 2\n" \
                     "ELEVATION\n 1\n" \
                     "{4:.3f}\n" \
                     " 10\n" \
                     "{5:.4f}\n" \
                     " 20\n" \
                     "{7:.4f}\n" \
                     " 30\n" \
                     "{4:.4f}\n" \
                     " 0\nATTRIB\n 8\nPoints\n 40\n0.01000000\n" \
                     " 70\n0\n 2\n" \
                     "DESCRIPTION\n 1\n" \
                     "{1}\n" \
                     " 10\n" \
                     "{5:.4f}\n"  \
                     " 20\n" \
                     "{8:.4f}\n" \
                     " 30\n" \
                     "{4:.4f}\n" \
                     "0\nSEQEND\n 6\nCONTINUOUS\n".format(num, code, x, y, z,
                                                          x_offset, point_number_y,
                                                          elevation_y, description_y)
        return point_code

    def create(self, fname):
        dxf_fname = self.format_fname(fname, 'dxf')
        with open(dxf_fname, 'w') as dxf:
            dxf.write(self.start)
            for i, pnt in enumerate(self.points):
                data = pnt.split(',')
                x, y, z = self.convert2float(data)
                pnt_data = self._make_pointnameblock(i + 1, data[0], x, y, z)
                dxf.write(pnt_data)
            dxf.write(self.end)
        return


class PNT(Utils):

    def __init__(self, points):
        self.points = points

    def create(self, fname):
        pnt_fname = self.format_fname(fname, 'pnt')
        with open(pnt_fname, 'w') as pnt:
            for point in self.points:
                data = point.split(',')
                x, y, z = self.convert2float(data)
                pnt.write('{},{:.4f},{:.4f},{:.4f},\n'.format(data[0], x, y, z))
        return


def get_lines(fname, search=None, datum=True, multi=False):

    coords = {}
    x = []
    y = []
    z = []
    for line in points:
            data = None
            if datum and search:
                if search in line and 'datum' in line.lower():
                    print(line.replace(',', ', '))
                    split_line = line.split(',')
                    pnt_name = split_line[0]
                    data = convert2float(split_line)
            elif datum:
                if 'datum' in line.lower():
                    print(line.replace(',', ', '))
                    split_line = line.split(',')
                    pnt_name = split_line[0]
                    data = convert2float(split_line)
            else:
                if search in line:
                    print(line.replace(',', ', '))
                    split_line = line.split(',')
                    pnt_name = split_line[0]
                    data = convert2float(split_line)
            if data:
                if multi:
                    if pnt_name in coords:
                        coords[pnt_name]['X'].append(data[0])
                        coords[pnt_name]['Y'].append(data[1])
                        coords[pnt_name]['Z'].append(data[2])
                    else:
                        coords[pnt_name] = {'X': [], 'Y': [], 'Z': []}
                        coords[pnt_name]['X'] = [data[0]]
                        coords[pnt_name]['Y'] = [data[1]]
                        coords[pnt_name]['Z'] = [data[2]]
                else:
                    x.append(data[0])
                    y.append(data[1])
                    z.append(data[2])
    if multi:
        return coords
    else:
        return x, y, z


def get_stats(values, name):

    x, y, z = values
    print('\n{} result(s) found for {}:\n'.format(len(x), name))
    print('\t\tNorthing\tEasting\t\tElevation')
    print('-' * 60)
    print('Mean\t\t{:.3f}\t{:.3f}\t{:.3f}'.format(np.mean(y), np.mean(x), np.mean(z)))
    print('Std Dev.\t{:.3f}\t\t{:.3f}\t\t{:.3f}'.format(np.std(y), np.std(x), np.std(z)))
    print()
    print('Min\t\t{:.3f}\t{:.3f}\t{:.3f}'.format(min(y), min(x), min(z)))
    print('Max\t\t{:.3f}\t{:.3f}\t{:.3f}'.format(max(y), max(x), max(z)))

    return


def get_multi_stats(datums):

    for datum, coords in datums.iteritems():
        values = (coords['X'], coords['Y'], coords['Z'])
        get_stats(values, datum)

    return


def choices(fname=None):

        if fname:
            print('\nWithin {}:'.format(fname))
        print()
        print(' 1: Get statistics for a datum')
        print(' 2: Get statistics for all datums')
        print(' 3: Get statistics for a point')
        
        return


def get_stats_single():

    fname = input('Enter the file to analyze: ')
    if fname:
        options = (1, 2, 3)
        option = 1
        while option in options:
            try:
                choices(fname)
                option = int(input('\nSelect an option: '))
            except ValueError:
                return
            if option == 1:
                datum = input('\nEnter a datum to search: ')
                if datum:
                    print('\nResults:\n')
                    values = get_lines(fname, search=datum)
                    if values[0]:
                        get_stats(values, datum)
                    else:
                        print('No results found.')
            elif option == 2:
                print('\nResults:\n')
                coords = get_lines(fname, multi=True)
                if coords:
                    get_multi_stats(coords)
                else:
                    print('No results found.')
            elif option == 3:
                point = input('\nEnter a point to search: ')
                if point:
                    print('\nResults:\n')
                    values = get_lines(fname, search=point, datum=False)
                    if values[0]:
                        get_stats(values, point)
                    else:
                        print('No results found.')
            else:
                return
    return


def get_stats_all():
    # TODO This still needs work
    options = (1, 2, 3)
    option = 1
    while option in options:
        all_x = []
        all_y = []
        all_z = []
        try:
            choices()
            option = int(input('\nSelect an option: '))
        except ValueError:
            return
        if option == 1:
            datum = input('\nEnter a datum to search: ')
            if datum:
                print('\nResults:\n')
                for root, dirs, fnames in os.path.walk('./'):
                    for fname in fnames:
                        values = get_lines(fname, search=datum)
                        all_x.append(values[0])
                        all_y.append(values[1])
                        all_z.append(values[2])
                if all_x:
                    values = (all_x, all_y, all_z)
                    get_stats(values, datum)
                else:
                    print('No results found.')
        elif option == 2:
            print('\nResults:\n')
            coords = get_lines(fname, multi=True)
            if coords:
                get_multi_stats(coords)
            else:
                print('No results found.')
        elif option == 3:
            point = input('\nEnter a point to search: ')
            if point:
                print('\nResults:\n')
                values = get_lines(fname, search=point, datum=False)
                if values[0]:
                    get_stats(values, point)
                else:
                    print('No results found.')
        else:
            return
    return


def main():

    def choices():

        print()
        print('--------------------------')
        print('Mt Lykaion Survey Program')
        print('--------------------------\n')
        print('Current folder: {}\n'.format(os.getcwd()))
        print('Within the current folder:\n')
        print(' 1: Convert a file to DXF format')
        print(' 2: Convert all files to DXF format')
        print(' 3: Convert a file to PNT format')
        print(' 4: Convert all files to PNT format')
        print(' 5: Get point statistics from a file')
        print(' 6: Get point statistics from all files')

        return

    options = (1, 2, 3, 4, 5, 6)
    option = 1

    while option in options:

        choices()

        try:
            option = int(input('\nSelect an option: '))
        except ValueError:
            return

        if option == 1:
            convert_single('dxf')
        elif option == 2:
            convert_all('dxf')
        elif option == 3:
            convert_single('pnt')
        elif option == 4:
            convert_all('pnt')
        elif option == 5:
            get_stats_single()
        elif option == 6:
            get_stats_all()
        else:
            return


if __name__ == '__main__':

    # main()
    path = 'TEST'
    d = os.path.join(path, 'DIR')
    f = os.path.join(path, '07-19-18.dxf')
    dxf = Data(f)