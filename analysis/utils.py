from PIL import Image
from io import BytesIO

def save_figure_as_tiff(figure, output_file_path, **kwargs):
    ''' saves the matplotlib figure to the output_file_path with the original options

    Note that the format parameter should NOT be passed to this command
    '''

    in_mem_png = BytesIO()
    kwargs['format'] = "png"
    figure.savefig(in_mem_png, **kwargs)
    pil_png = Image.open(in_mem_png)
    pil_png.save(output_file_path, "TIFF")
    in_mem_png.close()
