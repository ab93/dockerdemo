import logging
import os.path

import torch
from torch import nn
from torch.optim import SGD
from torch.utils.data import DataLoader
from torchvision.datasets import MNIST
from torchvision.transforms.v2 import ToImage, ToDtype, Compose

from src.constants import ARTIFACT_DIR
from src.model import ConvNet

logger = logging.getLogger(__name__)

LR = 3e-4
MAX_EPOCHS = 20
BATCH_SIZE = 128
WEIGHT_DECAY = 1e-5
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"


def fit(model):
    transforms = Compose([ToImage(), ToDtype(torch.float32)])
    train_loader = DataLoader(
        MNIST("data/", train=True, transform=transforms),
        batch_size=BATCH_SIZE,
        shuffle=True,
    )
    optimizer = SGD(model.parameters(), lr=LR, momentum=0.9, weight_decay=1e-5)
    criterion = nn.NLLLoss()
    n_batches = len(train_loader)

    model.train()
    model.to(DEVICE)
    for epoch in range(MAX_EPOCHS):
        running_loss = 0.0
        for x, y in train_loader:
            optimizer.zero_grad()

            y_pred = model(x.to(DEVICE))
            loss = criterion(y_pred, y.to(DEVICE))
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        if epoch % 2 == 0:
            logger.info("Epoch %s: loss: %.5f", epoch, running_loss / n_batches)

    _path = os.path.join(ARTIFACT_DIR, "model.pth")
    # with open(_path, "wb") as f:
    #     torch.save(model.to("cpu"), f)
    logger.info("Saved model to %s", _path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fit(ConvNet())
