import os
import numpy as np


def make_pointnameblock(num, code, x, y, z):

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


def begin_dxf():

    return "0\nSECTION\n2\nHEADER\n 9\n$ACADVER\n 1\nAC1009\n 9\n$EXTMIN\n 10\n" \
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


def end_dxf():

    return "0\nENDSEC\n0\nEOF\n"


def format_numbers(data):

    return float(data[1]), float(data[2]), float(data[3])


def format_fname(fname, ftype=None):

    fnew = '{}.{}'.format(os.path.splitext(fname)[0], ftype.upper())
    if os.path.exists(fnew):
        index = 1
        ftemplate = '{}({{}}).{}'.format(os.path.splitext(fname)[0], ftype.upper())
        fnew = ftemplate.format(index)
        while os.path.exists(fnew):
            index += 1
            fnew = ftemplate.format(index)
        return fnew
    else:
        return fnew


def get_coords(content):

    desc = content[54].strip().upper()
    e = float(content[2])
    n = float(content[4])
    z = float(content[6])

    return [desc, e, n, z]


def get_points_nikon(line):

    data = line.rstrip().split(',')[1:]
    n = data[0]
    e = data[1]
    z = data[2]
    desc = data[3]

    return '{},{},{},{}'.format(desc, e, n, z)


def get_points_topcon(line):

    return line.rstrip().rstrip(',')


def get_points_dxf(lines):

    points = []
    for i, line in enumerate(lines):
        if i > 164:
            line = line.strip()
            if 'POINTNAMEBLOCK' in line:
                pnt_line = get_coords(lines[i:i+59])
                line = ','.join(str(i) for i in pnt_line)
                points.append(line)
                
    return points


def get_points(path, ts):
    
    points = []
    with open(path) as f:
        if ts.upper() == 'NIKON':
            for line in f:
                pnt_line = get_points_nikon(line)
                points.append(pnt_line)
        elif ts.upper() == 'TOPCON':
            for line in f:
                pnt_line = get_points_topcon(line)
                points.append(pnt_line)
        elif ts.upper() == 'DXF':
            lines = f.readlines()
            points = get_points_dxf(lines)

    return points


def make_dxf(fname, points):

    dxf_fname = format_fname(fname, 'dxf')
    with open(dxf_fname, 'w') as dxf:
        dxf.write(begin_dxf())
        for i, pnt in enumerate(points):
            data = pnt.split(',')
            x, y, z = format_numbers(data)
            pnt_data = make_pointnameblock(i + 1, data[0], x, y, z)
            dxf.write(pnt_data)
        dxf.write(end_dxf())

    return dxf_fname


def make_pnt(fname, points):

    pnt_fname = format_fname(fname, 'pnt')    
    with open(pnt_fname, 'w') as pnt:
        for point in points:
            data = point.split(',')
            x, y, z = format_numbers(data)
            pnt.write('{},{:.4f},{:.4f},{:.4f},\n'.format(data[0], x, y, z))

    return pnt_fname


def processor(fname):

    points = []
    ftypes = ['.csv', '.pnt', '.dxf']
    fl = fname.lower()
    if os.path.splitext(fl)[1] in ftypes:
        path = os.path.join('./', fname)
        try:
            if fl.endswith('.csv'):
                points = get_points(path, 'Nikon')
            elif fl.endswith('.pnt'):
                points = get_points(path, 'TopCon')
            else:
                points = get_points(path, 'DXF')
        except IOError:
            return None

    return points


def convert_to_dxf(fname):

    f_lower = fname.lower()
    if f_lower.endswith('.csv') or f_lower.endswith('.pnt'):
        points = processor(fname)
        if points:
            dxf_name = make_dxf(fname, points)
            print '\n  {} was converted to {}'.format(fname, dxf_name)
        else:
            print '\n  {} does not exist.'.format(fname)
            convert_single('dxf')
    elif f_lower.endswith('.dxf') or f_lower.endswith('.py'):
        pass
    else:
        print '\n  {} is not a valid file type.'.format(fname)
        convert_single('dxf')
        
    return


def convert_to_pnt(fname):

    f_lower = fname.lower()
    if f_lower.endswith('.csv') or f_lower.endswith('.dxf'):
        points = processor(fname)
        if points:
            pnt_name = make_pnt(fname, points)
            print '\n  {} was converted to {}'.format(fname, pnt_name)
        else:
            print '\n  {} does not exist.'.format(fname)
            convert_single('pnt')
    elif f_lower.endswith('.pnt') or f_lower.endswith('.py'):
        pass
    else:
        print '\n  {} is not a valid file type.'.format(fname)
        convert_single('pnt')

    return


def convert_single(ftype=None):

    fname = raw_input('Enter the file to convert: ')
    if fname:
        if ftype == 'dxf':
            convert_to_dxf(fname)
        elif ftype == 'pnt':
            convert_to_pnt(fname)

    return


def convert_all(ftype=None):

    for root, dirs, fnames in os.walk('./'):
        for fname in fnames:
            if ftype == 'dxf':
                convert_to_dxf(fname)
            elif ftype == 'pnt':
                convert_to_pnt(fname)

    return


def get_lines(fname, search=None, datum=True, multi=False):

    coords = {}
    x = []
    y = []
    z = []
    points = processor(fname)
    if points:
        for line in points:
            data = None
            if datum and search:
                if search in line and 'datum' in line.lower():
                    print line.replace(',', ', ')
                    split_line = line.split(',')
                    pnt_name = split_line[0]
                    data = format_numbers(split_line)
            elif datum:
                if 'datum' in line.lower():
                    print line.replace(',', ', ')
                    split_line = line.split(',')
                    pnt_name = split_line[0]
                    data = format_numbers(split_line)
            else:
                if search in line:
                    print line.replace(',', ', ')
                    split_line = line.split(',')
                    pnt_name = split_line[0]
                    data = format_numbers(split_line)
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
    print '\n{} result(s) found for {}:\n'.format(len(x), name)
    print '\t\tNorthing\tEasting\t\tElevation'
    print '-' * 60
    print 'Mean\t\t{:.3f}\t{:.3f}\t{:.3f}'.format(np.mean(y), np.mean(x), np.mean(z))
    print 'Std Dev.\t{:.3f}\t\t{:.3f}\t\t{:.3f}'.format(np.std(y), np.std(x), np.std(z))
    print
    print 'Min\t\t{:.3f}\t{:.3f}\t{:.3f}'.format(min(y), min(x), min(z))    
    print 'Max\t\t{:.3f}\t{:.3f}\t{:.3f}'.format(max(y), max(x), max(z))

    return


def get_multi_stats(datums):

    for datum, coords in datums.iteritems():
        values = (coords['X'], coords['Y'], coords['Z'])
        get_stats(values, datum)

    return


def choices(fname=None):

        if fname:
            print '\nWithin {}:'.format(fname)
        print
        print ' 1: Get statistics for a datum'
        print ' 2: Get statistics for all datums'
        print ' 3: Get statistics for a point'
        
        return


def get_stats_single():

    fname = raw_input('Enter the file to analyze: ')
    if fname:
        options = (1, 2, 3)
        option = 1
        while option in options:
            try:
                choices(fname)
                option = int(raw_input('\nSelect an option: '))
            except ValueError:
                return
            if option == 1:
                datum = raw_input('\nEnter a datum to search: ')
                if datum:
                    print '\nResults:\n'
                    values = get_lines(fname, search=datum)
                    if values[0]:
                        get_stats(values, datum)
                    else:
                        print 'No results found.'
            elif option == 2:
                print '\nResults:\n'
                coords = get_lines(fname, multi=True)
                if coords:
                    get_multi_stats(coords)
                else:
                    print 'No results found.'
            elif option == 3:
                point = raw_input('\nEnter a point to search: ')
                if point:
                    print '\nResults:\n'
                    values = get_lines(fname, search=point, datum=False)
                    if values[0]:
                        get_stats(values, point)
                    else:
                        print 'No results found.'
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
            option = int(raw_input('\nSelect an option: '))
        except ValueError:
            return
        if option == 1:
            datum = raw_input('\nEnter a datum to search: ')
            if datum:
                print '\nResults:\n'
                for root, dirs, fnmes in os.path.walk('./'):
                    for fname in fnames:
                        values = get_lines(fname, search=datum)
                        all_x.append(values[0])
                        all_y.append(values[1])
                        all_z.append(values[2])
                if all_x:
                    values = (all_x, all_y, all_z)
                    get_stats(values, datum)
                else:
                    print 'No results found.'
        elif option == 2:
            print '\nResults:\n'
            coords = get_lines(fname, multi=True)
            if coords:
                get_multi_stats(coords)
            else:
                print 'No results found.'
        elif option == 3:
            point = raw_input('\nEnter a point to search: ')
            if point:
                print '\nResults:\n'
                values = get_lines(fname, search=point, datum=False)
                if values[0]:
                    get_stats(values, point)
                else:
                    print 'No results found.'
        else:
            return
    return



def main():

    def choices():

        print
        print '--------------------------'
        print 'Mt Lykaion Survey Program'
        print '--------------------------\n'
        print 'Current folder: {}\n'.format(os.getcwd())
        print 'Within the current folder:\n'
        print ' 1: Convert a file to DXF format'
        print ' 2: Convert all files to DXF format'
        print ' 3: Convert a file to PNT format'
        print ' 4: Convert all files to PNT format'
        print ' 5: Get point statistics from a file'
        print ' 6: Get point statistics from all files'

        return

    options = (1, 2, 3, 4, 5, 6)
    option = 1

    while option in options:

        choices()
        try:
            option = int(raw_input('\nSelect an option: '))
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

    main()

