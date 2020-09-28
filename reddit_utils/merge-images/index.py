from PIL import Image
import sys
import os

ec_logos__dir_path = os.path.join(os.getcwd(), '..', '..', 'ec_clubs_logos')
el_logos_dir_path = os.path.join(os.getcwd(), '..', '..', 'el_clubs_logos')

ec_logos_paths = [os.path.join(ec_logos__dir_path, f) for f in os.listdir(
    ec_logos__dir_path) if os.path.isfile(os.path.join(ec_logos__dir_path, f))]
el_logos_paths = [os.path.join(el_logos_dir_path, f) for f in os.listdir(
    el_logos_dir_path) if os.path.isfile(os.path.join(el_logos_dir_path, f))]

ec_images = [(os.path.splitext(f)[0].split('\\')[-1], Image.open(f))
             for f in ec_logos_paths]
el_images = [(os.path.splitext(f)[0].split('\\')[-1], Image.open(f))
             for f in el_logos_paths]

ec_widths, ec_heights = zip(*(i[1].size for i in ec_images))
el_widths, el_heights = zip(*(i[1].size for i in el_images))

total_width = max(sum(ec_widths), sum(el_widths))
max_height = max(ec_heights + el_heights)

new_im = Image.new('RGBA', (total_width, max_height * 2))

placeholder_css = ".md a[href*=\"clubcode={code}\"]::before {{\n\tbackground-position: {x}px {y}px;\n}}"
placeholder_css_base = ".md a[href*=\"clubcode={code}\"]::before"
placeholder_css_base_before = ".md a[href*=\"clubcode={code}\"]"

css_rules = list()
css_base_rules = list()
css_base_before_rules = list()

x_offset = 0
for idx, (club_code, im) in enumerate(ec_images):
    new_im.paste(im, (x_offset, 0))
    x_offset += im.size[0]

    css_rules.append(placeholder_css.format(
        code=club_code, x=str(idx * -22), y=0))
    css_base_rules.append(placeholder_css_base.format(code=club_code))
    css_base_before_rules.append(
        placeholder_css_base_before.format(code=club_code))

x_offset = 0
for idx, (club_code, im) in enumerate(el_images):
    new_im.paste(im, (x_offset, max_height))
    x_offset += im.size[0]

    css_rules.append(placeholder_css.format(
        code=club_code, x=str(idx * -22), y="22"))
    css_base_rules.append(placeholder_css_base.format(code=club_code))
    css_base_before_rules.append(
        placeholder_css_base_before.format(code=club_code))

print('\n\n'.join(css_rules))
print()
# print(',\n'.join(css_base_rules))
print()
# print(',\n'.join(css_base_before_rules))


new_im.save('spritesheet.png')
