#import pickle
from flask import Flask,request,jsonify,url_for,render_template
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib as mpl
import matplotlib.pyplot as plt


app = Flask(__name__)
#Carrega o modelo
modelo = KMeans(n_clusters=8, init='k-means++', algorithm='elkan', n_init=1, random_state=42)

def extrai_recurso(imagem):
    image = mpl.image.imread(imagem)
    if image is None:
        print(f"Erro ao carregar a imagem: {imagem}")
        return None
    # Transforma a imagem em uma matriz 1D
    image = image.reshape(-1, 3)
    return image
def gera_paleta(imagem):
    novos_clusters = modelo.fit_predict(imagem)
    # Exibe a contagem de pixels em cada cluster
    print(pd.Series(novos_clusters).value_counts())

    # Visualiza a paleta de cores para a nova imagem
    new_palette_2 = modelo.cluster_centers_.astype(int)
    new_palette_hex = ['#%02x%02x%02x' % (r, g, b) for (r, g, b) in new_palette_2]
    plt.imshow([new_palette_2])
    plt.axis('off')
    plt.show()

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload', methods=['POST'])
def upload_imagem():
    if 'imagem' not in request.files:
        return 'Nenhuma imagem foi localizada'

    imagem = request.files['imagem']
    
    imagem = extrai_recurso(imagem)
    # Aqui, você pode processar a imagem conforme necessário.
    # Por exemplo, salvá-la no servidor ou realizar operações.
    return gera_paleta(imagem)

if __name__=="__main__":
    app.run(debug=True)
    