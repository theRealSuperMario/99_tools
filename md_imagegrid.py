import os
import glob
import click


def gen_header(n_cols):
    header = "| " * (n_cols - 1) + '|'
    header += "\n"
    header += "|:-------------------------:" * (n_cols - 1) + "|"
    return header

CELL_TEMPLATE = '|<img width="{}" alt="{}" src="{}">  {}'

def make_cell(width, img_fname):
    return CELL_TEMPLATE.format(width, img_fname, img_fname, img_fname)



@click.command()
@click.argument('out-file')
@click.argument('img-dir')
@click.argument('n-cols', type=int)
@click.argument('cell-width', type=int)
@click.option('--skip', type=int, default=4)
def main(out_file, img_dir, n_cols, cell_width, skip):
    png_files = glob.glob(os.path.join(img_dir, '*.png'))
    numbers = list(map(lambda x: int(x[-11:-4]), png_files))ga
    _dict = dict(zip(numbers, png_files))
    unique_numbers = set(numbers)
    unique_numbers = sorted(list(unique_numbers))
    with open(os.path.join(img_dir, out_file), 'w') as f:
        header = gen_header(n_cols)
        f.write(header)
        f.write('\n')
        s = 0
        for un in unique_numbers:
            if s % skip == 0:
                found_files = list(filter(lambda x: '{:07d}.png'.format(un) in x, png_files))
                found_files = list(map(lambda x: os.path.basename(x), found_files))
                line = [make_cell(cell_width, f) for f in found_files]
                diff = n_cols - len(line)
                # assert diff >= 0
                # if diff > 0:
                #     line += ['| '] * diff
                line = ' '.join(line) + '|'
                f.write(line)
                f.write("\n")
                s = 0
            s += 1

if __name__ == '__main__':
    main()