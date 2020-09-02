from scripts.complete_validation.comp_process import id_all_flow as comp_flow
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--front", help="Path to the front image.")
parser.add_argument("-b", "--back", help="Path to the back image.")

args = parser.parse_args()

def main():

    comp_prcss = comp_flow(front_img_path=args.front,
                            back_img_path=args.back,
                            f_heigths = [200, 700, 900],
                            b_heigths = [200, 700, 900])
    _, validation = comp_prcss.id_wrapper()
    
    if len(validation[1]) > 0:
        with open('results/result.html', 'w') as filename:
            filename.write(str(validation[0]))
        print(validation[1])
    
  
    else:
        print('NOT RESULT')
    
if __name__ == '__main__':
    main()