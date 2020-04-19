import shutil

import numpy as np
import tensorflow as tf
from tensorflow.compat.v1 import InteractiveSession

from captcha.pretreatment import *

tmp = "tmp"
predict_list = []
tmp_image_list = ["./tmp/0.png", "./tmp/1.png", "./tmp/2.png", "./tmp/3.png"]
label_dic = {
    0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9",
    10: "a", 11: "b", 12: "c", 13: "d", 14: "e", 15: "f", 16: "g", 17: "h", 18: "i",
    19: "j", 20: "k", 21: "l", 22: "m", 23: "n", 24: "o", 25: "p", 26: "q", 27: "r",
    28: "s", 29: "t", 30: "u", 31: "v", 32: "w", 33: "x", 34: "y", 35: "z"
}


def GetPrediction(model, image):
    """
    利用训练好的模型和图像获得结果
    :param model: 模型
    :param image: 图片
    :return: 验证码结果
    """
    data = []
    if not os.path.exists(tmp):
        os.makedirs(tmp)
    image = image.convert("L")
    twoValue(image, 100)
    ClearNoise(image, 1, 1)
    image = SaveImage(image.size)
    x, y = CFS(image)
    SaveSmall(tmp, image, x)
    for image_file in tmp_image_list:
        try:
            # Load the image and convert it to grayscale
            image = cv2.imread(image_file)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Resize the letter so it fits in a 30x30 pixel box
            image = Resize2Fit(image, 30, 30)
            # Add a third channel dimension to the image to make Keras happy
            image = np.expand_dims(image, axis=2)
            data.append(image)
        except:
            print("自动识别验证码错误，请重试!")
            exit(0)
    data = np.array(data, dtype="float") / 255.0
    predictions = model.predict(data)
    try:
        for i in range(4):
            predict_list.append(np.argmax(predictions[i]))
        result = []
        for index, prediction in enumerate(predict_list):
            result.append(label_dic.get(prediction))
        result = "".join(result)
        return result
    except IndexError:
        print("验证失败")
    finally:
        shutil.rmtree(tmp)


def RecognizeCAPTCHA(captcha):
    """
    暴露给Login的接口，这里就不能把model作为参数了
    :param captcha: 验证码图片
    :return: 验证码结果
    """
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    model = tf.keras.models.load_model("./captcha/model.h5")
    result = GetPrediction(model, captcha)
    return result


