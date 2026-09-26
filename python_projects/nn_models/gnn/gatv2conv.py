import torch
import torch.nn.functional as F
import torch_geometric.nn as gnn
import torch.nn as nn
from torch_geometric.datasets import Planetoid
from tqdm import tqdm

dataset = Planetoid(
    root="data/Planetoid",
    name="Cora"
)

data = dataset[0]
print(data.x.shape)

class GraphAnalyser(nn.Module):
    def __init__(self, in_c, hidden_c, out_c):
        super().__init__()

        self.conv1 = gnn.GATv2Conv(
            in_c,
            hidden_c
        )

        self.conv2 = gnn.GATv2Conv(
            hidden_c,
            hidden_c * 2
        )

        self.conv3 = gnn.GATv2Conv(
            hidden_c * 2,
            hidden_c * 2
        )

        self.dropout = nn.Dropout(0.2)
        self.dropout2 = nn.Dropout(0.2)
        self.linear = nn.Linear(
            hidden_c*2,
            hidden_c*2
        )
        self.linear2 = nn.Linear(
            hidden_c*2,
            out_c
        )

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.dropout(x)

        x = self.conv2(x, edge_index)
        x = F.relu(x)

        x = self.conv3(x, edge_index)
        x = F.relu(x)
        x = self.dropout2(x)

        x = self.linear(x)
        x = F.relu(x)

        x = self.linear2(x)

        return x


model = GraphAnalyser(
    in_c=dataset.num_features,
    hidden_c=16,
    out_c=dataset.num_classes
)

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=2e-4,
    weight_decay=1e-5
)

epochs = 1500

progress = tqdm(range(epochs))

for epoch in progress:

    model.train()

    optimizer.zero_grad()

    preds = model(
        data.x,
        data.edge_index
    )

    loss = criterion(
        preds[data.train_mask],
        data.y[data.train_mask]
    )

    loss.backward()

    optimizer.step()

    model.eval()

    with torch.no_grad():
        preds_eval = model(
            data.x,
            data.edge_index
        )

        pred_classes = preds_eval.argmax(dim=-1)

        train_acc = (
            pred_classes[data.train_mask]
            == data.y[data.train_mask]
        ).float().mean()

        val_acc = (
            pred_classes[data.val_mask]
            == data.y[data.val_mask]
        ).float().mean()

    progress.set_postfix(
        loss=f"{loss.item():.4f}",
        train_acc=f"{train_acc.item():.3f}",
        val_acc=f"{val_acc.item():.3f}"
    )


model.eval()

with torch.no_grad():
    preds = model(
        data.x,
        data.edge_index
    )

    pred_classes = preds.argmax(dim=-1)

    test_acc = (
        pred_classes[data.test_mask]
        == data.y[data.test_mask]
    ).float().mean()

print(f"Test accuracy: {test_acc.item() * 100:.4f}%")
