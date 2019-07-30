import os

def make_point(num, code, x, y, z):

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

    return "0\nSECTION\n 2\nHEADER\n" \
            "9\n$ACADVER\n 1\nAC1009\n 9\n$INSUNITS\n 70\n6\n 9\n$EXTMIN\n 10\n" \
            "0.00000000\n 20\n0.00000000\n 30\n0.00000000\n 9\n$EXTMAX\n 10\n" \
            "0.00000000\n 20\n0.00000000\n 30\n0.00000000\n 9\n$LIMMIN\n 10\n" \
            "0.00000000\n 20\n0.00000000\n 9\n$LIMMAX\n 10\n12.00000000\n 20\n"\
            "9.00000000\n0\nENDSEC\n" \
            "0\nSECTION\n 2\nTABLES\n" \
            "0\nTABLE\n 2\nLAYER\n" \
            "0\nLAYER\n 2\n0\n 70\n0\n 62\n7\n 6\nCONTINUOUS\n 0\nLAYER\n 2\n" \
            "Points\n 70\n0\n 62\n7\n 6\nCONTINUOUS\n0\nENDTAB\n0\nENDSEC\n" \
            "0\nSECTION\n 2\nBLOCKS\n" \
            "0\nBLOCK\n 8\n0\n 70\n2\n 3\nPOINTNAMEBLOCK\n" \
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

def make_dxf(pnt_file):

    pnt_dir = os.path.dirname(pnt_file)
    dxf_dir = os.path.join(os.path.dirname(pnt_dir), 'UDXF')
    dxf_name = os.path.splitext(os.path.basename(pnt_file))[0] + ".DXF"
    dxf_file = os.path.join(dxf_dir, dxf_name)
    with open(dxf_file, 'w') as dxf:
        with open(pnt_file) as pnt:
            dxf.write(begin_dxf())
            for i, line in enumerate(pnt):
                data = line.strip().rstrip(',').split(',')
                x, y, z = format_numbers(data)
                pnt_data = make_point(i + 1, data[0], x, y, z)
                dxf.write(pnt_data)
            dxf.write(end_dxf())
    return

if __name__ == '__main__':

    for root, ds, fs in os.walk(os.getcwd()):
        for f in fs:
            if f.endswith('.pnt'):
                path = os.path.join(root, f)
                make_dxf(path)
