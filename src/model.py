import torch
from torch import nn, Tensor


class ConvBlock(nn.Module):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: int,
        stride: int = 1,
        dilation: int = 1,
        padding: int = 0,
    ):
        super().__init__()
        self.conv = nn.Conv2d(
            in_channels,
            out_channels,
            kernel_size=kernel_size,
            stride=stride,
            dilation=dilation,
            padding=padding,
        )
        self.bnorm = nn.BatchNorm2d(out_channels)

    def forward(self, x: Tensor) -> Tensor:
        return torch.relu(self.bnorm(self.conv(x)))


class ConvNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv_layers = nn.Sequential(
            ConvBlock(1, 16, kernel_size=3, stride=2),
            ConvBlock(16, 32, kernel_size=3, stride=2),
            ConvBlock(32, 64, kernel_size=3, stride=2),
        )
        self.dense_layers = nn.Sequential(
            nn.Flatten(start_dim=1),
            nn.LazyLinear(out_features=10),
        )

    def forward(self, x: Tensor) -> Tensor:
        x = self.conv_layers(x)
        return torch.log_softmax(self.dense_layers(x), dim=1)
        # return log_softmax(self.dense_layers(x))
