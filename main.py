import click
from utils.detection import process_video, process_image

@click.group()
def cli():
    "CLI Tool for License Plate Detection"
    pass

@cli.command()
@click.argument('video_path', type=click.Path(exists=True))
@click.option('--method', type=click.Choice(['easyocr', 'tesseract'], case_sensitive=False), default='easyocr',
              help="OCR method to use for license plate detection")
def video(video_path, method):
    "Process a video to detect license plates."
    click.echo(f"Processing video: {video_path} with method: {method}")
    process_video(video_path, method=method)

@cli.command()
@click.argument('image_path', type=click.Path(exists=True))
@click.option('--method', type=click.Choice(['easyocr', 'tesseract'], case_sensitive=False), default='easyocr',
              help="OCR method to use for license plate detection")
def frame(image_path, method):
    "Process an image to detect license plates."
    click.echo(f"Processing image: {image_path} with method: {method}")
    process_image(image_path, method=method)

if __name__ == "__main__":
    cli()
