import torch
import torch.nn as nn

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class ResidualBlock(nn.Module):
    def __init__(self, in_dim, out_dim, dropout, use_residual):
        super().__init__()
        self.linear = nn.Linear(in_dim, out_dim)
        self.bn = nn.BatchNorm1d(out_dim)
        self.activation = nn.GELU()
        self.dropout = nn.Dropout(dropout)
        self.use_residual = use_residual
        if use_residual and in_dim != out_dim:
            self.proj = nn.Linear(in_dim, out_dim)
        else:
            self.proj = None

    def forward(self, x):
        residual = x
        out = self.linear(x)
        out = self.bn(out)
        out = self.activation(out)
        out = self.dropout(out)
        if self.use_residual:
            if self.proj is not None:
                residual = self.proj(residual)
            out = out + residual
        return out


class ResidualMLP(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.blocks = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.BatchNorm1d(128),
            nn.GELU(),
            nn.Dropout(0.2),
            ResidualBlock(128, 256, 0.3, False),
            ResidualBlock(256, 256, 0.3, True),
            ResidualBlock(256, 128, 0.3, True),
            ResidualBlock(128, 64, 0.2, False),
        )
        self.head = nn.Linear(64, 1)

    def forward(self, x):
        out = self.blocks(x)
        return self.head(out).squeeze(-1)
