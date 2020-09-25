import os.path
from comp_process_local import id_local_flow as comp_flow
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--front", help="Path to the front image.")
parser.add_argument("-b", "--back", help="Path to the back image.")

args = parser.parse_args()

    
def main():
    if not args.front or not args.back:
        print('Error, imagen vacia')
        return -1
    if os.path.exists(args.front) and os.path.exists(args.back):
        comp_prcss = comp_flow(front_img_path=args.front,
                                back_img_path=args.back,
                                f_heigths = [200, 700, 900],
                                b_heigths = [200, 700, 900])
    data_dict = comp_prcss.id_wrapper()
    print(data_dict)
    validation = comp_prcss.call_api()
    if validation.json():
        val = validation.json()
        print(val)
        with open('results/result.html', 'w') as filename:
            filename.write(val['content'])
        print(val['valid_yn'])
    else:
        print('NOT RESULT')
    
if __name__ == '__main__':
    main()
