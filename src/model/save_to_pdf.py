from fpdf import FPDF
import platform

def save_pdf_images(data, titles, path, epoch, step):
    for idx in range(data.shape[0]):
        image = data[idx]
        path_image = f'{path}/tmp/{idx}.png' 
        vutils.save_image(image, path_image, normalize=True)
    document = FPDF()

    if platform.system() == 'Windows':
        document.add_font('current_font', '', r"c:\WINDOWS\Fonts\arial.ttf", uni=True)
    if platform.system() == 'Linux':
        document.add_font('current_font','', '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf', uni=True)

    document.set_font('current_font', size=6)

    startPoint = (6, 6)
    image_size = 60
    block_size = 70
    image_per_line = 3
    line_per_page = 4

    for image_idx in range(data.shape[0]):
        if image_idx % (line_per_page * image_per_line) == 0:
            document.add_page()
        elif image_idx % image_per_line == 0 and image_idx > 0:
            document.ln()
      
        index_in_page = image_idx % (line_per_page * image_per_line)
        line = index_in_page // image_per_line
        idx = index_in_page % image_per_line

        document.text(idx * block_size + startPoint[0], line * block_size + startPoint[1], titles[image_idx])
        document.image(f'{path}/tmp/{image_idx}.png', x = idx * block_size + startPoint[0], y = line * block_size + startPoint[1] + 3, w = image_size, h = image_size)
     
    document.output(f'{path}/{config["MODEL_NAME"]}_{epoch}_{step}.pdf')