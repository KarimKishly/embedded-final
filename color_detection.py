from PIL import Image

def find_zone(image: str, color: str):
    return get_zone(get_percentage_avg_color(
        image=image,
        color=color
    ))
def get_zone(avg_percentages: list):
    print(avg_percentages)
    max_index = 0
    max_percentage = -1
    valid_zones = []
    for index in range(len(avg_percentages)):
        if avg_percentages[index][0] > 150 and avg_percentages[index][1] > 50:
            valid_zones.append(
                (index+1, avg_percentages[index])
            )
    print(valid_zones)
    for zone in valid_zones:
        if max_percentage < zone[1][1]:
            max_percentage = zone[1][1]
            max_index = zone[0]
    return max_index if max_percentage > 50 else -1
def get_percentage_avg_color(image: str, color: str):
    index = 0
    if color == 'red':
        index = 0
    if color == 'green':
        index = 1
    if color == 'blue':
        index = 2

    image = Image.open(image)
    image = image.convert('RGB')
    width, height = image.size

    zone_values = []

    height_values = [
        int(0.2*height),
        int(0.5*height),
        int(0.8*height)
    ]

    width_values = [
        range(int(width * 0.1), int(width * 0.25)),
        range(int(width * 0.4), int(width * 0.6)),
        range(int(width * 0.75), int(width * 0.9))
    ]

    for vheight in height_values:
        for vwidth in width_values:
            color_values = []
            for i in vwidth:
                pixel_rgb = image.getpixel((i, vheight))
                color_values.append(find_color_average(pixel_rgb,index))
            zone_values.append((sum([rgb[0] for rgb in color_values])/len(color_values),
                                sum([percentage[1] for percentage in color_values])/len(color_values)))
    return zone_values

def find_color_average(pixel_rgb, index):
    sum_pixel_rgb = sum(pixel_rgb)
    if sum_pixel_rgb == 0:
        return 0
    else:
        return (pixel_rgb[index], float(pixel_rgb[index]*100)/sum_pixel_rgb)
if __name__ == '__main__':
    print("Zone:", get_zone(get_percentage_avg_color(
        image='resources/red-reference8.jpg',
        color='red'
    )))
