

class TradingAgent1(L.LightningModule):
    
    def __init__(self, sentiment_model, time_series_model):
        super().__init__()
        self.sentiment_model = sentiment_model
        self.time_series_model = time_series_model
        
    def training_step(self, batch, batch_idx):
        x, _ = batch
        x_hat = self.sentiment_model(x)
        loss = F.mse_loss(x_hat, x)
        
    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer
    