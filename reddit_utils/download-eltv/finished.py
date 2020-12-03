import sys
import subprocess
import os


def merge_audio_with_video(ts_file, aac_file, output_file):
    subprocess.call(['ffmpeg', '-i', ts_file, '-i', aac_file, '-map', '0:V:0', '-map',
                     '1:a:0', '-c', 'copy', '-f', 'mp4', '-movflags', '+faststart', output_file])


def concat_mp4_files(hl_dir, out_dir):
    input_file = os.path.join(hl_dir, 'input.txt')
    output_file = os.path.join(out_dir, 'output.mp4')

    subprocess.call(['ffmpeg', '-f', 'concat', '-safe', '0',
                     '-i', input_file, '-c', 'copy', output_file])


def write_input_file(hl_dir, output_files):
    input_file = os.path.join(hl_dir, 'input.txt')
    with open(input_file, mode='w') as ifile:
        for f in output_files:
            ifile.write('file \'{}\'\n'.format(f))


def generate_mp4_files(hl_dir, out_dir):
    all_files = [f for f in os.listdir(hl_dir) if os.path.isfile(
        os.path.join(os.path.join(hl_dir, f)))]

    aac_files = list(filter(lambda x: x.endswith('.aac'), all_files))
    ts_files = list(filter(lambda x: x.endswith('.ts'), all_files))

    # Creates a tuple association between the audio and transport streaming file
    # Assumes sorted list
    zipped_files = zip(aac_files, ts_files)

    # Will later be used to create the input file for the concat command
    output_files = list()

    for z in zipped_files:
        aac_file = os.path.join(hl_dir, z[0])
        ts_file = os.path.join(hl_dir, z[1])

        filename = os.path.splitext(z[0])[0] + '.mp4'
        output_file = os.path.join(out_dir, filename)
        output_files.append(output_file)

        merge_audio_with_video(ts_file, aac_file, output_file)

    return output_files


if __name__ == '__main__':
    hl_dir = os.path.join(os.getcwd(), sys.argv[1])
    out_dir = os.path.join(hl_dir, 'out')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    output_files = generate_mp4_files(hl_dir, out_dir)
    write_input_file(hl_dir, output_files)
    concat_mp4_files(hl_dir, out_dir)
