from sklearn.neural_network import MLPRegressor

def MLP():
    # Número máximo de épocas durante o treinamento.
    EPOCHS = 1000
    # Número máximo de épocas sem mudança
    EPOCHS_NOCHANGE = 5
    # tolerância para a otimização
    ERROR = 1e-4
    model = MLPRegressor(max_iter = EPOCHS,
                         tol = ERROR,
                         n_iter_no_change = EPOCHS_NOCHANGE,
                         early_stopping = True,
                         verbose=False,
                         random_state=42)
    return model