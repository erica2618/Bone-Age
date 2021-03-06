from keras.applications.resnet50 import ResNet50 as KerasResNet50
from keras.layers import (Flatten, Dense, Dropout)
from keras.models import Model

import config
from models.base_model import BaseModel


class ResNet50(BaseModel):
    noveltyDetectionLayerName = 'fc1'
    noveltyDetectionLayerName1 = 'fc2'

    def __init__(self, *args, **kwargs):
        super(ResNet50, self).__init__(*args, **kwargs)
        if not self.freeze_layers_number:
            # we chose to train the top 2 identity blocks and 1 convolution block
            self.freeze_layers_number = 80

    def _create(self):
        base_model = KerasResNet50(include_top=False, input_tensor=self.get_input_tensor())
        self.make_net_layers_non_trainable(base_model)

        x = base_model.output
        x = Flatten()(x)
        x = Dropout(0.5)(x)
        x = Dense(128, activation='elu', name=self.noveltyDetectionLayerName)(x)
        x = Dense(128, activation='elu', name=self.noveltyDetectionLayerName1)(x)
        x = Dropout(0.5)(x)
        predictions = Dense(len(config.classes), activation='softmax', name='predictions')(x)

        self.model = Model(input=base_model.input, output=predictions)
        self.model.summary()

def inst_class(*args, **kwargs):
    return ResNet50(*args, **kwargs)
