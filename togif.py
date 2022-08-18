import imageio
import os
# 用来把图片转化为动图，但是图片不够多
dirr = 'D:\\PycharmProjects\\webspider\\pictures'


def main():
    duration = 0.05  # 每秒20帧
    image_list = os.listdir(dirr+'/')
    gif_name = dirr+'.gif'
    create_gif(image_list, gif_name, duration)


def create_gif(image_list, gif_name, duration=0.05):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(dirr+'/'+image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return


if __name__ == '__main__':
    main()
