import time

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import CIFAR10

from resnet_model import resnet_models

from torchgpipe import GPipe


if __name__ == '__main__':
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]

    train = transforms.Compose([
            transforms.RandomResizedCrop(32),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(mean, std)
        ])
    dataset = CIFAR10(root='./cifar10', train=True, transform=train, download=True)
    dataloader = DataLoader(dataset, batch_size=64)

    criterion = nn.CrossEntropyLoss()
    model = resnet_models("101", 10)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.05, weight_decay=1e-5, momentum=0.9)

    # model = VolatilityDNN(model, 1)
    model = GPipe(model.get_sequential_module(), balance=[8,], chunks=8)

    for i, t in dataloader:
        i, t = i.cuda(), t.cuda()

        pred = model(i)
        loss = criterion(pred, t)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

