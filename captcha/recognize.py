import shutil
import numpy as np
from captcha.pretreatment import *

from PIL import Image
import tensorflow as tf
from tensorflow.compat.v1 import InteractiveSession

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
    data = []
    if not os.path.exists(tmp):
        os.makedirs(tmp)
    image = image.convert("L")
    twoValue(image, 100)
    clearNoise(image, 1, 1)
    image = saveImage(image.size)
    x, y = cfs(image)
    saveSmall(tmp, image, x)
    for image_file in tmp_image_list:
        # Load the image and convert it to grayscale
        image = cv2.imread(image_file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Resize the letter so it fits in a 30x30 pixel box
        image = Resize2Fit(image, 30, 30)
        # Add a third channel dimension to the image to make Keras happy
        image = np.expand_dims(image, axis=2)
        data.append(image)
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
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    model = tf.keras.models.load_model("./captcha/model.h5")
    result = GetPrediction(model, captcha)
    return result


if __name__ == "__main__":
    src = Image.open("./img/test.jpeg")
    print(RecognizeCAPTCHA(src))
