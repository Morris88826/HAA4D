import glob
import ffmpeg

def convert(folder):
    view = folder.split('/')[-1]
    (
        ffmpeg
        .input(folder+'/*.png', pattern_type='glob', framerate=25)
        .output(folder+'/{}.mp4'.format(view))
        .run()
    )

if __name__ == '__main__':

    class_name = 'bench_dip'
    for folder in glob.glob('./results/views/{}/*/*'.format(class_name)):
        convert(folder)