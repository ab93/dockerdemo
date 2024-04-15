import os
import logging
import torch
from PIL.Image import Image
from torch import nn
from torch.utils.data import DataLoader
from torchvision.datasets import MNIST
from torchvision.transforms.v2 import Compose, ToImage, ToDtype
from torchvision.transforms.v2.functional import pil_to_tensor
from argmax_cpp import argmax

from src.constants import ARTIFACT_DIR, DATA_DIR

logger = logging.getLogger(__name__)

BATCH_SIZE = 64
DEVICE = "cpu"


def get_test_score() -> tuple[float, float]:
    model = torch.load(os.path.join(ARTIFACT_DIR, "model.pth"))
    transforms = Compose([ToImage(), ToDtype(torch.float32)])
    test_loader = DataLoader(
        MNIST(DATA_DIR, train=False, transform=transforms), batch_size=BATCH_SIZE
    )
    model.eval()
    criterion = nn.NLLLoss()

    loss = 0.0
    correct = 0
    n_batches = len(test_loader)
    n_imgs = len(test_loader.dataset)

    with torch.no_grad():
        for x, labels in test_loader:
            out = model(x.to(DEVICE))
            loss += criterion(out, labels.to(DEVICE)).item()

            y_pred = torch.argmax(out, dim=1)
            correct += y_pred.eq(labels.to(DEVICE)).sum()

    loss /= n_batches
    accuracy = correct / n_imgs * 100
    logger.info("Loss: %.4f, accuracy: %.2f%", loss, accuracy)
    return loss, accuracy


def classify_image(image: Image):
    x = pil_to_tensor(image)
    tx = Compose([ToImage(), ToDtype(torch.float32)])
    x = tx(x).unsqueeze(0)
    model = torch.load(os.path.join(ARTIFACT_DIR, "model.pth"))
    with torch.no_grad():
        out = model(x)
        prediction = argmax(out)
    return prediction
